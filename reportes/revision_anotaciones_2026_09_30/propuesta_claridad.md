# Revisión inicial de anotaciones y muestra de reescritura

Versión: 1. Fecha: 30 de septiembre de 2026. Estado: propuesta editorial; no integrada al documento principal.

## Alcance y veredicto

Se revisó visualmente el PDF «Kami Export - proyecto.pdf», de 18 páginas, con anotaciones sobre fragmentos de los capítulos 3 y 4. Se consultaron el modelo de estilo «planteamiento del problema.txt», el archivo `Plantilla_ProyAplicado/desarrollo1.tex`, la celda de comprobaciones de rangos del notebook `01_carga_exploracion.ipynb`, las funciones pertinentes de `src/ventanas_oulad.py` y las tablas guardadas de la revisión del 10 de septiembre de 2026. No se ejecutaron nuevamente los notebooks ni se recalcularon los resultados desde los datos originales.

El texto requiere una revisión de claridad que explique los conceptos antes de emplearlos, desarrolle el propósito de los procedimientos y acompañe los resultados con una interpretación comprensible. Las anotaciones muestran dificultades de vocabulario, secuencia de explicación, notación y presentación visual. Estos problemas de exposición no demuestran, por sí solos, que los procedimientos sean incorrectos.

Las notas del PDF se consideran observaciones para analizar, no instrucciones que autoricen automáticamente cambios metodológicos. La siguiente matriz agrupa los asuntos identificados; no es una transcripción literal exhaustiva de cada trazo manuscrito. Las páginas corresponden a la numeración impresa del proyecto. La página 13 del archivo recibido contiene una anotación general sin texto del proyecto y requiere confirmar a qué apartado se refiere.

## Matriz inicial de observaciones

| ID | Ubicación | Severidad | Evidencia y dificultad | Corrección propuesta | Evidencia necesaria para cerrar |
|---|---|---|---|---|---|
| C01 | p. 19, sección 3.1 | Menor | Se señala la referencia a la fecha de ejecución y al notebook dentro de la explicación inicial. | Explicar primero el propósito de la revisión y ubicar los datos de ejecución en una nota breve de reproducibilidad. | Texto revisado con trazabilidad conservada. |
| C02 | p. 20, sección 3.2 | Mayor | La nota pide ilustrar cómo se relacionan las tablas. | Añadir un ejemplo de una inscripción que reúne matrícula, entregas e interacciones, definiendo previamente módulo y presentación. | Ejemplo coherente con las claves utilizadas en el código. |
| C03 | pp. 20–21, sección 3.3 | Mayor | Se cuestionan «Exactos adicionales», «Sin exactos» y la explicación de la sensibilidad del volumen. | Distinguir una fila idéntica de una coincidencia de identificadores. Explicar qué cambia al retirar duplicados exactos y qué no permite concluir esa comparación. | Encabezados comprensibles y descripción contrastada con el cálculo. |
| C04 | p. 21, sección 3.4 | Mayor | Se pide un ejemplo y se pregunta por la «bandera de reconocimiento» y la «revisión de pesos». | Definir los campos y desarrollar ejemplos antes de presentar sus comprobaciones. | Muestra incluida abajo; pendiente de integración. |
| C05 | p. 22, sección 3.4 | Mayor | Se cuestionan el uso del día 28, los registros posteriores al retiro y las siglas MAR/MNAR. | Distinguir la revisión descriptiva de fechas del filtrado aplicado en cada corte. Explicar la limitación sobre las causas de los faltantes en lenguaje común. | Correspondencia comprobada entre explicación, tablas y filtros. |
| C06 | pp. 22–23, sección 3.5 | Mayor | Se pide aclarar la definición del retiro y se señala `Withdrawn`. | Definir por separado la fecha administrativa y el resultado final; explicar las discordancias sin tratarlos como equivalentes. | Definición consistente en capítulos 3 y 4, con denominadores identificados. |
| C07 | p. 24, sección 3.6 | Menor | Se señalan términos como «log» y productos técnicos de la revisión. | Usar «registro de actividad» y explicar para qué sirve cada producto que se conserve en el cuerpo del texto. | Lectura del párrafo sin términos técnicos innecesarios. |
| C08 | p. 25, sección 3.8 | Mayor | Se pregunta por los grupos, el efecto biserial, sus símbolos y los intervalos; se solicitan ejemplos. | Introducir la pregunta de comparación, identificar los grupos y explicar el signo del resultado antes de la fórmula. Describir el remuestreo por personas con un ejemplo. | Ejemplo y fórmula consistentes con la implementación; comprobación pendiente. |
| C09 | pp. 26–27, tablas y figuras de 3.8 | Mayor | Se piden explicaciones de los resultados y de las figuras; se señala espacio disponible. | Desarrollar cómo leer cada eje y qué significa una diferencia entre curvas o grupos. Ampliar figuras si mejora su legibilidad. | Texto interpretativo y revisión visual de la versión compilada. |
| C10 | pp. 28–29, secciones 3.9–3.10 | Mayor | Se pregunta por IMD, créditos y el alcance de «representa una inscripción». | Explicar las variables de contexto y precisar qué representa cada fila de la base preparada. | Definiciones contrastadas con el diccionario oficial y el código. |
| C11 | p. 31, sección 4.1 | Mayor | Se solicitan ejemplos y definiciones para inscripción, corte, conjuntos, símbolos y recencia. | Explicar primero un caso hipotético y después formalizar la regla. Definir cada símbolo junto a su primer uso. | Ejemplo que incluya retiro anterior, en el corte y posterior; fórmulas revisadas. |
| C12 | pp. 32–36, secciones 4.1–4.3 | Mayor | Hay dudas sobre ejemplos, diferencias frente al anteproyecto y porcentajes de retiro futuro; también marcas sobre espacios y figuras. | Conectar los ejemplos con los indicadores, distinguir decisiones metodológicas de cambios editoriales y aclarar el denominador de cada porcentaje. | Contraste con anteproyecto y decisiones documentadas; revisión visual final. |

