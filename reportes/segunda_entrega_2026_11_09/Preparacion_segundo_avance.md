# Preparación del segundo avance en video

Proyecto: Modelo predictivo del abandono estudiantil en entornos LMS mediante aprendizaje automático: análisis de factores académicos, conductuales y temporales.

Autores: Oriana Giraldo Arcia y Luis Javier Rubio Hernández.

Fecha de corte de esta preparación: 22 de octubre de 2026. Versión de trabajo para revisión de los autores; no acredita aprobación del asesor ni entrega en la plataforma.

## Propósito y requisitos

El video debe permitir comprender qué se ha desarrollado, cómo se relaciona con el cronograma y qué falta por completar. La guía de Semana 8 exige un máximo de cinco minutos, nombre y descripción breve del proyecto, actividades realizadas, porcentaje de avance frente al cronograma e inconvenientes. La captura del curso sitúa la actividad entre el 2 y el 9 de noviembre de 2026; no muestra la hora de cierre. Se propone terminar la entrega el 8 de noviembre como margen interno.

La guía permite publicar el video en YouTube como no listado y entregar el enlace en Word o PDF. Esta preparación no realiza ninguna publicación. Las recomendaciones de grabación indican cuidar iluminación, ruido, encuadre horizontal y claridad del audio; conviene ensayar con un guion antes de grabar.

## Cuadro de avance frente a la planificación guardada

La base es el cronograma fechado el 6 de octubre, contrastado con el seguimiento del 21 de octubre y los registros de cierre. No se ha acreditado que esa copia sea idéntica al archivo efectivamente enviado el 19 de octubre. Los estados siguientes describen productos técnicos: una actividad realizada puede conservar decisiones pendientes de revisión académica. Esta consulta revisa evidencia guardada; no reproduce entrenamientos ni construye nuevamente los datos originales.

| Actividad y periodo previsto | Producto disponible al corte | Estado técnico y pendiente | Evidencia de consulta |
|---|---|---|---|
| A1.1 Obtener y cargar OULAD; M1–M2 | Siete tablas cargadas y revisadas | Parcial: completar procedencia de descarga | Cronograma base y seguimiento |
| A1.2 Calidad; M2 | Caracterización de faltantes, duplicados e inconsistencias | Realizada según registros; no reproducida desde datos crudos en esta revisión | Cronograma base |
| A1.3 Variables base; M2–M3 | 26 indicadores candidatos y exclusiones | Parcial: revisar alcance del desempeño académico sin calificaciones como predictores | Cronograma base y seguimiento |
| A2.1–A2.2 Integración y ventanas; M3 | Conjuntos para días 7, 14, 28, 42 y 56 | Producto realizado; ratificación de delimitaciones pendiente | Seguimiento y estado de modelado |
| A2.3–A2.5 Indicadores; M3–M4 | Interacción, continuidad, entregas y calendario | Parcial: revisión del alcance académico | Seguimiento |
| A2.6–A2.7 Tendencias y consolidación; M4–M5 | Conjuntos utilizados en el modelado | Producto realizado; conservar trazabilidad | Seguimiento y cierre |
| A3.1 Resultado e inactividad; M5 | Retiro registrado posterior al corte; inactividad complementaria | Parcial: revisar correspondencia con el anteproyecto | Seguimiento |
| A3.2–A3.3 Separación y preparación; M5 | Separación por personas y preparación dentro de las particiones internas | Producto realizado; revisión metodológica pendiente | Seguimiento y cierre |
| A3.4 Desbalance; M5–M6 | Comparaciones con y sin ponderación; umbral fijado antes de prueba | Producto realizado; no define una política institucional de atención | Seguimiento |
| A3.5 Entrenar y ajustar; M6 | Cinco familias, cinco cortes y 3.200 ajustes de validación cruzada | Completo técnicamente | Estado de modelado |
| A3.6 Evaluar; M6–M7 | Evaluación reservada con paquete congelado | Completa técnicamente; interpretación académica pendiente | Verificación de cierre |
| A4.1 Errores; M7 | Métricas y matrices de confusión | Producto realizado; discutir implicaciones de falsas alertas y retiros omitidos | Revisión de cierre |
| A4.2 SHAP; M7–M8 | 500 explicaciones y comprobación de su suma | Producto realizado; estabilidad no evaluada y sin interpretación causal | Verificación de cierre |
| A4.3 Selección; M8 | Principales seleccionados por validación antes de la prueba | Producto realizado; no cambiar selección al observar prueba | Revisión de cierre |
| A5.1 Definir prototipo; M8 | Herramienta local y cobertura de requisitos documentada | Producto disponible; revisar cobertura con destinatarios | Seguimiento |
| A5.2 Implementar; M9 | Visualizaciones de resultados y explicaciones | Parcial: cobertura restante por revisar | Estado de modelado |
| A5.3 Revisar y documentar; M9–M10 | Comprobaciones funcionales y documentación | Parcial: revisión visual de versión actual y evaluación de comprensión pendientes | Estado de modelado |

