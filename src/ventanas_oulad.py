"""Construcción uniforme de indicadores al cierre de cada corte administrativo."""
import numpy as np
import pandas as pd
from oulad_revision import KEY, COURSE

PREDICTORS = [
    'total_clics', 'dias_activos', 'proporcion_dias_activos',
    'promedio_clics_por_dia_activo', 'coef_variacion_clics', 'cv_intensidad_activa',
    'dias_desde_ultima_interaccion', 'recencia_relativa',
    'semanas_completas_activas', 'proporcion_semanas_completas_activas',
    'clics_pre_inicio', 'clics_ultimos_7d', 'clics_7d_previos',
    'log_ratio_7d', 'log_ratio_14d', 'sin_actividad_acumulada',
    'sin_actividad_ultimos_7d', 'sin_actividad_ultimos_14d',
    'sin_actividad_ultimos_28d', 'n_evaluaciones_entregadas',
    'n_entregas_pre_inicio', 'n_evaluaciones_programadas',
    'n_programadas_entregadas_al_corte', 'proporcion_programadas_entregadas',
    'sin_evaluacion_programada', 'sin_entregas_acumuladas',
]
CONTEXT = ['gender','region','highest_education','imd_band','age_band',
           'disability','num_of_prev_attempts','studied_credits']


def eligible_at(base, cut):
    """Filtrado secuencial; excluye retiros ocurridos exactamente en el corte."""
    steps = [{'corte':cut,'etapa':'Fuente','inscripciones':len(base),
              'personas':base.id_student.nunique(),'excluidas':0}]
    d = base.copy()
    for name, condition in [
        ('Matrícula conocida', lambda x:x.date_registration.notna()),
        ('Matriculada al corte', lambda x:x.date_registration.le(cut)),
        ('Sin retiro hasta corte', lambda x:x.date_unregistration.isna()|x.date_unregistration.gt(cut)),
        ('Final posterior al corte', lambda x:x.module_presentation_length.gt(cut))]:
        previous=len(d); d=d.loc[condition(d)].copy()
        steps.append({'corte':cut,'etapa':name,'inscripciones':len(d),
                      'personas':d.id_student.nunique(),'excluidas':previous-len(d)})
    d['retiro_futuro']=(d.date_unregistration.gt(cut)&d.date_unregistration.le(d.module_presentation_length)).astype('int8')
    return d, pd.DataFrame(steps)


def build_at_cut(base, daily, deliveries, assessments, cut):
    """Una fila por inscripción elegible. Las notas solo se exportan para auditoría.

    La función no calcula estadísticos ajustados con desenlaces. El filtro de
    elegibilidad/etiqueta usa fechas administrativas; los predictores no dependen
    del desenlace posterior ni de registros posteriores al corte.
    """
    assert isinstance(cut,int) and cut>=0
    d, flow=eligible_at(base,cut)
    idx=pd.MultiIndex.from_frame(d[KEY])
    history=daily.loc[daily.date.between(0,cut)]
    panel=(history.pivot(index=KEY,columns='date',values='clics')
           .reindex(index=idx,columns=range(cut+1)).fillna(0))
    f=panel.sum(axis=1).rename('total_clics').to_frame()
    f['dias_activos']=panel.gt(0).sum(axis=1)
    f['proporcion_dias_activos']=f.dias_activos/(cut+1)
    f['n_registros_vle']=history.groupby(KEY,observed=True).registros.sum().reindex(idx).fillna(0)
    f['promedio_clics_por_dia_activo']=f.total_clics/f.dias_activos.replace(0,np.nan)
    f['coef_variacion_clics']=panel.std(axis=1,ddof=1)/panel.mean(axis=1).replace(0,np.nan)
    active_panel=panel.where(panel.gt(0))
    f['cv_intensidad_activa']=active_panel.std(axis=1,ddof=1)/active_panel.mean(axis=1)
    last=history.groupby(KEY,observed=True).date.max().reindex(idx)
    f['dias_desde_ultima_interaccion']=cut-last
    f['recencia_relativa']=f.dias_desde_ultima_interaccion/(cut+1)
    weeks=(cut+1)//7
    f['semanas_completas_activas']=sum(panel.loc[:,range(w*7,w*7+7)].sum(axis=1).gt(0).astype(int) for w in range(weeks))
    f['proporcion_semanas_completas_activas']=f.semanas_completas_activas/weeks if weeks else np.nan
    f['clics_pre_inicio']=daily.loc[daily.date.lt(0)].groupby(KEY,observed=True).clics.sum().reindex(idx).fillna(0)
    f['sin_actividad_acumulada']=f.total_clics.eq(0).astype('int8')
    for span in [7,14,28]:
        f[f'sin_actividad_ultimos_{span}d']=(panel.loc[:,range(cut-span+1,cut+1)].sum(axis=1).eq(0).astype(float)
                                                    if cut+1>=span else np.nan)
    f['clics_ultimos_7d']=panel.loc[:,range(cut-6,cut+1)].sum(axis=1) if cut>=6 else np.nan
    f['clics_7d_previos']=panel.loc[:,range(cut-13,cut-6)].sum(axis=1) if cut>=13 else np.nan
    for span in [7,14]:
        if cut+1>=2*span:
            first=panel.loc[:,range(cut-2*span+1,cut-span+1)].sum(axis=1)
            second=panel.loc[:,range(cut-span+1,cut+1)].sum(axis=1)
            f[f'log_ratio_{span}d']=np.log((second+1)/(first+1)).where((first+second).gt(0))
        else:
            f[f'log_ratio_{span}d']=np.nan
    current=deliveries.loc[deliveries.is_banked.eq(0)&deliveries.assessment_type.ne('Exam')]
    observed=current.loc[current.date_submitted.between(0,cut)]
    academic=observed.groupby(KEY,observed=True).agg(
        n_evaluaciones_entregadas=('id_assessment','nunique'),
        n_puntajes_observados=('score','count'), score_promedio_observado=('score','mean')).reset_index()
    before=current.loc[current.date_submitted.lt(0)].groupby(KEY,observed=True).size().rename('n_entregas_pre_inicio').reset_index()
    due=assessments.loc[assessments.assessment_type.ne('Exam')&assessments.date.between(0,cut)]
    calendar=due.groupby(COURSE,observed=True).size().rename('n_evaluaciones_programadas').reset_index()
    completed=(current.loc[current.id_assessment.isin(due.id_assessment)&current.date_submitted.le(cut)]
               .groupby(KEY,observed=True).id_assessment.nunique().rename('n_programadas_entregadas_al_corte').reset_index())
    result=d.merge(f.reset_index(),on=KEY,validate='one_to_one')
    for frame, keys, validation in [(academic,KEY,'one_to_one'),(before,KEY,'one_to_one'),
                                     (calendar,COURSE,'many_to_one'),(completed,KEY,'one_to_one')]:
        result=result.merge(frame,on=keys,how='left',validate=validation)
    counts=['n_evaluaciones_entregadas','n_puntajes_observados','n_entregas_pre_inicio',
            'n_evaluaciones_programadas','n_programadas_entregadas_al_corte']
    result[counts]=result[counts].fillna(0).astype('int32')
    result['proporcion_programadas_entregadas']=result.n_programadas_entregadas_al_corte/result.n_evaluaciones_programadas.replace(0,np.nan)
    result['sin_evaluacion_programada']=result.n_evaluaciones_programadas.eq(0).astype('int8')
    result['sin_entregas_acumuladas']=result.n_evaluaciones_entregadas.eq(0).astype('int8')
    result['corte']=cut
    result['dias_calendario_observados']=cut+1
    result['horizonte_restante']=result.module_presentation_length-cut
    # Medida de exposición nominal; el cociente de actividad usa todo el calendario.
    result['dias_matriculada_en_ventana']=cut-result.date_registration.clip(lower=0)+1
    assert len(result)==len(d) and not result.duplicated(KEY).any()
    assert result.dias_activos.between(0,cut+1).all()
    assert result.proporcion_programadas_entregadas.dropna().between(0,1).all()
    assert result.dias_desde_ultima_interaccion.dropna().between(0,cut).all()
    assert result.date_registration.le(cut).all()
    assert (result.date_unregistration.isna()|result.date_unregistration.gt(cut)).all()
    return result, flow