Todos los asuntos permanecen abiertos para el documento principal. La muestra atiende C04 y parte de C05 como propuesta; no equivale al cierre de esos pendientes. No se identifican hallazgos bloqueantes demostrados en esta revisión editorial inicial. Las marcas manuscritas cuya lectura o referencia no sea inequívoca deberán conservarse como pendientes de interpretación.

## Criterio de reescritura

La explicación debe responder, en un orden natural, qué se está examinando, por qué importa y qué se encontró. El detalle técnico se incorpora después de establecer esa base. Se conservan las distinciones necesarias —personas e inscripciones, ausencia de datos y cero, retiro registrado e inactividad— con una explicación cercana a los datos del proyecto. No se eliminarán fórmulas o limitaciones por resultar difíciles; se revisará su ubicación y la explicación que las acompaña.

La referencia de voz es el planteamiento del problema. Se mantiene su tono académico e impersonal, pero se reducen la densidad de las oraciones y la acumulación de conceptos cuando dificulten la lectura.

## Muestra propuesta: sección 3.4

**Título propuesto: Información faltante y revisión de valores y fechas**

Antes de construir los indicadores, se revisó qué información estaba disponible y si los valores registrados eran coherentes con la descripción de los datos. Esta revisión permitió identificar campos vacíos, comprobar los valores de las evaluaciones y examinar las fechas de matrícula, entrega y retiro. Cada situación requiere una interpretación distinta, pues un campo vacío no siempre representa el mismo problema.

Por ejemplo, una inscripción sin fecha de retiro se trata en este estudio como un caso sin retiro registrado. Esto no permite afirmar, por sí solo, que el estudiante haya aprobado el curso. En cambio, cuando falta la fecha de matrícula, no se puede comprobar si la inscripción ya existía en el momento elegido para hacer la predicción. A ese momento se le denomina día de corte. Si se quisiera predecir al finalizar el día 28, sería necesario saber si la matrícula ocurrió a más tardar ese día.

Algo similar sucede con las evaluaciones. Puede existir un registro de entrega sin que aparezca su calificación; por ello, la ausencia de una nota no debe interpretarse automáticamente como una actividad no entregada. La Tabla 3.4 presenta los campos con información faltante. En cada caso, el porcentaje se calcula sobre el total de filas del archivo correspondiente, no sobre una misma cantidad de estudiantes.

