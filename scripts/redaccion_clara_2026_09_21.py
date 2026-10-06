"""Reescritura editorial trazable desde el respaldo, sin modificar análisis.

Reaplicar solo tras reconciliar cualquier cambio posterior en las fuentes.
"""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'Plantilla_ProyAplicado'
OLD=ROOT/'respaldo/2026-09-21_pre_redaccion_clara/Plantilla_ProyAplicado'
OUT=ROOT/'reportes/redaccion_clara_2026_09_21'
changes=[]


def paragraph(text, start, replacement, file):
    assert text.count(start)==1,(file,start,text.count(start))
    a=text.index(start)
    match=re.search(r'\n\s*\n|\n(?=\\(?:Needspace|begin|input|section|subsection))',text[a:])
    b=a+match.start() if match else len(text)
    changes.append({'archivo':file,'antes':text[a:b],'despues':replacement})
    return text[:a]+replacement+text[b:]



def main():
    OUT.mkdir(parents=True,exist_ok=True)
    intro=r'''El proyecto busca identificar de forma temprana el riesgo de retiro de un curso a partir de la información registrada en una plataforma de aprendizaje. Para ello, utiliza OULAD, un conjunto de datos que reúne matrículas, evaluaciones y actividad de estudiantes de la Open University. El propósito es desarrollar un modelo que permita estimar ese riesgo y explicar qué información interviene en sus predicciones.

Esta versión presenta el trabajo necesario para preparar los datos antes de entrenar el modelo. Se revisaron siete tablas y se distinguió entre personas e inscripciones: una misma persona puede aparecer en más de un curso. Después se definieron cinco momentos de observación, en los días 7, 14, 28, 42 y 56. En cada uno se utilizaron los datos disponibles hasta ese día y se excluyeron las inscripciones cuyo retiro ya había ocurrido.

La comparación permitió observar que disponer de más días de información también cambia el grupo analizado y el tiempo que queda para registrar un retiro. Por esta razón, las diferencias entre cortes no permiten elegir todavía el mejor momento para predecir. Se compararon los resultados con los de un grupo común de inscripciones para examinar este cambio de población. La inactividad se mantuvo como una señal de participación, sin considerarla por sí sola evidencia de abandono.

El documento presenta primero el problema, los objetivos y los conceptos necesarios para entender el estudio. Luego explica la revisión de las fuentes, la construcción de indicadores y sus resultados. Los capítulos de modelos, SHAP y prototipo indican el trabajo que aún falta. Las conclusiones recogen lo encontrado hasta ahora y los anexos conservan el detalle de los procedimientos.

La Figura~\ref{editorial:ruta} resume el avance y las etapas pendientes. La guía preliminar permite consultar los símbolos; el Anexo~\ref{corr:anexodiccionario} relaciona los indicadores con las columnas del conjunto de datos. Las formulaciones y demostraciones más especializadas se consultan en el Anexo~\ref{editorial:matematica}.
\input{figura_ruta}
'''
    (P/'introduccion.tex').write_text(intro,encoding='utf-8')
    abstract=r'''El proyecto busca predecir de forma temprana el retiro de estudiantes en entornos de aprendizaje virtual mediante datos académicos y de participación. Esta versión presenta la revisión y preparación de OULAD, siguiendo la metodología CRISP-DM. Se examinaron siete tablas que incluyen 32\,593 inscripciones de 28\,785 personas, y se construyeron indicadores para los días 7, 14, 28, 42 y 56 del curso.

En cada corte se utilizó información registrada hasta ese momento y se excluyeron los retiros ya ocurridos. El evento que se busca predecir es el retiro administrativo posterior al corte y hasta el final de la presentación; la inactividad se conserva como indicador complementario. Las inscripciones elegibles pasaron de 29\,076 en el primer corte a 26\,506 en el último. Se observaron diferencias en la actividad, las entregas y su relación con el retiro. Estas comparaciones deben leerse teniendo en cuenta que cambian tanto el grupo analizado como el tiempo restante de seguimiento. En el corte 7 no había evaluaciones con vencimiento dentro de la ventana, aunque ya existían entregas; por ello, no entregar todavía no equivale necesariamente a incumplir una actividad.

Los análisis se ejecutaron desde las fuentes y se acompañaron de comprobaciones independientes de clics, días activos, variabilidad entre días activos y entregas. Los resultados dejan una base documentada para comparar modelos, pero aún no permiten elegir una ventana óptima ni afirmar capacidad predictiva o efectividad educativa. El entrenamiento, la interpretación mediante SHAP y el prototipo de visualización permanecen pendientes.

\textbf{Palabras clave}: abandono estudiantil, OULAD, analítica de aprendizaje, ventanas temporales, retiro administrativo.
'''
    (P/'abstract.tex').write_text(abstract,encoding='utf-8')
    text=(OLD/'descripcion.tex').read_text(encoding='utf-8')
    replacements=[
    ('La analítica de aprendizaje se define',r'La analítica de aprendizaje utiliza datos de los estudiantes y de su contexto para comprender el proceso educativo y apoyar su mejora \cite{longsiemens2011,educsci11090552}.'),
    ('La distinción respecto a la minería',r'La minería de datos educativos se concentra en encontrar patrones y desarrollar métodos para analizarlos. La analítica de aprendizaje pone mayor atención en cómo interpretar esos resultados y comunicarlos a docentes e instituciones \cite{siemensbaker2012,romeroventura2020}. El proyecto reúne ambas perspectivas: construye indicadores y prevé comparar modelos, pero también busca que sus resultados sean comprensibles para quienes podrían utilizarlos.'),
    ('Los registros de un LMS solo alcanzan',r'Los registros del LMS permiten observar una parte de la participación conductual. No muestran directamente la motivación, el bienestar o la intención de continuar estudiando. La literatura advierte que la presencia de actividad digital puede confundirse con un mayor compromiso con el aprendizaje \cite{henrie2015}. Por ello, los clics y las entregas se interpretan aquí como señales observables de participación, con ese límite.'),
    ('La formulación probabilística permite ordenar',r'La probabilidad estimada permite ordenar las inscripciones según su riesgo, pero es necesario comprobar si esas estimaciones se ajustan a lo que ocurre: esto se conoce como calibración. Además, convertir una probabilidad en una clase requiere elegir un umbral. El valor $\tau=0{,}5$ minimiza el coste esperado cuando las probabilidades son correctas y ambos tipos de error tienen el mismo coste. Con costes positivos $c_{FP}$ y $c_{FN}$ para falsos positivos y falsos negativos, la comparación entre $c_{FP}(1-p(\mathbf x))$ y $c_{FN}p(\mathbf x)$ conduce al umbral $c_{FP}/(c_{FP}+c_{FN})$.\n\nOtras métricas o restricciones de capacidad pueden requerir un criterio distinto. El umbral se elegirá con datos de validación dentro del entrenamiento, antes de evaluar la prueba final \cite{revthreshold}.'),
    ('El coeficiente $\\beta_{j}$ expresa',r'Cada coeficiente $\beta_j$ indica cómo cambia el logaritmo de la razón de probabilidades al aumentar una unidad su predictor, manteniendo los demás constantes. La cantidad $e^{\beta_j}$ expresa ese cambio como un factor multiplicativo. Esta interpretación corresponde a una asociación dentro del modelo, no al efecto de intervenir sobre el estudiante.'),
    ('Como ejemplo hipotético, no como resultado',r'Como ejemplo hipotético, un coeficiente de $0{,}40$ para los días desde la última interacción multiplicaría la razón de probabilidades por aproximadamente 1,49 por cada día adicional, con los demás predictores constantes \cite{hosmer2013}. Esto representa un aumento cercano al 49\,\% en esa razón, no un aumento de 49 puntos porcentuales en la probabilidad. Esta posibilidad de interpretar sus coeficientes justifica utilizar la regresión logística como referencia.'),
    ('La comparación entre estos modelos exige',r'La comparación deberá considerar que las clases pueden tener tamaños distintos. Un modelo que asigne a todos los estudiantes a la clase más frecuente puede acertar muchas veces y, aun así, no identificar los retiros. Por ello, se prevé evaluar su capacidad para distinguir ambas clases mediante las curvas ROC y de precisión y exhaustividad, junto con métricas calculadas para el umbral elegido \cite{1049482020222124425,s41598025939181}. El protocolo, las métricas definitivas y el tratamiento del desbalance aún deben fijarse; el capítulo de modelos conserva ese estado pendiente.'),
    ('Un proyecto de minería de datos requiere',r'CRISP-DM ofrece una forma de organizar el trabajo, desde la comprensión del problema hasta la entrega de los resultados. Su utilidad en este proyecto consiste en hacer explícito qué se busca en cada etapa y qué decisiones permiten pasar a la siguiente. La preparación de datos forma parte de este proceso y no es solo un paso previo al entrenamiento \cite{fayyad1996,chapman2000,wirth2000}.'),
    ('CRISP-DM organiza el trabajo en seis fases.',r'La metodología comprende seis fases. Primero se define el problema y se revisan las fuentes disponibles. Luego se preparan los datos y se construyen los modelos. La evaluación examina si los resultados responden al propósito del estudio, mientras que el despliegue organiza su entrega en una forma útil, como un informe, un procedimiento o una herramienta \cite{chapman2000,shearer2000}.'),
    ('La propiedad relevante del modelo no es',r'Estas fases permiten volver sobre decisiones anteriores. Por ejemplo, encontrar una limitación en las fechas puede exigir cambiar la forma de construir una variable antes de continuar \cite{chapman2000}. En este estudio, la revisión de las matrículas, los retiros y el calendario de evaluación orientó la selección de inscripciones y de indicadores para cada corte.'),
    ('Revisiones críticas recientes han señalado',r'CRISP-DM no resuelve por sí solo todas las decisiones de un proyecto de ciencia de datos. La operación de un modelo, su seguimiento posterior y las implicaciones éticas requieren atención adicional \cite{martinezplumed2021}. En educación, también interesa saber si el desempeño cambia entre grupos de estudiantes. Una evaluación exhaustiva de equidad queda fuera del alcance actual y no puede darse por resuelta con los resultados descriptivos \cite{zenodo8115786}.'),
    ('En el ámbito educativo, el proceso analítico',r'En educación, los resultados deben poder ser comprendidos por docentes, tutores y responsables institucionales, además de analistas \cite{romeroventura2020,educsci11090552}. Por ello, el proyecto prevé comunicar las predicciones y sus explicaciones mediante un prototipo. Su desarrollo no equivale a demostrar que una intervención reduzca el abandono.'),
    ('La visualización es el medio por el cual',r'Las visualizaciones ayudan a comunicar patrones de participación, niveles de riesgo y resultados de evaluación \cite{info16040326}. En esta fase se utilizan para explicar el análisis realizado. La Tabla~\ref{tab:crispdm-proyecto} relaciona las fases de CRISP-DM con los objetivos y capítulos del documento.'),
    ('La base corresponde a la distribución',r'La explicación parte de un valor de referencia, que bajo la formulación habitual es $\mathbb{E}[f(X)]$. Las contribuciones se suman en la misma escala de la salida explicada. Si el modelo se explica en puntuación logística, no pueden leerse como aumentos o disminuciones directas de probabilidad. También importa qué datos se toman como referencia: cambiar esa elección puede cambiar la explicación \cite{revshapdocs}.'),
    ('Este trabajo adopta en consecuencia SHAP',r'El proyecto prevé utilizar SHAP después de comparar los modelos. Se buscarán explicaciones individuales, que muestren qué variables intervienen en una predicción, y resúmenes del conjunto, que permitan reconocer cuáles usa más el modelo. Para ensambles de árboles se prevé utilizar la variante exacta correspondiente. El capítulo de interpretabilidad indica que este análisis aún no se ha ejecutado; las futuras explicaciones describirán el modelo y no las causas del abandono.'),
    ]
    for start,new in replacements:
        text=paragraph(text,start,new.replace(r'\n\n','\n\n'),'descripcion.tex')
    appendix=(OLD/'anexos.tex').read_text(encoding='utf-8')
    # El detalle se conserva literalmente en anexos; el cuerpo explica su propósito.
    a=text.index('Los parámetros se estiman por máxima verosimilitud')
    b=text.index(r'\paragraph{Random Forest}',a)
    logistic=text[a:b]
    text=text[:a]+r'''El ajuste busca coeficientes que representen la relación entre los predictores y el retiro. Para evitar valores excesivos puede aplicarse regularización, una penalización de la magnitud de los coeficientes. Esta decisión y el tratamiento de variables relacionadas deberán definirse durante el entrenamiento. La formulación del ajuste, sus condiciones y la penalización se conservan en el Anexo~\ref{clara:logistica}.

'''+text[b:]
    appendix+='\n\\subsection{Ajuste y regularización de la regresión logística}\\label{clara:logistica}\n'+logistic
    a=text.index(r'\begin{proposicion}[Varianza')
    b=text.index('En un remuestreo de $n$ filas',a)
    rf=text[a:b]
    prop=rf[:rf.index(r'\end{proposicion}')+len(r'\end{proposicion}')]
    text=text[:a]+r'''La idea es que promediar árboles puede reducir la variación de sus predicciones, pero el beneficio depende de cuánto se parezcan sus errores. Añadir árboles no garantiza que todas las métricas mejoren. El Anexo~\ref{editorial:rf} conserva la expresión matemática, sus supuestos y la demostración \cite{breiman2001}.

'''+text[b:]
    appendix=appendix.replace('Bajo las hipótesis de la Proposición',prop+'\nBajo las hipótesis de la Proposición',1)
    a=text.index('LightGBM utiliza histogramas')
    b=text.index(r'\paragraph{TabNet}',a)
    lgb=text[a:b]
    text=text[:a]+r'''LightGBM también construye árboles de manera secuencial. Agrupa los valores de las variables en intervalos para buscar divisiones con menos trabajo de cálculo y suele ampliar la hoja que ofrece mayor mejora \cite{revlightfeatures,revlighttuning}. Por ello, controlar la profundidad y el número de hojas será importante para evitar ajustes demasiado complejos.

Sus procedimientos de muestreo y agrupación de variables buscan mejorar la eficiencia \cite{ke2017}. El Anexo~\ref{clara:lightgbm} conserva los detalles y las condiciones de esas operaciones. Su inclusión como candidato no supone que vaya a superar a los demás modelos en OULAD.

'''+text[b:]
    appendix+='\n\\subsection{Procedimientos de eficiencia de LightGBM}\\label{clara:lightgbm}\n'+lgb
    a=text.index('TabNet es una arquitectura')
    b=text.index('El artículo de TabNet utiliza',a)
    tabnet=text[a:b]
    text=text[:a]+r'''TabNet es una red neuronal diseñada para datos organizados en filas y columnas. Procesa cada observación en varios pasos y asigna pesos a las variables que utiliza en cada uno. Esos pesos forman una máscara de atención: algunas variables reciben mayor peso y otras pueden quedar en cero. Una variable puede volver a utilizarse en pasos posteriores \cite{arXiv190807442}.

Este mecanismo permite examinar qué variables atiende la red, aunque sus máscaras no equivalen a explicaciones causales ni a valores SHAP. Las ecuaciones de las máscaras y de su penalización se conservan en el Anexo~\ref{clara:tabnet}.

'''+text[b:]
    appendix+='\n\\subsection{Máscaras y penalización de TabNet}\\label{clara:tabnet}\n'+tabnet
    # Fórmula combinatoria: primero la explicación aplicada; el cálculo queda accesible.
    a=text.index('Dentro de las técnicas')
    b=text.index('El resultado formal de unicidad',a)
    shap=text[a:b].replace('ofrece el fundamento te\u00f3rico m\u00e1s s\u00f3lido.', 'utiliza una formulaci\u00f3n basada en la teor\u00eda de juegos.')
    text=text[:a]+r'''SHAP permite descomponer una predicción en un valor de referencia y contribuciones de las variables. Para ello utiliza los valores de Shapley, que distribuyen el resultado de un juego entre sus participantes según su contribución \cite{shapley1953,lundberg2017}. En la aplicación al modelo, los participantes son las variables de una inscripción. El cálculo considera distintas combinaciones de variables, no solo un orden de incorporación. Su formulación completa se conserva en el Anexo~\ref{clara:shapcalculo}.

'''+text[b:]
    appendix+='\n\\subsection{Cálculo de las contribuciones de Shapley}\\label{clara:shapcalculo}\n'+shap
    (P/'descripcion.tex').write_text(text,encoding='utf-8')
    (P/'anexos.tex').write_text(appendix,encoding='utf-8')
    rewrite_results()
    project=(OLD/'proyecto.tex').read_text(encoding='utf-8').replace('13 de septiembre de 2026','21 de septiembre de 2026')
    (P/'proyecto.tex').write_text(project,encoding='utf-8')
    (OUT/'comparacion_parrafos.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Reescritura registrada: {len(changes)} párrafos y reorganización de contenidos especializados.')


