"""Calcula SHAP solo tras completar la evaluación del paquete congelado."""
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
import shap
from threadpoolctl import threadpool_limits

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from entrenamiento_oulad import KEY, require, sha, save_json
from evaluacion_reservada_oulad import verify_package


def explain(package_path, evaluation_folder, output):
    package=json.loads(package_path.read_text(encoding='utf-8'))
    verify_package(ROOT,package)
    closure=json.loads((evaluation_folder/'cierre.json').read_text(encoding='utf-8'))
    require(closure['estado']=='evaluacion_completa' and closure['paquete_sha256']==sha(package_path), 'Evaluación no completada con este paquete')
    design=package['diseno_shap']
    people=pd.read_csv(ROOT/package['personas'])
    ids=people.loc[people.conjunto.eq('prueba'),'id_student'].tolist()
    output.mkdir(parents=True,exist_ok=True)
    for cut in package['cortes']:
        name=package['principales'][str(cut)]
        candidate=next(r for r in package['candidatos'] if r['corte']==cut and r['modelo']==name)
        reference_record=design['referencia'][str(cut)]
        require(sha(ROOT/reference_record['archivo'])==reference_record['sha256'], 'Referencia SHAP alterada')
        reference=pd.read_parquet(ROOT/reference_record['archivo'])[package['predictores']]
        data=pd.read_parquet(ROOT/package['datos'][str(cut)], columns=KEY+package['predictores'],
                             filters=[('id_student','in',ids)]).sort_values(KEY).reset_index(drop=True)
        sample=data.sample(n=min(design['n_explicaciones'],len(data)),random_state=20261024+cut)
        X=sample[package['predictores']]
        model=joblib.load(ROOT/candidate['archivo_modelo'])
        def predict(values):
            return model.predict_proba(pd.DataFrame(values,columns=package['predictores']))[:,1]
        masker=shap.maskers.Independent(reference,max_samples=len(reference))
        explainer=shap.PermutationExplainer(predict,masker,seed=design['semilla']+cut)
        with threadpool_limits(limits=2):
            result=explainer(X,max_evals=design['ciclos']*(2*len(package['predictores'])+1),batch_size=256,silent=True)
            probabilities=predict(X)
        error=np.max(np.abs(np.asarray(result.base_values)+result.values.sum(axis=1)-probabilities))
        require(np.isfinite(result.values).all() and error<1e-6,'Aditividad SHAP no verificada')
        folder=output/f'corte_{cut:02d}'
        folder.mkdir(exist_ok=True)
        values=sample[KEY].reset_index(drop=True)
        for index,column in enumerate(package['predictores']):
            values[column]=result.values[:,index]
        values['base']=result.base_values
        values['probabilidad']=probabilities
        values.to_parquet(folder/'contribuciones.parquet',index=False)
        sample.to_parquet(folder/'inscripciones_explicadas.parquet',index=False)
        pd.DataFrame({'predictor':package['predictores'],'media_absoluta':np.abs(result.values).mean(axis=0),
                      'media_con_signo':result.values.mean(axis=0)}).sort_values('media_absoluta',ascending=False).to_csv(folder/'resumen.csv',index=False)
        save_json(folder/'verificacion.json',{'modelo':name,'corte':cut,'filas':len(sample),'shap':shap.__version__,
            'error_aditividad_maximo':float(error),'paquete_sha256':sha(package_path),'referencia_sha256':reference_record['sha256'],
            'huellas':{str(p.name):sha(p) for p in folder.glob('*') if p.is_file() and p.name!='verificacion.json'},
            'limites':design['dependencia']})
        print(f'SHAP terminado: corte {cut}, modelo {name}, {len(sample)} inscripciones',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paquete',type=Path,required=True)
    parser.add_argument('--evaluacion',type=Path,required=True)
    parser.add_argument('--salida',type=Path,required=True)
    args=parser.parse_args()
    explain(args.paquete,args.evaluacion,args.salida)
