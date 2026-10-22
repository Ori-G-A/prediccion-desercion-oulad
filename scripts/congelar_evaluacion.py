"""Prepara un paquete reservado solo después de seleccionar y verificar candidatos."""
import argparse
import json
import os
import sys
from pathlib import Path

for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[variable] = '2'
import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from entrenamiento_oulad import TrainingData, KEY, sha, require, save_json, choose_threshold
from evaluacion_reservada_oulad import verify_package


def freeze(root, selection_path, design_path, tests_path, output):
    root, output = root.resolve(), output.resolve()
    require(not output.exists(), 'No sobrescribir un paquete congelado')
    loader = TrainingData(root)
    selection = json.loads(selection_path.read_text(encoding='utf-8'))
    require(selection['estado'] == 'seleccion_completa', 'Selección pendiente')
    design = json.loads(design_path.read_text(encoding='utf-8'))
    require(all(k in design for k in ['objeto', 'escala', 'variante', 'referencia', 'muestreo', 'dependencia']), 'Diseño SHAP incompleto')
    tests = json.loads(tests_path.read_text(encoding='utf-8'))
    require(tests.get('correcto') and tests.get('paquete_completo_verificado'), 'Falta verificar el evaluador integral con paquete sintético completo')
    require(tests.get('codigo_sha256') == sha(root/'src/evaluacion_reservada_oulad.py'), 'Verificación de otro código')
    candidates, prevalences, majority = [], {}, {}
    files = [selection_path, design_path, tests_path, loader.folder/'personas.csv', loader.folder/'configuracion.json',
             root/'decision_temporal.json', root/'src/evaluacion_reservada_oulad.py', root/'src/metricas_evaluacion_oulad.py',
             root/'src/entrenamiento_oulad.py', Path(__file__), root/'scripts/consolidar_validacion.py']
    files += [root/'scripts/explicar_modelos.py', root/'requirements-interpretacion.txt']
    for reference in design['referencia'].values():
        path = root/reference['archivo']
        require(sha(path) == reference['sha256'], 'Referencia SHAP alterada')
        files.append(path)
    for cut in loader.config['cortes']:
        fit = loader.load(cut, 'ajuste')
        prevalences[str(cut)] = float(fit.retiro_futuro.mean())
        majority[str(cut)] = int(prevalences[str(cut)] > .5)
    for selected in selection['seleccion_por_familia']:
        folder = root/selected['carpeta']
        record_path = folder/'modelo_congelado.json'
        record = json.loads(record_path.read_text(encoding='utf-8'))
        require(record['parametros'] == loader.config['configuraciones'][selected['modelo']][selected['configuracion']], 'Parámetros distintos del seleccionado')
        model_path = folder/'modelo_calibrado.joblib'
        require(sha(model_path) == record['modelo_sha256'], 'Modelo alterado')
        model = joblib.load(model_path)
        threshold_data = loader.load(selected['corte'], 'umbral')
        p = model.predict_proba(threshold_data[loader.predictors])[:, 1]
        saved = pd.read_parquet(folder/'predicciones_umbral.parquet')
        require(saved[KEY+['retiro_futuro']].equals(threshold_data[KEY+['retiro_futuro']]), 'Cobertura de umbral diferente')
        require(np.allclose(saved.probabilidad, p, rtol=0, atol=1e-12), 'Predicción recargada diferente')
        require(choose_threshold(threshold_data.retiro_futuro, p) == record['umbral'], 'Umbral no reproducible')
        candidates.append({'corte':selected['corte'], 'modelo':selected['modelo'], 'configuracion':selected['configuracion'],
                           'archivo_modelo':str(model_path.relative_to(root)), 'umbral':record['umbral']})
        files += [record_path, model_path, folder/'predicciones_umbral.parquet']
    data_paths = {str(c): f'data/processed/correcciones_2026_09_10/dataset_corte_{c:02d}.parquet' for c in loader.config['cortes']}
    files += [root/p for p in data_paths.values()]
    package = {'estado':'congelado', 'seleccion':str(selection_path.relative_to(root)), 'principales':selection['principales'],
        'cortes':loader.config['cortes'], 'predictores':loader.predictors, 'personas':str((loader.folder/'personas.csv').relative_to(root)),
        'datos':data_paths, 'candidatos':candidates, 'prevalencia_ajuste':prevalences, 'clase_mayoritaria_ajuste':majority,
        'bootstrap':{'replicas':2000,'semilla':20261022,'unidad':'persona'}, 'diseno_shap':design,
        'verificacion_evaluador':str(tests_path.relative_to(root)), 'huellas':{str(p.relative_to(root)):sha(p) for p in files},
        'comparaciones':'Todas las parejas, diferencias a menos b; intervalos percentiles descriptivos sin pruebas de significancia.',
        'anticipacion':'Mediana y cuartiles de date_unregistration menos corte entre verdaderos positivos; no efectividad educativa.',
        'subconjunto_comun':'No incluido; análisis opcional no necesario para la evaluación principal.',
        'prueba_final_abierta':False}
    verify_package(root, package)
    save_json(output, package)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seleccion', type=Path, required=True)
    parser.add_argument('--diseno-shap', type=Path, required=True)
    parser.add_argument('--verificacion', type=Path, required=True)
    parser.add_argument('--salida', type=Path, required=True)
    args=parser.parse_args()
    freeze(ROOT, args.seleccion.resolve(), args.diseno_shap.resolve(), args.verificacion.resolve(), args.salida)
