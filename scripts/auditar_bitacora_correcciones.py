"""Contrastes de la bitácora; no modifica productos ni notebooks entregados."""
from pathlib import Path
import json
import hashlib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reportes/revision_bitacora_2026_09_10'
OUT.mkdir(parents=True, exist_ok=True)
KEY = ['id_student','code_module','code_presentation']
cuts = [7,14,28,42,56]
base = pd.read_parquet(ROOT/'data/processed/multiventana_2026_09_08/base_auditoria.parquet')
parts=[]
rows=0
for chunk in pd.read_csv(ROOT/'data/raw/studentVle.csv',chunksize=500000):
    rows += len(chunk)
    a=chunk.loc[chunk.date.between(0,56)]
    parts.append(a.groupby(KEY+['date'],observed=True).sum_click.sum())
daily=pd.concat(parts).groupby(level=list(range(4))).sum().rename('clics').reset_index()
results=[]
flows=[]
for t in cuts:
    d=pd.read_parquet(ROOT/f'data/processed/multiventana_2026_09_08/dataset_corte_{t:02}.parquet').set_index(KEY)
    a=daily.loc[daily.date.le(t)]
    agg=a.groupby(KEY).clics.agg(['sum','count','mean','std']).reindex(d.index)
    total=agg['sum'].fillna(0)
    k=agg['count'].fillna(0)
    assert np.array_equal(total.to_numpy(),d.total_clics.to_numpy())
    assert np.array_equal(k.to_numpy(),d.dias_activos.to_numpy())
    cvact=agg['std']/agg['mean']
    q=d.proporcion_dias_activos
    ok=k.ge(2)
    exact=(t+1)/t*((1-q[ok])/q[ok]+(k[ok]-1)/(k[ok]*q[ok])*cvact[ok]**2)
    err=float((exact-d.loc[ok,'coef_variacion_clics']**2).abs().max())
    assert err < 1e-9
    results.append({'corte':t,'n':len(d),'n_k_mayor_igual_2':int(ok.sum()),
                    'n_cv_activo_ausente':int(cvact.isna().sum()),
                    'rho_cv_calendario_q':d.coef_variacion_clics.corr(q,method='spearman'),
                    'rho_cv_calendario_q_mismos_casos':d.loc[ok,'coef_variacion_clics'].corr(q[ok],method='spearman'),
                    'rho_cv_activo_q':cvact.corr(q,method='spearman'),
                    'error_max_identidad_cv_cuadrado':err,'clics_y_dias_activos_contraste_completo':True})
    r,u=base.date_registration,base.date_unregistration
    prior=r.notna() & r.le(t)
    selected=prior & (u.isna()|u.gt(t)) & base.module_presentation_length.gt(t)
    assert int(selected.sum()) == len(d)
    pre=int((prior & u.lt(0)).sum())
    during=int((prior & u.between(0,t)).sum())
    unknown=int(r.isna().sum()); late=int((r.notna() & r.gt(t)).sum())
    ended=int((prior & (u.isna()|u.gt(t)) & base.module_presentation_length.le(t)).sum())
    assert len(d)+pre+during+unknown+late+ended==len(base)
    flows.append({'corte':t,'elegibles':len(d),'matricula_ausente':unknown,'matricula_tardia':late,
                  'retiro_pre_inicio_tras_filtrar_matricula':pre,'retiro_0_t_tras_filtrar_matricula':during,
                  'final_no_posterior':ended,'doble_conteo_si_se_usan_2678':2678-pre})
pd.DataFrame(results).to_csv(OUT/'contraste_cv.csv',index=False)
pd.DataFrame(flows).to_csv(OUT/'particion_exclusiones.csv',index=False)
assess=pd.read_csv(ROOT/'data/raw/assessments.csv')
courses=pd.read_csv(ROOT/'data/raw/courses.csv')
first=assess.loc[assess.assessment_type.ne('Exam')].groupby(['code_module','code_presentation']).date.min()
first.to_csv(OUT/'primera_evaluacion_continua.csv')
weights=assess.groupby(['code_module','code_presentation']).weight.sum()
weights.loc[weights.ne(200)].to_csv(OUT/'pesos_distintos_200.csv')
examples={}
for name,vals in {'A':[30,30,0,0,0,0,0,0],'B':[5,5,5,5,5,5,0,0],'C':[10,50,0,0,0,0,0,0]}.items():
    x=np.array(vals,dtype=float);active=x[x>0]
    examples[name]={'CV':float(x.std(ddof=1)/x.mean()),'CV_activo':float(active.std(ddof=1)/active.mean())}
out={'filas_vle_leidas':rows,'cortes_con_contraste_completo':results,'exclusiones':flows,
     'evaluaciones_sin_fecha_por_tipo':assess.loc[assess.date.isna()].assessment_type.value_counts().to_dict(),
     'duracion_min':int(courses.module_presentation_length.min()),'duracion_max':int(courses.module_presentation_length.max()),
     'primera_evaluacion_continua_min':float(first.min()),'primera_evaluacion_continua_max':float(first.max()),
     'ejemplos_cv':examples,'tendencia_200_100':float(np.log(101/201)),
     'tendencia_20_10':float(np.log(11/21)),
     'sha256_bitacora':hashlib.sha256((ROOT/'correcciones_proyecto_aplicado.md').read_bytes()).hexdigest(),
     'alcance':'Auditoría independiente; no sustitución del indicador, no PCA ni bootstrap reejecutados, no modelos.'}
(OUT/'verificaciones.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
