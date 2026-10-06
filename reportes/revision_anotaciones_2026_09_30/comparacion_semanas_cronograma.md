# Preparación del primer avance frente al cronograma del anteproyecto

Fecha: 30 de septiembre de 2026. Revisión provisional, previa a la rúbrica. No modifica el cronograma aprobado ni equivale a una evaluación del curso.

## Veredicto

El proyecto dispone de material para presentar un avance sustantivo en comprensión de datos, construcción de indicadores y análisis exploratorio. La entrega aún debe complementarse con un cronograma actualizado con el director. No se ha verificado una versión de ese cronograma con fechas actuales y acuerdos de seguimiento. Tampoco se dispone todavía de la rúbrica ni del contenido del archivo «Estructura documento proyecto» enlazado desde Semana 2.

La comparación por actividades es posible. La comparación de puntualidad no es verificable: el cronograma aprobado utiliza M1–M10 y no se ha establecido en esta revisión qué mes y año corresponde a M1. No sería correcto afirmar que el proyecto está al día, atrasado o ejecutado en un porcentaje específico sin esa correspondencia.

## Qué indican los documentos nuevos

**Semana 1, páginas 1–2.** Presenta la agenda del encuentro inicial, la explicación de los roles del director y tutor y la orientación sobre el documento, los aspectos evaluados y los artefactos. Señala que la grabación estará en Panopto y que cada grupo debe concertar con su director encuentros periódicos. La agenda no contiene por sí sola los criterios específicos que se hayan explicado oralmente. No se ha consultado esa grabación ni se dispone de evidencia de acuerdos de reunión.

**Semana 2, página 1.** Solicita ordenar los avances de acuerdo con dos recursos: «Estructura documento proyecto» y «Plantilla Latex». Además, pide actualizar el cronograma de trabajo definido con el director y cargarlo junto con el documento PDF. Por tanto, no basta con tener únicamente el PDF del proyecto. El texto no establece en esta página un porcentaje mínimo de avance ni exige que ya exista un modelo entrenado.

El enlace de estructura apunta a `Estructura_Documento_Proyecto_MCD_Vers2025-1.docx`; el de plantilla, a `Plantilla_ProyAplicado.zip`, en la plataforma institucional. Existe una plantilla de ese nombre en el espacio local, pero no se ha verificado identidad entre esa copia y el archivo actualmente enlazado. El contenido de la estructura no se infiere a partir de su nombre.

## Comparación de las actividades

Los meses siguientes se leyeron en la tabla 9.1 del anteproyecto, página impresa 24 (página 25 del PDF). Los estados describen lo respaldado por código, archivos y registros disponibles; no significan que los análisis completos se hayan repetido en esta revisión.