DEFINITIONS={
 'total_clics': ('Suma de clics en 0..t', 'entero >= 0'),
 'dias_activos': ('Días con clics en 0..t', '0..t+1'),
 'proporcion_dias_activos': ('dias_activos/(t+1); calendario completo, no exposición individual', '[0,1]'),
 'n_registros_vle': ('Filas de la fuente en 0..t; no son sesiones', 'entero >= 0'),
 'promedio_clics_por_dia_activo': ('total_clics/dias_activos', 'NaN sin actividad'),
 'coef_variacion_clics': ('SD muestral de t+1 totales diarios / media; incluye ceros', 'NaN sin actividad'),
 'cv_intensidad_activa': ('SD muestral / media de clics solo en días activos; intensidad condicional', 'NaN si días activos < 2'),
 'dias_desde_ultima_interaccion': ('t - último día activo dentro de 0..t', 'NaN sin actividad'),
 'recencia_relativa': ('Recencia/(t+1)', 'NaN sin actividad'),
 'semanas_completas_activas': ('Bloques completos de 7 días desde 0 con actividad; omite bloque final parcial', '0..floor((t+1)/7)'),
 'proporcion_semanas_completas_activas': ('Semanas completas activas / floor((t+1)/7)', '[0,1]'),
 'clics_pre_inicio': ('Clics con fecha < 0', 'entero >= 0'),
 'clics_ultimos_7d': ('Clics en t-6..t', 'NaN si observación < 7 días'),
 'clics_7d_previos': ('Clics en t-13..t-7', 'NaN si observación < 14 días'),
 'log_ratio_7d': ('ln((clics últimos 7d+1)/(clics 7d previos+1))', 'NaN con historia <14 días o cero en ambos bloques'),
 'log_ratio_14d': ('Razón logarítmica suavizada entre últimos dos bloques de 14 días', 'NaN con historia <28 días o cero en ambos bloques'),
 'sin_actividad_acumulada': ('1 si total_clics=0', '0/1'),
 'n_evaluaciones_entregadas': ('Evaluaciones no Exam ni banked entregadas en 0..t', 'entero >= 0'),
 'n_entregas_pre_inicio': ('Entregas no Exam ni banked anteriores a 0', 'entero >= 0'),
 'n_evaluaciones_programadas': ('Evaluaciones no Exam con fecha de calendario en 0..t', 'entero >= 0'),
 'n_programadas_entregadas_al_corte': ('Evaluaciones programadas en 0..t entregadas hasta t, sin banked', '0..n programadas'),
 'proporcion_programadas_entregadas': ('Entregadas programadas / programadas; no mide puntualidad', 'NaN si no hay programadas'),
 'sin_evaluacion_programada': ('1 si no existen evaluaciones programadas en 0..t', '0/1'),
 'sin_entregas_acumuladas': ('1 si no hay entregas no Exam ni banked en 0..t; no implica incumplimiento', '0/1'),
}
for span in [7,14,28]:
    DEFINITIONS[f'sin_actividad_ultimos_{span}d']=(f'1 si no hay clics en t-{span-1}..t',f'NaN con menos de {span} días observados')
