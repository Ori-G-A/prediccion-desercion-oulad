# Trabajo compartido con Git

Repositorio común: Ori-G-A/prediccion-desercion-oulad. La edición, ejecución y compilación pueden hacerse localmente; Git registra cambios y GitHub permite compartirlos.

1. Clonar el repositorio en una carpeta nueva, sin sobrescribir el espacio local de trabajo.
2. Antes de una tarea, revisar `git status`, actualizar `main` con `git pull --ff-only` y crear una rama.
3. Trabajar sobre las fuentes activas. Revisar `git diff` y seleccionar archivos; no agregar datos crudos, entornos, libros ni respaldos.
4. Ejecutar las comprobaciones pertinentes y registrar qué se ejecutó y qué sigue pendiente.
5. Crear commits descriptivos, subir la rama y abrir una propuesta de cambios hacia `main`.
6. Integrar después de revisar. Si ambos autores cambian el mismo notebook, reconciliar su código y salidas antes de sustituirlo; no resolver conservando automáticamente una de las copias.

La rama `actualizacion/avance-local-2026-10-06` reúne la etapa local para revisión. No cambia por sí sola `main`. No modificar ni borrar la bitácora histórica: añadir una entrada que explique el cambio de decisión.

La carpeta original de trabajo permanece separada del clon preparado durante esta integración. Hasta elegir una carpeta activa de Git para el trabajo cotidiano, no asumir que una edición en la carpeta original aparece automáticamente en GitHub.
