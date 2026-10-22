"""Pruebas de aislamiento, pesos, faltantes y umbral sin datos de prueba."""
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[variable] = '2'
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, recall_score
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
import joblib
from entrenamiento_oulad import (TrainColumns, TrainingData, fit_pipeline, choose_threshold,
                                 build_pipeline, save_json)


class ProtocolTests(unittest.TestCase):
    def test_train_only_columns_and_median(self):
        X = pd.DataFrame({'a': [1., 2., np.nan, 4.], 'vacia': [np.nan] * 4, 'constante': [3.] * 4})
        model, _ = build_pipeline('regresion_logistica', {'C': 1., 'max_iter': 3000}, 3)
        model.fit(X, [0, 0, 1, 1])
        before = joblib.hash(model)
        changed = pd.DataFrame({'a': [1e9, np.nan], 'vacia': [20., 40.], 'constante': [9., 80.]})
        model.predict_proba(changed)
        self.assertEqual(model['columnas'].columns_, ['a'])
        self.assertEqual(model['imputacion'].statistics_[0], 2.)
        self.assertEqual(joblib.hash(model), before)

    def test_schema_and_infinite_rejected(self):
        selector = TrainColumns().fit(pd.DataFrame({'x': [0, 1], 'y': [1, 3]}))
        with self.assertRaises(ValueError):
            selector.transform(pd.DataFrame({'y': [1, 3], 'x': [0, 1]}))
        with self.assertRaises(ValueError):
            selector.transform(pd.DataFrame({'x': [0, float('inf')], 'y': [1, 3]}))

    def test_weights_from_training_only(self):
        X = pd.DataFrame({'x': np.arange(8, dtype=float)})
        y = np.array([0] * 6 + [1] * 2)
        with patch('entrenamiento_oulad.compute_sample_weight', wraps=__import__(
                'sklearn.utils.class_weight', fromlist=['compute_sample_weight']).compute_sample_weight) as weights:
            model, _, ok = fit_pipeline('regresion_logistica', {'class_weight': 'balanced', 'max_iter': 3000}, X, y, 1)
        self.assertTrue(ok)
        np.testing.assert_array_equal(weights.call_args.args[1], y)
        self.assertIsNone(model['modelo'].class_weight)  # no double weighting

    def test_threshold_matches_exhaustive_search(self):
        rng = np.random.default_rng(24)
        for _ in range(40):
            y = np.r_[0, 1, rng.integers(0, 2, 30)]
            p = rng.choice([0., 0.1, 0.3, 0.5, 1.], len(y))
            options = np.r_[np.nextafter(p.min(), -np.inf), np.unique(p)]
            expected = max(options, key=lambda t: (f1_score(y, p > t), recall_score(y, p > t), -t))
            self.assertEqual(choose_threshold(y, p), expected)

    def test_equal_scores_and_boundary(self):
        y = np.array([0, 0, 1, 1])
        for p in [np.zeros(4), np.ones(4)]:
            t = choose_threshold(y, p)
            self.assertTrue((p > t).all())

    def test_calibration_does_not_refit_pipeline(self):
        X = pd.DataFrame({'x': np.arange(20, dtype=float)})
        y = np.tile([0, 1], 10)
        model, _, _ = fit_pipeline('regresion_logistica', {'max_iter': 3000}, X.iloc[:10], y[:10], 1)
        before = joblib.hash(model)
        calibrated = CalibratedClassifierCV(FrozenEstimator(model), method='sigmoid')
        calibrated.fit(X.iloc[10:], y[10:])
        self.assertEqual(joblib.hash(model), before)

    def test_test_partition_rejected_before_parquet_read(self):
        loader = TrainingData(ROOT)
        with patch('entrenamiento_oulad.pd.read_parquet') as read:
            with self.assertRaisesRegex(ValueError, 'prueba final'):
                loader.load(28, 'prueba')
            read.assert_not_called()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ProtocolTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    save_json(ROOT / 'reportes/entrenamiento_2026_10_19/pruebas.json',
              {'ejecutadas': result.testsRun, 'fallos': len(result.failures), 'errores': len(result.errors),
               'correcto': result.wasSuccessful(), 'prueba_final_leida': False})
    sys.exit(0 if result.wasSuccessful() else 1)
