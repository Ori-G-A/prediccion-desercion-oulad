# Protocolo de validación predictiva — versión de trabajo, 19 de octubre de 2026

Orden operativo vigente: `../../PROTOCOLO_EJECUCION_MODELOS.md`, verificado y conservado el 19 de octubre de 2026 por solicitud del usuario. Precisa las condiciones para pasar de búsqueda a selección, congelación, prueba e interpretación; este documento conserva las definiciones del diseño.

Actualización de ejecución del mismo día: tras la autorización posterior del usuario, se implementó el entrenamiento y se completó la búsqueda de regresión logística en los cinco cortes, con calibración y umbral separados. La comprobación de las otras familias y el alcance exacto se documentan en `../entrenamiento_2026_10_19/revision.md`. La prueba final permanece reservada. Las referencias a «esta etapa» en la preparación siguiente describen su estado antes de esa ejecución; no implican que el modelado siga sin iniciar.

## Estado y alcance

El usuario eligió explícitamente evaluar **personas no vistas durante el entrenamiento, dentro de las ofertas de módulos disponibles** y posteriormente autorizó avanzar. Se implementa la preparación de las particiones y de la configuración descritas a continuación; los resultados de ejecución se registran en `implementacion/verificacion.json`. Esta autorización no acredita aprobación del director. No se entrenan modelos en esta etapa.

El propósito es estimar la capacidad de predecir el retiro registrado futuro de una inscripción. Una persona puede tener varias inscripciones: todas deberán permanecer en el mismo conjunto, incluso cuando aparezcan en diferentes módulos, ofertas o cortes. Esta evaluación no demuestra desempeño en periodos futuros, módulos nuevos ni otras instituciones.

Se conserva `decision_temporal.json`: cortes 7, 14, 28, 42 y 56; matrícula conocida y registrada hasta el corte; ausencia de retiro hasta ese día; cierre de la oferta posterior al corte. El evento es un retiro con fecha estrictamente posterior al corte y hasta el cierre de la oferta, incluido este último día. La ventana de actividad comprende de 0 a t, ambos incluidos; los indicadores previos al inicio conservan su definición explícita. El horizonte cambia entre ofertas y disminuye entre cortes. La cobertura administrativa completa sigue siendo un supuesto no verificable individualmente.

## Separación de personas y función de cada conjunto

Se propone una asignación única por `id_student`, común a los cinco cortes y a todos los modelos. Se conservará un manifiesto con persona, conjunto y pliegue; las claves de inscripción se unirán después a ese manifiesto. Ningún identificador de persona se utilizará como predictor.

| Conjunto | Proporción aproximada | Uso permitido |
|---|---:|---|
| Ajuste y selección | 60 % | Transformaciones, hiperparámetros, pesos de clase y selección de modelos mediante validación cruzada |
| Calibración | 10 % | Ajustar la correspondencia entre puntuaciones y frecuencia de retiro, una vez seleccionado el modelo |
| Umbral | 10 % | Fijar la regla de clasificación del modelo calibrado |
| Prueba final | 20 % | Evaluar una sola vez los procedimientos congelados |

Son proporciones orientativas de filas; agrupar personas impide garantizar simultáneamente porcentajes exactos de inscripciones, personas y clases. La separación adicional de calibración y umbral reduce los datos de ajuste, pero permite explicar y auditar cada decisión sin reutilizar la prueba.

Para concretar la estratificación de A3.2 se propone `StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=20261019)` sobre las filas elegibles de los cinco cortes, agrupadas por persona. El estrato será la combinación de corte y clase; la etiqueta utilizada para entrenar continuará siendo únicamente `retiro_futuro`. Los pliegues 0–1 se destinarán a prueba, el 2 a calibración, el 3 a umbral y los restantes a ajuste. Esta construcción intenta equilibrar clases por corte; no garantiza equilibrio por oferta y pondera más a quienes tienen más inscripciones elegibles. Se documentarán esas distribuciones sin buscar semillas que produzcan mejor desempeño.

