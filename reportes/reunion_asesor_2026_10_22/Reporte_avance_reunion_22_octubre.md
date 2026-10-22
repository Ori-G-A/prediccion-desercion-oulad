# Avance del proyecto y explicación del modelado
Reunión con el asesor: 22 de octubre de 2026
Oriana Giraldo Arcia y Luis Javier Rubio Hernández
Proyecto Aplicado de Ciencia de Datos · PUJ Cali

## 1. Qué cambió desde la entrega
**Estado comprobado al 2026-10-21 14:02:30 (hora de Colombia).** Se completaron y verificaron las búsquedas de cinco familias de modelos: 3.200 ajustes en total. Se seleccionaron candidatos mediante validación interna, se verificaron sus probabilidades calibradas y umbrales y se congeló el paquete de evaluación. La prueba reservada terminó para los cinco cortes, con intervalos de incertidumbre. El cálculo SHAP terminó en los cinco cortes; sus salidas y patrones se revisaron; la discusión con el asesor está pendiente. Se revisaron las salidas, se integraron los hallazgos y límites en las fuentes activas y se implementó una primera versión local del prototipo. La revisión con el asesor y la evaluación del prototipo con usuarios siguen pendientes.

El registro del proyecto sitúa la entrega del avance y el cronograma el **19 de octubre**, según lo comunicado por los autores. Ese es el punto de referencia de este reporte. Las aclaraciones de terminología del 8 de octubre son antecedentes, no avances posteriores a esa entrega. Las actividades realizadas el propio día 19 se presentan como continuidad de esa jornada; no se conoce la hora exacta de envío para ordenarlas todas antes o después de la entrega.

| En el avance entregado / antecedente | Trabajo posterior o continuidad comprobada |
| --- | --- |
| Datos revisados e indicadores construidos; protocolo predictivo por concretar. | Se definió el escenario de evaluación y se guardaron particiones, semillas, predictores y configuraciones. |
| Modelado sin comparación terminada. | Se ejecutaron 200 ajustes logísticos y 750 por cada una de las otras cuatro familias. Se verificaron los cinco cortes. |
| Sin evaluación reservada terminada. | Se guardaron 25 candidatos, se congeló su evaluación y se ejecutó la prueba con 2.000 remuestreos de personas por corte. |
| Interpretación y prototipo pendientes. | Se preparó y comprobó el procedimiento SHAP; se implementó una primera versión local del prototipo de predicción e interpretación. |

También se mejoró la continuidad del documento y la proximidad de tablas y figuras a sus explicaciones. La versión integrada del 20 de octubre incorporó el protocolo y los avances disponibles entonces, se compiló y se revisaron páginas afectadas. El 21 de octubre se incorporaron posteriormente la evaluación final, la interpretación de SHAP y sus límites. Se conserva el respaldo de la versión previa.

El cambio principal es pasar de tener datos e indicadores preparados a contar con una comparación ejecutada bajo reglas comunes y resultados reservados disponibles para revisión. Esto no equivale todavía a demostrar utilidad educativa ni a recibir aprobación académica.

<!-- PAGE -->
## 2. Qué se está haciendo y para qué
El propósito es predecir el **retiro registrado futuro de una inscripción**, usando únicamente información disponible en el momento de predecir. Una inscripción corresponde a una persona en un módulo y una oferta de ese módulo en un periodo específico. El retiro registrado no informa por sí mismo su motivo ni su voluntariedad. La inactividad es un indicador complementario, no otra definición de retiro.

Se estudian cinco momentos: días **7, 14, 28, 42 y 56**. En cada uno se consideran las inscripciones que siguen vigentes y se usan señales de actividad y entregas disponibles hasta ese día. Por ejemplo, un retiro ocurrido el día 20 no puede contarse como un retiro futuro al predecir en el día 28. Los cinco cortes permiten estudiar cómo cambia la predicción al disponer de más información, aunque también cambian la población y el tiempo de seguimiento restante.

