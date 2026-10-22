"""Comprueba SHAP con una función sintética de contribuciones conocidas."""
import os
import sys
from pathlib import Path
for variable in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[variable]='2'
import numpy as np
import pandas as pd
import shap

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from entrenamiento_oulad import save_json

reference=pd.DataFrame({'a':[0.,1.,0.,1.],'b':[0.,0.,1.,1.]})
sample=pd.DataFrame({'a':[1.,0.],'b':[1.,0.]})
def predict(values):
    a=np.asarray(values)
    return .2+.1*a[:,0]+.2*a[:,1]

explainer=shap.PermutationExplainer(predict,shap.maskers.Independent(reference),seed=20261025)
result=explainer(sample,max_evals=100,silent=True)
expected=(sample-reference.mean()).to_numpy()*np.array([.1,.2])
np.testing.assert_allclose(result.values,expected,atol=1e-12)
np.testing.assert_allclose(result.base_values+result.values.sum(axis=1),predict(sample),atol=1e-12)
save_json(ROOT/'reportes/continuacion_modelado_2026_10_20/pruebas_shap.json',
          {'correcto':True,'shap':shap.__version__,'datos':'sintéticos','contribuciones_analiticas':True,'aditividad':True,
           'limite':'No verifica todavía modelos OULAD ni estabilidad de la aproximación en ellos.'})
print('SHAP sintético: contribuciones analíticas y aditividad correctas.')