def rewrite_results():
    replacements={
    'desarrollo1.tex':[
    ('La preparación de un modelo de abandono',r'Antes de construir un modelo es necesario entender qué contiene cada archivo y cómo puede utilizarse. Por esta razón, se revisaron las siete tablas de OULAD, sus relaciones y sus fechas. Este trabajo corresponde al primer objetivo específico y a la comprensión de datos de CRISP-DM. Los resultados proceden de la ejecución del notebook \texttt{01\_carga\_exploracion.ipynb} documentada el 10 de septiembre de 2026; esta revisión de redacción no representa una nueva ejecución.'),
    ('El descriptor de OULAD identifica',r'OULAD reúne información de matrícula, evaluaciones e interacciones con recursos virtuales \cite{sdata2017171}. La revisión examinó los archivos disponibles en el proyecto. Se utilizaron huellas SHA-256, códigos que permiten detectar si un archivo cambió, para comprobar que las fuentes se conservaron durante el procesamiento. Estas huellas identifican los archivos utilizados, pero no certifican su procedencia.'),
    ('La relación entre las tablas se comprobó',r'Las tablas se unieron utilizando sus identificadores completos. Se comprobó que cada evaluación y cada recurso correspondieran a la inscripción, el módulo y la presentación esperados. Las nueve verificaciones de relaciones no encontraron registros sin correspondencia. Las uniones de información y matrícula conservaron una fila por inscripción; el calendario se vinculó con la presentación correspondiente.'),
    ('Las claves de las tablas de entidades',r'Las tablas de estudiantes, matrículas, cursos y entregas no presentaron claves repetidas. En cambio, el registro de actividad VLE contiene filas idénticas y filas que comparten estudiante, módulo, presentación, recurso y día. Los archivos no incluyen un identificador de sesión que permita explicar esas repeticiones. Por ello, no se interpretan como sesiones diferentes.'),
    ('Los registros posteriores al retiro documentan',r'Se encontraron actividades con fecha posterior al retiro administrativo. Los archivos no permiten saber si se deben a demoras de registro, accesos posteriores u otra situación. Estas actividades no deben utilizarse como señales anteriores a un retiro que ya ocurrió. De igual manera, observar datos faltantes no basta para determinar por qué faltan; no se asumió un mecanismo MAR o MNAR.'),
    ('Se describen cuantiles, dispersión, faltantes',r'La exploración describe cómo se distribuyen los valores, cuánto varían y cuántos datos faltan. Se distingue entre un cero y un indicador que no puede calcularse: por ejemplo, no hay recencia cuando no existe actividad previa, ni proporción entregada cuando no hay evaluaciones programadas. Los métodos basados en el rango intercuartílico y la desviación absoluta mediana permiten señalar valores alejados del resto, pero no se utilizaron para eliminar registros. Si la escala de referencia es cero, el diagnóstico queda sin definir. Estos resultados tampoco prueban un mecanismo MAR o MNAR.'),
    ('Los intervalos puntuales del 95 por ciento',r'Para acompañar las asociaciones con una medida de incertidumbre, se construyeron intervalos del 95 por ciento mediante 5\,000 remuestreos. En cada repetición se seleccionaron personas con reposición y se conservaron juntas sus inscripciones, usando la semilla 20260908 \cite{revfield2007}. Así se reconoce que varias inscripciones de una misma persona pueden estar relacionadas. Los cursos observados se mantuvieron fijos; no se estimó la incertidumbre que surgiría al estudiar otros cursos. Los intervalos corresponden a cada estimación por separado y son exploratorios: su solapamiento no se usa como prueba de diferencia entre ventanas.'),
    ('La auditoría permitió distinguir la inscripción',r'La revisión permitió precisar qué representa una inscripción, reconocer las limitaciones de los registros y separar el retiro administrativo de la inactividad. La exploración mostró relaciones entre indicadores y retiro en cada corte. Estos resultados orientan la preparación de datos, pero todavía no indican cómo funcionará un modelo al predecir casos nuevos.'),
    ],
    'desarrollo2.tex':[
    ('El conteo \\texttt{n\\_registros\\_vle}',r'La variable \texttt{n\_registros\_vle} cuenta filas de actividad dentro de $[0,t]$. No cuenta sesiones, porque la fuente no permite identificarlas ni explicar todas las repeticiones. Por esta razón, se conserva para revisar los datos, pero se excluye de los candidatos del modelo. Su relación con otros indicadores, examinada mediante VIF, aporta una razón adicional para no tratarla como información independiente.'),
    ('La diversidad de recursos y tipos',r'En esta versión no se construyen indicadores de diversidad de recursos o tipos de actividad. El trabajo se concentra en volumen, continuidad, recencia, cambios temporales y participación en evaluaciones, e incluye la comparación de los dos CV. Esta decisión no significa que la diversidad carezca de utilidad. Para estudiarla sería necesario integrar el catálogo de recursos y considerar que los módulos ofrecen oportunidades distintas de interacción.'),
    ('La rejilla se adoptó antes',r'Los cinco cortes representan una, dos, cuatro, seis y ocho semanas desde el inicio. Se fijaron antes de comparar modelos. Las presentaciones duran entre 234 y 269 días, por lo que el día 56 todavía está dentro del primer cuarto del curso. Esta elección permite comparar distintas cantidades de historia disponible, pero no demuestra que sean los mejores cortes posibles ni que se hayan elegido sin conocimiento previo del retiro. El calendario también permite examinar indicadores académicos, ya disponibles en el corte 14.'),
    ('La disminución de la población refleja',r'El número de inscripciones disminuye sobre todo porque se excluyen retiros que ya ocurrieron. También entran algunas matrículas nuevas entre cortes. Por tanto, las filas de la tabla no representan exactamente al mismo grupo de estudiantes. La menor proporción de retiro en los cortes posteriores no demuestra una mejora educativa: cambian el grupo analizado y el tiempo que queda para observar el evento. Las tablas de filtros y de módulo y presentación conservan los denominadores de cada comparación.'),
    ('Los siguientes diagnósticos examinan',r'Varios indicadores pueden describir aspectos cercanos de la misma actividad. Para revisar esa relación se utilizaron correlaciones, VIF y análisis de componentes principales (PCA). Las correlaciones comparan pares de variables; el VIF examina su dependencia lineal dentro de un conjunto definido; el PCA resume cómo varían en conjunto. Estos procedimientos ayudan a entender la información disponible antes del modelado.'),
    ('El análisis de componentes principales utiliza',r'El PCA combina cinco indicadores conductuales: el logaritmo de uno más los clics, la proporción de días activos, el logaritmo de uno más los clics por día activo, la recencia relativa y el CV. Se utilizan únicamente los casos con actividad y datos completos. Las variables se estandarizan para llevarlas a una escala comparable y el análisis se ajusta por separado en cada corte \cite{revpca}. Por ello, los componentes de un corte no son los mismos ejes de los demás cortes y no deben usarse para seguir trayectorias individuales entre ventanas.'),
    ('La covarianza robusta mediante MCD',r'También se utilizó MCD para revisar observaciones alejadas del patrón conjunto de las variables. Este método estima el centro y la variación de los datos buscando reducir la influencia de valores extremos \cite{revmcd}. Se ajustó con una muestra reproducible de 5\,000 casos por corte y después se calcularon distancias para todos los casos completos. Se marcaron los que superaron el percentil empírico 97,5 de esas distancias. La marca es descriptiva: no equivale a una probabilidad de anomalía ni a una prueba de Hotelling, y no se eliminaron observaciones. Los resultados detallados de MCD, PCA y VIF se conservan en los CSV.'),
    ('La especificación original incluye logaritmos',r'La primera versión del PCA utiliza los cinco indicadores originales. La segunda retira el volumen de clics. La tercera, además, reemplaza el CV de calendario por el CV entre días activos. Las tres versiones se ajustan sobre los mismos casos, con variables estandarizadas y por separado en cada corte. Como cambia el conjunto de variables, también cambia la variación que se intenta resumir. Un porcentaje mayor no significa que el PCA explique mejor el abandono.'),
    ('Se compararon los primeros 500',r'Se compararon los resultados obtenidos con las primeras 500 y 2\,000 repeticiones con los de las 5\,000 de una misma secuencia. Se tomó como referencia una diferencia de 0,005 unidades del efecto entre extremos de los intervalos. Al compartir repeticiones, esta comprobación muestra estabilidad numérica en la secuencia utilizada, pero no asegura el mismo resultado con otras semillas. Los intervalos publicados utilizan 5\,000 remuestreos y mantienen su carácter exploratorio.'),
    ('La intersección de las poblaciones elegibles contiene',r'Para examinar cuánto influyen los cambios de población, se repitió la comparación con las 26\,429 inscripciones que seguían siendo elegibles en los cinco cortes. En este grupo se definió un mismo evento: retiro después del día 56 y hasta el final de la presentación, con 3\,985 casos. Se compararon cinco indicadores en cada corte. Aunque el grupo y el evento se mantienen, algunos indicadores solo pueden calcularse cuando hay actividad o evaluaciones programadas, por lo que sus tamaños observados todavía pueden variar.'),
    ('La selección exige conocer que',r'Este grupo solo puede formarse después de saber quiénes siguen siendo elegibles en el día 56. Por eso sirve para revisar los resultados, pero no para definir a quién se alertaría en el día 7: en ese momento aún no se dispone de esa información. La comparación ayuda a reconocer que el cambio de población importa; no permite medir por sí sola cuánto del cambio se debe a la duración de la ventana.'),
    ('Los resultados preparan la comparación posterior',r'Los resultados dejan preparados los datos para comparar modelos, pero aún no señalan la mejor ventana. Esa elección deberá considerar qué tan bien se distinguen los retiros, si las probabilidades estimadas se ajustan a lo observado y cuánto tiempo queda para actuar. Las reglas de comparación deben fijarse antes de seleccionar modelos, cortes o umbrales. Además, ya se exploró la fuente completa: separar ahora un conjunto y llamarlo prueba final no permite afirmar que nunca se utilizó información de él.'),
    ],
    'Conclusiones.tex':[
    ('La auditoría permitió integrar las fuentes',r'La revisión permitió reunir las fuentes y analizar cada inscripción de una persona en un módulo y una presentación. También mostró que una persona puede tener varias inscripciones; esta relación debe conservarse al estudiar la incertidumbre y al separar los datos para evaluar modelos. Se documentaron diferencias entre la fecha de retiro y el resultado final, repeticiones de actividad y registros posteriores al retiro. Los archivos no permiten establecer la causa de todas estas situaciones.'),
    ('La construcción temporal excluyó retiros',r'En cada corte se utilizaron datos observados hasta ese día y se excluyeron los retiros que ya habían ocurrido. La comparación mostró que las entregas deben interpretarse junto con el calendario. Por ejemplo, en el día 7 no había evaluaciones cuyo vencimiento estuviera dentro de la ventana, aunque algunos estudiantes ya habían entregado. Por ello, la ausencia de una entrega no siempre indica incumplimiento.'),
    ('Los indicadores de actividad y recencia presentan',r'Se encontraron relaciones entre la actividad, los días desde la última interacción y el retiro posterior. Estas relaciones cambian entre cortes, pero también cambian las inscripciones analizadas y el tiempo restante de seguimiento. Para revisar esta situación se repitió parte del análisis con un grupo común. Esa comparación utiliza información posterior y sirve como revisión de los resultados, no como población disponible para una alerta temprana.'),
    ('La caracterización y la ingeniería disponen',r'El estudio cuenta con fuentes revisadas, indicadores construidos y resultados documentados. Se excluyó el conteo de filas como candidato del modelo y se examinó qué cambia al retirar duplicados, utilizar otro CV o variar los indicadores del PCA. Estas comprobaciones ayudan a entender los datos; todavía no demuestran una mejora predictiva. La selección final de variables, la comparación de modelos, SHAP y el prototipo permanecen pendientes. Por tanto, el objetivo general sigue en desarrollo y no se afirma una reducción del abandono ni capacidad comprobada para predecir casos nuevos.'),
    ('La siguiente etapa requiere fijar',r'El siguiente paso es definir cómo se evaluarán los modelos y qué situaciones se espera que puedan predecir: nuevas personas, otras presentaciones o ambas. El protocolo deberá tener en cuenta las inscripciones repetidas y la exploración que ya se hizo de los datos. También deberá fijar cómo comparar ventanas, probabilidades y umbrales. La disponibilidad de las notas y las discrepancias de la fuente mantienen sus limitaciones; se conservan las exclusiones del anteproyecto.'),
    ]}
    for name,items in replacements.items():
        text=(OLD/name).read_text(encoding='utf-8')
        if name=='desarrollo2.tex':
            a=text.index('El día 0 es el inicio')
            b=text.index('La guía preliminar',a)
            new=r'El día 0 corresponde al inicio de una presentación, es decir, una edición de un módulo. Los días negativos son anteriores a ese inicio. La unidad de análisis es la inscripción de una persona en un módulo y una presentación. El corte $t$ indica el día en que se haría la predicción. Hasta ese momento se observan $n_t=t+1$ días, contando tanto el día 0 como el propio corte. Las fechas de matrícula, retiro y final de la presentación se representan mediante $r_i$, $u_i$ y $L_i$. Este último se fija según la longitud registrada de la presentación. La ventana de observación es $\{0,\ldots,t\}$ y el retiro futuro se busca en $(t,L_i]$. La actividad anterior al inicio se resume por separado.'
            changes.append({'archivo':name,'antes':text[a:b],'despues':new})
            text=text[:a]+new+'\n\n'+text[b:]
        for start,new in items:
            text=paragraph(text,start,new,name)
        (P/name).write_text(text,encoding='utf-8')


if __name__=='__main__':
    main()