**Separar datos evita evaluarse con las mismas respuestas utilizadas para aprender.** Las personas se asignaron a cuatro conjuntos con proporciones aproximadas: 60 % para ajuste y selección, 10 % para calibración, 10 % para umbral y 20 % para prueba. Todas las inscripciones de una persona permanecen en el mismo conjunto. El escenario estudiado es predecir para personas no vistas dentro de las ofertas disponibles, no demostrar desempeño en instituciones u ofertas futuras.

**Un ajuste es un entrenamiento concreto.** Dentro del conjunto de ajuste, las personas se dividieron en cinco grupos. Para una configuración y un corte se entrenó con cuatro grupos y se validó con el restante. Se repitió cinco veces cambiando el grupo reservado: esta es la validación cruzada de cinco pliegues, o k-fold con k = 5. El preprocesamiento también aprende exclusivamente de los grupos de entrenamiento.

Una configuración define opciones del algoritmo, por ejemplo la profundidad de los árboles o el tamaño de una red. Se compararon ocho configuraciones de regresión logística y treinta de cada otra familia. Las treinta constituyen el presupuesto definido previamente para este estudio; no son un mínimo universal ni una búsqueda de todas las configuraciones posibles.

**Después de comparar:** se eligió la configuración de cada familia y la familia principal por corte mediante precisión promedio (AP) de validación, una medida que resume la precisión al recuperar distintos porcentajes de retiros. Se reajustó cada candidato con todo el conjunto de ajuste. Luego se calibraron sus puntuaciones para expresarlas como probabilidades y se eligió un umbral de alerta en otro conjunto. La calibración ajusta las probabilidades; el umbral convierte esas probabilidades en una decisión. La prueba quedó fuera de todas esas elecciones.

La prueba final estima el desempeño del paquete ya fijado. Los 2.000 remuestreos por personas permiten observar cuánto varían las métricas al cambiar las personas representadas, manteniendo juntas sus inscripciones. **No son 2.000 entrenamientos adicionales.** SHAP describe cómo las variables contribuyen a la predicción del modelo; no identifica causas del retiro.

<!-- PAGE -->
## 3. Cuánto tardó cada modelo y por qué
El número de ajustes proviene de combinar configuraciones, grupos de validación y cortes temporales:

**Regresión logística: 8 × 5 × 5 = 200 ajustes.**

**Cada otra familia: 30 × 5 × 5 = 750 ajustes.**

En total se realizaron **3.200 ajustes**. El contador de 3.000 corresponde a las cuatro familias pendientes cuando ya se había completado logística. A continuación se suma el campo de duración de cada ajuste guardado, sin contar dos veces los resultados reutilizados al reanudar.

| Familia | Ajustes | Tiempo acumulado (h:min:s) | Promedio por ajuste |
| --- | --- | --- | --- |
| Regresión logística | 200 | 00:00:40 | 0,20 s |
| Random Forest | 750 | 01:50:08 | 8,81 s |
| XGBoost | 750 | 00:06:51 | 0,55 s |
| LightGBM | 750 | 00:05:44 | 0,46 s |
| TabNet | 750 | 20:24:52 | 97,99 s |

**Total medido: 22:28:15 (h:min:s). TabNet concentra el 90,8 % de ese tiempo.** El promedio por ajuste sirve para entender la diferencia de duración, pero no expresa el desempeño predictivo: un modelo más lento no es necesariamente mejor.

Cada duración incluye el preprocesamiento y entrenamiento de ese pliegue, la predicción de validación, sus métricas y la escritura de sus predicciones. Es tiempo transcurrido medido por el programa, no tiempo puro de CPU. No incluye la carga inicial de bibliotecas y datos, los intentos interrumpidos sin registro final, los modelos de referencia, los reajustes posteriores, calibración, selección de umbral, evaluación reservada ni SHAP. **No existe una medición separada completa por familia de todas esas actividades adicionales.**

La espera se explica principalmente por repetir entrenamientos bajo condiciones comparables y por el costo observado de TabNet. En esta implementación, TabNet realiza cien o doscientas épocas, según la configuración: en cada entrenamiento recorre repetidamente los datos para actualizar sus parámetros. Se fijó ese presupuesto sin detención temprana para no usar el grupo de validación también como control de cuándo detener el aprendizaje. Las épocas ocurren dentro de cada ajuste; no se suman como ajustes independientes al contador.