M3 termina el 26 de octubre; M4 comienza el 27 de octubre. Los productos de modelado e interpretación corresponden a actividades previstas para meses posteriores. Este adelanto técnico no modifica automáticamente el calendario ni demuestra cierre del proyecto. La entrega del curso del 30 de noviembre es distinta del cierre del proyecto previsto para mayo de 2027.

## Cómo resolver el porcentaje solicitado

El porcentaje global permanece pendiente de determinación. El cronograma consultado no contiene pesos ni una regla de medición. Tampoco conviene dividir las filas completas entre las filas totales: algunas filas agrupan varias actividades y su esfuerzo es diferente.

Se propone confirmar primero el cronograma enviado y revisar si contiene una regla de avance. Si no existe, se preparará una ponderación por productos o esfuerzo previsto, con criterios observables para considerar cada producto completo o parcial. La estimación se calcularía sumando el peso de cada actividad multiplicado por su grado de cumplimiento. Los pesos deben sumar 100 % y quedar documentados junto con la fecha de corte. Esta es una propuesta de medición, no una ponderación aprobada.

Ejemplo exclusivamente hipotético: si una actividad pesara 20 % del proyecto y hubiera completado la mitad de los productos previstos, aportaría 10 puntos porcentuales al avance global. Ese ejemplo no describe el avance de OULAD. No se asignará automáticamente 50 % a cualquier actividad parcial.

Antes de cerrar el video deben estar disponibles la base confirmada, la regla, los pesos y los productos que sustentan el porcentaje. Mientras tanto, puede informarse que terminó el cálculo del modelado previsto, pero eso no sustituye el porcentaje global exigido por la actividad.

## Mensajes principales y explicación propuesta

### 1. Qué se busca

El proyecto estudia si los registros de una plataforma educativa permiten anticipar el retiro futuro de una inscripción. Una inscripción corresponde a una persona en un módulo ofrecido en un periodo concreto. El estudio utiliza OULAD y no identifica las causas personales del retiro.

Ejemplo hipotético para explicar el tiempo: al predecir en el día 14, solo se utiliza información disponible hasta ese día. Un retiro registrado en el día 35 sería posterior al corte; uno del día 10 no sería un retiro futuro para esa predicción.

### 2. Qué cambió respecto del avance guardado

El documento de avance del 6 de octubre dejaba pendientes el entrenamiento, la comparación, SHAP y el prototipo. Actualmente existen resultados de las cinco familias de modelos, su evaluación reservada, explicaciones de predicciones y un prototipo local. Esta comparación se refiere a la copia guardada, hasta confirmar su correspondencia con la entrega enviada.

### 3. Cómo se cuidó la evaluación

Los datos se separaron por personas para evitar que las inscripciones de un mismo estudiante aparecieran a ambos lados de la separación. Los modelos se compararon mediante validación interna. La selección, la calibración de probabilidades y el umbral se fijaron antes de consultar la prueba reservada.

Ejemplo hipotético: si una persona cursó dos módulos, sus inscripciones se mantienen juntas en la partición correspondiente. Así se reduce el riesgo de evaluar con registros de una persona ya utilizada para ajustar el modelo.

### 4. Qué permiten afirmar los resultados

Los resultados muestran capacidad predictiva superior a la referencia constante en la medida AP, que resume la precisión al recuperar proporciones crecientes de retiros. Sin embargo, las falsas alertas siguen siendo numerosas y no se encontró evidencia concluyente de superioridad de los modelos principales sobre la regresión logística en las comparaciones pareadas de AP. Esto no demuestra que los modelos sean equivalentes.

Para el video basta comunicar: «La comparación ya produjo resultados y permite identificar tanto aciertos como limitaciones. Por ello, el trabajo actual se concentra en explicar qué puede aportar la predicción y en qué situaciones puede equivocarse». Si se incorpora una cifra, debe acompañarse de corte temporal, denominador y límite; no se requiere mostrar todas las métricas.

### 5. Qué se está haciendo ahora

El trabajo continúa con la revisión de resultados, la discusión y las conclusiones, la coherencia del documento y la evaluación de comprensión del prototipo. Las explicaciones SHAP muestran contribuciones a la predicción del modelo, no las causas del retiro. La herramienta es un prototipo académico local; no se ha demostrado que su uso reduzca el abandono.

