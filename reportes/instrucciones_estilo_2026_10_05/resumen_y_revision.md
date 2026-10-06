# Consolidación de redacción y presentación

Fecha y versión: 5 de octubre de 2026, versión 1, con precisión de voz 1.1. Alcance: revisión de instrucciones persistentes y de los ajustes editoriales documentados; no constituye una nueva auditoría estadística ni una evaluación integral del PDF. La precisión 1.1 se documenta al final; la verificación original corresponde a la versión 1.

## Veredicto

El proyecto dispone de una evolución editorial coherente: conserva la voz académica e impersonal y facilita la lectura mediante explicaciones directas, definiciones próximas al uso, ejemplos y apoyos visuales. Sin embargo, las instrucciones principales seguían centradas en la muestra inicial de estilo y no recogían suficientemente los ajustes posteriores. Tampoco identificaban una guía visual vigente ni un procedimiento para conservar las decisiones frente a integraciones desde versiones antiguas. Esas omisiones se corrigieron en los archivos de instrucciones disponibles.

El archivo editable que actúa como instrucción persistente de este espacio de trabajo es `AGENTS.md`. Su contenido anterior coincidía con las instrucciones del proyecto proporcionadas en esta conversación. Se actualizó ese archivo; no se afirma haber modificado el mensaje de sistema interno de la aplicación ni una configuración externa de ChatGPT. La documentación oficial describe la lectura de archivos AGENTS.md y la precedencia de archivos más próximos al directorio de trabajo: [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Resumen de los ajustes documentados

| Eje | Criterio que debe conservarse | Evidencia consultada |
|---|---|---|
| Voz y fluidez | Español académico impersonal, con palabras precisas y habituales; párrafos conectados y oraciones divididas cuando pierdan claridad. La muestra orienta la voz, sin exigir reproducir su densidad. | `planteamiento del problema.txt`; `reportes/redaccion_clara_2026_09_21/registro.md`. |
| Orden de explicación | Presentar primero qué se hace y para qué; explicar después el procedimiento, sus condiciones y límites. | Registro de redacción del 21 de septiembre; texto vigente de `Plantilla_ProyAplicado/desarrollo1.tex`. |
| Conceptos y símbolos | Definir inscripción, módulo, presentación, corte, seguimiento, indicadores y símbolos cerca de su uso. La guía de notación complementa esa explicación. | `reportes/revision_anotaciones_2026_09_30/cotejo_pagina_por_pagina.md`, K02, K08 y K43–K52. |
| Ejemplos didácticos | Usar casos breves e identificados como hipotéticos para explicar temporalidad, recencia, CV, uniones y cálculos. No confundirlos con observaciones de OULAD. | `reportes/revision_editorial_2026_09_13/integracion/cambios_y_pendientes.md`; `cv_y_lectura/cambios_y_pendientes.md`; cotejo K27, K30 y K53. |
| Cuerpo y anexos | Mantener en el cuerpo las decisiones y condiciones esenciales; trasladar derivaciones especializadas y detalles de ejecución que interrumpan la lectura, con remisiones. | Integración del 13 de septiembre; registro del 21 de septiembre; cotejo K01 y K23. |
| Orientación de lectura | Conservar una ruta inicial, guía de notación, diccionario y diagramas de proceso y temporalidad. El documento debe comprenderse sin leer antes los notebooks. | `Plantilla_ProyAplicado/introduccion.tex`; integración del 13 de septiembre. |
| Resultados | Explicar grupos, medida, ejes, signos, intervalos y denominadores; interpretar hallazgos sin repetir cada cifra ni atribuir causalidad. | Cotejo K26–K39 y K57; sección 3 vigente del AGENTS.md. |
| Figuras y tablas | Usar figuras para reconocer patrones y conservar tablas para los valores exactos. Seleccionar comparaciones útiles, sin crear una figura por cada tabla. | `reportes/figuras_cuerpo_2026_10_04/revision.md`; introducción vigente. |
| Identidad visual | Azul `#2C5697` como base, azul verdoso `#347B83` y tonos de apoyo; sin amarillo en elementos propios. Conservar el logotipo y el esquema original de OULAD. | `ESTILO_VISUAL.md`; `estilo_visual_javeriana.json`; revisión del 4 de octubre. La atribución institucional de la guía no se revalidó en esta revisión. |
| Excepción de curvas | Figura 3.4 con líneas continuas, sin marcadores ni etiquetas sobre las curvas; cinco colores consistentes entre paneles y leyenda común exterior. | Guía visual del 5 de octubre; implementación de las curvas acumuladas en `src/figuras_oulad.py`. |
| Legibilidad y composición | Tipografía de la plantilla en el texto; Arial o alternativa declarada en gráficos. Contraste, etiquetas y leyendas legibles a tamaño final, encabezados próximos a sus tablas y reducción de espacios innecesarios. | `ESTILO_VISUAL.md`; cotejo K33, K36, K41, K42 y K56; revisión de figuras del 4 de octubre. |
| Prudencia editorial | Distinguir trabajo previsto y ejecutado, corrección integrada, comprensión de los autores y aprobación académica. La edición no cambia datos, población, evento o estado de los análisis. | Registro del 21 de septiembre; cotejo de anotaciones, versión 3; revisión de figuras del 4 de octubre. |

Los recursos de Knaflic y Yau se reconocen como orientación de comunicación en la guía visual. No se realizó una nueva consulta de sus libros ni se atribuye lectura integral de esas obras. Las tesis revisadas anteriormente aportaron recursos de exposición; no constituyen por sí mismas requisitos institucionales ni validación técnica del estudio.

## Hallazgos y correcciones

| ID | Severidad | Evidencia y problema | Corrección | Estado |
|---|---|---|---|---|
| I01 | Mayor | El AGENTS.md anterior pedía oraciones elaboradas y fidelidad a la muestra sin precisar el criterio de claridad consolidado el 21 de septiembre. Podía favorecer el regreso a pasajes densos. | Sección 3 reformulada: claridad prioritaria, explicación del propósito, vocabulario accesible y ejemplos. | Cerrado en esta versión. |
| I02 | Mayor | La integración del 13 de septiembre advierte que `scripts/integrar_editorial.py` reconstruye capítulos desde un respaldo y puede sobrescribir cambios posteriores. | Sección 0: edición localizada de fuentes activas y revisión de integradores antes de usarlos. | Regla incorporada; no se ejecutaron integradores. |
| I03 | Menor | Las instrucciones no remitían a la guía visual vigente. Los registros del 30 de septiembre usaban amarillo y un esquema propio de OULAD; el 4 de octubre ambos fueron sustituidos. | Referencia a ESTILO_VISUAL.md y conservación explícita de las decisiones posteriores. | Cerrado en esta versión. |
| I04 | Menor | La regla general de trazos y marcadores podía competir con la excepción de la Figura 3.4. | Se identificó la prevalencia de la regla específica en la guía y en la sección 3. | Cerrado en esta versión. |
| I05 | Menor | `documento/AGENTS.md` repetía reglas de voz y apuntaba solo a la copia de referencias; src y notebooks remitían a la muestra sin sus ajustes posteriores. | Se centralizó la redacción en el AGENTS.md principal y se alinearon las remisiones locales. | Cerrado en esta versión. |
| I06 | Menor | El ejemplo de ESTILO_VISUAL.md importaba `YELLOW`, símbolo inexistente en el módulo vigente. | Sustitución por `ACCENT`, definido en `src/estilo_visual.py`. | Cerrado por cotejo de documentación y código; no se ejecutó Python. |
| I07 | Sugerencia | Una instrucción mantenida solo en el historial puede perderse o quedar enfrentada a una copia antigua. | Regla para actualizar la ubicación canónica y registrar qué decisión sustituye cada cambio permanente. | Incorporada como control de mantenimiento. |

Las omisiones anteriores constituyen riesgos de interpretación y mantenimiento; no prueban que un texto haya sido sobrescrito indebidamente. Los registros históricos permanecen intactos y se consultan como evidencia de evolución, no como guías actuales.

## Archivos y conservación

Se editaron `AGENTS.md`, `documento/AGENTS.md`, `src/AGENTS.md`, `notebooks/AGENTS.md` y `ESTILO_VISUAL.md`. Se conservaron originales en `respaldo/2026-10-05_pre_instrucciones_estilo`. Las secciones académicas 2 y 4–6 del AGENTS.md principal se conservaron; no se modificaron requisitos de evidencia, validación o fuentes. La sección 1 solo precisa la relación entre el modelo de voz y los ajustes de claridad.

No se modificaron capítulos, código analítico, scripts, notebooks ni el PDF. El alcance no requería compilar LaTeX ni ejecutar análisis. La validación de esta actualización se registra en `verificacion.json` mediante comparación con los respaldos, cotejo de referencias locales y huellas de archivos ajenos a la edición.

## Límites y seguimiento

| Pendiente | Ubicación | Severidad | Evidencia necesaria para cierre |
|---|---|---|---|
| Comprobar comprensión efectiva | Documento vigente; registro del 21 de septiembre y cotejo versión 3. | Sugerencia | Lectura de ambos autores y comentarios del asesor o revisores sobre pasajes concretos. |
| Comprobar instrucciones externas duplicadas | Configuración de proyecto en una aplicación distinta, si existe. | Sugerencia | Acceso a ese campo o copia exacta de su contenido. No fue inspeccionado ni editado. |
| Revalidar mantenimiento en una sesión posterior | AGENTS.md principal y guías enlazadas. | Sugerencia | Comprobar que una nueva tarea identifica la versión del 5 de octubre y conserva los criterios al editar. La comprobación estática no demuestra el comportamiento de todas las sesiones futuras. |

La carpeta no es un repositorio Git local según la comprobación efectuada; no se crearon commits ni se afirmó una actualización del repositorio remoto. El resumen cubre los ajustes con evidencia local consultada; no recupera decisiones que existan únicamente en conversaciones no disponibles.

Para continuar, las nuevas ediciones deben partir del AGENTS.md principal y de la guía visual enlazada. Si se mantiene además un campo externo de instrucciones del proyecto, debe usarse el contenido actualizado del AGENTS.md para reemplazar su versión anterior, evitando sumar reglas antiguas y nuevas en el mismo campo. La persistencia mediante AGENTS.md corresponde al mecanismo documentado por OpenAI; no garantiza la sincronización de un campo externo.

## Precisión 1.1: regla explícita para todo el proyecto

Fecha: 5 de octubre de 2026. Motivo: solicitud expresa del usuario de incorporar literalmente la formulación de voz académica, impersonal, clara y explicativa para lectores en formación, junto con el ejemplo sobre población común y disponibilidad temporal de información.

Se sustituyó únicamente el párrafo «Voz» de la sección 3 del AGENTS.md principal por la formulación solicitada, su alcance obligatorio y el ejemplo de exposición. Esta regla precisa la voz formal previa y prevalece sobre una interpretación de la muestra que favorezca redacción densa. Las instrucciones locales ya remiten a esa sección; no se añadió otra versión del criterio en subcarpetas.

Comprobación: se cotejaron la formulación literal, el ejemplo y la enumeración de apartados en el archivo guardado. No se modificaron capítulos, notebooks, código o PDF. El cumplimiento del documento completo sigue pendiente de una revisión de todos sus apartados; la actualización de instrucciones no se presenta como una reescritura integral ya realizada. La verificación de esta precisión se conserva en `verificacion_voz_1_1.json`.