El trabajo se ejecuta secuencialmente y cada ajuste usa hasta dos hilos de CPU. Además hubo interrupciones entre sesiones y demoras en la carga de bibliotecas cuya causa no se determinó. El 20 de octubre se corrigió una interrupción del supervisor causada por el límite de espera del contador; el entrenamiento permaneció activo. Por ello, **el tiempo de calendario desde el inicio hasta el cierre es mayor que la suma de la tabla** y no puede atribuirse íntegramente al aprendizaje de los modelos.

<!-- PAGE -->
## 4. El equipo utilizado y su relación con la espera
Las siguientes características se consultaron directamente en Windows el 21 de octubre. No se infieren a partir de una ficha comercial.

| Componente | Característica comprobada |
| --- | --- |
| Equipo | HP Pavilion Gaming Laptop 15-dk0xxx. |
| Procesador | Intel Core i5-9300H; cuatro núcleos y ocho procesadores lógicos; frecuencia nominal informada de 2,40 GHz. |
| Memoria | Aproximadamente 8 GB; Windows informa 7,84 GiB de memoria física visible. |
| Gráficos | NVIDIA GeForce GTX 1650 e Intel UHD Graphics 630. |
| Disco del proyecto | Unidad D: en disco mecánico HDD WDC WD10SPSX, de aproximadamente 1 TB. El equipo también dispone de un SSD de aproximadamente 128 GB. |
| Sistema | Windows 11 Home Single Language. |
| Ejecución utilizada | Python local, CPU, hasta dos hilos por ajuste y una búsqueda a la vez. TabNet se configuró expresamente en CPU; no utilizó la GTX 1650. |

**La configuración de ejecución sí influye:** no se ejecutaron varios ajustes simultáneos ni se utilizó la GPU para TabNet. Esto permite describir las condiciones reales de los tiempos observados. Sin embargo, tener ocho procesadores lógicos no significa que usar los ocho dividiría el tiempo entre cuatro: la ganancia depende del algoritmo y del trabajo que puede hacerse en paralelo.

La memoria disponible y el almacenamiento mecánico pueden influir en la carga y escritura de datos. En esta ejecución no se recogieron mediciones suficientes de paginación, saturación de disco, temperatura o frecuencia sostenida para cuantificar ese efecto. **No se ha demostrado que la RAM o el HDD hayan sido el cuello de botella**, ni puede calcularse un ahorro específico al cambiar de equipo.

El dato más sólido para explicar la espera es el tiempo registrado de TabNet: aproximadamente veinte horas y veinticinco minutos para sus 750 ajustes, frente a duraciones mucho menores en las otras familias. Esta comparación describe estas configuraciones, datos y equipo; no es una clasificación general de velocidad de los algoritmos.

Cambiar a GPU, aumentar el paralelismo o trasladar el proyecto a otro disco sería una decisión técnica para una ejecución futura, con pruebas de compatibilidad y nuevas mediciones. No se modificaron estas condiciones durante la comparación para acelerar selectivamente un candidato.

<!-- PAGE -->
## 5. Estado actual y trabajo que falta
La tabla distingue el cierre de cálculos de la terminación académica del proyecto. El estado corresponde al corte de verificación indicado en la primera página, no constituye una garantía de que permanezca igual hasta la reunión.

