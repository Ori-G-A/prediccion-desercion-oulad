"""Definiciones observacionales de las variables derivadas de la revisión."""
DEFINITIONS = {
 'total_clics': ('Suma de clics registrados en días 0 a 27', 'studentVle', 'entero >= 0; ausencia de registros = 0'),
 'dias_activos': ('Número de días con clics registrados en días 0 a 27', 'studentVle', 'entero entre 0 y 28'),
 'n_registros_vle': ('Número de filas originales en días 0 a 27; no son sesiones', 'studentVle', 'entero >= 0'),
 'promedio_clics_por_dia_activo': ('total_clics / dias_activos', 'studentVle', 'positivo; NaN si dias_activos = 0'),
 'coef_variacion_clics': ('Desviación estándar muestral de 28 totales diarios / media diaria', 'studentVle', '>= 0; NaN si total_clics = 0'),
 'semanas_activas': ('Número de bloques 0-6, 7-13, 14-20 y 21-27 con clics', 'studentVle', 'entero entre 0 y 4'),
 'dias_desde_ultima_interaccion': ('27 - último día con clics dentro de la ventana', 'studentVle', '0 a 27; NaN sin actividad'),
 'clics_quincena_1': ('Suma de clics en días 0 a 13', 'studentVle', 'entero >= 0'),
 'clics_quincena_2': ('Suma de clics en días 14 a 27', 'studentVle', 'entero >= 0'),
 'log_ratio_actividad': ('ln((clics_quincena_2 + 1)/(clics_quincena_1 + 1))', 'studentVle', 'real; NaN si ambas quincenas son cero'),
 'sin_actividad_ventana': ('1 cuando no existen clics registrados en días 0 a 27', 'studentVle', '0 o 1'),
 'clics_pre_inicio': ('Suma de clics con date < 0; límite inicial dado por la fuente', 'studentVle', 'entero >= 0'),
 'n_evaluaciones_entregadas': ('Número de evaluaciones distintas, no Exam y no banked, entregadas en días 0 a 27', 'studentAssessment + assessments', 'entero >= 0'),
 'n_entregas_pre_inicio': ('Número de entregas no Exam y no banked con date_submitted < 0', 'studentAssessment + assessments', 'entero >= 0'),
 'n_evaluaciones_programadas': ('Evaluaciones no Exam con fecha de calendario en días 0 a 27', 'assessments', 'entero >= 0; calendario de presentación'),
 'n_programadas_entregadas_al_corte': ('Evaluaciones del calendario 0-27 entregadas antes de 28, sin banked', 'studentAssessment + assessments', '0 hasta n_evaluaciones_programadas'),
 'sin_evaluacion_programada': ('1 si n_evaluaciones_programadas = 0', 'assessments', '0 o 1'),
 'sin_entregas_ventana': ('1 si n_evaluaciones_entregadas = 0; no significa incumplimiento', 'studentAssessment + assessments', '0 o 1'),
 'proporcion_programadas_entregadas': ('n_programadas_entregadas_al_corte / n_evaluaciones_programadas', 'studentAssessment + assessments', '0 a 1; NaN si denominador = 0'),
 'score_promedio_temprano': ('Promedio de puntajes no nulos de entregas no Exam/no banked en días 0-27', 'studentAssessment + assessments', '0 a 100; NaN sin puntaje; auditoría'),
 'n_puntajes_observados': ('Número de puntajes no nulos en entregas tempranas', 'studentAssessment', 'entero >= 0; auditoría'),
 'retiro_futuro': ('1 si 28 < date_unregistration <= module_presentation_length', 'studentRegistration + courses', '0 o 1; solo población elegible'),
 'sin_vle_en_todo_registro': ('Ausencia de registros VLE en toda la fuente para la inscripción', 'studentVle', '0 o 1; retrospectivo'),
}
for d in [7,14,28]:
    DEFINITIONS[f'sin_actividad_ultimos_{d}d'] = (
        f'1 si no hay clics en los últimos {d} días de la ventana terminada en 27',
        'studentVle', '0 o 1; indicador exploratorio complementario')
