# Decisiones y resultados del modelado

Reunión con el asesor · 22 de octubre de 2026. Evidencia disponible al 21 de octubre. Oriana Giraldo Arcia y Luis Javier Rubio Hernández · PUJ Cali.

## Qué se completó después de la entrega

Se completaron las búsquedas de cinco familias, la selección por validación, el reajuste, la calibración, la elección de umbrales y la prueba final congelada. Se realizaron 3.200 ajustes de validación cruzada. Este informe concentra las decisiones y resultados; no acredita aprobación académica ni utilidad institucional.

## Qué se decidió y por qué

| Decisión ejecutada | Propósito y alcance |
| --- | --- |
| Evento y población | Predecir el retiro registrado después del corte y hasta el cierre de la oferta del módulo. Solo inscripciones vigentes en ese corte; no se atribuye motivo ni voluntariedad. Una persona puede tener varias inscripciones. |
| Cinco momentos | Modelos separados en días 7, 14, 28, 42 y 56; actividad de 0 al corte, ambos incluidos. Cambian población y horizonte: comparar AP no determina por sí solo el día óptimo. |
| Separación por personas | Aproximadamente 60 % ajuste, 10 % calibración, 10 % umbral y 20 % prueba. Todas las inscripciones de una persona permanecen juntas. Objetivo: personas nuevas en las ofertas disponibles. |
| Cinco pliegues (k-fold) | En el conjunto de ajuste, entrenar en cuatro partes y validar en la restante, cinco veces. Se conservan los mismos pliegues por personas para todas las familias; no son cinco pruebas finales. |
| 26 predictores | Indicadores académicos de entregas, actividad y temporalidad. Se excluyeron identificadores, resultado final, fechas de retiro y notas sin disponibilidad temporal acreditada; contexto demográfico no incluido. |
| Preparación dentro del pliegue | Retirar columnas enteramente ausentes y constantes según entrenamiento; imputar medianas con indicadores de ausencia. Escalar logística y TabNet. Así la parte validada no enseña su distribución al modelo. |
| Comparación predefinida | 8 configuraciones de logística y 30 por cada otra familia, en cada corte. Se exploró ponderación de clases; sin sobremuestreo sintético. Árboles/épocas fijos y sin detención temprana. |
| Selección y decisiones finales | Mayor AP media interna; después reajuste con todo el ajuste, calibración sigmoidal exclusiva y umbral que maximiza F1 en su conjunto exclusivo. Alerta si probabilidad > umbral; no se impuso 0,5. |
| Reserva de prueba | Se congelaron modelos, calibradores, umbrales y evaluación antes de abrir la prueba. No se sustituyó al principal por el mejor valor de prueba. Primera apertura registrada: 21 de octubre. |

Calibrar busca que las probabilidades concuerden con las frecuencias observadas: entre casos con probabilidad cercana al 20 %, se esperaría una frecuencia de retiro próxima al 20 %. No garantiza acertar cada caso. El umbral convierte esa probabilidad en alerta; bajarlo puede detectar más retiros y producir más falsas alertas.

Semillas conservadas: partición 20261019; validación 20261020; búsqueda 20261021; remuestreo 20261022. Las precisiones metodológicas se presentan al asesor para revisión; no se presume su ratificación.

# Resultados de la búsqueda y la selección

Entrenar es ajustar el modelo. Validar es medirlo en personas excluidas de ese ajuste. La tabla siguiente muestra la AP media de los cinco pliegues para la mejor configuración de cada familia; sirvió para seleccionar, por lo que no es una evaluación independiente del ganador.

| Día | Logística | Random Forest | LightGBM | XGBoost | TabNet |
| --- | --- | --- | --- | --- | --- |
| 7 | 0,2907 | 0,2908 | 0,2903 | 0,2919 | 0,2888 |
| 14 | 0,2457 | 0,2474 | 0,2448 | 0,2463 | 0,2467 |
| 28 | 0,2863 | 0,2897 | 0,2908 | 0,2916 | 0,2855 |
| 42 | 0,2663 | 0,2709 | 0,2686 | 0,2722 | 0,2625 |
| 56 | 0,2532 | 0,2628 | 0,2636 | 0,2644 | 0,2628 |

Principal seleccionado: XGBoost en días 7, 28, 42 y 56; Random Forest en día 14. Las diferencias internas son pequeñas y la regla de selección no prueba superioridad estadística. Empate a seis decimales: logística, Random Forest, LightGBM, XGBoost y TabNet; dentro de familia, orden congelado.

