"""Congela particiones y candidatos sin entrenar ni evaluar modelos.

Uso: .venv/Scripts/python.exe scripts/preparar_validacion.py --root .
Una segunda ejecución verifica identidad; nunca sustituye archivos diferentes.
"""
import argparse
import ast
import hashlib
import itertools
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import StratifiedGroupKFold

KEY = ['id_student', 'code_module', 'code_presentation']
SETS = ['ajuste', 'calibracion', 'umbral', 'prueba']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def grouped_folds(frame, n, seed):
    strata = frame.corte.astype(str) + ':' + frame.retiro_futuro.astype(str)
    folds = np.full(len(frame), -1, dtype=int)
    splitter = StratifiedGroupKFold(n_splits=n, shuffle=True, random_state=seed)
    for fold, (_, val) in enumerate(splitter.split(np.zeros(len(frame)), strata, frame.id_student)):
        require((folds[val] == -1).all(), 'Asignación repetida')
        folds[val] = fold
    require((folds >= 0).all(), 'Filas sin asignación')
    require(pd.DataFrame({'id': frame.id_student.to_numpy(), 'fold': folds})
            .groupby('id').fold.nunique().eq(1).all(), 'Persona compartida entre pliegues')
    return folds


def summarize(frame, columns):
    return frame.groupby(columns, observed=True).agg(
        inscripciones=('id_student', 'size'), personas=('id_student', 'nunique'),
        eventos=('retiro_futuro', 'sum'), prevalencia=('retiro_futuro', 'mean')
    ).reset_index()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    source = root / 'data/processed/correcciones_2026_09_10'
    out = root / 'reportes/protocolo_validacion_2026_10_19/implementacion'
    temporal = root / 'decision_temporal.json'
    cuts = json.loads(temporal.read_text(encoding='utf-8'))['cortes']
    predictor_source = root / 'src/ventanas_oulad.py'
    tree = ast.parse(predictor_source.read_text(encoding='utf-8'))
    predictors = next(ast.literal_eval(node.value) for node in tree.body
                      if isinstance(node, ast.Assign) and any(
                          isinstance(t, ast.Name) and t.id == 'PREDICTORS' for t in node.targets))
    require(len(predictors) == len(set(predictors)), 'Predictores repetidos')
    require(not set(predictors) & set(KEY + ['retiro_futuro', 'date_unregistration',
                'final_result', 'score_promedio_observado', 'n_registros_vle']), 'Predictor prohibido')
    frames, hashes = [], {}
    for cut in cuts:
        path = source / f'dataset_corte_{cut:02d}.parquet'
        hashes[str(path.relative_to(root))] = digest(path)
        d = pd.read_parquet(path)
        require(d.corte.eq(cut).all(), f'Corte incorrecto: {cut}')
        require(not d.duplicated(KEY).any() and d[KEY].notna().all().all(), 'Clave inválida')
        require(set(predictors).issubset(d.columns), 'Faltan predictores')
        require(d.date_registration.notna().all() and d.date_registration.le(cut).all(), 'Matrícula no elegible')
        require((d.date_unregistration.isna() | d.date_unregistration.gt(cut)).all(), 'Retiro anterior al corte')
        require(d.module_presentation_length.gt(cut).all(), 'Oferta finalizada')
        expected = d.date_unregistration.gt(cut) & d.date_unregistration.le(d.module_presentation_length)
        require(d.retiro_futuro.eq(expected.astype(int)).all(), 'Etiqueta incoherente')
        frames.append(d[KEY + ['corte', 'retiro_futuro']])
    data = pd.concat(frames, ignore_index=True).sort_values(['corte'] + KEY).reset_index(drop=True)
    data['pliegue_externo'] = grouped_folds(data, 10, 20261019)
    data['conjunto'] = data.pliegue_externo.map(
        {0: 'prueba', 1: 'prueba', 2: 'calibracion', 3: 'umbral', **dict.fromkeys(range(4, 10), 'ajuste')})
    data['pliegue_interno'] = -1
    training = data.loc[data.conjunto.eq('ajuste')].copy().reset_index(drop=True)
    training['pliegue_interno'] = grouped_folds(training, 5, 20261020)
    mapping = training.groupby('id_student').pliegue_interno.first()
    data['pliegue_interno'] = data.id_student.map(mapping).fillna(-1).astype(int)
    manifest = data[['id_student', 'conjunto', 'pliegue_externo', 'pliegue_interno']].drop_duplicates().sort_values('id_student')
    require(manifest.id_student.is_unique, 'Cruce de personas entre conjuntos')
    require(data.merge(manifest[['id_student', 'conjunto']], on='id_student', validate='many_to_one')
            .eval('conjunto_x == conjunto_y').all(), 'Unión incorrecta del manifiesto')
    totals = summarize(data, ['corte', 'conjunto'])
    require(len(totals) == len(cuts) * 4, 'Falta un conjunto')
    require(((totals.eventos > 0) & (totals.eventos < totals.inscripciones)).all(), 'Falta una clase')
    offers = summarize(data, ['corte', 'conjunto', 'code_module', 'code_presentation'])
    for cut in cuts:
        d = data.loc[data.corte.eq(cut)]
        all_offers = set(map(tuple, d[['code_module', 'code_presentation']].to_numpy()))
        for name in SETS:
            require(set(map(tuple, d.loc[d.conjunto.eq(name), ['code_module', 'code_presentation']].to_numpy())) == all_offers,
                    f'Oferta ausente: {cut}, {name}')
        for fold in range(5):
            fit = d.loc[d.conjunto.eq('ajuste') & d.pliegue_interno.ne(fold)]
            val = d.loc[d.conjunto.eq('ajuste') & d.pliegue_interno.eq(fold)]
            require(set(fit.id_student).isdisjoint(val.id_student), 'Cruce interno')
            require(fit.retiro_futuro.nunique() == val.retiro_futuro.nunique() == 2, 'Falta clase interna')
    inner = summarize(data.loc[data.conjunto.eq('ajuste')], ['corte', 'pliegue_interno'])
    # Espacios acotados; se congelan las configuraciones concretas antes de ajustar.
    spaces = {
        'regresion_logistica': {'C': [0.01, 0.1, 1., 10.], 'class_weight': [None, 'balanced'],
                               'solver': ['lbfgs'], 'max_iter': [3000]},
        'random_forest': {'n_estimators': [300, 600], 'max_depth': [None, 8, 16],
                          'min_samples_leaf': [2, 10, 30], 'max_features': ['sqrt', 0.8],
                          'class_weight': [None, 'balanced']},
        'xgboost': {'n_estimators': [200, 500], 'max_depth': [2, 4, 6], 'learning_rate': [0.03, 0.1],
                    'subsample': [0.8, 1.], 'colsample_bytree': [0.8], 'reg_lambda': [1., 10.],
                    'ponderacion': ['ninguna', 'balanceada']},
        'lightgbm': {'n_estimators': [200, 500], 'num_leaves': [7, 15, 31],
                     'learning_rate': [0.03, 0.1], 'min_child_samples': [20, 60],
                     'reg_lambda': [0., 10.], 'class_weight': [None, 'balanced']},
        'tabnet': {'n_d': [8, 16], 'n_a': [8, 16], 'n_steps': [3, 5],
                   'gamma': [1.3, 1.5], 'lambda_sparse': [0.0001, 0.001],
                   'max_epochs': [100, 200], 'ponderacion': ['ninguna', 'balanceada']},
    }
    rng = np.random.default_rng(20261021)
    configs = {}
    for model, space in spaces.items():
        candidates = [dict(zip(space, values)) for values in itertools.product(*space.values())]
        chosen = np.arange(len(candidates)) if len(candidates) <= 30 else rng.choice(len(candidates), 30, replace=False)
        configs[model] = [candidates[i] for i in chosen]
    policy = {
        'version': '2026-10-19-v1', 'estado': 'preparado_sin_entrenamiento',
        'generalizacion': 'personas nuevas dentro de ofertas disponibles', 'cortes': cuts,
        'predictores': predictors, 'contexto_incluido': False,
        'semillas': {'particion': 20261019, 'cv': 20261020, 'busqueda': 20261021, 'bootstrap': 20261022},
        'seleccion': 'media AP en cinco pliegues internos, por corte',
        'calibracion': 'sigmoidal en conjunto exclusivo, modelo base congelado',
        'umbral': 'maximizar F1; empates: mayor sensibilidad y menor umbral; p > umbral',
        'preprocesamiento': 'por pliegue: retirar columnas enteramente ausentes y constantes; mediana e indicadores de ausencia; StandardScaler solo en logística y TabNet',
        'regularizacion_logistica': 'L2; conservar coeficientes como asociaciones del modelo, no inferencia causal; no usar VIF global para seleccionar',
        'pesos': 'balanced: n/(2*n_clase) calculados solo en ajuste; ponderacion es metadato, no parámetro del estimador',
        'tabnet_balanceado': 'implementar pesos en pérdida; no convertir inadvertidamente a remuestreo',
        'detencion_temprana': False,
        'iteraciones': 'fijas en cada candidato; TabNet sin early stopping; verificar convergencia y registrar fallos',
        'paralelismo': 'máximo 2 procesos o hilos por ajuste; sin búsquedas concurrentes',
        'configuraciones': configs,
        'advertencia': 'Este archivo define el contrato del futuro entrenador; no acredita implementación ni ejecución de estos modelos.'
    }
    checks = {'estado': 'correcto', 'personas': len(manifest), 'filas_cinco_cortes': len(data),
              'personas_compartidas': 0, 'cortes': cuts, 'conjuntos': SETS,
              'ofertas_representadas_todos_conjuntos': True, 'ambas_clases_cada_conjunto_y_pliegue': True,
              'etiquetas_y_elegibilidad_verificadas': True, 'modelos_entrenados': 0,
              'python': platform.python_version(), 'sklearn': sklearn.__version__,
              'pandas': pd.__version__, 'numpy': np.__version__, 'fuentes_sha256': hashes,
              'decision_temporal_sha256': digest(temporal), 'predictores_fuente_sha256': digest(predictor_source),
              'script_sha256': digest(Path(__file__))}
    def json_bytes(obj):
        return (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    files = {
        'personas.csv': manifest.to_csv(index=False, lineterminator='\n').encode(),
        'distribucion_conjuntos.csv': totals.to_csv(index=False, lineterminator='\n').encode(),
        'distribucion_ofertas.csv': offers.to_csv(index=False, lineterminator='\n').encode(),
        'distribucion_cv.csv': inner.to_csv(index=False, lineterminator='\n').encode(),
        'configuracion.json': json_bytes(policy), 'verificacion.json': json_bytes(checks)}
    files['huellas.json'] = json_bytes({name: hashlib.sha256(content).hexdigest() for name, content in files.items()})
    for name, content in files.items():
        target = out / name
        require(not target.exists() or target.read_bytes() == content, f'Archivo congelado diferente: {target}; usar una versión nueva, no sobrescribir')
    out.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        if not (out / name).exists():
            (out / name).write_bytes(content)
    print(totals.to_string(index=False))
    print(f'Correcto: {len(manifest)} personas; sin entrenamiento. Salidas: {out}')


if __name__ == '__main__':
    main()
