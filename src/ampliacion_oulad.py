"""Sensibilidades descriptivas y controles completos de la versión corregida."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from oulad_revision import KEY, COURSE, RAW, OUT, PROCESSED, table, figure, save_json
from ventanas_oulad import build_at_cut, PREDICTORS


def efecto(frame, variable):
    d=frame.loc[frame[variable].notna()]
    a=d.loc[d.retiro_futuro.eq(1),variable];b=d.loc[d.retiro_futuro.eq(0),variable]
    return 2*mannwhitneyu(a,b).statistic/(len(a)*len(b))-1 if len(a) and len(b) else np.nan


def ejecutar_ampliacion(datasets):
    base=pd.read_parquet(PROCESSED/'base_auditoria.parquet')
    assessments=pd.read_csv(RAW/'assessments.csv')
    deliveries=pd.read_parquet(PROCESSED/'entregas_metadatos.parquet')
    alternative=pd.read_parquet(PROCESSED/'actividad_diaria_sin_exactos.parquet')
    checks=[];cvrows=[];pcarows=[];duprows=[];partitions=[]
    # Reconstrucción directa desde todo el CSV, independiente del panel guardado.
    pieces=[];source_rows=0
    for chunk in pd.read_csv(RAW/'studentVle.csv',chunksize=500000):
        source_rows+=len(chunk)
        current=chunk.loc[chunk.date.between(0,56)]
        pieces.append(current.groupby(KEY+['date'],observed=True).sum_click.sum())
    daily=pd.concat(pieces).groupby(level=list(range(4))).sum().rename('clics').reset_index()
    assert source_rows==10655280
    for cut,d in datasets.items():
        d=d.copy();idx=pd.MultiIndex.from_frame(d[KEY])
        days=daily.loc[daily.date.le(cut)]
        agg=days.groupby(KEY).clics.agg(['sum','count','mean','std']).reindex(idx)
        assert np.array_equal(agg['sum'].fillna(0),d.total_clics)
        assert np.array_equal(agg['count'].fillna(0),d.dias_activos)
        actual_cv=(agg['std']/agg['mean']).to_numpy()
        assert np.allclose(actual_cv,d.cv_intensidad_activa,equal_nan=True)
        X=pd.read_parquet(PROCESSED/f'predictores_corte_{cut:02}.parquet')
        assert 'n_registros_vle' not in X and set(X.columns)==set(KEY+['corte']+PREDICTORS)
        checks.append({'corte':cut,'inscripciones':len(d),'clics_dias_cv_desde_csv_completo':True,'conteo_filas_fuera_candidatos':True})
        valid=d.dias_activos.ge(2);a=d.loc[valid];k=a.dias_activos;q=a.proporcion_dias_activos
        exact=(cut+1)/cut*((1-q)/q+(k-1)/(k*q)*a.cv_intensidad_activa**2)
        assert np.allclose(exact,a.coef_variacion_clics**2)
        cvrows.append({'corte':cut,'n':len(d),'observados_calendario':int(d.coef_variacion_clics.notna().sum()),
                       'observados_activos':int(valid.sum()),'rho_calendario_q':d.coef_variacion_clics.corr(d.proporcion_dias_activos,method='spearman'),
                       'rho_calendario_q_mismos':a.coef_variacion_clics.corr(q,method='spearman'),
                       'rho_activo_q':a.cv_intensidad_activa.corr(q,method='spearman')})
        shared=pd.DataFrame({'log_volumen':np.log1p(a.total_clics),'proporcion_activa':q,
                              'log_intensidad':np.log1p(a.promedio_clics_por_dia_activo),
                              'recencia':a.recencia_relativa,'CV_calendario':a.coef_variacion_clics,'CV_activo':a.cv_intensidad_activa})
        specs={'original_mismos_casos':['log_volumen','proporcion_activa','log_intensidad','recencia','CV_calendario'],
               'sin_volumen':['proporcion_activa','log_intensidad','recencia','CV_calendario'],
               'intensidad_activa':['proporcion_activa','log_intensidad','recencia','CV_activo']}
        for name,cols in specs.items():
            pca=PCA(svd_solver='full').fit(StandardScaler().fit_transform(shared[cols]))
            pcarows.append({'corte':cut,'especificacion':name,'n':len(shared),'variables':len(cols),
                            'columnas':' | '.join(cols),'varianza_2_pct':100*pca.explained_variance_ratio_[:2].sum()})
        alt,_=build_at_cut(base,alternative,deliveries,assessments,int(cut))
        alt=d[KEY].merge(alt,on=KEY,validate='one_to_one')
        assert np.array_equal(d.retiro_futuro,alt.retiro_futuro)
        for v in ['total_clics','proporcion_dias_activos','recencia_relativa','coef_variacion_clics','cv_intensidad_activa','log_ratio_7d','log_ratio_14d']:
            before=efecto(d,v);after=efecto(alt,v)
            duprows.append({'corte':cut,'variable':v,'n_original':int(d[v].notna().sum()),'n_alternativo':int(alt[v].notna().sum()),
                            'efecto_original':before,'efecto_sin_exactos':after,'diferencia':after-before})
        r,u=base.date_registration,base.date_unregistration;known=r.notna()&r.le(cut)
        pieces={'matricula_desconocida':int(r.isna().sum()),'matricula_posterior':int((r.notna()&r.gt(cut)).sum()),
                'retiro_preinicio_tras_matricula':int((known&u.lt(0)).sum()),'retiro_0_t_tras_matricula':int((known&u.between(0,cut)).sum()),
                'fin_no_posterior':int((known&(u.isna()|u.gt(cut))&base.module_presentation_length.le(cut)).sum()),
                'elegibles':len(d)}
        assert sum(pieces.values())==len(base)
        partitions.append({'corte':cut,**pieces})
    table('02_particion_exclusiones',pd.DataFrame(partitions))
    table('03_comparacion_cv',pd.DataFrame(cvrows));table('03_sensibilidad_pca',pd.DataFrame(pcarows))
    table('03_sensibilidad_duplicados_efectos',pd.DataFrame(duprows))
    first=assessments.loc[assessments.assessment_type.ne('Exam')].groupby(COURSE,observed=True).date.min().reset_index(name='primera_fecha')
    table('02_primera_evaluacion',first)
    # Publicación de los atributos fuente: denominadores, distribución y faltantes.
    context=[]
    for t,d in datasets.items():
        for v in ['studied_credits','num_of_prev_attempts']:
            x=d[v];context.append({'corte':t,'variable':v,'n':len(d),'observados':int(x.notna().sum()),
                                   'faltantes':int(x.isna().sum()),'min':x.min(),'q25':x.quantile(.25),
                                   'mediana':x.median(),'q75':x.quantile(.75),'max':x.max(),'efecto':efecto(d,v)})
    table('03_contexto_numerico',pd.DataFrame(context))
    # Verifica estabilidad numérica de extremos; tolerancia descriptiva fijada antes de ejecutar.
    stability=pd.read_csv(OUT/'tablas/03_estabilidad_bootstrap.csv')
    s=stability.loc[stability.B.eq(2000)].copy();s['tolerancia']=.005
    s['dentro_tolerancia']=s.cambio_max_frente_5000.le(.005)
    table('03_estabilidad_resumen',s)
    save_json('verificaciones_ampliacion.json',{'filas_csv_leidas':source_rows,'cortes':checks,
              'identidad_cv_verificada':True,'poblacion_y_evento_invariantes_deduplicacion':True,
              'bootstrap_tolerancia_extremos':.005,'bootstrap_comparaciones':len(s),
              'bootstrap_dentro_tolerancia':int(s.dentro_tolerancia.sum()),
              'bootstrap_cambio_max':float(s.cambio_max_frente_5000.max()),'modelos_entrenados':False})
    # Funciones de presentación compartidas por notebooks y PDF.
    from figuras_oulad import fechas_retiro, calendario_evaluaciones, disponibilidad_indicadores
    fechas_retiro(base, list(datasets)); figure('01_fechas_retiro')
    calendario_evaluaciones(first, list(datasets)); figure('02_calendario_evaluaciones')
    disponibilidad_indicadores(datasets); figure('02_disponibilidad_indicadores')