## Configuraciones principales conservadas

| Corte / familia | Configuración seleccionada |
| --- | --- |
| 7 / XGBoost | 200 árboles; profundidad 2; tasa de aprendizaje 0,03; fracción de filas 1,0 y de variables por árbol 0,8; regularización L2 = 1; pesos balanceados. |
| 14 / Random Forest | 600 árboles; profundidad sin límite explícito; mínimo 30 inscripciones por hoja; raíz cuadrada del número de variables en cada división; pesos balanceados. |
| 28, 42 y 56 / XGBoost | 200 árboles; profundidad 2; tasa 0,03; fracción de filas 0,8 y de variables 0,8; regularización L2 = 1; sin ponderación. |

## AP en prueba final: comparación posterior, sin nueva selección

| Día | Logística | Random Forest | LightGBM | XGBoost | TabNet |
| --- | --- | --- | --- | --- | --- |
| 7 | 0,2782 | 0,2807 | 0,2826 | 0,2827 | 0,2753 |
| 14 | 0,2321 | 0,2327 | 0,2337 | 0,2369 | 0,2349 |
| 28 | 0,2796 | 0,2844 | 0,2895 | 0,2862 | 0,2638 |
| 42 | 0,2689 | 0,2718 | 0,2745 | 0,2720 | 0,2574 |
| 56 | 0,2437 | 0,2618 | 0,2604 | 0,2551 | 0,2477 |

AP resume la precisión al recuperar progresivamente más retiros; no equivale al porcentaje de aciertos. Las páginas 4 a 8 explican todos los resultados del principal de cada corte. El archivo CSV adjunto conserva las demás métricas de las cinco familias y dos referencias en los cinco cortes.

# Cómo leer las métricas y la matriz

La clase positiva es retiro futuro. La predicción positiva es una alerta al superar el umbral. “Negativo” significa ausencia de alerta o de retiro, según el eje; no significa una valoración del estudiante. Las métricas cuentan inscripciones, no personas únicas.

| Real / predicho | Alerta | Sin alerta |
| --- | --- | --- |
| Retiro posterior | VP: verdadero positivo. Retiro detectado. | FN: falso negativo. Retiro que no se detectó. |
| Sin retiro posterior | FP: falso positivo. Falsa alerta. | VN: verdadero negativo. Ausencia de retiro correctamente clasificada. |

Se leen filas por desenlace real y columnas por decisión del modelo. N = VP + FP + FN + VN. Las matrices siguientes conservan ese orden; la diagonal correcta es VP y VN.

| Medida y cálculo | Qué indica y qué no indica |
| --- | --- |
| Accuracy / exactitud; (VP + VN) / N | Fracción total de clasificaciones correctas. Puede ser alta por acertar la clase mayoritaria sin detectar retiros. No equivale a precisión. |
| Precisión; VP / (VP + FP) | De las alertas, qué proporción corresponde a retiros. El complemento es la proporción de falsas alertas entre alertas, no la tasa FP/(FP+VN). |
| Recall / sensibilidad; VP / (VP + FN) | De los retiros que ocurrieron, qué proporción se detectó. No informa cuántas falsas alertas se produjeron. |
| Especificidad; VN / (VN + FP) | De las inscripciones sin retiro, qué proporción quedó sin alerta. Su complemento es la tasa de falsos positivos. |
| F1; 2VP / (2VP + FP + FN) | Media armónica de precisión y sensibilidad. Va de 0 a 1; mayor es mejor bajo este criterio. No es porcentaje de aciertos y no considera VN. Depende del umbral. |
| AP / precisión promedio | Resume precisión a lo largo de cambios de sensibilidad al variar el umbral; pondera por incrementos de sensibilidad. Mayor es mejor, con la prevalencia como referencia constante. No es área trapezoidal ni precisión al umbral elegido. |
| ROC-AUC | Capacidad de ordenar mayor riesgo a un retiro que a un no retiro (empates aportan la mitad). 0,5 indica ausencia de discriminación; 1, orden perfecto. No es accuracy. |
| Brier; Promedio de (probabilidad - desenlace)² | Error cuadrático de las probabilidades frente a desenlaces 0/1. En este problema va de 0 a 1; menor es mejor. No se lee como porcentaje de error y no mide solo calibración. |
| Proporción de alertas; (VP + FP) / N | Fracción que recibiría alerta con la regla congelada. Describe volumen potencial de atención, no eficacia educativa. |
| Anticipación mediana | Tiempo desde el corte hasta el retiro entre VP. La mitad tiene tiempos iguales o menores y la otra mitad iguales o mayores. No representa a los FN ni demuestra que una intervención funcione. |

