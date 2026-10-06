# Integración de la revisión de claridad

Fecha: 30 de septiembre de 2026. Versión: 2, integrada en los capítulos 3 y 4.

Registro histórico: esta versión fue ampliada y corregida por `cotejo_pagina_por_pagina.md` (versión 3). Consultar ese archivo para el estado vigente de las anotaciones.

Se incorporó la propuesta de la sección 3.4 y se ampliaron las explicaciones de las secciones 3.8 y 4.1. También se revisaron las conexiones entre tablas, los registros repetidos, las variables de contexto y los porcentajes de retiro futuro de la sección 4.3. El alcance de esta entrega corresponde a los capítulos anotados; no constituye una reescritura integral de los restantes capítulos.

## Cambios

- Definiciones y ejemplos de inscripción, módulo, presentación, día de corte, seguimiento y retiro futuro.
- Explicación de información faltante, evaluaciones reconocidas, pesos, fechas negativas y registros posteriores al retiro.
- Denominadores explícitos en la tabla de faltantes, conservando los valores de las salidas guardadas.
- Explicación de los grupos, símbolos y signo del efecto biserial; ejemplo hipotético comprobable de cuatro pares, con efecto −0,5.
- Explicación del remuestreo por personas y de la construcción de los intervalos percentiles, contrastada con `cluster_effect_ci`.
- Orientación para leer las curvas acumuladas, la V de Cramér, la mediana y los cuartiles.
- Definiciones de IMD, créditos e intentos previos, y ejemplo del denominador del retiro futuro al día 28.
- Ajustes de espacios reservados, tabla de faltantes y ubicación de la figura comparativa de los CV. Se conservaron las figuras originales y sus datos.

## Pendientes por versión

Los identificadores remiten a la matriz de `propuesta_claridad.md`; las ubicaciones originales permiten reconocer los comentarios aunque cambie la paginación.

| ID | Severidad original | Estado en versión 2 | Evidencia o pendiente |
|---|---|---|---|
| C01 | Menor | Atendido parcialmente | Se separó el contexto de ejecución en un párrafo; no se trasladó al anexo. |
| C02 | Mayor | Atendido | Se añadió un ejemplo de una persona con dos inscripciones y se explicaron las claves. |
| C03 | Mayor | Atendido | Se distinguieron filas idénticas y claves repetidas; se aclararon encabezados y alcance de la comparación. |
| C04 | Mayor | Atendido | Se integró la reescritura completa y se añadieron denominadores. |
| C05 | Mayor | Atendido | Se explicó el día 28 de referencia, la información posterior al retiro y el límite sobre causas de faltantes. |
| C06 | Mayor | Atendido en redacción | Se aclararon Withdrawn y Fail; no se modificó la definición metodológica existente. |
| C07 | Menor | Atendido parcialmente | Se sustituyó «log»; puede desarrollarse más el detalle de los productos en un anexo. |
| C08 | Mayor | Atendido | Se explicaron grupos, fórmula, ejemplo y remuestreo por personas. |
| C09 | Mayor | Atendido parcialmente | Se añadió lectura de ejes y curvas; se conservó el diseño de los gráficos existentes. |
| C10 | Mayor | Atendido | Se aclararon IMD, créditos, intentos, cuartiles y unidad de la base integrada. |
| C11 | Mayor | Atendido | Se explicó el caso temporal antes de las fórmulas y se definieron los símbolos e indicadores. |
| C12 | Mayor | Atendido parcialmente | Se añadió el cálculo del porcentaje al día 28 y se ajustó la composición. La ratificación académica de diferencias frente al anteproyecto sigue pendiente, como indica el documento. |

«Atendido» indica que la corrección editorial está integrada; no sustituye la lectura de los autores ni una nueva comprobación empírica. La anotación general sin texto de referencia y los trazos de interpretación incierta permanecen pendientes de precisión.

## Validación y límites

Se utilizó el script existente `scripts/compilar_proyecto.ps1`, pues el proyecto LaTeX depende de múltiples archivos, una clase institucional, bibliografía y figuras. Se revisaron referencias, claves bibliográficas y ecuaciones destacadas. Los resultados se registran en `verificacion_integracion.json`. Se renderizaron páginas de los capítulos afectados para revisar tablas, fórmulas y figuras; se corrigieron un desbordamiento vertical y la partición inicial de la tabla de faltantes.

Las cifras proceden de las salidas guardadas consultadas en la propuesta. No se ejecutaron los notebooks ni se modificaron los modelos, los filtros o los datos. La revisión no certifica la corrección integral de los análisis estadísticos ni la aprobación de cambios de alcance.

Se conservaron originales de los archivos modificados y del PDF anterior en `respaldo/2026-09-30_pre_anotaciones`. La carpeta de trabajo no es un repositorio Git local; no se crearon commits.

Archivos fuente modificados: `Plantilla_ProyAplicado/desarrollo1.tex`, `desarrollo2.tex`, `ejemplo_cv.tex` y `proyecto.tex`. También se regeneraron los archivos auxiliares de compilación y `proyecto.pdf`.
