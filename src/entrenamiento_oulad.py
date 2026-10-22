"""Entrenamiento por personas sin acceso predictivo al conjunto de prueba."""
import hashlib
import importlib.metadata
import importlib.util
import json
import platform
import time
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from sklearn.calibration import CalibratedClassifierCV
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.frozen import FrozenEstimator
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (average_precision_score, brier_score_loss, confusion_matrix,
                             precision_score, recall_score, f1_score, roc_auc_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_sample_weight
from threadpoolctl import threadpool_limits

KEY = ['id_student', 'code_module', 'code_presentation']
MODULES = {'regresion_logistica': 'sklearn', 'random_forest': 'sklearn',
           'xgboost': 'xgboost', 'lightgbm': 'lightgbm', 'tabnet': 'pytorch_tabnet'}
ORDER = ['regresion_logistica', 'random_forest', 'lightgbm', 'xgboost', 'tabnet']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def save_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    temp.replace(path)


def available_models():
    return {name: importlib.util.find_spec(module) is not None and
            (name != 'tabnet' or importlib.util.find_spec('torch') is not None)
            for name, module in MODULES.items()}


class TrainColumns(TransformerMixin, BaseEstimator):
    """Retira constantes y columnas enteramente ausentes usando solo ajuste."""
    def fit(self, X, y=None):
        require(isinstance(X, pd.DataFrame), 'Se requieren columnas con nombres')
        require(not np.isinf(X.to_numpy(dtype=float)).any(), 'Predictores infinitos')
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.columns_ = X.columns[X.nunique(dropna=True).gt(1)].tolist()
        require(bool(self.columns_), 'No quedan predictores variables')
        return self

    def transform(self, X):
        require(list(X.columns) == list(self.feature_names_in_), 'Esquema de predictores diferente')
        values = X.loc[:, self.columns_].to_numpy(dtype=float)
        require(not np.isinf(values).any(), 'Predictores infinitos')
        return values


class TabNetAdapter(ClassifierMixin, BaseEstimator):
    """Pesos en la pérdida; no activa muestreo ponderado ni early stopping."""
    def __init__(self, parameters=None, seed=20261021):
        self.parameters = parameters
        self.seed = seed

    def fit(self, X, y):
        import torch
        from pytorch_tabnet.tab_model import TabNetClassifier
        torch.set_num_threads(2)
        params = dict(self.parameters or {})
        balance = params.pop('ponderacion', 'ninguna') == 'balanceada'
        epochs = params.pop('max_epochs', 100)
        self.classes_ = np.array([0, 1])
        self.n_features_in_ = X.shape[1]
        counts = np.bincount(np.asarray(y, dtype=int), minlength=2)
        require((counts > 0).all(), 'TabNet requiere ambas clases')
        loss = torch.nn.CrossEntropyLoss(weight=torch.tensor(len(y) / (2 * counts), dtype=torch.float32)) if balance else None
        self.model_ = TabNetClassifier(**params, seed=self.seed, device_name='cpu', verbose=0)
        self.model_.fit(np.asarray(X, dtype=np.float32), np.asarray(y, dtype=np.int64),
                        eval_set=[], max_epochs=epochs, patience=0, weights=0, loss_fn=loss,
                        batch_size=1024, virtual_batch_size=128, num_workers=0, drop_last=False)
        return self

    def predict_proba(self, X):
        return self.model_.predict_proba(np.asarray(X, dtype=np.float32))

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] > 0.5).astype(int)


def build_pipeline(name, parameters, seed):
    params = dict(parameters)
    balanced = params.pop('class_weight', None) == 'balanced'
    balanced = params.pop('ponderacion', 'ninguna') == 'balanceada' or balanced
    if name == 'regresion_logistica':
        model = LogisticRegression(**params, random_state=seed)
    elif name == 'random_forest':
        model = RandomForestClassifier(**params, random_state=seed, n_jobs=2)
    elif name == 'xgboost':
        from xgboost import XGBClassifier
        model = XGBClassifier(**params, objective='binary:logistic', eval_metric='logloss',
                              tree_method='hist', random_state=seed, n_jobs=2)
    elif name == 'lightgbm':
        from lightgbm import LGBMClassifier
        model = LGBMClassifier(**params, random_state=seed, n_jobs=2, verbosity=-1)
    elif name == 'tabnet':
        model = TabNetAdapter({**params, 'ponderacion': 'balanceada' if balanced else 'ninguna'}, seed)
    elif name == 'referencia':
        model = DummyClassifier(strategy='prior')
    else:
        raise ValueError(name)
    steps = [('columnas', TrainColumns()), ('imputacion', SimpleImputer(strategy='median', add_indicator=True))]
    if name in ('regresion_logistica', 'tabnet'):
        steps.append(('escala', StandardScaler()))
    return Pipeline(steps + [('modelo', model)]), balanced