| Componente | Estado comprobado y pendiente |
| --- | --- |
| Comprensión y preparación de datos | Auditoría, exploración y 26 predictores disponibles. Continúan los límites sobre procedencia histórica, disponibilidad de notas y ratificación de precisiones del alcance. |
| Protocolo y particiones | Implementados y congelados; separación por persona y cinco cortes. No equivale a ratificación del asesor. |
| Búsqueda y selección | Completas y verificadas: 3.200 ajustes, 25 candidatos y una familia principal por corte. |
| Calibración y umbral | Comprobados para los 25 candidatos; modelos guardados y probabilidades reproducidas al recargarlos. |
| Prueba final | Evaluación completada para cinco cortes, predicciones guardadas e intervalos con 2.000 remuestreos por corte. Métricas e intervalos revisados desde salidas guardadas; falta discusión con el asesor. |
| Explicación SHAP | El cálculo SHAP terminó en los cinco cortes; sus salidas y patrones se revisaron; la discusión con el asesor está pendiente. El diseño usa el predictor calibrado, referencia de ajuste y hasta cien inscripciones de prueba por corte. |
| Documento | Resultados y límites integrados el 21 de octubre; revisión académica de los autores y el asesor pendiente. |
| Prototipo | Primera versión local implementada: métricas, calibración y explicaciones por corte. Evaluación con usuarios y cobertura completa de requisitos pendientes. |

**Selección realizada antes de la prueba:** XGBoost fue la familia principal en los días 7, 28, 42 y 56; Random Forest en el día 14. Los candidatos de las otras familias también se evaluaron para la comparación prevista. Estas decisiones provienen de validación interna, no de cambiar retrospectivamente el ganador al ver la prueba. Tampoco identifican por sí solas un día óptimo para alertar.

La prueba se abrió por primera vez el **21 de octubre a las 13:40**, después de verificar el paquete congelado. El cierre de evaluación corresponde al mismo paquete. Se comprobaron sus 56 archivos de salida contra las huellas registradas. El archivo histórico de progreso de entrenamiento puede conservar “prueba no abierta” porque fue escrito antes de esa apertura; para esta situación prevalecen el registro de apertura y el cierre de evaluación.

Se revisaron conjuntamente discriminación, calibración, errores, intervalos y anticipación, se interpretó SHAP y se integraron resultados en los capítulos. El siguiente trabajo es discutir las conclusiones con el asesor y evaluar el prototipo con sus usuarios previstos. No se presenta una reducción del abandono ni efectividad de intervenciones, que no han sido evaluadas. SVM quedó registrada únicamente como opción de exploración futura.

<!-- PAGE -->
## 6. Cómo presentarlo al asesor y qué acordar
**Síntesis para exponer en aproximadamente un minuto:**

Desde la entrega se concretó el protocolo de evaluación y se ejecutó la comparación de cinco familias de modelos en cinco momentos del curso. Se mantuvieron juntas las inscripciones de cada estudiante y se reservaron conjuntos distintos para calibrar, fijar las alertas y evaluar. Las búsquedas ya terminaron: fueron 3.200 entrenamientos, no 3.200 modelos finales. Se conservaron 25 candidatos y la evaluación reservada ya produjo predicciones e intervalos. La mayor parte del tiempo medido correspondió a TabNet, ejecutado en CPU. Las explicaciones ya se calcularon y revisaron; se integraron los resultados en la tesis y se preparó una primera versión local del prototipo. Quedan pendientes su evaluación con usuarios y la discusión académica de los hallazgos. La ejecución técnica no sustituye la revisión del alcance y del protocolo por parte del asesor.

**Acuerdos concretos que conviene buscar en la reunión:**

1. Confirmar si evaluar personas nuevas dentro de ofertas conocidas responde al alcance esperado. Por ejemplo, el diseño permite evaluar a otro estudiante de las ofertas disponibles, pero no demuestra todavía desempeño en un curso de un periodo futuro.
2. Revisar las precisiones frente al anteproyecto: retiro registrado futuro sin atribuir voluntariedad, inactividad complementaria y notas excluidas como predictores por falta de fecha verificable de disponibilidad. Se busca una ratificación explícita o una indicación concreta de ajuste, sin presentarla como ya obtenida.
3. Acordar el orden de entrega de resultados interpretados, capítulos actualizados y prototipo, con responsables y fechas. La terminación del entrenamiento no constituye una fecha de cierre del proyecto completo.

**Evidencias utilizadas y límites de este reporte**

