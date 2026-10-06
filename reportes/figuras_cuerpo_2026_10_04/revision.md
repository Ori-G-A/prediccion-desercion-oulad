# Integración de figuras y ajuste de paleta

Versión: 4 de octubre de 2026. Revisión puntual autorizada por los autores.

La versión incorpora ocho figuras al cuerpo del trabajo, conserva las tablas existentes y restaura la imagen original de las tablas y relaciones de OULAD. El azul institucional permanece como color principal, acompañado de azul verdoso, azules derivados y grises. El amarillo se retiró de los elementos propios. La imagen original de OULAD conserva sus colores por solicitud expresa.

## Cambios y evidencia

| Ubicación | Cambio | Evidencia y estado |
|---|---|---|
| Figuras 3.6 a 3.9; páginas impresas 32 a 34 | Barras de edad, discapacidad registrada, IMD y región al corte 28, con denominadores. | Integradas con introducción, interpretación y referencia a la Tabla 9.2 del Anexo 9.2. |
| Figuras 3.10 y 3.11; páginas impresas 35 y 36 | Matrices de porcentajes de contexto en los cinco cortes, con escala común. | Integradas; se explican los cambios de población y horizonte. |
| Figura 3.5; página impresa 31 | Matriz de V de Cramér de las ocho variables publicadas. | Cotejadas las 40 celdas con la Tabla 3.9. |
| Figura 4.8; página impresa 53 | Relación de ambos CV con la proporción de días activos. | Diez correlaciones cotejadas con la Tabla 4.8; ambas series usan los mismos casos dentro de cada corte. |
| Figura 9.1; página impresa 68 | Restitución de `model.png`. | Imagen idéntica a la original conservada; referencia bibliográfica restaurada. |
| Figuras previas, diagramas y notebooks | Sustitución del amarillo por tonos que acompañan al azul. | Generadores compartidos y metadatos actualizados; guía `ESTILO_VISUAL.md`. |

Se priorizaron comparaciones donde una figura facilita reconocer diferencias entre grupos o patrones entre cortes. Las tablas de auditoría, definiciones, flujos y sensibilidad conservan su detalle. No se añadió una figura por cada tabla, pues algunas tienen como función principal documentar procedimientos y valores exactos.

## Verificación

El documento pasó de 13 a 21 figuras. La comparación de los archivos LaTeX confirmó que todos los bloques de tablas preexistentes conservan su contenido. Se mantuvieron las huellas SHA-256 de 71 archivos de datos procesados y tablas analíticas. Las 145 celdas de contexto se cotejaron con el anexo y los porcentajes se comprobaron a partir de sus numeradores y denominadores.

Los generadores gráficos se ejecutaron desde las salidas guardadas; no se repitieron los notebooks completos ni se ajustaron modelos. El código de las celdas de los tres notebooks se conservó en esta revisión; se actualizaron sus gráficos mediante las funciones compartidas. Se verificó la sintaxis de los módulos y scripts modificados.

El PDF final contiene 91 páginas y compiló sin errores, referencias indefinidas ni avisos `Overfull`. Persisten los avisos previos de la plantilla sobre la clase, los índices y la conversión EPS, sin impedir la compilación. Las páginas se renderizaron con Poppler y se inspeccionaron en conjunto; las ocho figuras nuevas, los encabezados afectados, el esquema original y las láminas se revisaron ampliados. Se corrigió el encabezado de créditos e intentos previos para mantenerlo junto a su tabla.

Los registros `verificacion_figuras.json`, `verificacion_regeneracion.json`, `verificacion_conservacion.json` y `verificacion_compilacion.json` documentan las comprobaciones. El respaldo previo se encuentra en `respaldo/2026-10-04_pre_figuras_cuerpo`.

## Hallazgos y pendientes de esta versión

| Severidad | Hallazgo | Corrección o seguimiento |
|---|---|---|
| Menor, cerrado | Amarillo no deseado en los elementos propios. | Configuración común azul y azul verdoso; imágenes y PDF regenerados. |
| Menor, cerrado | Figuras de contexto separadas del análisis principal. | Seis figuras de impresión integradas en la sección 3.9, con remisiones al anexo. |
| Menor, cerrado | Esquema de elaboración propia no aceptado por los autores. | Imagen original de OULAD restituida. |
| Menor, cerrado | Encabezado separado de su tabla tras insertar figuras. | Reserva de espacio antes de la subsección 3.9.4 y nueva inspección de la página. |
| Sugerencia, pendiente previo | La tabla de niveles del anexo cubre cuatro variables; módulo, presentación, género y educación previa solo cuentan aquí con el resumen de asociación. | Se conserva el alcance editorial existente; ampliar sus tablas por nivel requerirá una edición posterior. |

La revisión no determina cumplimiento de una rúbrica aún no aportada ni aprobación del asesor. Las asociaciones y porcentajes siguen siendo descriptivos; no se atribuye causalidad, significancia nueva, equidad predictiva o superioridad de un corte.