def fit_pipeline(name, parameters, X, y, seed):
    pipeline, balanced = build_pipeline(name, parameters, seed)
    kwargs = {'modelo__sample_weight': compute_sample_weight('balanced', y)} if balanced and name != 'tabnet' else {}
    with threadpool_limits(limits=2), warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        pipeline.fit(X, y, **kwargs)
    messages = [str(w.message) for w in caught]
    converged = not any(issubclass(w.category, ConvergenceWarning) for w in caught)
    return pipeline, messages, converged


def probability_metrics(y, p):
    require(len(y) == len(p) and np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all(), 'Probabilidades inválidas')
    return {'ap': float(average_precision_score(y, p)), 'roc_auc': float(roc_auc_score(y, p)),
            'brier': float(brier_score_loss(y, p)), 'prevalencia': float(np.mean(y))}


def threshold_metrics(y, p, threshold):
    predicted = np.asarray(p) > threshold
    tn, fp, fn, tp = confusion_matrix(y, predicted, labels=[0, 1]).ravel()
    return {'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp),
            'precision': float(precision_score(y, predicted, zero_division=0)),
            'sensibilidad': float(recall_score(y, predicted, zero_division=0)),
            'especificidad': float(tn / (tn + fp)), 'f1': float(f1_score(y, predicted, zero_division=0)),
            'proporcion_alertas': float(predicted.mean())}


def choose_threshold(y, p):
    """Máximo F1, mayor sensibilidad, menor umbral; desigualdad estricta."""
    y, p = np.asarray(y, dtype=int), np.asarray(p, dtype=float)
    require(set(y) == {0, 1}, 'Se requieren ambas clases para fijar umbral')
    require(np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all(), 'Probabilidades inválidas')
    # Al recorrer valores ascendentes se eliminan de las alertas todos los empates.
    order = np.argsort(p, kind='stable')
    scores, labels = p[order], y[order]
    ends = np.r_[np.flatnonzero(np.diff(scores)), len(scores) - 1]
    removed_tp = np.cumsum(labels)[ends]
    tp = np.r_[y.sum(), y.sum() - removed_tp]
    positive = np.r_[len(y), len(y) - ends - 1]
    f1 = 2 * tp / (positive + y.sum())
    recall = tp / y.sum()
    thresholds = np.r_[np.nextafter(scores[0], -np.inf), scores[ends]]
    best = max(range(len(thresholds)), key=lambda i: (f1[i], recall[i], -thresholds[i]))
    return float(thresholds[best])


def calibration_table(y, p):
    d = pd.DataFrame({'y': np.asarray(y), 'p': np.asarray(p)})
    d['intervalo'] = np.minimum((d.p * 10).astype(int), 9)
    return d.groupby('intervalo').agg(n=('y', 'size'), probabilidad_media=('p', 'mean'),
                                     frecuencia_retiro=('y', 'mean')).reindex(range(10)).reset_index()


def model_fingerprint(pipeline):
    """Compara el estado aprendido sin ordenar claves tensoriales de optimizadores."""
    model = pipeline['modelo']
    if isinstance(model, TabNetAdapter):
        state = {key: value.detach().cpu().numpy().copy()
                 for key, value in model.model_.network.state_dict().items()}
        return joblib.hash((pipeline.steps[:-1], model.parameters, model.classes_, state))
    return joblib.hash(pipeline)


class TrainingData:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.folder = self.root / 'reportes/protocolo_validacion_2026_10_19/implementacion'
        hashes = json.loads((self.folder / 'huellas.json').read_text(encoding='utf-8'))
        for name, expected in hashes.items():
            require(sha(self.folder / name) == expected, f'Archivo congelado alterado: {name}')
        self.config = json.loads((self.folder / 'configuracion.json').read_text(encoding='utf-8'))
        self.audit = json.loads((self.folder / 'verificacion.json').read_text(encoding='utf-8'))
        require(sha(self.root / 'decision_temporal.json') == self.audit['decision_temporal_sha256'], 'Cambió la definición temporal')
        self.people = pd.read_csv(self.folder / 'personas.csv')
        require(self.people.id_student.is_unique, 'Personas repetidas en manifiesto')
        self.predictors = self.config['predictores']
        self.read_log = []
        self.checked_sources = set()

    def load(self, cut, group):
        require(group in {'ajuste', 'calibracion', 'umbral'}, 'La prueba final no está disponible en este entrenador')
        require(cut in self.config['cortes'], 'Corte no autorizado')
        members = self.people.loc[self.people.conjunto.eq(group)]
        path = self.root / f'data/processed/correcciones_2026_09_10/dataset_corte_{cut:02d}.parquet'
        if cut not in self.checked_sources:
            expected = self.audit['fuentes_sha256'][str(path.relative_to(self.root))]
            require(sha(path) == expected, 'Fuente diferente a la partición congelada')
            self.checked_sources.add(cut)
        # Predicado antes de convertir a pandas: no devuelve filas de prueba.
        columns = KEY + ['corte', 'retiro_futuro'] + self.predictors
        d = pd.read_parquet(path, columns=columns, filters=[('id_student', 'in', members.id_student.tolist())])
        require(not d.duplicated(KEY).any(), 'Inscripciones duplicadas')
        d = d.merge(members, on='id_student', how='left', validate='many_to_one')
        require(d.conjunto.eq(group).all(), 'Persona fuera del conjunto permitido')
        require(d.corte.eq(cut).all() and d.retiro_futuro.nunique() == 2, 'Corte o clases inválidos')
        self.read_log.append({'corte': cut, 'conjunto': group, 'filas': len(d)})
        return d.sort_values(KEY).reset_index(drop=True)