La referencia de entrega procede de `reportes/redundancia_composicion_2026_10_19/revision.md`, que registra la comunicación de los autores; no se verificó el envío en correo o plataforma. El antecedente de pendientes está en `reportes/entrega_avance_2026_10_06/Revision_y_pendientes.md`. Las fechas y estados posteriores se contrastaron con el protocolo, los registros de ejecución y sus artefactos, no solamente con el resumen de estado.

Las duraciones proceden de los archivos `config_*_fold_*.json` de las carpetas de entrenamiento completo de logística y las cuatro familias restantes. Se comprobaron 3.200 combinaciones únicas de familia, corte, configuración y pliegue, todas registradas correctas. La auditoría integral de selección y la verificación de candidatos se conservan en `seleccion_validacion.json` y `paquete_evaluacion.json`; el cierre reservado está en `evaluacion/cierre.json`.

Esta carpeta conserva `hardware.json`, `evidencia.json`, `registros_tiempos.json` y los scripts de generación. El reporte es una fotografía fechada del avance y no sustituye la interpretación científica de métricas y explicaciones. La autoría del proyecto corresponde exclusivamente a Oriana Giraldo Arcia y Luis Javier Rubio Hernández.



<!-- PAGE -->
## 7. Hallazgos revisados para discutir en la reunión
La tabla resume los candidatos principales elegidos antes de observar la prueba. AP describe la ordenación de casos a distintos niveles de recuperación de retiros; precisión y sensibilidad corresponden al umbral congelado de cada candidato.

| Día | Principal | AP e intervalo del 95 % | Precisión | Sensibilidad |
| --- | --- | --- | --- | --- |
| 7 | XGBoost | 0,283 [0,264; 0,303] | 25,9 % | 72,6 % |
| 14 | Random Forest | 0,233 [0,216; 0,251] | 22,9 % | 69,5 % |
| 28 | XGBoost | 0,286 [0,261; 0,314] | 29,9 % | 35,7 % |
| 42 | XGBoost | 0,272 [0,247; 0,299] | 22,2 % | 68,8 % |
| 56 | XGBoost | 0,255 [0,232; 0,285] | 25,5 % | 44,0 % |

**Hay señal predictiva, pero también límites importantes.** La AP de los principales supera la referencia constante en los cinco cortes; los intervalos pareados de la diferencia quedaron por encima de cero. No obstante, los intervalos de la diferencia de AP entre principal y logística incluyen cero en los cinco cortes. No corresponde afirmar una superioridad concluyente de los principales sobre logística, ni equivalencia entre modelos.

**Las falsas alertas requieren atención.** Al día 7 se detectan 964 de 1.327 retiros posteriores y se generan 2.756 falsas alertas; se alertaría sobre el 64,0 % de las inscripciones. Al día 28 se detectan 358 retiros, se omiten 645 y se generan 841 falsas alertas; se alertaría sobre el 21,8 %. Detectar más retiros y concentrar mejor las alertas son objetivos distintos. El criterio F1 usado para comparar no reemplaza una política institucional de atención.

**La probabilidad no equivale a certeza.** Los principales tienen menor Brier que la referencia constante, pero la diferencia es pequeña. No se demuestra calibración perfecta, utilidad educativa ni mejora atribuible exclusivamente a calibrar. Las medianas de anticipación, de 61,5 a 88 días, describen únicamente alertas correctas; no prueban que una intervención hubiera evitado esos retiros.

**SHAP describe el modelo, no las causas.** En el primer corte destacan los clics recientes; desde el día 28 domina la proporción entregada de evaluaciones con vencimiento hasta el corte. Las contribuciones dependen de la referencia y de indicadores relacionados. Se verificaron 500 explicaciones, pero no su estabilidad ante otras muestras. Las cinco poblaciones y sus horizontes cambian, por lo que no se propone un día óptimo comparando solamente AP.

La revisión reprodujo las métricas desde las predicciones, verificó 56 huellas de salidas, recalculó los percentiles desde las réplicas guardadas y comprobó las sumas SHAP. No repitió entrenamientos ni utilizó la prueba para cambiar los candidatos. El prototipo muestra estas mismas cifras y permite consultar casos sin identificadores de estudiantes; sus pruebas funcionales no sustituyen una evaluación con usuarios.
