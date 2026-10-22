"""Revisa cobertura de CV y reproduce predicciones de modelos guardados."""
import os
import sys
import json
from pathlib import Path

for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[variable] = '2'
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import joblib
import numpy as np
import pandas as pd
from entrenamiento_oulad import TrainingData, sha, require, choose_threshold, save_json


def main():
    loader = TrainingData(ROOT)
    output = ROOT / 'reportes/entrenamiento_2026_10_19'
    distributions = pd.read_csv(loader.folder / 'distribucion_conjuntos.csv')
    checked_fits = checked_predictions = checked_models = 0
    for cut in loader.config['cortes']:
        folder = output / f'logistica/corte_{cut:02d}/regresion_logistica'
        for candidate in range(8):
            predictions = []
            for fold in range(5):
                path = folder / f'config_{candidate:02d}_fold_{fold}.json'
                row = json.loads(path.read_text(encoding='utf-8'))
                require(row['estado'] == 'correcto', 'Ajuste no convergente o fallido')
                require(sha(path.with_suffix('.parquet')) == row['predicciones_sha256'], 'Predicciones alteradas')
                d = pd.read_parquet(path.with_suffix('.parquet'))
                checked = d.merge(loader.people, on='id_student', validate='many_to_one')
                require(len(checked) == len(d), 'Persona sin manifiesto')
                require(checked.conjunto.eq('ajuste').all() and checked.pliegue_interno.eq(fold).all(),
                        'Predicciones de personas fuera del pliegue reservado')
                predictions.append(d)
                checked_fits += 1
            stacked = pd.concat(predictions, ignore_index=True)
            require(not stacked.duplicated(['id_student', 'code_module', 'code_presentation']).any(),
                    'Inscripción predicha dos veces en CV')
            expected = distributions.loc[distributions.corte.eq(cut) & distributions.conjunto.eq('ajuste'), 'inscripciones'].item()
            require(len(stacked) == expected, 'Cobertura incompleta en CV')
            checked_predictions += len(stacked)
        record = json.loads((folder / 'modelo_congelado.json').read_text(encoding='utf-8'))
        require(sha(folder / 'modelo_calibrado.joblib') == record['modelo_sha256'], 'Modelo alterado')
        # Solo se carga un artefacto local producido por esta ejecución.
        model = joblib.load(folder / 'modelo_calibrado.joblib')
        d = loader.load(cut, 'umbral')
        p = model.predict_proba(d[loader.predictors])[:, 1]
        saved = pd.read_parquet(folder / 'predicciones_umbral.parquet')
        require(d[['id_student', 'code_module', 'code_presentation']].equals(
            saved[['id_student', 'code_module', 'code_presentation']]), 'Orden de predicciones diferente')
        require(np.allclose(p, saved.probabilidad, rtol=0, atol=1e-12), 'La recarga no reproduce predicciones')
        require(choose_threshold(d.retiro_futuro, p) == record['umbral'], 'Umbral no reproducible')
        checked_models += 1
    save_json(output / 'verificacion_resultados.json', {
        'correcto': True, 'ajustes_logisticos_verificados': checked_fits,
        'predicciones_cv_verificadas': checked_predictions,
        'modelos_recargados_y_reproducidos': checked_models,
        'prueba_final_evaluada': False, 'lecturas_verificacion': loader.read_log})
    print(f'Correcto: {checked_fits} ajustes, {checked_models} modelos recargados; sin prueba final.')


if __name__ == '__main__':
    main()
