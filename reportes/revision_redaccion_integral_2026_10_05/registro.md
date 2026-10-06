# Revisión integral de redacción

Versión: 5 de octubre de 2026. Fuentes activas: `Plantilla_ProyAplicado`. Criterio aplicado: secciones 0 y 3 de `AGENTS.md` y `ESTILO_VISUAL.md`. Las dos copias de la muestra de voz tienen la misma huella SHA-256. Respaldo previo completo: `respaldo/2026-10-05_pre_revision_redaccion_integral/Plantilla_ProyAplicado`.

## Veredicto y alcance

Se completó la revisión editorial de todos los capítulos, anexos y textos de tablas y figuras de las fuentes vigentes. Se conservaron los pasajes que ya explicaban con claridad el propósito, el procedimiento y sus límites. Los cambios son de exposición: no modifican población, evento, ventanas, procedimientos analíticos, resultados ni estado de desarrollo. Esta revisión no constituye aprobación académica ni demuestra la comprensión efectiva de autores o jurados.

El documento actualizado está en `Plantilla_ProyAplicado/proyecto.pdf`; las fuentes editables permanecen en esa misma carpeta. El detalle completo de los cambios frente al respaldo está en `cambios.diff`; `cambios.json` registra la primera aplicación de ajustes y el diff incluye también los refinamientos finales.

## Apartados revisados

| Apartado | Cambios o decisión de conservación |
|---|---|
| Resumen e introducción | Desarrollo de OULAD y explicación de CRISP-DM y SHAP; conservación de cifras, propósito, estado y ruta de lectura. |
| Contextualización: problema, preguntas, objetivos y alcance | Simplificación del párrafo de señales conductuales y temporalidad. Conservación de la formulación de preguntas, objetivos y exclusiones del proyecto. |
| Marco teórico | Definiciones cercanas al uso; explicación aplicada de clasificación, regresión logística, Random Forest, XGBoost, TabNet y SHAP. Eliminación de una repetición sobre varianza en Random Forest. Conservación de LightGBM y de las formulaciones matemáticas. |
| Antecedentes | Revisión de continuidad con el problema, evento y límites del estudio; conservación de los pasajes y sus citas. Las afirmaciones bibliográficas no se presentan como verificadas en esta edición. |
| Caracterización | Clarificación de IMD, dependencia entre indicadores y comparabilidad de medidas relativas. Conservación de ejemplos, poblaciones, incertidumbre y orientación de lectura de resultados. El ejemplo de lectura de curvas se situó antes de la figura para evitar su interrupción por el flotante. |
| Ingeniería de características | Explicación del cociente de tendencia, signo, bloques y suavizado; desarrollo de Spearman, VIF, PCA y MCD. Ajustes de vocabulario en disponibilidad, duplicados y calendario. Conservación de elegibilidad, CV, sensibilidades y resultados. |
| Modelos, interpretabilidad y prototipo | Separación del propósito y condiciones del futuro modelado; explicación de calibración y requisitos de SHAP. El prototipo conserva su texto y su estado pendiente. |
| Conclusiones y avance de objetivos | Desarrollo de CV y PCA; conservación de respuestas, límites, estados y ratificaciones pendientes. |
| Anexos | Clarificación de reproducibilidad, lectura de celdas, NaN, SD y `floor`; propósitos y símbolos junto a las derivaciones de Random Forest, XGBoost, regresión logística, LightGBM, TabNet y Shapley. Se conservan pruebas e hipótesis. |
| Notación, tablas, figuras y auxiliares | Revisión de guía, diccionario, pies, títulos y orientación visual. Ajuste puntual del diagrama de indicadores y definición de coalición. Conservación de ejemplos didácticos, figuras de contexto, cascada, esquema OULAD, logotipo, colores y excepción de la Figura 3.4. |

Se revisaron los 21 archivos `.tex` y se modificaron 11, incluidos los auxiliares incorporados mediante `input`. También se revisaron el archivo principal, el formato y el tema visual. La bibliografía se comprobó para integridad de claves y conservación del archivo; no se hizo una nueva auditoría de sus fuentes.