def run_training(root, output, models, cuts, mode='completo', finalize=False):
    data = TrainingData(root)
    root, output = Path(root).resolve(), Path(output).resolve()
    availability = available_models()
    require(set(models).issubset(MODULES), 'Familia desconocida')
    require(not finalize or mode == 'completo', 'No finalizar modelos de comprobación')
    environment = {'python': platform.python_version()}
    for package in ['numpy', 'pandas', 'scikit-learn', 'pyarrow', 'xgboost', 'lightgbm', 'torch', 'pytorch-tabnet', 'joblib']:
        try:
            environment[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            environment[package] = None
    contract = {'modo': mode, 'modelos': models, 'cortes': cuts, 'finalizar_familias': finalize,
                'configuracion_sha256': sha(data.folder / 'configuracion.json'),
                'manifiesto_sha256': sha(data.folder / 'personas.csv'),
                'codigo_sha256': sha(Path(__file__)), 'entorno': environment}
    output.mkdir(parents=True, exist_ok=True)
    contract_path = output / 'contrato.json'
    if contract_path.exists():
        require(json.loads(contract_path.read_text(encoding='utf-8')) == contract,
                'La ejecución existente tiene otro contrato; utilizar otra carpeta de salida')
    else:
        save_json(contract_path, contract)
    pending = [m for m in models if not availability[m]]
    save_json(output / 'dependencias.json', {'disponibilidad': availability, 'no_ejecutados': pending})
    all_results = []
    for cut in cuts:
        fit = data.load(cut, 'ajuste')
        if mode == 'comprobacion':
            # Muestra determinista por persona y pliegue, nunca por resultado.
            sampled = (fit[['id_student', 'pliegue_interno']].drop_duplicates()
                       .groupby('pliegue_interno', group_keys=False)
                       .apply(lambda x: x.sample(min(120, len(x)), random_state=20261021), include_groups=False))
            fit = fit.loc[fit.id_student.isin(sampled.id_student)].reset_index(drop=True)
        for model in ['referencia'] + [m for m in models if availability[m]]:
            parameters = [{}] if model == 'referencia' else data.config['configuraciones'][model]
            if mode == 'comprobacion':
                parameters = parameters[:1]
            rows = []
            folder = output / f'corte_{cut:02d}' / model
            folder.mkdir(parents=True, exist_ok=True)
            for candidate_id, params in enumerate(parameters):
                for fold in range(5):
                    marker = folder / f'config_{candidate_id:02d}_fold_{fold}.json'
                    if marker.exists():
                        saved = json.loads(marker.read_text(encoding='utf-8'))
                        if 'predicciones_sha256' in saved:
                            require(sha(marker.with_suffix('.parquet')) == saved['predicciones_sha256'],
                                    'Predicciones de un pliegue alteradas')
                        rows.append(saved)
                        continue
                    train = fit.loc[fit.pliegue_interno.ne(fold)]
                    valid = fit.loc[fit.pliegue_interno.eq(fold)]
                    require(set(train.id_student).isdisjoint(valid.id_student), 'Contaminación de personas')
                    require(train.retiro_futuro.nunique() == valid.retiro_futuro.nunique() == 2, 'Falta una clase')
                    started = time.monotonic()
                    row = {'modelo': model, 'corte': cut, 'configuracion': candidate_id, 'pliegue': fold,
                           'n_ajuste': len(train), 'n_validacion': len(valid), 'parametros': params}
                    try:
                        estimator, caught, converged = fit_pipeline(model, params, train[data.predictors],
                            train.retiro_futuro, data.config['semillas']['busqueda'] + fold)
                        p = estimator.predict_proba(valid[data.predictors])[:, 1]
                        row.update(probability_metrics(valid.retiro_futuro, p))
                        row.update({'estado': 'correcto' if converged else 'sin_convergencia',
                                    'advertencias': caught, 'columnas_retenidas': estimator['columnas'].columns_})
                        predictions = valid[KEY + ['retiro_futuro']].copy()
                        predictions['probabilidad'] = p
                        pred_path = marker.with_suffix('.parquet')
                        predictions.to_parquet(pred_path, index=False)
                        row['predicciones_sha256'] = sha(pred_path)
                    except Exception as exc:
                        row.update({'estado': 'fallido', 'error': f'{type(exc).__name__}: {exc}'})
                    row['segundos'] = time.monotonic() - started
                    save_json(marker, row)
                    rows.append(row)
                    print(f'{mode} corte={cut} {model} config={candidate_id} fold={fold}: {row["estado"]}', flush=True)
            candidates = []
            for candidate_id in range(len(parameters)):
                values = [r for r in rows if r['configuracion'] == candidate_id]
                ok = len(values) == 5 and all(r['estado'] == 'correcto' for r in values)
                candidates.append({'configuracion': candidate_id, 'valida': ok,
                                   'ap_media': float(np.mean([r['ap'] for r in values])) if ok else None})
            valid_candidates = [c for c in candidates if c['valida']]
            best = min(valid_candidates, key=lambda c: (-round(c['ap_media'], 6), c['configuracion'])) if valid_candidates else None
            result = {'modelo': model, 'corte': cut, 'modo': mode, 'candidatos': candidates,
                      'mejor_configuracion': best, 'busqueda_completa': mode == 'completo' and len(valid_candidates) == len(parameters),
                      'es_resultado_de_prueba': False}
            save_json(folder / 'seleccion.json', result)
            all_results.append(result)
            if finalize and model != 'referencia' and result['busqueda_completa']:
                finalize_family(data, fit, cut, model, parameters[best['configuracion']], folder)
    save_json(output / 'lecturas.json', data.read_log)
    complete = mode == 'completo' and not pending and set(models) == set(MODULES) and all(
        r['busqueda_completa'] for r in all_results)
    save_json(output / 'resumen.json', {'estado': 'comparacion_completa' if complete else 'parcial',
              'modo': mode, 'resultados': all_results, 'familias_no_disponibles': pending,
              'prueba_final_evaluada': False, 'seleccion_global_realizada': False})
    return all_results


def finalize_family(data, fit, cut, model, params, folder):
    """Congela un candidato de familia, sin elegir ganador entre familias."""
    marker = folder / 'modelo_congelado.json'
    if marker.exists():
        record = json.loads(marker.read_text(encoding='utf-8'))
        require(sha(folder / 'modelo_calibrado.joblib') == record['modelo_sha256'], 'Modelo guardado alterado')
        return
    cal = data.load(cut, 'calibracion')
    threshold_data = data.load(cut, 'umbral')
    people_sets = [set(x.id_student) for x in [fit, cal, threshold_data]]
    require(all(people_sets[i].isdisjoint(people_sets[j]) for i in range(3) for j in range(i)), 'Cruce entre etapas')
    base, caught, converged = fit_pipeline(model, params, fit[data.predictors], fit.retiro_futuro,
                                           data.config['semillas']['busqueda'])
    require(converged, 'Reajuste final sin convergencia; no se congela el modelo')
    before = model_fingerprint(base)
    calibrated = CalibratedClassifierCV(FrozenEstimator(base), method='sigmoid', n_jobs=1)
    with threadpool_limits(limits=2):
        calibrated.fit(cal[data.predictors], cal.retiro_futuro)
    require(model_fingerprint(base) == before, 'La calibración modificó el ajuste base')
    p = calibrated.predict_proba(threshold_data[data.predictors])[:, 1]
    threshold = choose_threshold(threshold_data.retiro_futuro.to_numpy(), p)
    predictions = threshold_data[KEY + ['retiro_futuro']].copy()
    predictions['probabilidad'] = p
    predictions.to_parquet(folder / 'predicciones_umbral.parquet', index=False)
    calibration_table(predictions.retiro_futuro, p).to_csv(folder / 'calibracion_en_umbral.csv', index=False)
    joblib.dump(calibrated, folder / 'modelo_calibrado.joblib')
    save_json(marker, {'modelo': model, 'corte': cut, 'parametros': params, 'umbral': threshold,
        'metricas_en_conjunto_de_seleccion_de_umbral': {**probability_metrics(predictions.retiro_futuro, p),
                                                       **threshold_metrics(predictions.retiro_futuro, p, threshold)},
        'referencia_umbral_05': threshold_metrics(predictions.retiro_futuro, p, 0.5),
        'advertencia': 'Métricas de desarrollo: el umbral se eligió en estos datos; no son prueba final.',
        'advertencias_ajuste': caught, 'base_inmutable_durante_calibracion': True,
        'modelo_sha256': sha(folder / 'modelo_calibrado.joblib'), 'prueba_final_evaluada': False})
