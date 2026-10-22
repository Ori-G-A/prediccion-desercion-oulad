"""Pruebas sintéticas: no carga datos OULAD ni modelos entrenados."""
import os
import sys
import unittest
from pathlib import Path

for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[variable] = '2'
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from metricas_evaluacion_oulad import metrics, person_weights, paired_bootstrap
from entrenamiento_oulad import save_json


class EvaluationTests(unittest.TestCase):
    def test_strict_threshold_and_counts(self):
        result = metrics([0, 1, 1, 0], [.1, .5, .8, .9], .5)
        self.assertEqual([result[k] for k in ['tn', 'fp', 'fn', 'tp']], [1, 1, 1, 1])
        self.assertEqual(result['f1'], .5)

    def test_cluster_weights(self):
        weights = person_weights([1, 1, 2, 3, 3], [1, 2, 3], np.random.default_rng(4))
        self.assertEqual(weights[0], weights[1])
        self.assertEqual(weights[3], weights[4])
        self.assertEqual(weights[[0, 2, 3]].sum(), 3)

    def test_weighted_equals_repeated_rows(self):
        y, p, w = np.array([0, 1, 1, 0]), np.array([.2, .6, .4, .9]), np.array([2, 2, 1, 0])
        weighted = metrics(y, p, .5, w)
        repeated = metrics(np.repeat(y, w), np.repeat(p, w), .5)
        for key in weighted:
            self.assertAlmostEqual(weighted[key], repeated[key])

    def test_single_class_is_undefined(self):
        result = metrics([0, 0], [.1, .2], .5)
        self.assertIsNone(result['ap'])
        self.assertIsNone(result['roc_auc'])
        self.assertIsNone(result['sensibilidad'])
        self.assertIsNone(result['precision'])
        self.assertAlmostEqual(result['brier'], .025)

    def test_paired_reproducible_bootstrap(self):
        args = ([1, 1, 2, 3], [0, 1, 1, 0], {'a': [.1, .8, .7, .2], 'b': [.1, .8, .7, .2]}, {'a': .5, 'b': .5}, [1, 2, 3])
        first, intervals, differences = paired_bootstrap(*args, repetitions=40)
        second, _, _ = paired_bootstrap(*args, repetitions=40)
        self.assertTrue(first.equals(second))
        self.assertTrue(all(d['inferior_a_menos_b'] == d['superior_a_menos_b'] == 0 for d in differences))
        self.assertTrue(all(d['replicas_validas'] + d['replicas_excluidas'] == 40 for d in intervals))

    def test_invalid_probabilities_rejected(self):
        with self.assertRaises(ValueError):
            metrics([0, 1], [.1, np.nan], .5)


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(EvaluationTests))
    save_json(ROOT / 'reportes/continuacion_modelado_2026_10_19/pruebas_metricas.json', {'correcto': result.wasSuccessful(), 'pruebas': result.testsRun, 'fallos': len(result.failures), 'errores': len(result.errors), 'datos': 'exclusivamente sintéticos', 'evaluador_integral_verificado': False})
    sys.exit(not result.wasSuccessful())