## Hallazgos y pendientes por versión

| ID | Severidad | Ubicación y evidencia | Corrección o condición de cierre | Estado al 05-10-2026 |
|---|---|---|---|---|
| R01 | Menor | Marco teórico y anexos: párrafos densos, símbolos explicados principalmente en la guía y vocabulario especializado sin explicación inmediata. | Reescritura localizada y significado aplicado de las expresiones, con detalle formal conservado. | Cerrado editorialmente. |
| R02 | Menor | Random Forest: dos párrafos consecutivos repetían el beneficio y límite de promediar árboles. | Integración en un solo párrafo; cita y remisión conservadas. | Cerrado. |
| R03 | Menor | Caracterización: un flotante interrumpía el ejemplo de lectura de la distribución acumulada. | Ejemplo antes del flotante y comprobación de la nueva composición. | Cerrado. |
| P01 | Mayor | `descripcion.tex`, Tabla 2.3: la fila Modelado menciona «Partición estratificada». `desarrollo3.tex` mantiene las particiones y generalización por definir. | Contradicción de estado registrada por separado; la tabla se conserva para no fijar ni sustituir una decisión metodológica mediante edición de estilo. Cierre: protocolo aprobado y armonización posterior de la tabla. | Pendiente. |
| P02 | Mayor | `desarrollo2.tex` y `avance_objetivos.tex`: A2.5 y A3.1 conservan diferencias con el anteproyecto y ratificación académica pendiente. | No se presume aprobación. Cierre: ratificación documentada sobre notas, retiro administrativo e inactividad complementaria. | Pendiente previo, conservado. |
| P03 | Sugerencia | Documento completo: la revisión editorial no prueba comprensión efectiva de los lectores. | Cierre: lectura de ambos autores y comentarios concretos del asesor o revisores. | No verificable con la evidencia disponible. |
| P04 | Menor | Registro de LaTeX: advertencias de clase `thesis`, listas redefinidas por `tocbibind` y avisos de `minitoc`. | No hay errores de compilación, desbordamientos ni remisiones indefinidas. Una depuración de la plantilla requiere una tarea específica. | Limitación de plantilla, conservada. |

## Verificaciones y límites

Se compiló con `scripts/compilar_proyecto.ps1`: pdfLaTeX, BibTeX y tres pasadas adicionales, usando las fuentes activas. No se ejecutaron integradores ni migradores. El PDF final tiene 93 páginas.

La comparación automática con el respaldo confirmó conservación literal de los bloques matemáticos mostrados, de las cifras de las celdas de tablas, de las claves y cantidades de citas por archivo, de `biblio.bib` y de todas las imágenes referidas. Se comprobaron 87 etiquetas únicas, 114 remisiones con destino y 69 claves citadas distintas. El registro final no presenta errores LaTeX, desbordamientos `Overfull`, destinos duplicados ni referencias indefinidas. La evidencia reproducible está en `verificacion.json` y `scripts/verificar_redaccion_integral_2026_10_05.py`.

Se renderizaron todas las páginas con Poppler a 95 ppp. Se revisaron las ocho hojas de contacto y se ampliaron las páginas con fórmulas, Figura 3.4, cascada, diccionario y derivaciones. No se detectaron superposiciones, recortes ni pérdida de legibilidad en esas comprobaciones. Las páginas breves de modelos, SHAP y prototipo corresponden al estado pendiente del proyecto; no se completaron con resultados inexistentes.

No se reprodujeron análisis o notebooks ni se verificaron nuevamente las afirmaciones contra los artículos citados. Se conserva la evidencia de ejecuciones históricas sin atribuirla a esta sesión. No existe repositorio Git local detectado; no se hicieron commits ni actualizaciones remotas.

El siguiente paso es la lectura de los autores y la resolución documentada de P01 y P02 antes de armonizar la presentación del futuro protocolo predictivo.
