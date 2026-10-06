# Comparación del repositorio y la versión local

Fecha: 6 de octubre de 2026. Repositorio: https://github.com/Ori-G-A/prediccion-desercion-oulad. Referencia examinada: main, commit ec19d357b004397fd3d2ec49aeb02211d8c03012. Consulta mediante conector GitHub y clon independiente sin checkout en tmp/revision_repo_oriana_2026_10_06. No se modificó el remoto ni se vinculó la carpeta activa a Git.

## Veredicto

Se recomienda conservar el repositorio de Oriana como repositorio compartido del proyecto. Mantiene el historial de ambos autores y las decisiones iniciales; la cuenta LuisJRubioH dispone de lectura y escritura, aunque no de administración. Crear otro repositorio desde cero separaría innecesariamente la etapa inicial de los cambios locales. Trabajar localmente y usar GitHub son actividades compatibles: se puede editar y verificar en el equipo, registrar versiones con Git y sincronizar después.

## Evidencia histórica

Se encontraron 15 commits alcanzables desde main: 12 de junio a 6 de septiembre de 2026. Estas son fechas registradas en Git; no acreditan por sí solas el día exacto de ejecución o finalización de una actividad.

| Periodo registrado | Evidencia | Relación con el avance |
|---|---|---|
| 12 de junio | bf7d3143 y a0a22c84: inicio y estructura CRISP-DM, de Oriana | Organización inicial y bitácora. |
| 8-10 de julio | Dependencias, carga, exploración e ingeniería inicial, de Luis | Trabajo previo al inicio del semestre; no debe omitirse del historial. |
| 11 de agosto | Actualizaciones de notebooks 01-03, auditoría y dependencias | Desarrollo de caracterización e indicadores. |
| 5-6 de septiembre | Ingeniería v2, CV, multicolinealidad, integración de EDA y exclusión de un intermedio | Última etapa registrada en main antes de las revisiones locales posteriores. |

La bitácora docs/bitacora.md contiene cuatro entradas fechadas el 5 y 6 de junio, incorporadas a Git el 12 de junio. Tratan CRISP-DM, definición dual de abandono, categorías de variables y tratamiento condicional del desbalance. Es un registro de decisiones, no un diario completo de actividades; sus fechas internas se distinguen de las fechas de commit. No tiene entradas de la etapa local posterior.

Las ramas de modelado, SHAP y prototipo apuntan al mismo commit antiguo aef29715; su nombre no demuestra implementación de esas fases. Al comparar todos los refs descargados con main, el único commit adicional corresponde a una actualización de dependencias de Dependabot, no a nuevos resultados del proyecto.

## Cambios comprobados entre el remoto y lo local

| Componente | Remoto revisado | Versión local vigente |
|---|---|---|
| Notebooks | Tres notebooks principales y 03b de verificación v2 | Los tres principales tienen código diferente y apoyan su ejecución en módulos de src; 03b no está en la raíz activa. Debe conservarse como antecedente al integrar. |
| Ventana temporal | Notebook 02 declara una ventana de días 0 a 27 | Cinco cortes 7, 14, 28, 42 y 56, con observación inclusiva 0..t. |
| Evento y población | Notebook 02 define abandono mediante fecha de retiro no nula y conserva la base completa para su auditoría | Elegibilidad por corte y retiro posterior hasta el final de la presentación; los retiros ya ocurridos quedan fuera de la población de predicción. |
| Candidatos | 03b construye una selección de 27 columnas, con criterios de la v2 | 26 indicadores candidatos, contexto separado, notas y conteo de filas solo para auditoría. No son conjuntos equivalentes ni la diferencia de tamaño mide mejora predictiva. |
| Variabilidad | CV de calendario corregido en la v2 remota | Se conserva CV de calendario y se añade CV activo con comparación y límites explícitos. |
| Verificación | Auditoría y verificaciones anteriores guardadas | Scripts independientes y registros versionados; 49 comprobaciones reejecutadas el 6 de octubre. No se repitió la ejecución analítica en esta comparación. |
| Documento | El árbol de main no contiene Plantilla_ProyAplicado ni fuentes .tex del documento | Fuentes activas, bibliografía, figuras, PDF de 94 páginas y paquete para revisión del director. |
| Seguimiento | Bitácora inicial sin actualización posterior | Reportes de correcciones, decisiones, estilo y revisión hasta el 6 de octubre. |

Los cambios se comprobaron con el código de los notebooks remotos, src/ventanas_oulad.py, src/oulad_revision.py, decision_temporal.json y los registros locales. Se guardaron extracciones y diferencias de código de los tres notebooks, inventario resumido e historial en esta carpeta. No se ejecutaron los notebooks remotos ni se validaron sus afirmaciones numéricas antiguas como resultados vigentes.

## Hallazgos y condiciones de integración

| ID | Severidad | Evidencia | Acción propuesta |
|---|---|---|---|
| G01 | Mayor | Remoto con última versión de septiembre; fuentes y análisis posteriores solo locales | Incorporar cambios en una rama de actualización conservando main hasta revisar la comparación. |
| G02 | Mayor | README y bitácora conservan definiciones históricas; decision_temporal.json documenta cambios posteriores | Actualizar README y añadir entradas fechadas que expliquen qué decisiones se sustituyeron; conservar las entradas originales. |
| G03 | Menor | Notebooks en notebooks/ remotamente y en raíz localmente | Elegir una ubicación activa al integrar y adaptar rutas; evitar dos copias divergentes. No mover archivos como parte de esta revisión. |
| G04 | Mayor | .gitignore local solo excluye entorno y cachés | Preparar exclusiones para datos, respaldos, temporales, libros y archivos de compilación antes de publicar. Seleccionar explícitamente los productos reproducibles. |
| G05 | Menor | 03b remoto no está en la raíz local y existe un commit de dependencias no integrado | Conservar 03b como histórico y evaluar la actualización de dependencias por separado. No borrar ni incorporar automáticamente. |

## Aclaración del cronograma comunicada por los autores

El usuario informó que Oriana construyó el cronograma desde el 27 de julio de 2026; la meta es terminar en mayo de 2027 trabajando durante el receso. También comunicó que el director permite revisarlo al finalizar el semestre según el avance. Esta información sustituye el estado de «inicio desconocido» del paquete preparado antes de esas aclaraciones, sin convertir las nuevas fechas estimadas en un calendario detallado aprobado.

Como correspondencia propuesta, diez bloques mensuales consecutivos abarcan del 27 de julio de 2026 al 26 de mayo de 2027: M1 27/07-26/08; M2 27/08-26/09; M3 27/09-26/10; M4 27/10-26/11; M5 27/11-26/12; M6 27/12-26/01; M7 27/01-26/02; M8 27/02-26/03; M9 27/03-26/04; M10 27/04-26/05. El 6 de octubre corresponde a M3 bajo esta convención. El trabajo de junio y julio se registra como antecedente; no cambia automáticamente el inicio previsto del cronograma ni permite inferir adelanto global.

Los PDF del paquete anterior todavía no incorporan esta nueva información. Su actualización debe incluir estas fechas estimadas, los hitos del curso de octubre y noviembre y una revisión de la planificación al cierre del semestre. La fecha exacta de esa revisión y los responsables por actividad siguen por acordar.

## Siguiente paso propuesto

Preparar una rama de actualización en el repositorio existente, incorporar selectivamente el estado local, actualizar bitácora y documentación, ejecutar las verificaciones y presentar la comparación antes de integrar en main. Preservar la licencia y el historial existentes. Esta revisión no ha creado ramas, commits, pull requests ni publicaciones remotas.
