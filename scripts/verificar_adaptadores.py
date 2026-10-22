"""Prueba sintética de dependencias opcionales y comprobación OULAD al día 7.

Los ajustes sintéticos reducen árboles/épocas; no seleccionan hiperparámetros.
La comprobación OULAD usa la primera configuración congelada de cada familia.
"""
import os
import sys
from pathlib import Path
for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[variable] = '2'
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
import pandas as pd
import joblib
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from entrenamiento_oulad import fit_pipeline, save_json, require, run_training, model_fingerprint


def main():
    rng = np.random.default_rng(20261021)
    X = pd.DataFrame(rng.normal(size=(240, 4)), columns=list('abcd'))
    y = np.tile([0, 0, 0, 1], 60)
    parameters = {
        'xgboost': {'n_estimators': 10, 'max_depth': 2, 'ponderacion': 'balanceada'},
        'lightgbm': {'n_estimators': 10, 'num_leaves': 7, 'min_child_samples': 5, 'class_weight': 'balanced'},
        'tabnet': {'n_d': 8, 'n_a': 8, 'n_steps': 3, 'max_epochs': 2, 'ponderacion': 'balanceada'}}
    results = []
    for name, params in parameters.items():
        base, caught, converged = fit_pipeline(name, params, X.iloc[:160], y[:160], 20261021)
        require(converged, f'Fallo de ajuste: {name}')
        if name == 'tabnet':
            weights = base['modelo'].model_.loss_fn.weight.detach().numpy()
            np.testing.assert_allclose(weights, [2 / 3, 2.])
            require(base['modelo'].model_.patience == 0, 'Early stopping activado')
        before = model_fingerprint(base)
        calibrated = CalibratedClassifierCV(FrozenEstimator(base), method='sigmoid')
        calibrated.fit(X.iloc[160:200], y[160:200])
        require(before == model_fingerprint(base), 'Calibración reajustó el modelo base')
        p = calibrated.predict_proba(X.iloc[200:])
        require(p.shape == (40, 2) and np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all(), 'Probabilidades inválidas')
        np.testing.assert_allclose(p.sum(axis=1), 1.)
        target = ROOT / f'reportes/entrenamiento_2026_10_19/artefactos_sinteticos/{name}.joblib'
        target.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(calibrated, target)
        restored = joblib.load(target)
        np.testing.assert_allclose(restored.predict_proba(X.iloc[200:]), p, rtol=0, atol=1e-12)
        results.append({'familia': name, 'ajuste_ponderado': True, 'calibracion_base_inmutable': True,
                        'predicciones_validas': True, 'parametros_sinteticos': params, 'advertencias': caught})
        print(f'Adaptador {name}: ajuste ponderado y calibración correctos.', flush=True)
    save_json(ROOT / 'reportes/entrenamiento_2026_10_19/pruebas_adaptadores.json',
              {'correcto': True, 'resultados': results, 'datos': 'sintéticos; no estiman desempeño OULAD'})
    results = run_training(ROOT, ROOT / 'reportes/entrenamiento_2026_10_19/comprobacion_adaptadores',
                           list(parameters), [7], mode='comprobacion')
    require(all(all(c['valida'] for c in r['candidatos']) for r in results), 'Falló la comprobación OULAD')


if __name__ == '__main__':
    main()
