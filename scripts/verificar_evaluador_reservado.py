"""Verifica barreras y ejecución sintética; nunca abre la prueba OULAD."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[variable] = '2'

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import evaluacion_reservada_oulad as evaluation
from entrenamiento_oulad import save_json, sha, ORDER

TEMP_ROOT = ROOT / 'tmp/pruebas_evaluador'
TEMP_ROOT.mkdir(parents=True, exist_ok=True)


class FrozenSyntheticModel:
    def fit(self, *args, **kwargs):
        raise AssertionError('No está autorizado reajustar')

    def predict_proba(self, X):
        p = X['x'].to_numpy()
        return np.column_stack([1-p, p])


class ReservedTests(unittest.TestCase):
    def test_invalid_package_rejected_before_data(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp:
            root = Path(temp)
            save_json(root/'package.json', {'estado': 'pendiente'})
            with patch.object(evaluation.pd, 'read_parquet') as read:
                with self.assertRaisesRegex(ValueError, 'no congelado'):
                    evaluation.evaluate(root, root/'package.json', root/'results')
                read.assert_not_called()
            self.assertFalse((root/'reportes/continuacion_modelado_2026_10_19/primera_apertura_prueba.json').exists())

    def test_missing_hash_rejected(self):
        package = {'estado': 'congelado', 'bootstrap': {'replicas': 2000, 'semilla': 20261022, 'unidad': 'persona'},
                   'seleccion': 's.json', 'personas': 'p.csv', 'datos': {'7':'d.parquet'}, 'candidatos': [], 'huellas': {}}
        with self.assertRaisesRegex(ValueError, 'huellas obligatorias'):
            evaluation.verify_package(ROOT, package)

    def test_synthetic_flow_without_refitting(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp:
            root = Path(temp)
            pd.DataFrame({'id_student': [1,2,3,4], 'conjunto': ['prueba']*4}).to_csv(root/'people.csv', index=False)
            frame = pd.DataFrame({'id_student':[1,2,3,4], 'code_module':['AAA']*4, 'code_presentation':['2000A']*4,
                                  'retiro_futuro':[0,1,1,0], 'date_unregistration':[np.nan,15,20,np.nan], 'corte':[7]*4, 'x':[.1,.5,.8,.9]})
            frame.to_parquet(root/'synthetic.parquet', index=False)
            package = {'personas':'people.csv', 'cortes':[7], 'datos':{'7':'synthetic.parquet'}, 'predictores':['x'],
                       'candidatos':[{'corte':7,'modelo':'synthetic','archivo_modelo':'dummy','umbral':.5}],
                       'principales':{'7':'synthetic'}, 'prevalencia_ajuste':{'7':.4}, 'clase_mayoritaria_ajuste':{'7':0}}
            save_json(root/'package.json',package)
            # Esta prueba aísla el flujo; las barreras se prueban por separado.
            original_bootstrap = evaluation.paired_bootstrap
            def small_bootstrap(*args):
                return original_bootstrap(*args, repetitions=20)
            with patch.object(evaluation, 'verify_package'), patch.object(evaluation.joblib, 'load', return_value=FrozenSyntheticModel()), patch.object(evaluation, 'paired_bootstrap', side_effect=small_bootstrap):
                evaluation.evaluate(root, root/'package.json', root/'results')
                result=json.loads((root/'results/metricas.json').read_text(encoding='utf-8'))['resultados'][0]
                self.assertEqual(result['tp'],1)
                self.assertEqual(result['fn'],1)
                self.assertEqual(result['anticipacion_tp']['mediana'],13)
                self.assertTrue((root/'results/cierre.json').exists())
                save_json(root/'other.json', {**package, 'modificado':True})
                with self.assertRaisesRegex(ValueError,'otro paquete'):
                    evaluation.evaluate(root,root/'other.json',root/'results')

    def test_complete_package_and_tampering(self):
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temp:
            root = Path(temp).resolve()
            candidates, selected, paths = [], [], []
            cuts = [7, 14, 28, 42, 56]
            for name in ['src/evaluacion_reservada_oulad.py', 'src/metricas_evaluacion_oulad.py', 'src/entrenamiento_oulad.py']:
                target = root/name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT/name).read_bytes())
                paths.append(target)
            (root/'people.csv').write_text('id_student,conjunto\n1,prueba\n', encoding='utf-8')
            paths.append(root/'people.csv')
            for cut in cuts:
                data_path = root/f'data_{cut}.parquet'
                data_path.write_bytes(b'synthetic fixture for hash checks; no real data')
                paths.append(data_path)
                for name in ORDER:
                    folder = root/f'cut_{cut}/{name}'
                    folder.mkdir(parents=True)
                    model_path = folder/'model.joblib'
                    model_path.write_bytes(b'synthetic model bytes')
                    record = {'umbral': .5, 'base_inmutable_durante_calibracion': True, 'modelo_sha256': sha(model_path)}
                    save_json(folder/'modelo_congelado.json', record)
                    paths += [model_path, folder/'modelo_congelado.json']
                    candidates.append({'corte':cut,'modelo':name,'archivo_modelo':str(model_path.relative_to(root)),'umbral':.5})
                    selected.append({'corte':cut,'modelo':name,'carpeta':str(folder.relative_to(root))})
            selection = {'estado':'seleccion_completa','principales':{str(c):ORDER[0] for c in cuts},
                         'seleccion_por_familia':selected,'evidencias_sha256':{}}
            save_json(root/'selection.json',selection)
            paths.append(root/'selection.json')
            package = {'estado':'congelado','bootstrap':{'replicas':2000,'semilla':20261022,'unidad':'persona'},
                       'seleccion':'selection.json','personas':'people.csv','datos':{str(c):f'data_{c}.parquet' for c in cuts},
                       'candidatos':candidates,'principales':selection['principales'],'cortes':cuts,
                       'diseno_shap':{'objeto':'sintético'},'verificacion_evaluador':'synthetic-test',
                       'huellas':{str(p.relative_to(root)):sha(p) for p in paths}}
            evaluation.verify_package(root,package)
            (root/candidates[0]['archivo_modelo']).write_bytes(b'altered')
            with self.assertRaisesRegex(ValueError,'alterado'):
                evaluation.verify_package(root,package)


if __name__ == '__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ReservedTests))
    save_json(ROOT/'reportes/continuacion_modelado_2026_10_19/pruebas_evaluador.json', {'correcto':result.wasSuccessful(), 'pruebas':result.testsRun, 'errores':len(result.errors), 'fallos':len(result.failures), 'datos':'sintéticos', 'paquete_completo_verificado':result.wasSuccessful(), 'codigo_sha256':sha(ROOT/'src/evaluacion_reservada_oulad.py'), 'limite':'Validación de manifiesto completo y alteración de huellas; flujo sintético separado con 20 réplicas, no evaluación OULAD.'})
    sys.exit(not result.wasSuccessful())
