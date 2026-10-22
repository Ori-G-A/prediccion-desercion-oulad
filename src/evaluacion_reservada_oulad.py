"""Evaluación de artefactos congelados; no contiene operaciones de ajuste."""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from entrenamiento_oulad import KEY, require, sha, save_json, calibration_table
from metricas_evaluacion_oulad import metrics, paired_bootstrap


def verify_package(root, package):
    require(package['estado'] == 'congelado', 'Paquete no congelado')
    require(package['bootstrap'] == {'replicas': 2000, 'semilla': 20261022, 'unidad': 'persona'}, 'Remuestreo diferente del protocolo')
    required = [package['seleccion'], package['personas'], *package['datos'].values(),
                'src/evaluacion_reservada_oulad.py', 'src/metricas_evaluacion_oulad.py', 'src/entrenamiento_oulad.py']
    required += [r['archivo_modelo'] for r in package['candidatos']]
    hash_paths = {Path(p) for p in package['huellas']}
    require({Path(p) for p in required}.issubset(hash_paths), 'Faltan huellas obligatorias')
    require(package.get('diseno_shap') and package.get('verificacion_evaluador'), 'Falta diseño SHAP o verificación del evaluador')
    for relative, expected in package['huellas'].items():
        path = (root / relative).resolve()
        require(path.is_relative_to(root.resolve()), 'Artefacto fuera del proyecto')
        require(sha(path) == expected, f'Artefacto congelado alterado: {relative}')
    selection = json.loads((root / package['seleccion']).read_text(encoding='utf-8'))
    require(selection['estado'] == 'seleccion_completa', 'Selección incompleta')
    for relative, expected in selection['evidencias_sha256'].items():
        require(sha(root / relative) == expected, f'Evidencia de selección alterada: {relative}')
    require(len(package['candidatos']) == 25, 'Se requieren cinco familias y cinco cortes')
    require(len({(r['corte'], r['modelo']) for r in package['candidatos']}) == 25, 'Candidatos duplicados')
    require(package['principales'] == selection['principales'], 'Principal distinto de validación')
    require(package['cortes'] == [7, 14, 28, 42, 56], 'Cortes diferentes del protocolo')
    expected = {(r['corte'], r['modelo']): r for r in selection['seleccion_por_familia']}
    require(set(expected) == {(r['corte'], r['modelo']) for r in package['candidatos']}, 'Candidatos diferentes de selección')
    for row in package['candidatos']:
        selected = expected[(row['corte'], row['modelo'])]
        record_path = root / selected['carpeta'] / 'modelo_congelado.json'
        require(record_path.relative_to(root) in hash_paths, 'Registro de modelo sin huella')
        record = json.loads(record_path.read_text(encoding='utf-8'))
        require(row['umbral'] == record['umbral'] and record['base_inmutable_durante_calibracion'], 'Umbral o calibración incompatibles')
        require(sha(root / row['archivo_modelo']) == record['modelo_sha256'], 'Modelo distinto del registro')


