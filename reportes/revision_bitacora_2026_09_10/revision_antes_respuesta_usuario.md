# Revisión crítica de la bitácora de correcciones

Fecha: 10 de septiembre de 2026. Documento revisado: `correcciones_proyecto_aplicado.md`. Contraste con las fuentes actuales de la plantilla, los notebooks de la versión multiventana, sus tablas, los CSV y la actividad A3.1 del anteproyecto aprobado.

## Veredicto

**La bitácora es pertinente como propuesta de revisión, pero no debe aplicarse literalmente.** Identifica mejoras reales de trazabilidad, definiciones, presentación de resultados y sensibilidad estadística. También contiene generalizaciones matemáticas incorrectas, diagnósticos que no corresponden a la fuente actual y textos de reemplazo que introducirían nuevas contradicciones.

Se recomienda aprobar un plan depurado: completar definiciones y diccionario; documentar las diferencias respecto de actividades concretas del anteproyecto; evaluar la variabilidad entre días activos como indicador distinto; ampliar la sensibilidad y publicar los diagnósticos ya calculados; después actualizar figuras y redacción. No corresponde cambiar automáticamente la etiqueta ni sustituir resultados por cifras esperadas. Esta entrega revisa las propuestas; no modifica los notebooks ni la plantilla entregados.

## Hallazgos principales y resolución propuesta

