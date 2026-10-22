# Avance de la etapa de modelado

Reunión de seguimiento con el asesor · 22 de octubre de 2026

Oriana Giraldo Arcia y Luis Javier Rubio Hernández · PUJ Cali

## 1. Qué se ha avanzado

Después de la entrega anterior, el proyecto avanzó a la etapa de modelado. Se trabajó con regresión logística, Random Forest, XGBoost, LightGBM y TabNet para predecir el retiro registrado después de distintos momentos del curso. Las ejecuciones ya produjeron resultados y se avanzó en su incorporación al documento; actualmente se está revisando su interpretación y consolidando la redacción. En esta reunión se presenta el procedimiento y el avance, sin anticipar conclusiones que los autores aún no han revisado suficientemente.

## 2. Qué información se utiliza para predecir

Se utilizan indicadores de actividad y entregas disponibles hasta los días 7, 14, 28, 42 y 56, con un modelo separado para cada corte. Se incluyen únicamente las inscripciones que siguen vigentes en ese momento. Se excluyen datos que revelarían lo ocurrido después, como el resultado final o la fecha futura de retiro. Las calificaciones no se usan como predictores porque su disponibilidad al momento de predecir no está acreditada.

> Ejemplo hipotético. Para predecir al día 14, pueden utilizarse los clics y entregas registrados hasta ese día. Si una inscripción se retira el día 35, ese retiro sirve después para comprobar la predicción, pero no puede usarse como información de entrada. Una inscripción retirada el día 10 ya no pertenece a la población que se intenta alertar al día 14.

## 3. Cómo se separaron los datos

La separación se realizó por estudiante, manteniendo juntas todas sus inscripciones. Se destinaron aproximadamente el 60 % de los datos al ajuste y selección, el 10 % a calibrar probabilidades, el 10 % a definir el umbral de alerta y el 20 % a la prueba final. Las proporciones no son exactas porque se conservan los grupos de personas. La evaluación busca representar personas nuevas dentro de las ofertas de módulos disponibles, no cursos futuros ni otras instituciones.

> Ejemplo hipotético. Si una estudiante tiene una inscripción en un módulo y otra en un módulo diferente, ambas quedan en el mismo conjunto. No se utiliza una para entrenar y la otra para evaluar como si correspondiera a una persona desconocida. Así se evita que la comparación aproveche información de alguien que ya apareció en el ajuste.

# Cómo se evalúa y cuál es el siguiente paso

## 4. Cómo se compararon las alternativas

Dentro del conjunto de ajuste se utilizó validación cruzada de cinco pliegues: se entrenó en cuatro partes y se validó en la restante, repitiendo el procedimiento hasta usar cada parte una vez para validar. Los modelos compartieron las mismas particiones por estudiante. La preparación de los datos se aprendió dentro de cada entrenamiento y la selección se basó en la precisión promedio (AP), que resume la precisión al detectar progresivamente más retiros.

> Ejemplo hipotético. Se distribuyen las personas del conjunto de ajuste en los grupos A, B, C, D y E. En la primera ronda se aprende con B, C, D y E y se comprueba con A; en la segunda, se aprende sin B y se comprueba con B. Se continúa de la misma manera. Estas cinco rondas sirven para elegir la configuración; no son cinco evaluaciones de la prueba final.

Después de la selección, se reajustó el modelo con todo el conjunto de ajuste. La calibración buscó que las probabilidades se correspondieran mejor con las frecuencias observadas. En otro conjunto se eligió el umbral que convierte la probabilidad en alerta, mediante el criterio F1. Solo después de congelar esas decisiones se utilizó la prueba final. Los resultados de esa prueba no se emplearon para volver a elegir el modelo.

> Ejemplo hipotético. En un grupo de inscripciones con probabilidad estimada cercana al 20 %, se esperaría observar una frecuencia de retiro próxima al 20 %. Esto no permite asegurar qué inscripción se retirará. El umbral decide cuándo emitir una alerta; bajarlo puede detectar más retiros y también producir más falsas alertas. Los valores de este ejemplo no son resultados del proyecto.

## 5. Qué se espera establecer con los resultados

Se busca determinar qué capacidad tienen los modelos para detectar retiros futuros, cuántas falsas alertas y retiros no detectados producen, y qué indicadores contribuyen a sus predicciones. La revisión explicará conjuntamente estos resultados; no se reducirá a señalar un porcentaje de aciertos ni se afirmará que el modelo evita el abandono.

## 6. Propuesta para el próximo encuentro, en dos semanas

Se propone presentar la sección de modelado consolidada y revisada por los autores: decisiones metodológicas, comparación de modelos, explicación de las métricas y matrices de confusión, y conclusiones sobre los resultados y los límites de la evaluación. También se precisará qué validación ya se realizó y qué comprobaciones adicionales serían pertinentes. Esta es una meta de preparación para el próximo encuentro, no una aprobación académica ni un compromiso de obtener mejores cifras.

Consulta al asesor: ¿Considera adecuado este enfoque de entrenamiento y evaluación, o hay algún aspecto que deba precisarse antes de consolidar la presentación de resultados?