Accuracy, precisión, sensibilidad, especificidad y F1 usan la matriz y el umbral. AP, ROC-AUC y Brier usan las probabilidades. Fuentes técnicas: documentación oficial de scikit-learn 1.8; referencias al final.

# Día 7: XGBoost en prueba final

5.815 inscripciones de 5.211 personas; 1.327 retiros posteriores (22,8 %). Alerta cuando p > 0,205683 (aproximadamente 20,6 %). El umbral se eligió antes de observar esta prueba.

| Desenlace real / decisión | Alerta | Sin alerta | Total real |
| --- | --- | --- | --- |
| Retiro posterior | VP = 964; Retiros detectados | FN = 363; Retiros no detectados | 1.327 |
| Sin retiro posterior | FP = 2.756; Falsas alertas | VN = 1.732; Sin retiro y sin alerta | 4.488 |
| Total predicho | 3.720 | 2.095 | 5.815 |

Lectura de la matriz: de 3.720 alertas, 964 correspondieron a retiros y 2.756 no. De 1.327 retiros reales, 363 quedaron sin alerta.

| Métrica | Resultado | Interpretación aplicada |
| --- | --- | --- |
| Accuracy | 46,4 % | 2.696 de 5.815 inscripciones se clasificaron correctamente. |
| Precisión | 25,9 % | 964 / 3.720 alertas fueron correctas; 74,1 % de las alertas fueron falsas. |
| Sensibilidad | 72,6 % | 964 / 1.327 retiros se detectaron; se omitió el 27,4 %. |
| Especificidad | 38,6 % | 1.732 / 4.488 inscripciones sin retiro quedaron sin alerta; 61,4 % recibió falsa alerta. |
| F1 | 0,382 | 2 × 964 / (2 × 964 + 2.756 + 363). Resume conjuntamente precisión y sensibilidad; no significa 38,2 % de aciertos. |
| AP | 0,283 | Frente a 0,228 de la referencia constante. IC 95 %: [0,264; 0,303]. Resume la ordenación al variar el umbral, no el porcentaje de alertas correctas. |
| ROC-AUC | 0,590 | Equivale a 59,0 % de concordancia al comparar pares retiro/no retiro, contando medio acierto en empates. Discriminación limitada; no es exactitud. |
| Brier | 0,1730 | Error probabilístico menor que la referencia constante (0,1761). No significa 17,3 % de predicciones equivocadas. |
| Alertas | 64,0 % | 3.720 / 5.815 inscripciones superaron el umbral; este sería el volumen de alertas de la regla evaluada. |
| Anticipación | 61,5 días | Mediana entre los 964 retiros detectados; el 50 % central está entre 18,0 y 135,2 días. |

Control de lectura: predecir “sin retiro” para todos obtendría 77,2 % de accuracy y 0 % de sensibilidad. Por ello, la exactitud aislada no responde al objetivo de detectar retiros. Se reportan ambas consecuencias, sin ocultar los errores del modelo.

# Día 14: Random Forest en prueba final

5.610 inscripciones de 5.048 personas; 1.116 retiros posteriores (19,9 %). Alerta cuando p > 0,188291 (aproximadamente 18,8 %). El umbral se eligió antes de observar esta prueba.

| Desenlace real / decisión | Alerta | Sin alerta | Total real |
| --- | --- | --- | --- |
| Retiro posterior | VP = 776; Retiros detectados | FN = 340; Retiros no detectados | 1.116 |
| Sin retiro posterior | FP = 2.615; Falsas alertas | VN = 1.879; Sin retiro y sin alerta | 4.494 |
| Total predicho | 3.391 | 2.219 | 5.610 |

Lectura de la matriz: de 3.391 alertas, 776 correspondieron a retiros y 2.615 no. De 1.116 retiros reales, 340 quedaron sin alerta.

