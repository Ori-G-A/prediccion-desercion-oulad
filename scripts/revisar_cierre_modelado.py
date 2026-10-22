"""Audita salidas congeladas y prepara síntesis; no ajusta ni selecciona modelos."""
import os
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']: os.environ[key]='2'
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from entrenamiento_oulad import sha, KEY, save_json
from evaluacion_reservada_oulad import verify_package
from metricas_evaluacion_oulad import metrics

SOURCE=ROOT/'reportes/continuacion_modelado_2026_10_20'
OUT=ROOT/'reportes/cierre_modelado_2026_10_21'
OUT.mkdir(exist_ok=True)
package=json.loads((SOURCE/'paquete_evaluacion.json').read_text(encoding='utf-8'))
verify_package(ROOT,package)
closure=json.loads((SOURCE/'evaluacion/cierre.json').read_text(encoding='utf-8'))
assert closure['paquete_sha256']==sha(SOURCE/'paquete_evaluacion.json')
for path,digest in closure['huellas_salidas'].items(): assert sha(SOURCE/'evaluacion'/path)==digest
people=pd.read_csv(ROOT/package['personas'])
test_ids=set(people.loc[people.conjunto.eq('prueba'),'id_student'])
results=json.loads((SOURCE/'evaluacion/metricas.json').read_text(encoding='utf-8'))['resultados']
principals=[]; intervals=[]; differences=[]; shap_summary=[]; checked=0
for cut in package['cortes']:
    folder=SOURCE/f'evaluacion/corte_{cut:02d}'
    predictions=pd.read_parquet(folder/'predicciones.parquet')
    assert not predictions.duplicated(KEY).any() and set(predictions.id_student)<=test_ids
    assert predictions.corte.eq(cut).all()
    for row in [r for r in results if r['corte']==cut]:
        actual=metrics(predictions.retiro_futuro,predictions[row['modelo']],row['umbral'])
        for field,value in actual.items():
            assert (value is None and row[field] is None) or (value is not None and np.isclose(value,row[field],rtol=0,atol=1e-12)),field
        assert len(predictions)==row['inscripciones'] and predictions.id_student.nunique()==row['personas']
        lead=predictions.loc[predictions.retiro_futuro.eq(1)&predictions[row['modelo']].gt(row['umbral']),'date_unregistration']-cut
        assert len(lead)==row['anticipacion_tp']['n'] and lead.gt(0).all()
        if len(lead):
            for label,q in [('q25',.25),('mediana',.5),('q75',.75)]: assert np.isclose(lead.quantile(q),row['anticipacion_tp'][label])
        checked+=1
    reps=pd.read_parquet(folder/'replicas.parquet')
    assert len(reps)==14000 and not reps.duplicated(['replica','modelo']).any()
    saved=json.loads((folder/'intervalos.json').read_text(encoding='utf-8'))
    for row in saved['intervalos']:
        values=reps.loc[reps.modelo.eq(row['modelo']),row['metrica']].dropna()
        assert len(values)==row['replicas_validas']
        if len(values): assert np.allclose(np.percentile(values,[2.5,97.5]),[row['inferior'],row['superior']],atol=1e-12)
        else: assert row['inferior'] is None and row['superior'] is None
        intervals.append({'corte':cut,**row})
    for row in saved['diferencias_pareadas']:
        a=reps.loc[reps.modelo.eq(row['a'])].set_index('replica')[row['metrica']]
        b=reps.loc[reps.modelo.eq(row['b'])].set_index('replica')[row['metrica']]
        values=(a-b).dropna()
        assert len(values)==row['replicas_validas']
        if len(values): assert np.allclose(np.percentile(values,[2.5,97.5]),[row['inferior_a_menos_b'],row['superior_a_menos_b']],atol=1e-12)
        else: assert row['inferior_a_menos_b'] is None and row['superior_a_menos_b'] is None
        differences.append({'corte':cut,**row})
    principal=next(r for r in results if r['corte']==cut and r['principal'])
    principals.append(principal)
    sf=SOURCE/f'shap/resultados/corte_{cut:02d}'
    check=json.loads((sf/'verificacion.json').read_text(encoding='utf-8'))
    assert check['paquete_sha256']==sha(SOURCE/'paquete_evaluacion.json')
    for path,digest in check['huellas'].items(): assert sha(sf/path)==digest
    contrib=pd.read_parquet(sf/'contribuciones.parquet')
    sample=pd.read_parquet(sf/'inscripciones_explicadas.parquet')
    assert contrib[KEY].equals(sample[KEY].reset_index(drop=True))
    merged=contrib.merge(predictions[KEY+[principal['modelo']]],on=KEY,validate='one_to_one')
    assert len(merged)==100 and np.allclose(merged.probabilidad,merged[principal['modelo']],rtol=0,atol=1e-12)
    assert np.max(np.abs(contrib['base']+contrib[package['predictores']].sum(axis=1)-contrib.probabilidad))<1e-12
    summary=pd.read_csv(sf/'resumen.csv').set_index('predictor')
    assert np.allclose(summary.loc[package['predictores'],'media_absoluta'],contrib[package['predictores']].abs().mean(),atol=1e-12)
    shap_summary.extend([{'corte':cut,**r} for r in summary.reset_index().to_dict('records')])
pd.DataFrame(results).drop(columns=['referencia_umbral_05','anticipacion_tp']).to_csv(OUT/'metricas_todas.csv',index=False)
pd.DataFrame(intervals).to_csv(OUT/'intervalos.csv',index=False)
pd.DataFrame(differences).to_csv(OUT/'diferencias.csv',index=False)
pd.DataFrame(shap_summary).to_csv(OUT/'shap_resumen.csv',index=False)
save_json(OUT/'sintesis.json',{'principales':principals,'intervalos':intervals,'diferencias':differences,'shap':shap_summary})
save_json(OUT/'verificacion.json',{'correcto':True,'modelos_referencia_cortes_verificados':checked,
    'huellas_evaluacion':len(closure['huellas_salidas']),'metricas_recalculadas':True,
    'intervalos_y_diferencias_recalculados_desde_replicas':True,'shap_inscripciones_verificadas':500,
    'limitaciones':'No repite entrenamientos ni 2000 remuestreos; verifica huellas, métricas, percentiles guardados y aditividad. No demuestra estabilidad de SHAP.',
    'paquete_sha256':sha(SOURCE/'paquete_evaluacion.json')})
for p in principals:
    ci=next(r for r in intervals if r['corte']==p['corte'] and r['modelo']==p['modelo'] and r['metrica']=='ap')
    tops=sorted([r for r in shap_summary if r['corte']==p['corte']],key=lambda r:-r['media_absoluta'])[:3]
    print(p['corte'],p['modelo'],'AP',p['ap'],'IC',ci['inferior'],ci['superior'],'FP/FN',p['fp'],p['fn'],'SHAP',tops)