| Actividad | Meses previstos | Estado sustentable | Evidencia disponible y cierre pendiente |
|---|---|---|---|
| A1.1. Obtener OULAD, revisar estructura y cargar | M1–M2 | Parcial al considerar toda la actividad; revisión y carga completas documentadas | Siete CSV, notebook 01, resumen e informe de ejecución. La procedencia oficial de la descarga no queda certificada solo por las huellas locales; requiere registro de origen o contraste con la fuente oficial. |
| A1.2. Explorar faltantes, duplicados, inconsistencias y atípicos | M2 | Completo documentado | Notebooks 01 y 03, tablas de revisión, capítulo 3. La existencia de limitaciones de la fuente no impide cerrar su identificación y documentación. |
| A1.3. Exploración y selección de variables base | M2–M3 | Parcial, con avance amplio | Distribuciones, asociaciones y variables utilizadas están documentadas; falta presentar un cierre explícito de la selección base respecto a participación, desempeño, inactividad y trayectoria, incluyendo el alcance de los puntajes. Esta actividad no exige seleccionar variables mediante rendimiento predictivo. |
| A2.1–A2.2. Integración y ventanas | M3 | Completo técnicamente para la versión actual | Cinco cortes, condiciones de inclusión y uniones implementadas en los notebooks 01–02 y `src/ventanas_oulad.py`. La discusión académica de diferencias frente al anteproyecto se registra aparte. |
| A2.3–A2.5. Interacción, continuidad y desempeño inicial | M3–M4 | Parcial como bloque | A2.3 y A2.4 tienen indicadores implementados. A2.5 incluye entregas y calendario; las calificaciones permanecen en auditoría, fuera de los predictores por falta de fecha de disponibilidad. |
| A2.6–A2.7. Tendencias y conjunto consolidado | M4–M5 | Parcial como bloque | Tendencias implementadas y cinco bases exportadas con etiquetas y candidatos. Se requiere cerrar la especificación de entrada al modelado; tener archivos candidatos no acredita por sí solo un conjunto final acordado. |
| A3.1. Resultado objetivo y exploración de abandono implícito | M5 | Parcial frente a la formulación original | Retiro registrado futuro implementado; inactividad como indicador complementario. Falta ratificación académica de esa delimitación y del uso de retiro sin atribuir voluntariedad. |
| A3.2–A3.3. Partición y transformaciones para modelado | M5 | No iniciado en la fase predictiva | Hay decisiones y limitaciones documentadas, pero no se dispone de una partición final ni de un flujo de entrenamiento ejecutado. Las transformaciones exploratorias no equivalen a ese flujo. |
| A3.4. Distribución de clases y tratamiento del desbalance | M5–M6 | Parcial | Se describieron las proporciones de retiro por corte. Queda evaluar, si corresponde, ponderación, remuestreo o umbrales dentro del entrenamiento. No se presupone que deba aplicarse remuestreo. |
| A3.5. Entrenamiento y ajuste | M6 | No iniciado | El capítulo 5 declara expresamente que aún no se han entrenado y comparado clasificadores. |
| A3.6. Evaluación comparativa | M6–M7 | No iniciado | No se dispone de resultados predictivos bajo un protocolo común. Las asociaciones exploratorias no sustituyen esta evaluación. |
| A4.1. Matriz de confusión y errores | M7 | No iniciado | Depende de modelos evaluados. |
| A4.2. SHAP y variables relevantes | M7–M8 | No iniciado | Existe fundamento teórico; el capítulo 6 identifica la aplicación como pendiente. |
| A4.3. Modelo final y patrones | M8 | No iniciado | Requiere comparación e interpretación de modelos. |
| A5.1. Definir elementos y herramienta del prototipo | M8 | No iniciado como actividad cerrada | Se describe un propósito general; no se verificó una especificación y selección de herramienta implementable. |
| A5.2. Implementar visualizaciones, predicciones y explicaciones | M9 | No iniciado | Las figuras de la tesis no equivalen al prototipo previsto. |
| A5.3. Revisar claridad, utilidad y documentar el prototipo | M9–M10 | No iniciado | Depende de la implementación del prototipo; no equivale a revisar la redacción de la tesis. |

La evidencia cubre buena parte del trabajo situado originalmente entre M1 y M5 y una parte descriptiva de A3.4. Esto no significa que los primeros cinco meses estén completamente cerrados ni permite convertir actividades en un porcentaje global: tienen alcances y esfuerzos distintos.

### Precisión respecto de la tabla de avance anterior

El registro previo vinculaba el pendiente de A1.3 a la selección predictiva definitiva. Esa exigencia es más fuerte que la formulación original, que habla de seleccionar variables base a partir del análisis exploratorio. Para cerrar A1.3 conviene documentar qué variables fuente se eligieron, cuáles se excluyeron y por qué; no es necesario esperar al entrenamiento para justificar esa selección inicial. La selección posterior dentro del entrenamiento es una tarea diferente. Se mantiene un estado parcial prudente por la necesidad de formalizar ese cierre y la delimitación de desempeño académico; no se añade una obligación ajena al anteproyecto.

## Qué se puede presentar y qué falta preparar