## Dificultades que pueden comunicarse

| Dificultad o pendiente | Tratamiento y situación |
|---|---|
| Coste del entrenamiento | Se completaron 3.200 ajustes internos. La búsqueda repetida consume tiempo; no se necesita repetirla para grabar el video. No confundir ajustes con estudiantes o con 3.200 modelos finales. |
| Incidencia de carga de bibliotecas | El estado registra que volvió a funcionar el 20 de octubre sin reinstalación. La causa no está determinada; no atribuirla al hardware sin evidencia. |
| Falsas alertas y retiros no detectados | Se documentaron métricas y errores. Se mantienen las reglas congeladas; no se cambian umbrales a partir de la prueba final. |
| Revisión académica de delimitaciones | Debe quedar constancia de las observaciones del asesor y su tratamiento; no se dispone aquí de una aprobación verificable. |
| Comprensión del prototipo | Las pruebas funcionales no sustituyen la evaluación con destinatarios. Se requiere observar si comprenden probabilidades, errores y explicaciones. |
| Porcentaje de avance | Falta confirmar la base enviada y documentar una regla de cálculo antes de presentarlo como cifra del proyecto. |

## Secuencia de presentación y preparación

Se propone una duración objetivo de 4:30 minutos, dejando margen frente al máximo de cinco. Los tiempos son orientativos y deben comprobarse mediante ensayo.

| Segmento | Tiempo | Apoyo visual propuesto |
|---|---|---|
| Nombre, autores y propósito | 0:00–0:30 | Título y una frase sobre el retiro futuro |
| Datos y ejemplo temporal | 0:30–1:15 | Línea sencilla con corte y retiro posterior |
| Actividades realizadas y evaluación | 1:15–2:30 | Secuencia preparación, entrenamiento y evaluación |
| Un resultado y su límite | 2:30–3:20 | Una visualización con denominador y mensaje explícitos |
| Cronograma e inconvenientes | 3:20–4:00 | Avance sustentado y dos dificultades principales |
| Trabajo restante | 4:00–4:30 | Revisión académica, discusión y prototipo |

El calendario interno propuesto es: cuadro y evidencias hasta el 26 de octubre; revisión de resultados del 27 al 30; guion y diapositivas del 31 al 2 de noviembre; ensayo del 3 al 5; grabación del 6 al 7; prueba de enlace y entrega el 8. La carga del video y su envío corresponden a acciones posteriores; no están ejecutadas.

## Verificaciones y pendientes de esta versión

Se consultaron las instrucciones de Semana 8 y de grabación, el cronograma guardado, el seguimiento, el estado de modelado y los informes de cierre. La verificación guardada informa 35 combinaciones de modelo/referencia y corte, 56 huellas y 500 explicaciones comprobadas; su alcance no incluye repetir entrenamientos. Se preservaron los resultados y los documentos anteriores.

| Prioridad | Pendiente | Evidencia necesaria para cerrarlo |
|---|---|---|
| Mayor, antes de grabar | Porcentaje global justificable | Cronograma efectivamente enviado, regla de cálculo y pesos documentados |
| Mayor, antes de grabar | Incorporar retroalimentación académica | Observaciones recibidas y registro de cómo se atendieron |
| Mayor, antes de entregar | Claridad y duración | Ensayo de ambos autores con tiempo medido; explicación correcta de los mensajes |
| Menor, antes de entregar | Hora exacta y acceso al enlace | Consulta de la actividad y apertura del video sin sesión iniciada |
| Trabajo posterior | Comprensión del prototipo | Registro de evaluación con destinatarios; no basta una prueba de software |

## Fuentes y trazabilidad

- Requisitos: `D:/Semana 8.pdf`, páginas 1–2.
- Grabación: `D:/recomendaciones_para_grabacion_2022.pdf`, páginas 1–2.
- Fechas: `D:/capturas/Captura de pantalla 2026-10-20 163446.png`.
- Base: `reportes/entrega_avance_2026_10_06/Cronograma_y_avance.md`.
- Seguimiento: `reportes/seguimiento_cronograma_2026_10_21/estado.md`.
- Ejecución: `estado_ejecucion_modelos.json`.
- Alcance de comprobaciones: `reportes/cierre_modelado_2026_10_21/verificacion.json`.
- Interpretación y límites: `reportes/cierre_modelado_2026_10_21/revision.md`.

Esta preparación añade un cuadro y mensajes para la entrega; no sustituye el protocolo, no cambia el cronograma original y no acredita cierre académico.