| Métrica | Resultado | Interpretación aplicada |
| --- | --- | --- |
| Accuracy | 47,3 % | 2.655 de 5.610 inscripciones se clasificaron correctamente. |
| Precisión | 22,9 % | 776 / 3.391 alertas fueron correctas; 77,1 % de las alertas fueron falsas. |
| Sensibilidad | 69,5 % | 776 / 1.116 retiros se detectaron; se omitió el 30,5 %. |
| Especificidad | 41,8 % | 1.879 / 4.494 inscripciones sin retiro quedaron sin alerta; 58,2 % recibió falsa alerta. |
| F1 | 0,344 | 2 × 776 / (2 × 776 + 2.615 + 340). Resume conjuntamente precisión y sensibilidad; no significa 34,4 % de aciertos. |
| AP | 0,233 | Frente a 0,199 de la referencia constante. IC 95 %: [0,216; 0,251]. Resume la ordenación al variar el umbral, no el porcentaje de alertas correctas. |
| ROC-AUC | 0,570 | Equivale a 57,0 % de concordancia al comparar pares retiro/no retiro, contando medio acierto en empates. Discriminación limitada; no es exactitud. |
| Brier | 0,1579 | Error probabilístico menor que la referencia constante (0,1594). No significa 15,8 % de predicciones equivocadas. |
| Alertas | 60,4 % | 3.391 / 5.610 inscripciones superaron el umbral; este sería el volumen de alertas de la regla evaluada. |
| Anticipación | 88,0 días | Mediana entre los 776 retiros detectados; el 50 % central está entre 34,0 y 144,0 días. |

Control de lectura: predecir “sin retiro” para todos obtendría 80,1 % de accuracy y 0 % de sensibilidad. Por ello, la exactitud aislada no responde al objetivo de detectar retiros. Se reportan ambas consecuencias, sin ocultar los errores del modelo.

# Día 28: XGBoost en prueba final

5.503 inscripciones de 4.968 personas; 1.003 retiros posteriores (18,2 %). Alerta cuando p > 0,201206 (aproximadamente 20,1 %). El umbral se eligió antes de observar esta prueba.

| Desenlace real / decisión | Alerta | Sin alerta | Total real |
| --- | --- | --- | --- |
| Retiro posterior | VP = 358; Retiros detectados | FN = 645; Retiros no detectados | 1.003 |
| Sin retiro posterior | FP = 841; Falsas alertas | VN = 3.659; Sin retiro y sin alerta | 4.500 |
| Total predicho | 1.199 | 4.304 | 5.503 |

Lectura de la matriz: de 1.199 alertas, 358 correspondieron a retiros y 841 no. De 1.003 retiros reales, 645 quedaron sin alerta.

| Métrica | Resultado | Interpretación aplicada |
| --- | --- | --- |
| Accuracy | 73,0 % | 4.017 de 5.503 inscripciones se clasificaron correctamente. |
| Precisión | 29,9 % | 358 / 1.199 alertas fueron correctas; 70,1 % de las alertas fueron falsas. |
| Sensibilidad | 35,7 % | 358 / 1.003 retiros se detectaron; se omitió el 64,3 %. |
| Especificidad | 81,3 % | 3.659 / 4.500 inscripciones sin retiro quedaron sin alerta; 18,7 % recibió falsa alerta. |
| F1 | 0,325 | 2 × 358 / (2 × 358 + 841 + 645). Resume conjuntamente precisión y sensibilidad; no significa 32,5 % de aciertos. |
| AP | 0,286 | Frente a 0,182 de la referencia constante. IC 95 %: [0,261; 0,314]. Resume la ordenación al variar el umbral, no el porcentaje de alertas correctas. |
| ROC-AUC | 0,634 | Equivale a 63,4 % de concordancia al comparar pares retiro/no retiro, contando medio acierto en empates. Discriminación limitada; no es exactitud. |
| Brier | 0,1432 | Error probabilístico menor que la referencia constante (0,1490). No significa 14,3 % de predicciones equivocadas. |
| Alertas | 21,8 % | 1.199 / 5.503 inscripciones superaron el umbral; este sería el volumen de alertas de la regla evaluada. |
| Anticipación | 76,0 días | Mediana entre los 358 retiros detectados; el 50 % central está entre 25,0 y 136,8 días. |

Control de lectura: predecir “sin retiro” para todos obtendría 81,8 % de accuracy y 0 % de sensibilidad. Por ello, la exactitud aislada no responde al objetivo de detectar retiros. Se reportan ambas consecuencias, sin ocultar los errores del modelo.

# Día 42: XGBoost en prueba final

5.400 inscripciones de 4.901 personas; 898 retiros posteriores (16,6 %). Alerta cuando p > 0,144768 (aproximadamente 14,5 %). El umbral se eligió antes de observar esta prueba.