Antes de aceptar el manifiesto se comprueban ambas clases en cada conjunto y corte, ausencia de personas compartidas y representación de las ofertas. Si alguna oferta no queda representada en los conjuntos, o una clase falta, la preparación se detiene antes de guardar el manifiesto. No se eliminan grupos silenciosamente para resolverlo. Los resultados se conservan en `implementacion/verificacion.json` y en las tablas de distribución.

Dentro del 60 % se construirán cinco pliegues de validación con el mismo principio de agrupación y estratos por corte y clase, semilla 20261020. Se guardará una única asignación interna de personas y se reutilizará para todos los modelos. Cada ajuste excluirá por completo a las personas del pliegue validado. Las métricas de estos pliegues servirán para selección; no se presentarán como estimación independiente del desempeño del ganador.

## Predictores y ajuste

La lista inicial propuesta es `PREDICTORS` de `src/ventanas_oulad.py`, exportada con nombres y huella digital antes del entrenamiento. Las variables de `CONTEXT` no se incorporarán automáticamente: cualquier ampliación deberá justificar disponibilidad, pertinencia y alcance antes de congelar la lista. Se excluirán identificadores, resultados finales, fechas de retiro, etiquetas derivadas y notas cuya disponibilidad temporal no está acreditada. `n_registros_vle` permanece excluido. Los datos de auditoría nunca se pasarán completos al estimador.

Se entrenará un modelo separado por corte. Los faltantes estructurales, por ejemplo una ventana de 28 días todavía inexistente al día 7, no se interpretarán como ausencia de actividad. Las columnas enteramente ausentes se identificarán en el entrenamiento; para las restantes se propone imputación por mediana e indicadores de ausencia, con escalado en regresión logística y TabNet. Cualquier codificación, eliminación de constantes o selección se ajustará dentro del entrenamiento del pliegue. Los algoritmos podrán usar tratamientos específicos documentados, con el mismo conjunto inicial de información disponible.

Se compararán una referencia de probabilidad constante igual a la prevalencia del entrenamiento y los cinco candidatos del documento: regresión logística, Random Forest, XGBoost, LightGBM y TabNet. La referencia adicional de clase mayoritaria permitirá interpretar la exactitud. Se compararán ajuste sin ponderación y pesos inversos a la frecuencia de clase calculados exclusivamente en el entrenamiento correspondiente. El protocolo inicial no requiere sobremuestreo sintético.

Los espacios de hiperparámetros y el presupuesto por familia quedan especificados en `implementacion/configuracion.json`, antes del primer ajuste. Se conservan como máximo 30 configuraciones por familia y corte, o todas si el espacio es menor, con semilla 20261021. Se reutilizan las mismas configuraciones entre cortes. No se ampliará el presupuesto de un modelo después de mirar la prueba. Esta primera configuración fija el número de árboles o épocas y desactiva la detención temprana, para no reutilizar el pliegue de evaluación como control del entrenamiento. Se documentarán convergencia y fallos. El archivo es un contrato para el futuro entrenador; no demuestra que los algoritmos estén implementados ni ejecutados.

## Selección, calibración y umbral

La medida principal propuesta para elegir configuración y familia en cada corte es la media de **precisión promedio** o AP en los cinco pliegues. AP resume la precisión alcanzada a medida que se recuperan más retiros; no es la exactitud ni el área trapezoidal bajo la curva de precisión y sensibilidad. Se reportará junto con la prevalencia y ROC-AUC. Cada inscripción tendrá el mismo peso al evaluar; la agrupación protege la separación de personas, pero no convierte la métrica en una medida por persona.

Se seleccionará la mayor AP media. En igualdad a seis decimales se preferirá, en orden preestablecido, regresión logística, Random Forest, LightGBM, XGBoost y TabNet; dentro de una familia se usará el orden de configuraciones previamente guardado. Esta regla resuelve empates operativos y no prueba superioridad estadística.

