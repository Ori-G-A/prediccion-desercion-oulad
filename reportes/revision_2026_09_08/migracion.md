# Preparación para migrar a la plantilla definitiva

Los informes se entregan como documentos independientes y como contenidos sin
preámbulo. La plantilla final no se modificó en esta fase.

| Objetivo y actividad | Notebook y evidencia | Contenido de informe | Destino propuesto |
|---|---|---|---|
| O1, A1.1–A1.2: fuente y calidad | 01; dimensiones, claves, rangos, huellas, faltantes | 01, secciones 1–4 | `desarrollo1.tex`: caracterización de fuentes y calidad |
| O1/O3: definición administrativa | 01; momento del retiro y discordancias | 01, sección 5 | `desarrollo1.tex`: variable de interés, remisión al contrato temporal |
| O2, A2.1–A2.2: población y ventana | 02; flujo de exclusiones y sensibilidad del evento | 02, secciones 1–2 | `desarrollo2.tex`: unidad de análisis, población, ventana y horizonte |
| O2, A2.3–A2.6: indicadores | 02; panel diario, calendario, diccionario | 02, secciones 3–5 y 7 | `desarrollo2.tex`: construcción de variables y tratamiento de faltantes |
| O2, A2.7: consolidación | 02; archivos de predictores, objetivo y auditoría | 02, secciones 6 y 8 | `desarrollo2.tex`: consolidación, verificaciones y decisiones |
| O1/O2: exploración estadística | 03; descriptivos, faltantes, efectos y categorías | 03, secciones 1–5 | `desarrollo1.tex`: resultados de caracterización; evitar repetir métodos |
| O2: redundancia y estructura conjunta | 03; Spearman, VIF, ACP y MCD | 03, secciones 6–7 | `desarrollo2.tex`: diagnóstico de indicadores; no llamarlo selección final |

## Procedimiento de migración

1. Conservar los wrappers `.tex` para reproducir los informes autónomos. Migrar los
   archivos `*_contenido.tex` por bloques lógicos, no los preámbulos ni los títulos.
2. Reubicar métodos y resultados según la organización institucional. Las referencias
   a notebooks pueden pasar a anexos de reproducibilidad. No duplicar el análisis
   estadístico completo en dos capítulos.
3. Copiar las figuras citadas y adaptar sus rutas desde `../figuras/`. Conservar las
   etiquetas `rev01:`, `rev02:` y `rev03:` o actualizarlas junto con todas sus remisiones.
4. Integrar `referencias_revision.bib` con la bibliografía final. La clave
   `sdata2017171` ya existe en la plantilla: conservar una única entrada verificada.
   Las demás claves llevan prefijo `rev` para evitar colisiones.
5. Sustituir los bloques repetidos de `desarrollo1.tex`; no añadir los informes al
   final de las duplicaciones existentes. Corregir en `desarrollo2.tex` la afirmación
   de unidad «curso» y la adopción automática de dos etiquetas.
6. Mantener explícito el estado provisional de la definición temporal hasta su
   ratificación. No presentar el uso de una ventana como comparación de varias.
7. Compilar la plantilla, verificar citas, etiquetas, tablas y figuras, y revisar
   las páginas completas después de adaptar el contenido.

## Cifras y productos de referencia

Los valores a migrar deben provenir de `01_resumen.json`, `02_resumen.json`,
`03_resumen.json` y los CSV de tablas de esta misma versión. No reutilizar cifras
del dataset v1 o v2 histórico. Las tablas LaTeX se generan desde estos archivos;
la redacción contiene interpretaciones específicas de esta versión y debe revisarse
si cambia la población, incluso cuando el generador pueda volver a compilar.

La transferencia deja O1 y O2 con evidencia reproducida, pero su cierre académico
depende de las decisiones pendientes. No completa O3 (modelos), O4 (SHAP) ni O5
(prototipo). Los informes no afirman que esas etapas se hayan ejecutado.