**Tabla 3.4. Información faltante en los archivos revisados.**

| Archivo | Información faltante | Registros sin dato | Total de registros del archivo | Porcentaje |
|---|---|---:|---:|---:|
| assessments | Fecha de la evaluación | 11 | 206 | 5,34 |
| vle | Semana prevista de inicio de uso del recurso | 5 243 | 6 364 | 82,39 |
| vle | Semana prevista de finalización de uso del recurso | 5 243 | 6 364 | 82,39 |
| studentInfo | Categoría de privación socioeconómica del área de residencia (IMD) | 1 111 | 32 593 | 3,41 |
| studentRegistration | Fecha de matrícula | 45 | 32 593 | 0,14 |
| studentRegistration | Fecha de retiro | 22 521 | 32 593 | 69,10 |
| studentAssessment | Calificación de la evaluación | 173 | 173 912 | 0,10 |

La ausencia de fechas de retiro debe leerse de acuerdo con la definición anterior y no como una pérdida general de información. Asimismo, las semanas previstas de uso de los recursos describen su programación; su ausencia no significa que no existan registros de interacción con esos materiales. La categoría IMD corresponde al área de residencia, por lo que no constituye una medida directa de los ingresos personales del estudiante.

También se revisaron las calificaciones y los conteos de clics. Los resultados guardados de la revisión no registran calificaciones fuera del intervalo de 0 a 100 ni conteos de clics menores o iguales a cero en las filas del archivo de interacciones. Esta última comprobación se refiere a los registros existentes: no significa que todos los estudiantes hayan tenido actividad todos los días.

OULAD incluye además el campo `is_banked`, que indica si el resultado de una evaluación fue trasladado desde una edición anterior del curso. En la revisión se comprobó que este campo solo contuviera los valores 0 y 1; no se encontraron valores distintos. Esta distinción importa porque un resultado reconocido de una edición anterior no equivale a una nueva entrega durante el periodo que se está observando. [Fuente de las definiciones: documentación oficial de OULAD.]

Otra comprobación examinó el peso de las evaluaciones, es decir, el porcentaje asignado a cada una. Las actividades realizadas durante el curso y los exámenes se revisaron por separado, de acuerdo con la organización descrita en OULAD. Por ello, sumar todos sus pesos y exigir que el total sea siempre 200 no se utilizó como regla general para identificar errores. La tabla detallada de esta comprobación se conserva entre las salidas del análisis. [Fuente de la definición de peso: documentación oficial de OULAD.]

Las fechas también necesitan una lectura particular. En OULAD, el día 0 corresponde al inicio de la edición del curso y los números negativos indican momentos anteriores. Por ejemplo, una matrícula registrada en el día −10 ocurrió diez días antes del inicio. Por esta razón, las fechas negativas no se eliminaron automáticamente. La Tabla 3.5 reúne los casos identificados al revisar las fechas y los resultados reconocidos de otras ediciones.

**Tabla 3.5. Casos identificados en la revisión de fechas y evaluaciones.**

| Situación | Número de casos |
|---|---:|
| Inscripciones sin fecha de matrícula | 45 |
| Inscripciones con matrícula posterior al día 28 | 16 |
| Inscripciones con retiro posterior al final de la edición del curso | 1 |
| Registros de entrega anteriores al inicio del curso | 2 057 |
| Resultados de evaluaciones reconocidos de una edición anterior | 1 909 |
| Registros de interacción anteriores a la matrícula | 0 |
| Registros de interacción posteriores al retiro | 29 440 |
| Registros de entrega posteriores al retiro | 601 |

El día 28 se utiliza en esta tabla como referencia para describir las fechas de matrícula. La selección de inscripciones para cada día de predicción se realiza por separado en el capítulo siguiente. Además, los casos de la tabla corresponden a distintos tipos de registro y pueden coincidir entre sí; no deben sumarse como si fueran estudiantes diferentes.