La configuración elegida se reajustará con todo el 60 %. Se propone aplicar después una calibración sigmoidal, fijada de antemano, usando únicamente el 10 % de calibración. Se conservará congelado el modelo base. No se elegirá el método de calibración examinando la prueba. Se evaluarán Brier y una curva de calibración con diez intervalos fijos de probabilidad; se informarán tamaños de los intervalos. Brier resume error probabilístico y no mide exclusivamente calibración.

En el 10 % de umbral se elegirá el valor que maximice F1 para retiro futuro; en empates se preferirá mayor sensibilidad y luego menor umbral. Se conservará la convención documental: alerta cuando p > umbral. La búsqueda considerará todos los patrones de clasificación alcanzables, incluidos todos positivos y ninguno positivo. Esta elección es una regla de comparación académica, no una política institucional óptima: no se conocen costes de error ni capacidad real de atención. Se informarán sensibilidad, precisión, especificidad y proporción de alertas, además de F1. El valor 0,5 se conservará como referencia secundaria.

Después de calibrar y fijar el umbral no se reajustará el modelo con esos conjuntos, porque ello modificaría la escala sobre la cual se tomaron las decisiones. Para comparar familias, se podrán congelar sus respectivas configuraciones, calibradores y umbrales mediante la misma secuencia; la familia principal seguirá siendo la seleccionada en validación y no se cambiará por el orden observado en prueba.

## Evaluación final y comparación entre cortes

Antes de abrir la prueba se guardarán predictores, particiones, configuración, modelo, calibrador, umbral, semillas, versiones y huellas de los datos. La prueba se ejecutará para el paquete completo previamente definido. Se reportarán inscripciones, personas, eventos, prevalencia, AP, ROC-AUC, Brier, matriz de confusión, sensibilidad, precisión, especificidad, F1 y proporción de alertas. Los resultados por oferta incluirán sus denominadores y se marcarán como descriptivos; una métrica sin ambas clases se declarará no definida.

Se proponen intervalos percentiles del 95 % con 2.000 remuestreos de personas de prueba, manteniendo juntas todas sus inscripciones y usando semilla 20261022. Las comparaciones entre modelos utilizarán las mismas muestras. Las réplicas sin ambas clases se contarán y excluirán de las métricas que lo requieran. Estos intervalos representan variación entre personas condicionada a los modelos y ofertas observados; no incluyen toda la incertidumbre del entrenamiento ni la variación entre futuras ofertas.

La evaluación principal de cada corte usará su población elegible real. No se declarará una ventana óptima comparando solamente AP: cambian la población, la prevalencia y el horizonte. Se presentarán conjuntamente desempeño, proporción de alertas y anticipación entre corte y retiro para los verdaderos positivos, con mediana y cuartiles. La anticipación describe tiempo disponible y no demuestra que una intervención hubiera sido efectiva. El subconjunto de inscripciones comunes a los cinco cortes podrá usarse como análisis complementario, aclarando que exige información posterior para formarlo y no representa a quienes serían alertados al inicio.

## Evidencia y condiciones de cierre

Se revisaron el capítulo activo `Plantilla_ProyAplicado/desarrollo3.tex`, las definiciones y candidatos de `descripcion.tex`, `decision_temporal.json`, la lista de variables y elegibilidad de `src/ventanas_oulad.py`, y las actividades A3.1–A3.4 del anteproyecto original mediante extracción de texto. A3.2 pide estratificación; la agrupación por personas constituye su precisión propuesta y permanece pendiente de revisión del director. No se reintroducen la voluntariedad del retiro ni una segunda etiqueta por inactividad presentes en la redacción original: rigen las precisiones posteriores documentadas.