| Desenlace real / decisión | Alerta | Sin alerta | Total real |
| --- | --- | --- | --- |
| Retiro posterior | VP = 618; Retiros detectados | FN = 280; Retiros no detectados | 898 |
| Sin retiro posterior | FP = 2.163; Falsas alertas | VN = 2.339; Sin retiro y sin alerta | 4.502 |
| Total predicho | 2.781 | 2.619 | 5.400 |

Lectura de la matriz: de 2.781 alertas, 618 correspondieron a retiros y 2.163 no. De 898 retiros reales, 280 quedaron sin alerta.

| Métrica | Resultado | Interpretación aplicada |
| --- | --- | --- |
| Accuracy | 54,8 % | 2.957 de 5.400 inscripciones se clasificaron correctamente. |
| Precisión | 22,2 % | 618 / 2.781 alertas fueron correctas; 77,8 % de las alertas fueron falsas. |
| Sensibilidad | 68,8 % | 618 / 898 retiros se detectaron; se omitió el 31,2 %. |
| Especificidad | 52,0 % | 2.339 / 4.502 inscripciones sin retiro quedaron sin alerta; 48,0 % recibió falsa alerta. |
| F1 | 0,336 | 2 × 618 / (2 × 618 + 2.163 + 280). Resume conjuntamente precisión y sensibilidad; no significa 33,6 % de aciertos. |
| AP | 0,272 | Frente a 0,166 de la referencia constante. IC 95 %: [0,247; 0,299]. Resume la ordenación al variar el umbral, no el porcentaje de alertas correctas. |
| ROC-AUC | 0,649 | Equivale a 64,9 % de concordancia al comparar pares retiro/no retiro, contando medio acierto en empates. Discriminación limitada; no es exactitud. |
| Brier | 0,1329 | Error probabilístico menor que la referencia constante (0,1386). No significa 13,3 % de predicciones equivocadas. |
| Alertas | 51,5 % | 2.781 / 5.400 inscripciones superaron el umbral; este sería el volumen de alertas de la regla evaluada. |
| Anticipación | 74,0 días | Mediana entre los 618 retiros detectados; el 50 % central está entre 30,0 y 125,0 días. |

Control de lectura: predecir “sin retiro” para todos obtendría 83,4 % de accuracy y 0 % de sensibilidad. Por ello, la exactitud aislada no responde al objetivo de detectar retiros. Se reportan ambas consecuencias, sin ocultar los errores del modelo.

# Día 56: XGBoost en prueba final

5.302 inscripciones de 4.824 personas; 800 retiros posteriores (15,1 %). Alerta cuando p > 0,165440 (aproximadamente 16,5 %). El umbral se eligió antes de observar esta prueba.

| Desenlace real / decisión | Alerta | Sin alerta | Total real |
| --- | --- | --- | --- |
| Retiro posterior | VP = 352; Retiros detectados | FN = 448; Retiros no detectados | 800 |
| Sin retiro posterior | FP = 1.029; Falsas alertas | VN = 3.473; Sin retiro y sin alerta | 4.502 |
| Total predicho | 1.381 | 3.921 | 5.302 |

Lectura de la matriz: de 1.381 alertas, 352 correspondieron a retiros y 1.029 no. De 800 retiros reales, 448 quedaron sin alerta.

| Métrica | Resultado | Interpretación aplicada |
| --- | --- | --- |
| Accuracy | 72,1 % | 3.825 de 5.302 inscripciones se clasificaron correctamente. |
| Precisión | 25,5 % | 352 / 1.381 alertas fueron correctas; 74,5 % de las alertas fueron falsas. |
| Sensibilidad | 44,0 % | 352 / 800 retiros se detectaron; se omitió el 56,0 %. |
| Especificidad | 77,1 % | 3.473 / 4.502 inscripciones sin retiro quedaron sin alerta; 22,9 % recibió falsa alerta. |
| F1 | 0,323 | 2 × 352 / (2 × 352 + 1.029 + 448). Resume conjuntamente precisión y sensibilidad; no significa 32,3 % de aciertos. |
| AP | 0,255 | Frente a 0,151 de la referencia constante. IC 95 %: [0,232; 0,285]. Resume la ordenación al variar el umbral, no el porcentaje de alertas correctas. |
| ROC-AUC | 0,667 | Equivale a 66,7 % de concordancia al comparar pares retiro/no retiro, contando medio acierto en empates. Discriminación limitada; no es exactitud. |
| Brier | 0,1225 | Error probabilístico menor que la referencia constante (0,1281). No significa 12,3 % de predicciones equivocadas. |
| Alertas | 26,0 % | 1.381 / 5.302 inscripciones superaron el umbral; este sería el volumen de alertas de la regla evaluada. |
| Anticipación | 69,0 días | Mediana entre los 352 retiros detectados; el 50 % central está entre 23,0 y 114,0 días. |