def evaluate(root, package_path, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    package = json.loads(Path(package_path).read_text(encoding='utf-8'))
    verify_package(root, package)
    package_hash = sha(package_path)
    first_path = root / 'reportes/continuacion_modelado_2026_10_19/primera_apertura_prueba.json'
    if first_path.exists():
        first = json.loads(first_path.read_text(encoding='utf-8'))
        require(first['paquete_sha256'] == package_hash, 'La prueba ya se abrió con otro paquete')
        require(first['salida'] == str(output.relative_to(root)), 'Conservar la carpeta de primera evaluación')
    else:
        first_path.parent.mkdir(parents=True, exist_ok=True)
        with first_path.open('x', encoding='utf-8') as stream:
            json.dump({'fecha': datetime.now(ZoneInfo('America/Bogota')).isoformat(), 'paquete_sha256': package_hash, 'salida': str(output.relative_to(root)), 'estado': 'apertura_autorizada_tras_verificar_paquete'}, stream, ensure_ascii=False, indent=2)
    output.mkdir(parents=True, exist_ok=True)
    people = pd.read_csv(root / package['personas'])
    ids = people.loc[people.conjunto.eq('prueba'), 'id_student'].to_numpy()
    require(len(np.unique(ids)) == len(ids), 'Personas repetidas')
    summaries = []
    try:
        for cut in package['cortes']:
            destination = output / f'corte_{cut:02d}'
            destination.mkdir(exist_ok=True)
            path = root / package['datos'][str(cut)]
            columns = KEY + ['retiro_futuro', 'date_unregistration', 'corte'] + package['predictores']
            data = pd.read_parquet(path, columns=columns, filters=[('id_student', 'in', ids.tolist())]).sort_values(KEY).reset_index(drop=True)
            require(not data.duplicated(KEY).any() and data.id_student.isin(ids).all() and data.corte.eq(cut).all(), 'Población de prueba inválida')
            predictions, thresholds = {}, {}
            cut_models = [r for r in package['candidatos'] if r['corte'] == cut]
            for candidate in cut_models:
                name = candidate['modelo']
                model = joblib.load(root / candidate['archivo_modelo'])
                with threadpool_limits(limits=2):
                    p = model.predict_proba(data[package['predictores']])[:, 1]
                predictions[name], thresholds[name] = p, candidate['umbral']
            # Referencias fijadas únicamente con el conjunto de ajuste.
            predictions['referencia'] = np.full(len(data), package['prevalencia_ajuste'][str(cut)])
            thresholds['referencia'] = .5
            predictions['clase_mayoritaria'] = np.full(len(data), package['clase_mayoritaria_ajuste'][str(cut)])
            thresholds['clase_mayoritaria'] = .5
            saved = data[KEY + ['retiro_futuro', 'date_unregistration', 'corte']].copy()
            offers = []
            for name, p in predictions.items():
                saved[name] = p
                threshold = thresholds[name]
                lead = (data.loc[(data.retiro_futuro == 1) & (p > threshold), 'date_unregistration'] - cut)
                require(lead.gt(0).all(), 'Anticipación no positiva')
                summaries.append({'corte': cut, 'modelo': name, 'principal': package['principales'][str(cut)] == name,
                    'inscripciones': len(data), 'personas': int(data.id_student.nunique()), 'eventos': int(data.retiro_futuro.sum()),
                    'umbral': threshold, **metrics(data.retiro_futuro, p, threshold),
                    'referencia_umbral_05': metrics(data.retiro_futuro, p, .5),
                    'anticipacion_tp': {'n': len(lead), 'q25': float(lead.quantile(.25)) if len(lead) else None,
                        'mediana': float(lead.median()) if len(lead) else None, 'q75': float(lead.quantile(.75)) if len(lead) else None}})
                calibration_table(data.retiro_futuro, p).to_csv(destination / f'calibracion_{name}.csv', index=False)
                for (module, presentation), group in data.groupby(['code_module', 'code_presentation']):
                    offers.append({'modelo': name, 'modulo': module, 'oferta': presentation, 'inscripciones': len(group),
                        'personas': int(group.id_student.nunique()), 'eventos': int(group.retiro_futuro.sum()),
                        **metrics(group.retiro_futuro, p[group.index], threshold)})
            saved.to_parquet(destination / 'predicciones.parquet', index=False)
            save_json(destination / 'por_oferta.json', {'caracter': 'descriptivo', 'resultados': offers})
            # El mismo universo, semilla y orden de personas se usan en todos los cortes.
            replicas, intervals, differences = paired_bootstrap(data.id_student, data.retiro_futuro, predictions, thresholds, ids)
            replicas.to_parquet(destination / 'replicas.parquet', index=False)
            save_json(destination / 'intervalos.json', {'intervalos': intervals, 'diferencias_pareadas': differences,
                'limite': 'Variación por personas condicionada a modelos y ofertas; no incluye incertidumbre del entrenamiento.'})
            save_json(output / 'metricas.json', {'paquete_sha256': package_hash, 'resultados': summaries})
            print(f'Evaluación e intervalos terminados: corte {cut}', flush=True)
        save_json(output / 'cierre.json', {'estado': 'evaluacion_completa', 'paquete_sha256': package_hash,
            'huellas_salidas': {str(p.relative_to(output)): sha(p) for p in output.rglob('*') if p.is_file() and p.name != 'cierre.json'}})
    except Exception as exc:
        save_json(output / 'incidencia.json', {'paquete_sha256': package_hash, 'error': f'{type(exc).__name__}: {exc}',
            'regla': 'Corregir causa técnica conservando paquete y salidas; no seleccionar de nuevo.'})
        raise