Se leyeron los archivos preparados de `data/processed/correcciones_2026_09_10`; no se reprodujo su construcción desde las siete tablas originales:

| Corte | Inscripciones | Personas | Retiros futuros | Claves duplicadas |
|---:|---:|---:|---:|---:|
| 7 | 29.076 | 26.030 | 6.632 | 0 |
| 14 | 28.054 | 25.220 | 5.580 | 0 |
| 28 | 27.515 | 24.826 | 5.012 | 0 |
| 42 | 27.005 | 24.491 | 4.500 | 0 |
| 56 | 26.506 | 24.105 | 3.998 | 0 |

La unión contiene 26.089 personas. Las dos copias de la muestra de voz tienen la misma huella SHA-256. No se modificaron los capítulos ni las decisiones temporales, por lo que no corresponde afirmar una integración o compilación documental.

| Severidad / estado | Evidencia o limitación | Acción de cierre |
|---|---|---|
| Mayor / resuelto para preparar el protocolo | Generalización antes pendiente | Elección explícita del usuario: personas nuevas en ofertas disponibles |
| Preparación implementada / consultar ejecución | Manifiesto y comprobaciones en `implementacion/` | Conservar asignación, huellas y versiones; verificar identidad al reproducir |
| Configuración especificada / entrenador pendiente | Lista exacta y espacios de búsqueda en `implementacion/configuracion.json` | Implementar pipelines y verificar sus tratamientos con el contrato guardado |
| Antecedente documentado / sin error confirmado | Exploración previa sobre OULAD completo, reconocida en desarrollo3.tex | Registrar origen de decisiones; no equiparar exploración con selección indebida demostrada |
| Mayor / no verificable | Cobertura administrativa individual y disponibilidad de calificaciones | Conservar supuesto de seguimiento y exclusión de notas |
| Mayor / pendiente documental | Revisión del director no acreditada | Presentar precisión de A3.2 y registrar respuesta sin presumir aprobación |

## Referencias técnicas consultadas

### Aclaración y trazabilidad de la implementación

El 19 de octubre de 2026 se sustituye la clasificación de la exploración previa como «limitación permanente» por «antecedente documentado / sin error confirmado», atendiendo a la aclaración solicitada por el usuario. La exploración completa está documentada; no se ha demostrado que se escogieran predictores por un resultado favorable de clasificación sobre la futura prueba. La revisión de `reportes/correcciones_2026_09_10/actualizacion_asesor.md` identifica una justificación de interpretación para excluir `n_registros_vle`, conserva ambos CV como candidatos y niega que el PCA justifique automáticamente una selección predictiva. Esto no reconstruye exhaustivamente el origen de cada indicador. Se mantiene el control de decisiones futuras mediante particiones reservadas. La versión anterior se conserva en `protocolo_pre_implementacion.md` como evidencia histórica, no como instrucción vigente.

La revisión académica sigue pendiente documental y no se convierte en un requisito adicional para preparar código o avanzar con el trabajo autorizado. Las fuentes LaTeX no se modificaron en esta etapa; su integración y compilación siguen pendientes.

Documentación oficial de scikit-learn, consultada el 19 de octubre de 2026. Las versiones efectivamente instaladas deberán registrarse al implementar; consultar documentación no acredita ejecución local.

- Scikit-learn developers. *Cross-validation: evaluating estimator performance*. https://scikit-learn.org/stable/modules/cross_validation.html — separación por grupos y estratificación aproximada.
- Scikit-learn developers. *average_precision_score*. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html — definición de AP y diferencia con integración trapezoidal.
- Scikit-learn developers. *Tuning the decision threshold for class prediction*. https://scikit-learn.org/stable/modules/classification_threshold.html — separación entre ajuste del clasificador y del umbral.
- Scikit-learn developers. *Probability calibration*. https://scikit-learn.org/stable/modules/calibration.html — calibración con datos distintos a los del ajuste y evaluación probabilística.