Control de lectura: predecir “sin retiro” para todos obtendría 84,9 % de accuracy y 0 % de sensibilidad. Por ello, la exactitud aislada no responde al objetivo de detectar retiros. Se reportan ambas consecuencias, sin ocultar los errores del modelo.

# Qué comunicar al asesor y qué queda por discutir

## Resultado central

El protocolo completo ya se ejecutó. Los modelos principales superan la referencia constante en AP, pero la discriminación es limitada y se producen numerosas falsas alertas. La selección interna eligió XGBoost en cuatro cortes y Random Forest en uno; eso no permite afirmar que superen concluyentemente a logística en prueba.

Los intervalos pareados de diferencia de AP entre principal y logística incluyen cero en los cinco cortes. Esto no demuestra equivalencia. Los intervalos se obtuvieron con 2.000 remuestreos de personas, manteniendo sus inscripciones juntas; describen incertidumbre condicional a modelos y ofertas observados, no toda la variación del entrenamiento ni de futuras ofertas.

## Por qué tomó tiempo

Cada configuración se ajustó cinco veces por corte: logística 8 × 5 × 5 = 200; cada otra familia 30 × 5 × 5 = 750. Total: 3.200 ajustes. Un ajuste aprende parámetros; una configuración especifica, por ejemplo, profundidad o número de árboles. TabNet repite el aprendizaje durante 100 o 200 épocas por ajuste.

| Familia | Ajustes CV | Suma de tiempos (hh:mm:ss) |
| --- | --- | --- |
| Logística | 200 | 00:00:40 |
| Random Forest | 750 | 01:50:08 |
| XGBoost | 750 | 00:06:51 |
| LightGBM | 750 | 00:05:44 |
| TabNet | 750 | 20:24:52 |

Son sumas de tiempos registrados de ajustes CV terminados, incluyendo preparación, predicción, métricas y escritura de cada ajuste; no son la duración total del proyecto. Excluyen arranque, interrupciones sin marcador, reajustes finales, calibración, prueba y SHAP. Equipo registrado: Core i5-9300H, 4 núcleos/8 hilos, aproximadamente 8 GB de RAM; entrenamiento en CPU, máximo dos hilos, sin búsquedas concurrentes. La GPU no se utilizó; no se demostró un cuello de botella específico de memoria o disco.

## Discusión propuesta para la reunión

Revisar las decisiones de agrupación por personas y alcance temporal; discutir el compromiso entre retiros detectados y falsas alertas; confirmar cómo presentar las limitaciones. Maximizar F1 fue una regla académica predefinida, no una política institucional: no se conocen costos de error ni capacidad de atención. No corresponde volver a escoger modelos o umbrales mirando esta prueba.

## Fuentes y trazabilidad

Resultados: seleccion_validacion.json; paquete_evaluacion.json; evaluación/metricas.json; sintesis.json y metricas_todas.csv del cierre del 21 de octubre. Las matrices y seis métricas derivadas se recalcularon desde sus conteos para este informe; no se repitieron entrenamientos. CSV complementario: metricas_completas_reunion.csv.

Scikit-learn developers (2025-2026), documentación 1.8: <link href="https://scikit-learn.org/1.8/modules/model_evaluation.html" color="#2C5697">Metrics and scoring</link>; <link href="https://scikit-learn.org/1.8/modules/generated/sklearn.metrics.confusion_matrix.html" color="#2C5697">confusion_matrix</link>; <link href="https://scikit-learn.org/1.8/modules/generated/sklearn.metrics.f1_score.html" color="#2C5697">f1_score</link>; <link href="https://scikit-learn.org/1.8/modules/generated/sklearn.metrics.average_precision_score.html" color="#2C5697">average_precision_score</link>; <link href="https://scikit-learn.org/1.8/modules/generated/sklearn.metrics.brier_score_loss.html" color="#2C5697">brier_score_loss</link>. Consulta: 21 de octubre de 2026.