| ID | Ubicación de la bitácora | Severidad | Dictamen, evidencia y corrección |
|---|---|---|---|
| B01 | §1.1 | Mayor | **Se confirma la diferencia con A3.1.** El anteproyecto interpreta la fecha como retiro voluntario y prevé explorar la posibilidad de abandono implícito. La versión actual no infiere motivos y mantiene la inactividad como predictor. Registrar expresamente ambas diferencias, además de la restricción temporal de población y evento. |
| B02 | §1.1, acta | Mayor | **Ratificación pertinente; formato obligatorio no demostrado.** No se encontró una norma que exija específicamente acta firmada para continuar toda actividad. No incorporar «registrados en acta» sin evidencia. Puede prepararse una propuesta de decisión y llevarla al asesor. La exploración de una posibilidad no equivale a un compromiso incondicional de construir una segunda etiqueta. |
| B03 | §1.2 y §3.4.3 | Mayor | **Problema real de dependencia, conclusión excesiva.** El CV con ceros combina frecuencia e intensidad; solo bajo intensidad constante se reduce a una función de la proporción activa. El CV sobre días activos mide otra propiedad. Evaluarlo como alternativa o complemento, con nombre nuevo, sin llamar errónea por definición a la versión actual. Véase la identidad general más adelante. |
| B04 | §2.3 | Menor | **No se reproduce el error en la fuente actual.** `descripcion.tex:180` contiene una estimación de Pr(Y=1 dado X=x), no de la clase predicha. Marcar la observación como no aplicable a esa versión, verificando el PDF concreto si el asesor revisó otro archivo. |
| B05 | §2.1–2.2 | Mayor | **Aceptar con ajuste.** La tabla de símbolos y las definiciones mejoran la lectura. En la comparación de costes, pi debe representar probabilidad individual condicional, no prevalencia marginal. Usar p(x), pi(t) para prevalencia y p_nodo para el nodo. Distinguir también tamaño muestral n y longitud de ventana n_t. |
| B06 | §3.1 | Mayor | **Aceptar con ajuste.** No todos los predictores proceden de [0,t]: existen antecedentes preinicio y contexto. Escribir «indicadores de la ventana principal». Expresar explícitamente «u ausente o u>t», en vez de negar una desigualdad sobre un valor no definido. L se utiliza como final según la convención operativa; el campo fuente se denomina longitud de presentación. |
| B07 | §3.2 | Mayor | **Reconciliar con el diccionario existente.** Los nombres propuestos difieren del código. `clics_pre_inicio` y `n_entregas_pre_inicio` ya existen; `dias_activos_previos` no figura entre los 26 candidatos. El número de filas VLE sí es candidato. No introducir el diccionario reconstruido como si describiera la ejecución actual. |
| B08 | §3.2, diversidad | Sugerencia | **Justificar selección; no inventar obligación.** La tabla teórica enumera familias derivables, lo cual no compromete por sí solo construirlas todas. Es conveniente explicar por qué diversidad no se incluyó, o proponer su evaluación. No atribuir una decisión histórica sin registro ni afirmar que su dependencia del diseño obliga a excluirla. |
| B09 | §3.4.1–3.4.2 | Mayor | **Corregir antes de incorporar.** Con +1, caídas de 200 a 100 y de 20 a 10 no producen el mismo valor. La simetría exacta se obtiene al intercambiar los bloques: T(a,b)=-T(b,a). El suavizado pierde invariancia de escala. El intervalo propuesto depende de los propios valores observados y no es un rango global fijo. |
| B10 | §3.4.4, V10 | Mayor | **Aceptar sensibilidad del PCA; rechazar demostración propuesta.** V=nqm es exacta, pero el PCA utiliza q, no log(q). No se deduce dependencia lineal entre sus columnas ni que tres variables sean funciones de las otras dos. La redundancia influye en la estructura; no demuestra por sí sola que toda la varianza resumida sea un artefacto. Comparar conjuntos documentados, no invalidar automáticamente el PCA descriptivo. |
| B11 | §3.4.5 | Menor | **Aceptar con límites.** La equivalencia r=2AUC-1 se refiere al indicador como puntuación, casos observados y empates tratados consistentemente. No constituye una evaluación predictiva independiente. Para r=-0,179, AUC=0,4105 y 0,5895 al invertir el signo; declarar la precisión del redondeo. |
| B12 | §3.4.6 | Mayor | **Aceptar fórmula; retirar afirmación general.** La V de Cramér no aumenta necesariamente con el desbalance categórico. Puede ser cero bajo independencia con márgenes muy distintos. Mantener limitaciones de tamaños de celda, dimensiones y ausencia de ajuste por otros atributos. |
| B13 | §3.4.7–3.4.8 | Mayor | **Aceptar con precisión.** El umbral de costes exige probabilidades pertinentes y costes definidos; calibración no equivale automáticamente a conocer la probabilidad condicional verdadera. AP y área trapezoidal PR son resúmenes distintos. Restar prevalencia puede describir una ganancia, pero no hace comparables poblaciones, horizontes o tareas diferentes. |
| B14 | §4.1–4.6 | Mayor | **Figuras útiles con correcciones.** En la línea temporal debe indicarse L>=40 para el caso positivo. Las barras de exclusiones necesitan categorías mutuamente excluyentes: los 2.678 retiros preinicio de toda la fuente se solapan con filtros de matrícula. Los flujos exportados no desglosan por sí solos preinicio frente a 0..t; ese desglose requiere cruzar la base. |
| B15 | §4.7–4.8 | Menor | **No se confirma eje categórico.** Los notebooks 02 y 03 grafican directamente valores numéricos de corte. Se propone mejorar rótulos y explicitar poblaciones cambiantes. Añadir eventos e índices base 100 es útil; ejes truncados en líneas no constituyen por sí solos un error. No atribuir a la caída del denominador una reducción mecánica de prevalencia. |
| B16 | §5, corrección 2 | Mayor | **Rechazar el reemplazo literal.** «Ningún indicador cuenta filas» contradice `n_registros_vle`. Tampoco la suma de clics es insensible a retirar duplicados. Debe distinguirse interpretación de filas, conservación de fuente y sensibilidad a deduplicación. |
| B17 | §5, correcciones 1, 3, 8, 9, 11 | Menor | **Aceptar edición pertinente.** Usar «capítulo», trasladar historia de versiones al anexo, precisar el alcance de equidad y los denominadores del resumen. Unificar formato numérico sin instalar una dependencia solo por preferencia tipográfica. El registro histórico se conserva. |
| B18 | §5, correcciones 4 y 7 | Menor | **Aceptar con evidencia.** Reportar los pesos por tipo, sin imponer 200 como regla. Justificar que una entrega previa puede satisfacer una evaluación programada al corte mientras el conteo de actividad actual usa 0..t: son indicadores distintos, no una incoherencia automática. |
| B19 | §5, corrección 12; bloque D | Mayor | **A1.3 está parcialmente cubierta, no ausente en su totalidad.** El notebook 03 ya analiza región, discapacidad, edad e IMD por corte; sus resultados se exportan. Falta una integración más completa y la revisión específica de créditos e intentos previos. Sustituir un estado global por trazabilidad de actividades. |
| B20 | §6.1 | Mayor | **No incorporar el texto propuesto.** Los primeros cortes matemáticamente posibles para las tendencias son 13 y 27, no 14 y 28; estos últimos son los primeros de la rejilla elegida. El corte 14 ya tiene señal académica. La duración es 234–269 días: 56 cabe en el primer cuarto, pero ello no prueba optimalidad ni una curva continua de desempeño. |
| B21 | §6.1, independencia del desenlace | Mayor | **Evitar reconstruir retrospectivamente una preespecificación.** Existe registro de adopción antes de comparar modelos, pero también exploración previa del desenlace. Los hallazgos de disponibilidad sustentan la pertinencia de la rejilla; no prueban que esa fuera exactamente la razón histórica de selección ni que se fijara a ciegas. |
| B22 | §6.2–6.3 | Menor | **Aceptar con límites ya documentados.** Retiro registrado no identifica voluntariedad ni permanencia institucional. La secuencia de preparación y modelado debe exponerse sin presentar la corrección bibliográfica completa como requisito para comenzar una línea base. |
| B23 | V12 | Mayor | **Ampliación razonable, cierre no automático.** B=500 no demuestra por sí solo que los intervalos concretos sean inestables. Aumentar repeticiones y estudiar estabilidad de extremos; B>=2.000 es un punto de partida, no garantía universal. Mantener remuestreo por persona y distinguir error Monte Carlo de incertidumbre muestral. |
| B24 | §8–§9 | Menor | **Revisión bibliográfica y anotaciones parciales.** Confirmar edición, tipo de entrada y pasaje citado; no basta el recuerdo de páginas. No se han verificado visualmente las marcas manuscritas de un PDF anotado en esta entrega. No eliminarlas ni presumirlas presentes en la fuente actual. |