| Elemento de la primera entrega | Situación actual | Acción pertinente |
|---|---|---|
| PDF del proyecto | Disponible en la plantilla local; capítulos 3–4 revisados y capítulos pendientes identificados | Enviar al asesor para revisión, como plantearon los autores. No se ha realizado ese envío desde esta conversación. |
| Evidencia del trabajo realizado | Tres notebooks, módulos Python, tablas, figuras y registros de ejecución | Seleccionar evidencias que correspondan a las actividades del cronograma; no se afirma que deban subirse todos esos archivos, pues la página no lo exige. |
| Cronograma actualizado | No se ha verificado una versión con fechas reales y acuerdo vigente | Conservar actividades originales y añadir fechas previstas, fechas reales, estado, producto y siguiente acción; acordar cambios con el director. |
| Reuniones periódicas con el director | No verificable con los archivos consultados | Confirmar la periodicidad acordada y conservar una nota de decisiones. No se exige un formato de acta que los PDF no establecen. |
| Estructura y plantilla vigentes | Plantilla local disponible; estructura enlazada no consultada | Contrastar con los dos recursos institucionales cuando se acceda a ellos. |
| Rúbrica | Pendiente según los autores | Ajustar la presentación al publicarse; no inventar porcentajes de cumplimiento ni mínimos exigidos. |

## Hallazgos que requieren seguimiento

| ID | Severidad | Evidencia | Corrección o condición de cierre |
|---|---|---|---|
| P1 | Mayor | Semana 2 pide cronograma actualizado junto con PDF; no se verificó uno vigente | Prepararlo con fechas reales y contrastarlo con el director. |
| P2 | Mayor | Cronograma en M1–M10 sin correspondencia de fechas confirmada | Identificar mes y año de M1 y fechas pactadas; hasta entonces el estado de puntualidad es no verificable. |
| P3 | Mayor | Estructura enlazada y rúbrica sin contenido disponible | Revisarlas antes de declarar cumplimiento de la entrega. |
| P4 | Mayor | A2.5/A3.1 y delimitación de población difieren de la lectura literal del anteproyecto | Obtener concepto académico sobre la justificación y documentar la decisión. |
| P5 | Menor | Tabla de avance anterior asociaba A1.3 con selección predictiva definitiva | Corregir esa interpretación en el próximo ajuste de avance, separando selección base y selección dentro del entrenamiento. |

El protocolo de validación es bloqueante para iniciar una comparación predictiva interpretable, pero no se presenta como una prohibición para enviar el avance al asesor. La revisión del asesor es precisamente una oportunidad para resolver esa decisión.

## Siguiente paso propuesto

Preparar con el director la actualización del cronograma a partir de esta matriz, sin cambiar los objetivos por iniciativa editorial. El orden técnico siguiente es cerrar las decisiones de población, evento y variables disponibles; definir la evaluación y las particiones; y después entrenar una línea base y los modelos de comparación. En paralelo puede completarse el cierre documental de la selección inicial de variables y la revisión de la estructura exigida.

La fecha de comienzo de M1 sigue pendiente de confirmación. Si M1–M5 correspondieran a un periodo ya terminado, las actividades parciales de ese bloque requerirían reprogramación; si no, no puede hablarse de atraso por esa razón. La captura previa muestra una actividad del 6 al 19 de octubre, pero no convierte M1–M10 en semanas del curso ni especifica por sí sola cuál fase técnica debe estar terminada para esa entrega.

## Evidencia consultada

- `D:/Semana 1.pdf`, ambas páginas, lectura visual y textual.
- `D:/Semana 2.pdf`, página 1, lectura visual y textual; inspección de los destinos de sus enlaces sin atribuir acceso a su contenido.
- `Anteproyecto versión final.pdf`, actividades de metodología (páginas impresas 21–22) y cronograma (página impresa 24). Los meses se cotejaron visualmente y con la posición de las marcas X.
- `Plantilla_ProyAplicado/avance_objetivos.tex`, capítulos de estado de modelado, SHAP y prototipo; `decision_temporal.json`.
- `reportes/correcciones_2026_09_10/entrega.md`, los tres registros `*_ejecucion.json`, `01_resumen.json`, `02_resumen.json`, `productos_02.json` y diccionario de indicadores.
- `reportes/entorno_local_2026_09_30/verificacion.json`: comprobación del entorno y kernel. No acredita una nueva ejecución completa.

No se alteraron los notebooks, los datos, el anteproyecto ni el documento principal como parte de esta comparación.
