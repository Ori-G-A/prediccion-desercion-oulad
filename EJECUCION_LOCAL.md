# Ejecución local de los notebooks

Los notebooks activos están en la raíz de la carpeta del repositorio, no dentro de la carpeta `notebooks`.

## Abrir y ejecutar

1. Abrir `ABRIR_NOTEBOOKS.cmd` con doble clic desde el Explorador de archivos. Se inicia JupyterLab en el navegador con el Python del entorno `.venv`. No es necesario activar el entorno ni utilizar Overleaf.
2. Abrir `01_carga_exploracion.ipynb`. El kernel del entorno se identifica como **OULAD (.venv, Python 3.11)**. En el menú **Kernel**, elegir **Restart Kernel and Run All Cells** (reiniciar el kernel y ejecutar todas las celdas).
3. Esperar a que termine sin errores y guardar con **Ctrl+S**. Después, apagar su kernel mediante **Kernel → Shut Down Kernel** para liberar memoria.
4. Repetir el procedimiento con `02_feature_engineering.ipynb` y luego con `03_analisis_estadistico.ipynb`, uno a la vez. Cada uno depende de productos generados por el anterior.
5. Al terminar, guardar los notebooks y detener JupyterLab con **Ctrl+C** en la ventana desde la que se abrió; confirmar el cierre si se solicita. Cerrar únicamente la pestaña del navegador no necesariamente detiene el servidor.

Las celdas muestran `[*]` mientras están ocupadas. Si una celda produce un error rojo, no continuar con el siguiente notebook: conservar el mensaje y revisar la causa. Ejecutar una celda con Shift+Enter también es posible, pero para reproducir el análisis debe ejecutarse el notebook completo en orden y con el kernel reiniciado.

## Contenido y archivos

| Notebook | Trabajo que realiza |
|---|---|
| `01_carga_exploracion.ipynb` | Carga de las siete tablas originales, revisión de estructura, faltantes, duplicados y fechas; preparación de la base de auditoría. |
| `02_feature_engineering.ipynb` | Selección de inscripciones por corte y construcción de indicadores académicos, conductuales y temporales. |
| `03_analisis_estadistico.ipynb` | Estadística descriptiva, asociaciones, intervalos por remuestreo y análisis complementarios. |

El código auxiliar está en `src`. Los siete CSV se encuentran en `data/raw`; el archivo de interacciones ocupa aproximadamente 433 MiB. El tercer notebook incluye 5 000 remuestreos por persona y puede tardar considerablemente más que los anteriores; no se ha medido su duración en el nuevo entorno. No hay que ejecutar los tres simultáneamente.

Estos notebooks todavía no entrenan modelos predictivos ni ejecutan SHAP o el prototipo. Su ejecución no completa esas etapas pendientes.

## Resultados y conservación de la redacción

La versión analítica activa escribe en:

- `data/processed/correcciones_2026_09_10/`: bases e indicadores preparados.
- `reportes/correcciones_2026_09_10/tablas/`: resultados CSV.
- `reportes/correcciones_2026_09_10/figuras/`: figuras.

Al repetir la ejecución se reemplazan los resultados de esa versión. Guardar un respaldo de esas carpetas antes de ejecutar si se desea conservar una comparación completa. Los CSV originales no se modifican. Guardar un notebook también reemplaza sus salidas visibles anteriores.

**Para correr los notebooks no se debe ejecutar `scripts/integrar_correcciones.py`.** Ese generador reconstruye capítulos desde versiones anteriores y puede sobrescribir las correcciones de redacción realizadas el 30 de septiembre. Tampoco es necesario regenerar ni compilar la tesis para ejecutar el análisis.

El archivo `README_REVISION.md` conserva instrucciones históricas y de generación del documento. Para abrir y correr los notebooks, utilizar esta guía.

## Entorno y reproducción de la instalación

El entorno aislado es `.venv`, creado con Python 3.11.9. Las versiones del análisis son las de `requirements-revision.txt`; `requirements-local.txt` añade JupyterLab e ipykernel. `requirements-local-lock.txt` registra las dependencias instaladas, incluidas las indirectas.

El kernel se instala dentro del propio entorno; no se modifica el Python general. Si se utiliza VS Code, seleccionar `.venv\Scripts\python.exe` como entorno del notebook. El archivo de apertura utiliza rutas relativas y establece la raíz del proyecto automáticamente.

Para reinstalar en otro equipo Windows con Python 3.11, abrir PowerShell en la raíz del proyecto:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-local-lock.txt
.\.venv\Scripts\python.exe -m ipykernel install --prefix .venv --name python3 --display-name "OULAD (.venv, Python 3.11)"
```

Después se puede utilizar `ABRIR_NOTEBOOKS.cmd`. La reinstalación requiere acceso a PyPI; no se necesita conexión para ejecutar con las dependencias y los datos ya instalados. No copiar `.venv` a otro equipo: recrearlo con los comandos anteriores.

## Alcance de la comprobación

La preparación del entorno no equivale a una ejecución completa de los tres notebooks. Las comprobaciones efectivamente realizadas se registran en `reportes/entorno_local_2026_09_30/verificacion.json`; las salidas anteriores de los notebooks conservan su procedencia original.
