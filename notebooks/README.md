# Notebooks históricos y flujo vigente

Esta carpeta contiene **los tres notebooks vigentes**, en este orden:

1. [01_carga_exploracion.ipynb](01_carga_exploracion.ipynb): carga y exploración de los datos.
2. [02_feature_engineering.ipynb](02_feature_engineering.ipynb): construcción de indicadores.
3. [03_analisis_estadistico.ipynb](03_analisis_estadistico.ipynb): análisis estadístico exploratorio.

Desde la raíz del proyecto, `python scripts/ejecutar_notebooks.py` ejecuta esos tres archivos de `notebooks/`. En JupyterLab se pueden abrir directamente desde esta carpeta; la celda inicial encuentra la raíz del proyecto y sus datos recorriendo los directorios superiores, o mediante `OULAD_ROOT`.

Los cuatro archivos de `historico_2026_09_06/` corresponden a la versión anterior del repositorio, conservada al incorporar las modificaciones locales de septiembre y octubre. Incluyen `03b_verificacion_v2.ipynb`, que no forma parte del flujo vigente. Sus contenidos y salidas pueden diferir de los actuales porque pertenecen a otra etapa del trabajo; no deben combinarse con el análisis vigente ni interpretarse como una ejecución reciente.

La conservación histórica permite comparar etapas sin sobrescribir los originales. Para continuar el proyecto, editar y ejecutar únicamente los tres notebooks situados directamente en `notebooks/`, sin ejecutar los de la subcarpeta histórica.
