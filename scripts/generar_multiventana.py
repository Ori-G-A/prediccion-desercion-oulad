"""Redacción reproducible de los tres informes de comparación temporal."""
import shutil
import json
import re
import pandas as pd
from generar_informes import ROOT,OUT,DEST,data,summary,tab,fig,write_report,number

def build():
    old=ROOT/'reportes/revision_2026_09_08/informes'
    shutil.copy2(old/'referencias_revision.bib',DEST/'referencias_revision.bib')
    previous=json.loads((old.parent/'fuentes.json').read_text(encoding='utf-8'))
    current=summary('fuentes')
    assert {k:v['sha256'] for k,v in previous.items()}=={k:v['sha256'] for k,v in current.items()}, 'Fuentes cambiadas: revisar la redacción de auditoría'
    # La auditoría de las fuentes conserva su alcance; se sustituye su sensibilidad.
    body=(old/'01_exploracion_contenido.tex').read_text(encoding='utf-8')
    start=body.index('En los días 0 a 27,')
    end=body.index('\\section{Faltantes',start)
    sensitivity=data('01_sensibilidad_cortes')[['corte','clics_originales','clics_sin_exactos','reduccion_pct']]
    sensitivity.columns=['Corte','Clics originales','Sin exactos','Reducción (\\%)']
    sensitivity.columns=['Corte','Clics originales','Sin exactos','Reducción (%)']
    replacement=r'''El procesamiento principal conserva las filas originales. La Tabla~\ref{multi01:sensibilidad} presenta la alternativa de retirar repeticiones exactas dentro de cada ventana inclusiva de días 0 a $t$. Los totales corresponden a toda la actividad registrada en esas fechas, antes de restringirla a la población elegible; por ello, no equivalen a los totales de los conjuntos analíticos. La reducción se sitúa aproximadamente entre 3,27 y 3,50 por ciento. Se trata de una sensibilidad del volumen, no de evidencia de que la deduplicación represente la fuente verdadera ni de una evaluación de su impacto predictivo.

'''+tab(sensitivity,'Sensibilidad de los clics en cada ventana, sobre la fuente completa.','multi01:sensibilidad',[.12,.28,.28,.23])+ '\n'
    body=body[:start]+replacement+body[end:]
    # Actualizar también la paginación de las tablas heredadas de la auditoría.
    def reserve_legacy(match):
        block=match.group(0)
        a=block.index(r'\endfoot')+len(r'\endfoot')
        b=block.index(r'\end{longtable}')
        rows=block[a:b]
        count=rows.count(r'\\')
        if count<=12:
            rows=re.sub(r'\\\\(?!\*)',lambda m:r'\\*',rows)
            block=block[:a]+rows+block[b:]
        reserve=.18 if count<=3 else .23 if count<=7 else .28
        return r'\Needspace{'+str(reserve)+r'\textheight}'+block
    body=re.sub(r'\\begingroup.*?\\end\{longtable\}\\endgroup',reserve_legacy,body,flags=re.S)
    body=body.replace('\\section{Definición administrativa del retiro}',r'\section{Definición administrativa del retiro}'+'\nLa distribución por fechas conserva el día 28 como referencia de auditoría. La elegibilidad se recalcula separadamente para los cinco cortes 7, 14, 28, 42 y 56 en el segundo informe; no se aplica este desglose histórico como filtro común.\n')
    write_report('01_exploracion','Auditoría de OULAD para el análisis de cinco ventanas temporales',body)

    population=data('02_comparacion_cortes')
    body=r'''\section{Propósito y protocolo temporal}
El análisis de varias ventanas permite examinar la disponibilidad y el significado de los indicadores conforme avanza una presentación. Esta fase de preparación de datos, correspondiente al segundo objetivo específico, construye una definición uniforme para los días 7, 14, 28, 42 y 56. El protocolo fue adoptado para esta versión por autorización del usuario y se registra en \texttt{decision\_temporal.json}; este registro no constituye una aprobación institucional adicional.

La unidad continúa siendo la inscripción de una persona en un módulo y una presentación de OULAD \cite{sdata2017171}. Para un corte $t$, se incluyen las inscripciones con fecha conocida de matrícula $r_i\leq t$, sin retiro administrativo $u_i\leq t$ y cuyo final de presentación $L_i$ es posterior al corte. Las fechas de retiro ausentes se interpretan como ausencia de retiro registrado. La etiqueta corresponde a
\[
Y_i(t)=\mathbf{1}\{t<u_i\leq L_i\}.
\]
Un retiro ocurrido exactamente en el día del corte se excluye de la población en riesgo. La observación abarca los días $0,1,\ldots,t$, incluidos ambos extremos; contiene $t+1$ días de calendario. Los antecedentes anteriores al inicio se calculan separadamente. Se supone disponibilidad al cierre del día de los registros de interacción y entrega, y disponibilidad previa del calendario de evaluación. Los archivos no permiten verificar retrasos de publicación ni revisiones históricas del calendario.

El horizonte llega hasta el final de cada presentación; su duración cambia entre cortes y cursos. Por tanto, la comparación no mantiene un horizonte de seguimiento de longitud fija. La etiqueta identifica retiro administrativo registrado y no demuestra su carácter voluntario ni equivale automáticamente a \textit{Withdrawn}. Las discordancias documentadas en la auditoría permanecen como limitación de la fuente.

\section{Población elegible y cambio de composición}
'''
    pop=population[['corte','inscripciones','personas','retiros','prevalencia_pct']].copy()
    pop.columns=['Corte','Inscripciones','Personas','Retiros futuros','Porcentaje']
    body+=tab(pop,'Población y evento propios de cada corte; el porcentaje usa inscripciones elegibles.','multi02:poblacion',[.09,.24,.21,.23,.16])
    body+=r'''La disminución de la población refleja principalmente retiros ya ocurridos; también existen nuevas matrículas entre cortes. En consecuencia, las filas de cortes distintos no son observaciones independientes ni representan exactamente la misma población. La menor prevalencia posterior no demuestra una mejora educativa: se modifica la población en riesgo y se acorta el seguimiento. Los flujos secuenciales y los denominadores por módulo y presentación se conservan en las tablas exportadas.

'''
    transitions=data('02_transiciones');transitions.columns=['Desde','Hasta','Comunes','Salen','Entran']
    body+=tab(transitions,'Cambio de composición entre cortes consecutivos.','multi02:transiciones',[.12,.12,.24,.21,.21],digits=0)
    body+=fig('02_poblacion_cortes','Inscripciones elegibles, retiros futuros y prevalencia: índice con corte 7 igual a 100. Las líneas unen poblaciones distintas; no son trayectorias de una cohorte.','multi02:figpoblacion')
    body+=r'''\section{Construcción y disponibilidad de indicadores}
La actividad se resume mediante volumen de clics, días activos, frecuencia relativa, recencia y variabilidad de los totales diarios. Un día activo contiene al menos un clic; la proporción de días activos usa $t+1$ como denominador. Esta normalización facilita una lectura temporal, pero no corrige la menor exposición de las matrículas posteriores al inicio. Se exporta adicionalmente el número de días matriculados dentro de la ventana para identificar esta condición. El número de filas VLE no se denomina número de sesiones.

La recencia es la diferencia entre el corte y el último día activo; se conserva ausente cuando no existe actividad en la ventana. El coeficiente de variación emplea la desviación estándar muestral de los totales diarios, incluidos los ceros, dividida por su media. También se cuentan semanas completas desde el día 0 y se omite el bloque final incompleto. Estos indicadores describen conductas observables; los clics no constituyen una medición directa de motivación.

La tendencia compara bloques contiguos de igual longitud que terminan en el corte. Para $s=7$ o $s=14$, se calcula
\[
T_{i,s}(t)=\log\!\left(\frac{1+\sum_{d=t-s+1}^{t}c_{id}}
{1+\sum_{d=t-2s+1}^{t-s}c_{id}}\right).
\]
El término 1 permite razones finitas cuando un solo bloque tiene cero clics. Si ambos bloques son cero, la tendencia se conserva ausente; tampoco se calcula cuando existen menos de $2s$ días de historia. De este modo, la tendencia de siete días no está disponible en el corte 7 y la de catorce días solo se calcula desde el corte 28.

La inactividad acumulada y la ausencia de clics en los últimos 7, 14 o 28 días se conservan como indicadores complementarios. Una ventana reciente sin historia suficiente se representa como no observable, no como actividad ni como inactividad. Ninguna de estas banderas sustituye la etiqueta administrativa; su interpretación depende del calendario y de las oportunidades de participación.

Las entregas incluyen evaluaciones distintas de \textit{Exam}, sin reconocimiento de otra presentación (\textit{banked}), observadas entre 0 y $t$. Se distinguen las evaluaciones programadas hasta el corte y cuántas de ellas ya fueron entregadas; estas últimas pueden haberse entregado antes del inicio. La proporción entregada no mide puntualidad y queda ausente cuando no hay evaluaciones programadas. Los puntajes y su disponibilidad se conservan únicamente para auditoría, porque la fecha de entrega no acredita la fecha de publicación de la nota.

'''
    avail=population[['corte','sin_actividad','sin_evaluacion_programada','con_entregas','matricula_posterior_inicio']].copy()
    avail.columns=['Corte','Sin actividad','Sin evaluación programada','Con entregas','Matrícula después de 0']
    body+=tab(avail,'Disponibilidad y exposición en la población elegible; conteos de inscripciones.','multi02:disponibilidad',[.08,.20,.28,.19,.22],digits=0)
    body+=r'''En el corte 7 ninguna inscripción tiene evaluaciones con vencimiento entre 0 y 7, aunque 772 ya presentan entregas. Por ello, ausencia de entregas y falta de cumplimiento no son equivalentes. En el corte 28 persisten 4\,988 inscripciones sin evaluación programada y en el corte 56 son 2\,407; la ampliación de la ventana no elimina toda la heterogeneidad del calendario.

\section{Enlace con la versión anterior y productos}
La versión anterior del corte 28 observaba actividad hasta el día 27. La versión actual incorpora también el día 28 y mantiene las 27\,515 inscripciones elegibles. Esta modificación explica cambios de cifras sin atribuirlos a alteraciones de las fuentes.

'''
    bridge=data('02_enlace_corte28')[['variable','suma_anterior','suma_actual','inscripciones_con_cambio']]
    bridge['variable']=bridge.variable.map({'total_clics':'Clics','n_evaluaciones_entregadas':'Entregas'})
    bridge.columns=['Indicador','Anterior','Actual','Inscripciones con cambio']
    body+=tab(bridge,'Efecto de incluir el día 28 en las mismas inscripciones.','multi02:enlace',[.23,.23,.23,.25],digits=0)
    body+=r'''Se exportan conjuntos separados de datos auditables, predictores y etiquetas para cada corte; las claves se conservan para vincularlos, sin convertir el identificador de estudiante en predictor. El diccionario documenta 26 indicadores candidatos y separa las variables de contexto. La tabla apilada tiene una fila por inscripción y corte, no por persona. La intersección de los cinco conjuntos contiene 26\,429 inscripciones y se utiliza únicamente para una sensibilidad retrospectiva.

Los productos permiten continuar con un protocolo predictivo común. El ajuste de imputación, escalado, selección y cualquier remuestreo deberá realizarse dentro del entrenamiento de cada partición \cite{revsklearnpitfalls}. Esta fase no entrenó clasificadores, no seleccionó una ventana óptima y no ofrece evidencia de desempeño fuera de muestra. Antes de modelar deberán fijarse la generalización buscada y la separación por personas o presentaciones; una persona presente en varios cortes no debe contaminar conjuntos de entrenamiento y evaluación.
'''
    write_report('02_ingenieria','Ingeniería de variables en cinco cortes temporales',body)

    effects=data('03_efectos')
    names={'total_clics':'Clics acumulados','proporcion_dias_activos':'Proporción de días activos','recencia_relativa':'Recencia relativa','coef_variacion_clics':'CV de calendario','cv_intensidad_activa':'CV entre días activos','log_ratio_7d':'Tendencia de 7 días','log_ratio_14d':'Tendencia de 14 días','n_evaluaciones_entregadas':'Entregas acumuladas','proporcion_programadas_entregadas':'Proporción programada entregada'}
    body=r'''\section{Propósito y alcance estadístico}
El análisis examina la distribución y las asociaciones de los indicadores construidos en los cortes 7, 14, 28, 42 y 56. Corresponde a una exploración previa al modelado: se analizan todos los datos elegibles y no se atribuyen a estos resultados propiedades de validación predictiva. Cada corte mantiene su propia población en riesgo y su evento futuro hasta el final de la presentación.

Se describen cuantiles, dispersión, faltantes y valores extremos. Los faltantes estructurales se separan de valores cero: no existe recencia definida sin actividad ni proporción de cumplimiento observable sin evaluaciones programadas. Los diagnósticos de valores atípicos mediante rango intercuartílico y desviación absoluta mediana no eliminan registros; cuando la escala es cero, el diagnóstico respectivo se conserva como no definido. Los patrones observados no demuestran mecanismos MAR o MNAR.

\section{Asociaciones e incertidumbre dentro de cada corte}
La comparación numérica usa el efecto biserial por rangos, calculado a partir del estadístico de Mann--Whitney con tratamiento de empates \cite{revscipy}:
\[
r_{rb}=\frac{2U_1}{n_1n_0}-1.
\]
El grupo 1 corresponde al retiro futuro. Un efecto negativo indica valores generalmente menores en ese grupo y un efecto positivo indica valores mayores. Para cada indicador se utilizan los casos observables de ambos grupos; por ello, algunos denominadores cambian incluso dentro de un mismo corte. Las estimaciones no son efectos causales ni medidas del rendimiento de un clasificador.

Los intervalos puntuales del 95 por ciento se obtienen mediante 5\,000 remuestreos de personas con reposición, conservando conjuntamente sus inscripciones dentro del corte; se utiliza la semilla 20260908. Esta construcción reconoce la agrupación por estudiante \cite{revfield2007}. Las presentaciones observadas permanecen fijas y no se incorpora incertidumbre por muestreo de cursos. Los intervalos son exploratorios, no simultáneos: no se presentan pruebas de significancia múltiples ni se usa su solapamiento como contraste entre ventanas.

'''
    matrix=effects.loc[effects.variable.isin(names)].pivot(index='variable',columns='corte',values='efecto').reindex(names)
    matrix.index=matrix.index.map(names);matrix=matrix.reset_index();matrix.columns=['Indicador']+[str(x) for x in matrix.columns[1:]]
    body+=tab(matrix,'Efecto biserial por rangos en cada corte; no aplica indica ausencia de observaciones suficientes.','multi03:efectos',[.36,.12,.12,.12,.12,.12],digits=3)
    body+=r'''Los clics acumulados y la proporción de días activos presentan asociaciones negativas con el retiro futuro en todos los cortes. El CV de calendario y la recencia relativa presentan asociaciones positivas; el CV entre días activos se evalúa separadamente. La dependencia entre variabilidad y frecuencia impide presentar estas asociaciones como evidencia independiente. Sin embargo, las magnitudes cambian al variar simultáneamente la historia observada, la población y el horizonte; no permiten afirmar que un corte sea superior a otro para predecir.

'''
    body+=fig('03_efectos_cortes','Efectos por corte e intervalos puntuales mediante remuestreo de personas. Las líneas conectan estimaciones y no representan un contraste longitudinal.','multi03:figefectos')
    row=effects.loc[effects.corte.eq(56)&effects.variable.eq('log_ratio_7d')].iloc[0]
    body+=f"La tendencia de siete días en el corte 56 presenta un efecto de {number(row.efecto,3)}, con intervalo de {number(row.IC95_inferior,3)} a {number(row.IC95_superior,3)}. Este resultado no respalda una dirección clara de asociación para ese indicador en ese corte; tampoco demuestra ausencia de utilidad predictiva conjunta. La tendencia de catorce días conserva un significado distinto porque resume dos bloques de mayor duración.\n\n"
    body+=r'''\section{Disponibilidad, distribución y heterogeneidad}
La comparación de proporciones y recencias relativas reduce la dependencia aritmética de la duración observada, pero no iguala las oportunidades educativas. Las distribuciones empíricas se presentan por corte y las tablas completas conservan los tamaños observados y ausentes. La proporción entregada se analiza solo donde hay evaluaciones programadas; en el día 7 no existe este denominador y no se estima un efecto.

'''+fig('03_distribuciones_cortes','Distribuciones acumuladas de actividad relativa y recencia relativa; esta última excluye inscripciones sin actividad observable.','multi03:distribuciones')
    categorical=data('03_categoricas')
    body+=r'''La V de Cramér se calcula como $V=\sqrt{\chi^2/[N\min(f-1,g-1)]}$, donde $N$ es el total de la tabla de contingencia y $f,g$ sus dimensiones. Se utiliza como medida descriptiva de asociación, sin atribuir a su valor significancia estadística ni crecimiento necesario por desbalance de categorías.

'''
    cat=categorical.loc[categorical.variable.isin(['code_module','code_presentation','gender','highest_education','region','disability','age_band','imd_band'])].pivot(index='variable',columns='corte',values='V_cramer').reset_index()
    cat['variable']=cat.variable.map({'code_module':'Módulo','code_presentation':'Presentación','gender':'Género','highest_education':'Educación previa','region':'Región','disability':'Discapacidad','age_band':'Edad','imd_band':'Privación (IMD)'})
    cat.columns=['Categoría']+[str(x) for x in cat.columns[1:]]
    body+=tab(cat,'V de Cramér descriptiva; sin interpretación causal ni pruebas por filas independientes.','multi03:categorias',[.32,.13,.13,.13,.13,.13],digits=3)
    body+=r'''La asociación con el módulo evidencia heterogeneidad contextual que debe considerarse al diseñar la validación. La V de Cramér no indica una dirección del efecto ni ajusta por otros atributos. Las tasas por nivel y los conteos se exportan por separado; no se interpreta una diferencia descriptiva como efecto atribuible a una característica personal.

\section{Redundancia y estructura multivariada}
Se calculan correlaciones de Spearman y cantidades de pares observados para cada corte. El diagnóstico VIF usa un conjunto reducido de cuatro indicadores con intercepto; sus valores describen dependencia lineal en ese conjunto y no ordenan automáticamente las variables por utilidad. La relación entre volumen de clics, días activos y filas VLE exige evitar interpretaciones de contribuciones completamente independientes.

El análisis de componentes principales utiliza cinco indicadores conductuales: logaritmo de uno más el volumen, proporción de días activos, logaritmo de uno más el promedio por día activo, recencia relativa y coeficiente de variación. Se restringe a casos con actividad y datos completos; cada corte se estandariza y ajusta separadamente \cite{revpca}. Por ello, sus componentes no constituyen un sistema de ejes común para seguir trayectorias individuales entre ventanas.

'''
    pca=data('03_pca');pca=pca.loc[pca.componente.eq(2),['corte','n','acumulada']].copy();pca.acumulada*=100;pca.columns=['Corte','Casos observados','Varianza de dos componentes (%)']
    body+=tab(pca,'Resumen descriptivo del PCA ajustado separadamente por corte.','multi03:pca',[.13,.29,.50])
    body+=r'''La covarianza robusta mediante MCD se ajusta sobre una muestra reproducible de 5\,000 casos por corte y evalúa distancias en los casos completos \cite{revmcd}. La bandera usa el percentil empírico 97,5 de las distancias de todos los casos evaluados en ese corte. Este umbral es descriptivo, no una probabilidad calibrada de anomalía; no se utiliza una prueba de Hotelling ni se eliminan las observaciones marcadas. Las cargas de PCA, VIF y resúmenes MCD permanecen disponibles en CSV.

\section{Sensibilidad con población y evento comunes}
La intersección de las poblaciones elegibles contiene 26\,429 inscripciones. Se fija para ellas el evento de retiro posterior al día 56 y hasta el final, con 3\,985 eventos, y se describen nuevamente cinco indicadores en cada corte. Esta comparación mantiene población y etiqueta; los denominadores observables todavía cambian cuando un indicador requiere actividad o evaluaciones programadas.

'''
    common=data('03_cohorte_comun').pivot(index='variable',columns='corte',values='efecto').reset_index()
    common['variable']=common.variable.map(names);common.columns=['Indicador']+[str(x) for x in common.columns[1:]]
    body+=tab(common,'Efectos descriptivos en la cohorte común, sin intervalos ni contraste entre cortes.','multi03:comun',[.36,.12,.12,.12,.12,.12],digits=3)
    body+=r'''La selección exige conocer que una inscripción permanece elegible hasta el día 56. En consecuencia, es retrospectiva y condicionada a supervivencia administrativa; no puede utilizarse como población operativa de una alerta del día 7. La diferencia respecto de las asociaciones principales ayuda a reconocer el papel de la composición, pero no identifica causalmente su contribución ni permite atribuir a la duración de la ventana todo el cambio observado.

\section{Conclusiones y continuidad}
La comparación documenta que la disponibilidad académica y el significado de los indicadores cambian con el momento de observación. Las señales conductuales conservan asociaciones descriptivas con el retiro, mientras que algunas tendencias recientes presentan resultados menos definidos. La evidencia favorece mantener explícitos los denominadores, el calendario y la historia requerida, en lugar de completar automáticamente con ceros los indicadores no observables.

Los resultados preparan la comparación posterior de modelos, pero no establecen una ventana óptima. Esa decisión requerirá evaluar discriminación, calibración y utilidad de anticipación bajo particiones compatibles y un protocolo fijado antes de seleccionar modelos, umbrales o cortes. La exploración ya realizada sobre la fuente completa debe declararse al evaluar la independencia de una prueba final; no se presenta ningún subconjunto como intacto por el solo hecho de asignarle después ese nombre.
'''
    write_report('03_estadistica','Análisis estadístico comparado de cinco ventanas temporales',body)
    from contenido_correcciones import ampliar_informes
    ampliar_informes()
    print('Tres informes multiventana generados desde resultados ejecutados.')

if __name__=='__main__':build()
