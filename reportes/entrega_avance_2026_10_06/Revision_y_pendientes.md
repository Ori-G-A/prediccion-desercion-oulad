# Revisión y cierre de pendientes del avance

Versión documental: 6 de octubre de 2026. Versión analítica conservada: correcciones_2026_09_10.

## Veredicto

El paquete queda preparado para la revisión del director solicitada por los autores. Se cerraron las incoherencias documentales que podían resolverse con la evidencia disponible. No constituye todavía un cronograma acordado ni una certificación de cumplimiento de los recursos institucionales cuyo contenido no se ha consultado. La falta de modelos terminados se presenta como estado del proyecto, no como un defecto de esta entrega de avance.

## Hallazgos revalidados

| ID y antecedente | Severidad | Ubicación y evidencia | Corrección o condición de cierre | Estado al 06-10-2026 |
|---|---|---|---|---|
| E01 / P01 del 05-10 | Mayor | descripcion.tex, tabla CRISP-DM; desarrollo3.tex; A3.2 del anteproyecto | Tabla indica definición pendiente; capítulo explica estratificación prevista y necesidad de precisar personas repetidas, presentaciones y generalización. | Incoherencia documental cerrada; protocolo sigue pendiente. |
| E02 / P5 del 30-09 | Menor | avance_objetivos.tex; desarrollo2.tex, sección 4.2 | Se separa selección base A1.3 de selección durante entrenamiento. Se explicitan inclusiones, exclusiones y contexto condicionado. Código, diccionario y 26 candidatos cotejados. | Cierre documental en la versión actual; alcance académico por revisar. |
| E03 / A2.7 | Menor | avance_objetivos.tex y anteproyecto 8.1.2 | Se sustituye el requisito de selección predictiva final por el estado comprobado: bases exportadas pendientes de acordar como entrada al modelado. | Corrección documental cerrada. |
| E04 / P02 del 05-10 | Mayor | desarrollo2.tex; decision_temporal.json; aclaración del usuario de esta sesión | Ratificar notas solo para auditoría, retiro futuro sin atribuir voluntariedad, elegibilidad e inactividad complementaria. | Pendiente del director; consultas preparadas. |
| E05 / P1-P2 del 30-09 | Mayor | Cronograma original M1-M10; confirmación del usuario de que no hay acuerdos | Informe de avance preparado con todos los bloques originales y propuesta del 6 al 19. Faltan M1, fechas reales y actualizadas, responsables y periodicidad acordados. | Preparado para revisar; aprobación no verificable. |
| E06 / A1.1 | Menor | Siete CSV y fuentes.json | Huellas locales verificadas nuevamente. Falta evidencia del origen de descarga o contraste de archivos con la fuente oficial. | Integridad local comprobada; procedencia histórica no verificable. |
| E07 / estructura | Mayor | Captura de Semana 2 y comparación del 30-09 | Consultar Estructura_Documento_Proyecto_MCD_Vers2025-1.docx y contrastar la plantilla del curso con la local. No se encontró el documento de estructura en el inventario consultado. | Pendiente antes de declarar cumplimiento institucional. |
| E08 / bibliografía | Mayor | Antecedentes, planteamiento y registros de revisión bibliográfica | Las claves y citas se conservaron y resuelven; no se realizó una nueva comprobación de cada afirmación contra su fuente. | Auditoría exhaustiva no verificable en esta revisión; no se presume error. |
| E09 / protocolo | Bloqueante para comparación predictiva | desarrollo3.tex y evidencia de exploración completa de OULAD | Fijar escenario de generalización, particiones, métricas, calibración, umbrales y tratamiento de exploración previa antes de entrenar. | Pendiente; no bloquea enviar el avance al director. |
| E10 / modelos, SHAP, prototipo | Mayor respecto del cierre del proyecto | desarrollo3.tex, desarrollo4.tex, desarrollo5.tex | Ejecutar las fases conforme al protocolo y cronograma que se acuerden. | No iniciadas; no se añaden resultados inexistentes. |
| E11 / P03 del 05-10 | Sugerencia | Documento y autores | Lectura de ambos autores y observaciones concretas del director. | Pendiente; claridad editorial no acredita comprensión efectiva. |
| E12 / P04 del 05-10 | Menor | proyecto.log | Persisten advertencias de clase, tocbibind y minitoc; sin errores, cajas desbordadas ni referencias indefinidas. | Limitación de plantilla, conservada. |

La ausencia de rúbrica, confirmada por el usuario, se registra como condición de la entrega y no como incumplimiento. No se solicitan modelos terminados ni porcentajes mínimos que las capturas no establecen.

## Comprobaciones ejecutadas y límites

- Se reejecutaron 49 comprobaciones independientes. Incluyen las huellas de los siete CSV, unicidad de claves, población y evento por corte, ausencia de notas y desenlaces entre candidatos, clics de una muestra de 60 personas contrastados con CSV, entregas contrastadas con toda la fuente, faltantes estructurales, denominador inclusivo, cohorte común y casos de frontera e invariancia ante información futura. Tres comprobaciones leen contadores y salidas guardadas de notebooks; se renombraron expresamente para no presentarlas como reejecución de estos.
- Se cotejaron adicionalmente los 26 candidatos y ocho atributos de contexto entre el diccionario y el código. Las poblaciones de los cinco archivos exportados coinciden con las del documento: 29.076, 28.054, 27.515, 27.005 y 26.506 inscripciones. Al día 28 hay 24.826 personas y 5.012 retiros futuros.
- No se reejecutaron integralmente los notebooks, los 5.000 remuestreos, el PCA o los contrastes. Sus registros históricos se conservan como evidencia previa. No se entrenaron modelos ni se seleccionaron variables según desempeño predictivo.
- Se compiló el proyecto con su flujo ordinario: pdfLaTeX, BibTeX y pasadas de resolución. MiKTeX necesitó acceso a su configuración de Windows fuera del espacio de trabajo; la compilación autorizada finalizó correctamente. No se usaron integradores ni migradores.
- Se verificaron fórmulas desplegadas y citas conservadas por archivo, identidad de bibliografía e imágenes, 88 etiquetas únicas y 116 remisiones con destino. Se verificó que el PDF incorpora los nuevos pasajes y la fecha correcta. La conservación no constituye una nueva demostración de fórmulas ni una validación del contenido de las fuentes citadas.
- Se renderizó el documento completo, se revisaron sus ocho hojas de contacto y se ampliaron las páginas PDF 27, 56, 71 y 75. Se revisaron las tres páginas finales del cronograma y se ajustó su paginación. No se detectaron recortes ni superposiciones en las comprobaciones finales. Poppler emitió avisos de fuentes de sustitución Symbol y ArialUnicode al renderizar el cronograma; no se observaron caracteres ausentes en las páginas inspeccionadas.

## Conservación y trazabilidad

Se modificaron únicamente cinco fuentes del documento: proyecto.tex, descripcion.tex, desarrollo2.tex, desarrollo3.tex y avance_objetivos.tex. Las cifras y decisiones analíticas se conservaron; los datos y notebooks no se modificaron. Se creó un paquete nuevo para no sobrescribir registros históricos. El respaldo previo, la diferencia de fuentes, los registros de comprobación y las huellas de los PDF permiten identificar esta versión.

Próximo paso: los autores pueden compartir los dos PDF y las consultas preparadas con el director; no se envió ningún mensaje ni archivo a terceros desde esta sesión.