## Variabilidad: distinción matemática necesaria

Sean n=t+1, k el número de días con clics, q=k/n y CV_act el coeficiente muestral calculado entre los k días activos. Para k>=2, la descomposición de la suma de cuadrados permite obtener exactamente:

\[
CV_{cal}^{2}=\frac{n}{n-1}\left[\frac{1-q}{q}+\frac{k-1}{kq}CV_{act}^{2}\right].
\]

En efecto, la suma de cuadrados de los días activos es (k-1)s_act²+k m_act²; la media del calendario es q m_act. Al añadir los ceros y dividir por la media al cuadrado se obtiene la identidad. El primer término mide la contribución de los días sin actividad y el segundo incorpora dispersión de intensidad. Si los días activos tienen intensidad constante, CV_act=0 y se recupera la expresión de la bitácora. Para k=1, el coeficiente activo no es observable, pero el coeficiente de calendario está definido y vale raíz de n.

El ejemplo A frente a C de la propia bitácora ya refuta que q determine siempre el CV: ambos tienen q=0,25 y el mismo volumen, pero distintos coeficientes. Por tanto, es adecuado advertir dependencia y evitar presentar dos asociaciones como evidencia independiente. Es incorrecto afirmar que necesariamente son la misma asociación con signo contrario.

La auditoría calcula ambos coeficientes sobre todos los casos elegibles de los cinco cortes; `contraste_cv.csv` incluye los tamaños observables y la correlación original también restringida a los mismos casos. Esto evita atribuir al cambio de fórmula lo que podría deberse a excluir inscripciones con un solo día activo. Una correlación baja no se impone como criterio de éxito: la dependencia empírica puede persistir aunque la definición sea correcta.

| Corte | Correlación CV calendario–q, casos con actividad | CV calendario–q, solo k>=2 | CV activo–q, solo k>=2 | Casos con CV activo observable |
|---|---|---|---|---|
| 7 | -0,922 | -0,848 | 0,126 | 18.704 |
| 14 | -0,923 | -0,892 | 0,153 | 22.779 |
| 28 | -0,919 | -0,909 | 0,102 | 25.227 |
| 42 | -0,925 | -0,918 | 0,102 | 25.323 |
| 56 | -0,931 | -0,926 | 0,076 | 25.147 |

Las correlaciones de Spearman confirman que la alternativa activa reduce notablemente la asociación con q en estos datos. No prueban independencia estadística ni mayor utilidad predictiva. La contrapartida es la observabilidad: en el corte 7 quedan 10.372 inscripciones sin CV activo definido. La identidad general se verificó en todos los casos con k>=2, con error absoluto máximo inferior a 5×10^-14 en el cuadrado del coeficiente.

La partición de exclusiones aporta otra corrección concreta: después de filtrar matrícula quedan **2.643 retiros preinicio**, no 2.678. Los 35 restantes ya se contabilizan en exclusiones por matrícula. Usar 2.678 como segmento adicional junto al resto de filtros produciría doble conteo. Puede mantenerse ese total en un histograma de toda la fuente, donde describe otro denominador. Las primeras evaluaciones continuas por presentación vencen entre los días **12 y 61**; esta heterogeneidad justifica mostrar el calendario, sin etiquetar automáticamente los cortes 7 y 14 como exclusivamente conductuales.

