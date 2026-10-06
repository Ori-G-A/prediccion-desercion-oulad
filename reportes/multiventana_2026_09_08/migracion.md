# Guía de migración de la versión multiventana

Los tres informes están preparados como documentos individuales y bloques LaTeX sin preámbulo. La plantilla definitiva no se ha modificado. La autorización del usuario permite adoptar los cinco cortes en esta versión; no se atribuye una aprobación institucional adicional.

| Objetivo y actividad | Evidencia ejecutada | Bloque del informe | Destino propuesto |
|---|---|---|---|
| O1: comprensión y calidad | Notebook 01; fuentes, claves, fechas, faltantes y sensibilidad de repeticiones | 01, secciones 1–6 | `desarrollo1.tex`, caracterización y calidad |
| O2: delimitación temporal | Notebook 02; decisión temporal, flujos y transiciones | 02, secciones 1–2 | `desarrollo2.tex`, población, evento y ventanas |
| O2: construcción y consolidación | Notebook 02; diccionario, disponibilidad y conjuntos por corte | 02, secciones 3–4 | `desarrollo2.tex`, indicadores y reproducibilidad |
| O1/O2: exploración estadística | Notebook 03; descriptivos, efectos e intervalos, categorías | 03, secciones 1–3 | Métodos en metodología; resultados de caracterización en `desarrollo1.tex` |
| O2: diagnóstico y comparación temporal | Notebook 03; Spearman, VIF, PCA, MCD y cohorte común | 03, secciones 4–6 | `desarrollo2.tex`, diagnóstico de indicadores y límites |

## Procedimiento

1. Migrar por bloques desde `informes/*_contenido.tex`; conservar los documentos autónomos como respaldo. No insertar los preámbulos ni duplicar sus bibliografías.
2. Distribuir métodos, resultados y discusión según la estructura institucional. Sustituir los bloques históricos repetidos; no añadir estos informes al final de las duplicaciones existentes.
3. Copiar las figuras referidas y adaptar `../figuras/`. Mantener las etiquetas `rev01:` y `multi01:`, `multi02:`, `multi03:` o actualizar simultáneamente todas las remisiones.
4. Integrar `referencias_revision.bib`, conservando una sola entrada de `sdata2017171`. Verificar las demás claves contra la bibliografía de la plantilla.
5. Mantener la unidad inscripción y distinguir personas. La tabla apilada no es una muestra de observaciones independientes. Adoptar días 0..t inclusive y evento t < retiro <= final de presentación; no recuperar las cifras históricas de 0..27 como si fueran del nuevo corte 28.
6. Mantener la inactividad como indicador complementario; no convertirla en un segundo evento de abandono. Las calificaciones permanecen fuera de los candidatos por disponibilidad no verificable.
7. Diferenciar el análisis principal de la sensibilidad de cohorte común: esta última exige supervivencia hasta 56 y no representa una alerta operativa en los primeros cortes.
8. Compilar la plantilla completa y comprobar cifras, referencias, etiquetas y páginas después de la integración.

## Cifras y trazabilidad

Los resúmenes y CSV de esta carpeta constituyen la referencia de la versión. `02_comparacion_cortes.csv` contiene los denominadores principales; `02_enlace_corte28.csv` explica el cambio frente a la versión anterior. Los intervalos puntuales están en `03_efectos.csv` y los tamaños observados en `02_disponibilidad.csv` y `03_descriptivos.csv`.

El contenido de auditoría que permanece invariable se conserva de la revisión anterior, después de repetir los cálculos con las mismas fuentes. El generador comprueba la identidad de las huellas antes de reutilizar ese contenido. Las interpretaciones corresponden a esta versión y requieren revisión si cambian las fuentes o la definición temporal; no basta con recompilar.

O1 y O2 cuentan con evidencia reproducida para esta fase. El cierre académico completo permanece parcial hasta integrar y revisar el documento; no se han completado aquí O3 (modelos), O4 (SHAP) ni O5 (prototipo). La elección de una ventana óptima requiere validación predictiva posterior y valoración de la anticipación disponible.
