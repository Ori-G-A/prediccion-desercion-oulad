# Predicción temprana del retiro estudiantil con OULAD

Proyecto aplicado de la Maestría en Ciencia de Datos, PUJ Cali. Autores: Oriana Giraldo Arcia y Luis Javier Rubio Hernández.

## Estado de esta versión

Actualización del 22 de octubre de 2026: se completaron las búsquedas de cinco familias (3.200 ajustes de validación cruzada), la selección por validación, la calibración, los umbrales y la evaluación final congelada. Se calcularon 500 explicaciones SHAP y se implementó un prototipo local. **El cierre técnico del modelado no equivale al cierre académico: siguen pendientes la revisión con el asesor y la evaluación del prototipo con usuarios.**

- [PDF actualizado del proyecto](Plantilla_ProyAplicado/proyecto.pdf).
- [Reporte breve para la reunión](output/pdf/Avance_breve_modelado_reunion_22_octubre_2026.pdf).
- [Resultados y métricas explicadas](output/pdf/Reporte_entrenamiento_metricas_asesor_22_octubre_2026.pdf).
- [Prototipo autónomo](prototipo/OULAD.html): descargar y abrir en un navegador; GitHub muestra el código, no ejecuta el HTML.
- [Seguimiento del cronograma](reportes/seguimiento_cronograma_2026_10_21/estado.md).

La unidad es la inscripción (persona, módulo y presentación). Se utilizan los cortes 7, 14, 28, 42 y 56, con observación desde el día 0 hasta el corte inclusive. Se incluyen inscripciones matriculadas y sin retiro hasta el corte, cuyo curso continúa. El evento es el retiro registrado posterior al corte y hasta el final de la presentación. Las notas se conservan solo para auditoría; la inactividad es un indicador complementario. La ratificación académica de estas delimitaciones sigue pendiente. Detalle: [decisión temporal](decision_temporal.json).

## Archivos activos

| Contenido | Ubicación |
|---|---|
| Tres notebooks, en orden de ejecución | `notebooks/01_carga_exploracion.ipynb`, `notebooks/02_feature_engineering.ipynb`, `notebooks/03_analisis_estadistico.ipynb` |
| Funciones de análisis y figuras | `src/` |
| Fuentes vigentes del documento y PDF compilado | `Plantilla_ProyAplicado/` |
| Tablas, figuras y evidencia analítica | `reportes/correcciones_2026_09_10/` |
| Verificaciones y revisión del avance | `reportes/entrega_avance_2026_10_06/` |
| Decisiones e historial | [Bitácora](docs/bitacora.md) |
| Cronograma estimado actualizado | [Cronograma](docs/cronograma_estimado.md) |
| Flujo de colaboración | [Trabajo con Git](docs/trabajo_con_git.md) |

Los notebooks de `notebooks/historico_2026_09_06/`, las figuras de `reportes/figs/` y el antiguo parquet ya versionado en `data/processed/` son antecedentes. No representan el análisis vigente. Los informes fechados conservan su contexto; el cronograma del paquete inicial del 6 de octubre fue preparado antes de la aclaración de los autores y debe leerse junto con el cronograma estimado actual. No se publica su PDF anterior como cronograma vigente.

## Reproducción

1. Instalar Python 3.11 y crear un entorno virtual. Instalar `requirements-local-lock.txt` para el entorno con Jupyter, o `requirements-revision.txt` para el análisis. La lista antigua de dependencias se conserva en `docs/historico_2026_09_06/requirements.txt`.
2. Obtener OULAD desde su [fuente oficial](https://analyse.kmi.open.ac.uk/open_dataset) y colocar sus siete CSV sin modificar en `data/raw/`. Las huellas del conjunto local revisado están en `reportes/correcciones_2026_09_10/fuentes.json`; su existencia no certifica el origen histórico de descarga.
3. Desde la raíz ejecutar `python scripts/ejecutar_notebooks.py`. Genera los archivos procesados ignorados por Git y actualiza las salidas guardadas. El tercer notebook utiliza 5.000 remuestreos y puede tardar; respaldar los productos antes de repetirlo.
4. Ejecutar `python scripts/verificar_entrega_2026_10_06.py`. Requiere los productos procesados del paso anterior. La ejecución actual de comprobaciones no implica que todos los notebooks se hayan repetido en esta integración.

Los notebooks encuentran la raíz mediante `OULAD_ROOT` o desde el directorio de trabajo. No subir los CSV, nuevos parquet, entornos o respaldos. Las guías personales de trabajo (`AGENTS.md`, `EJECUCION_LOCAL.md` y `ESTILO_VISUAL.md`) se conservan localmente y están excluidas del seguimiento de Git.

Para compilar las fuentes vigentes, usar `./scripts/compilar_proyecto.ps1`, con MiKTeX instalado. Se puede indicar `-PdfLatex` y `-BibTex`, o disponer de ambos ejecutables en PATH. No se instalan paquetes automáticamente. **No ejecutar integradores o migradores históricos sobre las fuentes actuales:** pueden recuperar texto anterior y eliminar correcciones posteriores. Los scripts históricos de revisión que comparan con `respaldo/` requieren los respaldos locales, que no se publican.

## Evidencia y límites

Los registros analíticos del 10 de septiembre y la revisión editorial del 5 de octubre se conservan como evidencia histórica. El 6 de octubre se reejecutaron 49 comprobaciones independientes; tres de ellas inspeccionan salidas guardadas de notebooks, sin reejecutarlos. La integración al repositorio conserva cifras y decisiones y registra su propia comprobación en `docs/validacion_integracion_2026_10_06.json`.

La fuente completa fue explorada previamente, antecedente documentado. Posteriormente se fijó la generalización a personas nuevas en ofertas disponibles y se conservaron particiones por persona. La prueba del paquete congelado se abrió el 21 de octubre; no se reutiliza para volver a seleccionar modelos ni umbrales. La capacidad discriminativa observada es limitada y no se demuestra utilidad institucional ni reducción del abandono.

## Alcance de la publicación y reproducción del modelado

Se publican código, configuraciones, resultados agregados, fuentes del documento y reportes. Se conservan localmente los CSV crudos, las particiones individuales, predicciones por inscripción, réplicas y modelos binarios; no se añaden esos archivos al repositorio. El prototipo exporta casos sin identificadores de estudiantes. Los manifiestos conservan rutas y huellas de la ejecución original: clonar el repositorio permite consultar los resultados y abrir el prototipo, pero no equivale a disponer de todos los artefactos para repetir su auditoría.

El orden de ejecución está en [el protocolo](PROTOCOLO_EJECUCION_MODELOS.md). Las dependencias adicionales están en `requirements-modelado.txt` y `requirements-interpretacion.txt`. Los scripts de verificación integral requieren los artefactos locales referenciados. No se afirma haber repetido los 3.200 ajustes durante esta publicación.