**Recomendación:** conservar la variable de calendario en la versión histórica; evaluar una variable separada de intensidad activa y comparar su aporte y observabilidad. Si se adopta otra especificación de PCA, presentar su población y su sensibilidad. La decisión no debe fundamentarse en obtener el signo, la correlación o el porcentaje de varianza deseados.

## Precisiones adicionales del diccionario y las justificaciones

La primera semana completa existe cuando t+1>=7, es decir, desde t=6; la condición t<7 de la propuesta tiene un desfase en el dominio general, aunque no cambia los cinco cortes actuales. Para las evaluaciones programadas debe mantenerse el filtro 0<=date<=t, no únicamente date<=t. Los rangos 0,078–0,162 citados en la fila de recencia corresponden a recencia relativa; a corte fijo ambas recencias tienen los mismos rangos, pero debe identificarse cuál se reportó.

La frase «el faltante es informativo y no debe imputarse» es demasiado absoluta. Debe conservarse su significado en el conjunto analítico; un modelo que requiere datos completos puede usar una imputación documentada junto a un indicador de ausencia, ajustada dentro del entrenamiento. No se afirma que esa estrategia ya se haya seleccionado.

El suavizado de la tendencia produce log(101/201), aproximadamente -0,688, para 200→100, y log(11/21), aproximadamente -0,647, para 20→10. Se propone explicar +1 como una decisión de suavizado que permite valores finitos y reduce la inestabilidad cerca de cero, sensible a la escala de los conteos. La referencia precisa a Agresti y su equivalencia con correcciones de odds no se verificó y no debe insertarse como respaldo consultado. Sin cotas previas para los conteos, la transformación no posee un intervalo global finito; el intervalo de §3.4.2 es solo una cota condicionada a los dos bloques observados.

La circularidad de una etiqueta por inactividad tampoco es inevitable en cualquier diseño. Utilizar la misma actividad y el mismo periodo para definir etiqueta y predictores sería circular; predecir inactividad de un periodo estrictamente futuro sería otra tarea temporal posible. No es la tarea adoptada aquí y requeriría definición, justificación y validación propias.

## Estado de las verificaciones solicitadas

| Verificación | Estado en esta revisión | Evidencia o siguiente acción |
|---|---|---|
| V1 | Recontrastada la población en cinco cortes | Ya existía `02_flujos.csv`; se añade una partición de exclusiones sin solapamientos. No era necesario reconstruir desde cero la elegibilidad. |
| V2–V3 | Contraste independiente de ambos CV ejecutado | No se sustituyen predictores ni se regeneran los informes. Se exportan correlaciones, observabilidad y comprobación de la identidad algebraica. |
| V4 | Pendiente | El efecto de deduplicar sobre los tamaños de asociación requiere una sensibilidad específica. Deduplicar toda la fuente antes de agregar; no retirar filas que solo coinciden tras descartar campos. No adoptar deduplicación como limpieza definitiva sin evidencia. |
| V5 | Contraste completo de clics y días activos ejecutado | Se lee todo `studentVle.csv`, se agregan los días 0..56 y se contrastan todas las inscripciones elegibles de los cinco cortes. Esto amplía la comprobación previa por muestra. |
| V6 | Comprobada | Las 11 evaluaciones sin fecha son Exam y quedan fuera del calendario continuo definido. La tabla exportada ya lo mostraba. |
| V7 | Comprobada y exportada | Mínimo de fecha no Exam por módulo y presentación. Sirve para describir disponibilidad, no para afirmar que la rejilla fue optimizada previamente con este criterio. |
| V8 | Comprobada | Longitud de las presentaciones: mínimo 234, máximo 269 días. |
| V9 | Comprobada y exportada | Cinco presentaciones no suman 200: CCC 2014B y 2014J suman 300; GGG 2013J, 2014B y 2014J suman 100. La razón se describe por componentes registrados, sin inventar una regla institucional. |
| V10 | Propuesta de sensibilidad pendiente | No es necesaria para declarar válido el cálculo original, pero sí conveniente para revisar su interpretación y la elección de variables. |
| V11 | Valores y especificación ya disponibles; falta exposición | Las cuatro variables son clics, proporción de días activos, filas VLE y entregas. Al día 28: VIF 5,235; 4,696; 10,929; 1,319. El código usa todas las filas elegibles; añadir n efectivo al producto y a la presentación. |
| V12 | Pendiente | Aumentar remuestreos y comprobar estabilidad; no se reprodujeron intervalos en esta auditoría. |

## Bibliografía: alcance de la comprobación

