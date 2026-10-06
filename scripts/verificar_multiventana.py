"""Comprobaciones independientes de cortes, fuentes y casos de frontera."""
import json
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from oulad_revision import KEY, RAW, OUT, PROCESSED, sha256, save_json, weighted_rank_effect
from ventanas_oulad import build_at_cut,PREDICTORS

def main():
    checks=[]
    def check(name,result):
        assert bool(result),name
        checks.append({'verificacion':name,'estado':'correcta'})
    manifest=json.loads((OUT/'fuentes.json').read_text(encoding='utf-8'))
    check('Huellas de los siete CSV',all(sha256(RAW/f'{n}.csv')==r['sha256'] for n,r in manifest.items()))
    cuts=json.loads((ROOT/'decision_temporal.json').read_text(encoding='utf-8'))['cortes']
    stack=pd.read_parquet(PROCESSED/'dataset_multiventana.parquet')
    check('Clave inscripción y corte única',not stack.duplicated(KEY+['corte']).any())
    persons=set(stack.id_student.drop_duplicates().sample(60,random_state=20260908))
    logs=pd.concat([c.loc[c.id_student.isin(persons)] for c in pd.read_csv(RAW/'studentVle.csv',chunksize=500000)],ignore_index=True)
    deliveries=pd.read_csv(RAW/'studentAssessment.csv').merge(pd.read_csv(RAW/'assessments.csv'),on='id_assessment',validate='many_to_one')
    base=pd.read_parquet(PROCESSED/'base_auditoria.parquet')
    for t in cuts:
        d=stack.loc[stack.corte.eq(t)]
        X=pd.read_parquet(PROCESSED/f'predictores_corte_{t:02}.parquet')
        expected=base.loc[base.date_registration.notna()&base.date_registration.le(t)&(base.date_unregistration.isna()|base.date_unregistration.gt(t))&base.module_presentation_length.gt(t)]
        check(f'{t}: población exacta',set(map(tuple,d[KEY].to_numpy()))==set(map(tuple,expected[KEY].to_numpy())))
        check(f'{t}: evento futuro dentro del seguimiento',np.array_equal(d.retiro_futuro,(d.date_unregistration.gt(t)&d.date_unregistration.le(d.module_presentation_length)).astype(int)))
        check(f'{t}: candidatos sin desenlaces ni notas',set(X.columns)==set(KEY+['corte']+PREDICTORS) and not X.duplicated(KEY).any() and len(X)==len(d))
        sample=d.loc[d.id_student.isin(persons)]
        observed=logs.loc[logs.date.between(0,t)].groupby(KEY).sum_click.sum().reindex(pd.MultiIndex.from_frame(sample[KEY]),fill_value=0)
        check(f'{t}: clics desde CSV para muestra de 60 personas',np.array_equal(observed,sample.total_clics))
        valid=deliveries.loc[deliveries.is_banked.eq(0)&deliveries.assessment_type.ne('Exam')&deliveries.date_submitted.between(0,t)]
        counts=valid.groupby(KEY).id_assessment.nunique().reindex(pd.MultiIndex.from_frame(d[KEY]),fill_value=0)
        check(f'{t}: entregas desde toda la fuente CSV',np.array_equal(counts,d.n_evaluaciones_entregadas))
        check(f'{t}: faltantes estructurales',d.loc[d.total_clics.eq(0),'dias_desde_ultima_interaccion'].isna().all() and d.loc[d.n_evaluaciones_programadas.eq(0),'proporcion_programadas_entregadas'].isna().all())
        check(f'{t}: denominador inclusive',np.allclose(d.proporcion_dias_activos,d.dias_activos/(t+1)))
    common=pd.read_parquet(PROCESSED/'inscripciones_comunes.parquet')
    intersection=set.intersection(*[set(map(tuple,stack.loc[stack.corte.eq(t),KEY].to_numpy())) for t in cuts])
    check('Intersección de cinco cortes',set(map(tuple,common[KEY].to_numpy()))==intersection)
    b=pd.DataFrame({'id_student':[1,2,3,4,5],'code_module':['AAA']*5,'code_presentation':['2014J']*5,'date_registration':[0,0,0,8,np.nan],'date_unregistration':[np.nan,7,8,np.nan,np.nan],'module_presentation_length':[100]*5})
    daily=pd.DataFrame({'id_student':[1,1,1],'code_module':['AAA']*3,'code_presentation':['2014J']*3,'date':[0,7,8],'clics':[2,3,999],'registros':[1,1,1]})
    a=pd.DataFrame({'id_assessment':[10,11,12,13],'code_module':['AAA']*4,'code_presentation':['2014J']*4,'assessment_type':['TMA','TMA','Exam','TMA'],'date':[7,8,7,7]})
    s=a.merge(pd.DataFrame({'id_assessment':[10,11,12,13],'id_student':[1]*4,'date_submitted':[7,8,7,7],'is_banked':[0,0,0,1],'score':[80]*4}),on='id_assessment')
    before,_=build_at_cut(b,daily,s,a,7)
    check('Fronteras de elegibilidad y etiqueta',set(before.id_student)=={1,3} and before.set_index('id_student').loc[3,'retiro_futuro']==1)
    one=before.set_index('id_student').loc[1]
    check('Inclusión t, exclusión t+1, Exam y banked',one.total_clics==5 and one.n_evaluaciones_entregadas==1 and one.dias_desde_ultima_interaccion==0)
    check('CV activo de dos días calculado manualmente',np.isclose(one.cv_intensidad_activa,np.sqrt(.5)/2.5))
    single,_=build_at_cut(b,daily.loc[daily.date.eq(0)],s,a,7)
    point=single.set_index('id_student').loc[1]
    check('Un día activo: CV activo ausente y CV calendario definido',pd.isna(point.cv_intensidad_activa) and np.isclose(point.coef_variacion_clics,np.sqrt(8)))
    check('Conteo de filas conservado solo como auditoría','n_registros_vle' in before and 'n_registros_vle' not in PREDICTORS)
    check('Historia insuficiente distinta de cero',before[['log_ratio_7d','log_ratio_14d','sin_actividad_ultimos_14d','sin_actividad_ultimos_28d']].isna().all().all())
    daily.loc[daily.date.gt(7),'clics']=1000000
    s.loc[s.date_submitted.gt(7),'score']=0
    b.loc[b.id_student.eq(3),'date_unregistration']=99
    after,_=build_at_cut(b,daily,s,a,7)
    check('Invariancia frente a información futura',before[PREDICTORS].equals(after[PREDICTORS]))
    x=np.array([0.,1.,1.,3.,5.,2.]);y=np.array([0,1,0,1,0,1]);w=np.array([2,2,0,0,1,1])
    idx=np.repeat(np.arange(len(x)),w);xx,yy=x[idx],y[idx]
    expected=2*stats.mannwhitneyu(xx[yy==1],xx[yy==0]).statistic/((yy==1).sum()*(yy==0).sum())-1
    check('Bootstrap ponderado y empates',np.isclose(weighted_rank_effect(x,y,w),expected))
    for name in ['01_carga_exploracion.ipynb','02_feature_engineering.ipynb','03_analisis_estadistico.ipynb']:
        nb=json.loads((ROOT/name).read_text(encoding='utf-8'));cells=[c for c in nb['cells'] if c['cell_type']=='code']
        check(f'Ejecución completa: {name}',all(c['execution_count'] is not None and all(o['output_type']!='error' for o in c['outputs']) for c in cells))
    save_json('verificaciones_independientes.json',checks)
    print(f'{len(checks)} verificaciones satisfactorias.')

if __name__=='__main__':main()