Se identificaron interacciones y entregas con fecha posterior al retiro. Los archivos disponibles no permiten establecer por qué ocurrió esta situación. Sin embargo, esos registros no pueden emplearse como información previa para anticipar un retiro que ya había sucedido. Por ejemplo, si una inscripción tiene un retiro registrado en el día 20, una interacción del día 25 no sirve para predecir anticipadamente ese retiro.

Finalmente, identificar información faltante permite conocer una limitación de los datos, pero no explica por qué falta. La revisión no permite determinar si esas ausencias se relacionan con características observadas de los estudiantes o con información que no está disponible. Esta limitación debe considerarse al interpretar los análisis posteriores.

## Aclaraciones sobre la muestra

- Se añadieron los totales de filas a la Tabla 3.4 porque la versión actual afirma que presenta los denominadores, pero solo muestra la cantidad de ausencias y el porcentaje. Los denominadores se tomaron de `01_faltantes.csv`; no se estimaron a partir de porcentajes redondeados.
- Se mantuvieron los conteos de las salidas guardadas. Los ocho conteos de la Tabla 3.5 se contrastaron con `01_consistencia_temporal.csv` y coinciden; esto verifica la transcripción, no reproduce los cálculos.
- Los ejemplos de matrícula en el día −10 y de interacción posterior al retiro son hipotéticos. Ilustran reglas; no describen estudiantes identificados en OULAD.
- La explicación de `is_banked`, los pesos y las fechas se contrastó con la documentación oficial. El código de construcción de indicadores excluye `is_banked = 1` de las entregas actuales; esta es una comprobación por lectura del código, no una nueva ejecución.
- Se sustituyó la mención aislada a MAR/MNAR por la limitación que interesa al lector. Si esas categorías se utilizan después para justificar un método, deberán definirse en el apartado correspondiente.
- En la integración a LaTeX se conservarán las claves de tablas y se utilizará la referencia bibliográfica existente de OULAD, después de comprobar su entrada. Las notas entre corchetes de esta muestra son aclaraciones editoriales y no texto final de la tesis.

## Verificaciones y pendientes

Comprobado: correspondencia textual de la sección con `desarrollo1.tex`; valores de la Tabla 3.4 con la salida guardada; comprobaciones de rangos y agrupación de pesos en el notebook; reglas de matrícula y retiro en `eligible_at`; exclusión de evaluaciones reconocidas en `build_at_cut`; definiciones pertinentes en la documentación oficial.

No verificado en esta revisión: reproducción desde los archivos originales, corrección integral del análisis estadístico, cierre de todas las anotaciones manuscritas, ratificación de decisiones frente al anteproyecto y composición visual después de integrar la propuesta. No se modificaron el PDF original ni los archivos LaTeX del proyecto.

Siguiente paso: aplicar esta forma de explicación a la sección 4.1, utilizando un ejemplo temporal antes de la notación; continuar después con las comparaciones de la sección 3.8 y revisar la continuidad entre capítulos.

## Fuentes consultadas

- PDF anotado: `D:/Kami Export - proyecto.pdf`, páginas impresas 19–36 presentes en la selección y anotaciones generales.
- Referencia de voz: `planteamiento del problema.txt`. Sus cifras y citas no se verificaron para esta tarea editorial.
- Texto: `Plantilla_ProyAplicado/desarrollo1.tex`.
- Código: `01_carga_exploracion.ipynb`, celda de rangos y pesos; `src/ventanas_oulad.py`, funciones `eligible_at` y `build_at_cut`.
- Salidas guardadas: `reportes/correcciones_2026_09_10/tablas/01_faltantes.csv`, `01_rangos.csv`, `01_pesos.csv` y `01_consistencia_temporal.csv`.
- The Open University. *Open University Learning Analytics dataset: Data description*. https://research.stem.open.ac.uk/ouanalyse/open-dataset-more/ (consulta: 30 de septiembre de 2026).
- Referencia del conjunto de datos, identificada por la documentación oficial: Kuzilek, J., Hlosta, M. y Zdrahal, Z. (2017). *Open University Learning Analytics dataset*. Scientific Data, 4, 170171. DOI: 10.1038/sdata.2017.171. El artículo no pudo abrirse desde el navegador de esta sesión; las definiciones se consultaron en la documentación oficial anterior.