La recomendación de combinar referencias metodológicas y documentación de implementación es adecuada. No se recomienda sustituir mecánicamente todas las citas oficiales: las fuentes originales respaldan el método y la documentación acredita detalles del software.

Se comprobó que Kerby debe citarse como: Kerby, D. S. (2014). *The Simple Difference Formula: An Approach to Teaching Nonparametric Correlation*. Comprehensive Psychology, 3, artículo 1. DOI: 10.2466/11.IT.3.1. El fragmento «11.IT.3.1» pertenece al DOI; no debe convertirse en un intervalo de páginas. La edición republicada explica la continuidad del identificador. [Publicación de SAGE](https://journals.sagepub.com/doi/pdf/10.2466/11.IT.3.1).

Para Iglewicz y Hoaglin se contrastó la portada y los datos editoriales del original: Iglewicz, B., y Hoaglin, D. C. (1993). *How to Detect and Handle Outliers*. The ASQC Basic References in Quality Control: Statistical Techniques, volumen 16. Milwaukee: ASQC Quality Press. ISBN 0-87389-247-X. Corresponde a un libro/volumen; la entrada `incollection` propuesta carece de un libro contenedor. La edición electrónica anunciada actualmente por ASQ tiene otra fecha y no debe confundirse con la original. [Ejemplar del original](https://hwbdocs.env.nm.gov/Los%20Alamos%20National%20Labs/TA%2054/11587.pdf), [ficha editorial electrónica](https://asq.org/quality-press/display-item?item=E0801).

La diferencia entre precisión promedio y área trapezoidal se contrastó en la [documentación oficial de average_precision_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html): no son implementaciones equivalentes y la interpolación lineal puede ser optimista. La apertura del PDF de Davis y Goadrich intentada en esta revisión falló; no se declara leído. La pertinencia de examinar el número de remuestreos se apoya adicionalmente en Hesterberg, T. C. (2015), *What Teachers Should Know About the Bootstrap: Resampling in the Undergraduate Statistics Curriculum*, The American Statistician, 69(4), 371–386, DOI 10.1080/00031305.2015.1089789; se consultó su [registro del autor](https://www.timhesterberg.net/bootstrap-and-resampling), sin trasladar una recomendación numérica universal al proyecto.

Las restantes entradas y, especialmente, los pasajes o secciones concretos propuestos no quedaron cotejados exhaustivamente en esta entrega. Permanecen pendientes; no se incorporaron entradas nuevas a la bibliografía del proyecto.

## Orden de trabajo depurado

1. Precisar la trazabilidad de A3.1 y A2.5: evento, exploración de inactividad y exclusión de puntajes por disponibilidad. Separar lo adoptado en esta versión de la ratificación académica pendiente. Reconocer que el informe para la reunión debe explicitar A3.1 con más detalle: la redacción previa sobre «precisión de operacionalización» no sustituye ese contraste de actividades.
2. Incorporar notación, definiciones, diccionario reconciliado y resultados ya existentes de calendario, flujos, VIF y variables de contexto. Corregir afirmaciones literales equivocadas de la bitácora antes de usarlas.
3. Crear una versión analítica nueva para sensibilidad de CV activo, PCA y duplicados; ampliar bootstrap con un criterio explícito de estabilidad. Preservar la versión multiventana original y sus cifras.
4. Generar figuras que respondan a preguntas distintas: distribución del retiro, elegibilidad, disponibilidad y evolución agregada con eventos. Evitar seis figuras nuevas si solo duplican tablas sin facilitar la interpretación.
5. Actualizar informes, plantilla y guion del asesor con los resultados realmente ejecutados. Mantener el modelado como siguiente objetivo analítico, sujeto al protocolo de evaluación, sin condicionarlo a cerrar toda mejora editorial.

## Evidencia, límites y reproducción

`scripts/auditar_bitacora_correcciones.py` genera las comprobaciones adicionales en esta carpeta. Se ejecuta desde la raíz con `python scripts/auditar_bitacora_correcciones.py`. El archivo `verificaciones.json` registra la huella de la bitácora revisada, los conteos, los ejemplos y el alcance. Se consultaron los registros de ejecución anteriores; no se reejecutaron aquí los tres notebooks, el PCA, los intervalos bootstrap ni clasificadores.

La ubicación por página de las anotaciones manuscritas no se da por validada mediante el código fuente. Una revisión del PDF anotado concreto sigue pendiente. Tampoco se verificó una norma que obligue al formato de acta firmada. Estas limitaciones no impiden corregir redacción ni desarrollar comprobaciones reversibles dentro del alcance autorizado.
