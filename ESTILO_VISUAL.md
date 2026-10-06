# Identidad visual del proyecto

Versión vigente: 5 de octubre de 2026. Mantiene la sustitución del amarillo y precisa el estilo de la Figura 3.4 solicitado por los autores.

Esta guía desarrolla la presentación de la sección 3 del AGENTS.md principal. Los registros anteriores describen versiones históricas; sus paletas y propuestas sustituidas no se aplican al regenerar figuras vigentes. La regla específica de la Figura 3.4 prevalece sobre la combinación general de trazos y marcadores. Los cambios de estilo permanentes deben actualizar esta guía y su implementación correspondiente, con registro de la decisión.

El documento, las figuras y los notebooks deben mantener una identidad visual común. Se conserva el azul de la Pontificia Universidad Javeriana Cali como color principal, acompañado de azul verdoso, azules derivados, blanco y grises. Estos colores complementarios corresponden a decisiones editoriales del proyecto; no se presentan como parte de la paleta institucional.

## Paleta y usos

| Elemento | Color | Uso |
|---|---|---|
| Azul institucional | `#2C5697` | Encabezados, datos principales, líneas de tablas y diagramas. |
| Azul verdoso | `#347B83` | Resaltados puntuales y una serie de comparación cuando corresponda. |
| Azul oscuro | `#263C54` | Serie complementaria y énfasis cuando se requiera. |
| Blanco | `#FFFFFF` | Fondo general y separación entre elementos. |
| Negro institucional | `#000000` | Referencia de identidad; texto o contraste cuando se requiera. |
| Texto y tonos neutros | `#202020`, `#595959`, `#B8BDC5`, `#E3E5E8` | Texto, referencias, datos sin disponibilidad y rejillas discretas. |

Los tonos neutros y las mezclas de azul con blanco son recursos de visualización del proyecto, no colores institucionales adicionales. No se utiliza amarillo en los gráficos ni en los elementos editoriales propios. Las imágenes originales de fuentes externas conservan su apariencia cuando así se solicite, como sucede con el esquema OULAD.

Fuente de los valores institucionales: Pontificia Universidad Javeriana Cali, *Manual de Identidad*, página impresa 43; fuente de la recomendación tipográfica, página impresa 39. [Manual oficial](https://www.javerianacali.edu.co/sites/default/files/2024-10/Manual%20de%20Identidad_Javeriana-Cali.pdf).

## Reglas comunes

Las figuras usan Arial cuando está disponible, con DejaVu Sans como alternativa declarada. El texto académico y las ecuaciones conservan la tipografía de la plantilla; los diagramas TikZ usan su familia sin remates. Se mantiene una jerarquía estable de títulos, etiquetas y notas, aunque el tamaño se adapte al espacio de publicación.

El azul representa la información principal. El azul verdoso dirige la atención hacia una comparación explicada en el título o en la nota; el resaltado no constituye evidencia de significancia estadística. Las comparaciones con varias series combinan colores, trazos y marcadores. Las matrices de porcentajes usan una escala secuencial de azul claro a oscuro, con etiquetas de contraste calculado. No se emplean colores distintos para cada categoría si no cumplen una función explicativa.

Las barras parten de cero. Los gráficos comparables conservan la escala cuando su lectura lo requiere. Cada figura identifica qué mide, su unidad, la población, el corte y las limitaciones pertinentes. Se distingue entre número de personas e inscripciones y entre retiro formal, resultado final e inactividad. Las cifras del estudio proceden de los archivos analíticos; el estilo no modifica estimaciones, intervalos ni denominadores.

La Figura 3.4 utiliza exclusivamente líneas continuas, sin marcadores ni etiquetas sobre las curvas. Los cinco cortes se distinguen con azul, verde azulado, violeta, naranja tostado y frambuesa; los mismos colores identifican cada corte en los dos paneles. Una leyenda común exterior permite asociar color y día de corte. Esta paleta complementaria mejora la separación de las curvas superpuestas y no representa colores institucionales adicionales. Los nombres de los ejes se conservan para explicar qué se compara.

El logotipo institucional y el esquema original de tablas y relaciones de OULAD se conservan como recursos originales. El anexo vuelve a utilizar `Plantilla_ProyAplicado/model.png`, con su referencia bibliográfica. El esquema alternativo de elaboración propia ya no se incluye en el documento. Los demás diagramas propios utilizan la paleta compartida.

Las figuras del cuerpo acompañan una explicación y remiten a la tabla correspondiente. Las tablas se conservan para consultar los valores exactos. Los gráficos de contexto se diseñan a 6,8 pulgadas de ancho, con etiquetas legibles a la anchura del documento; no se insertan las láminas de presentación reducidas como si fueran figuras de impresión.

## Implementación y reproducción

La configuración se centraliza en `estilo_visual_javeriana.json`. `src/estilo_visual.py` aplica la paleta y las fuentes; `src/figuras_oulad.py` contiene las figuras compartidas por los notebooks y la regeneración editorial. `Plantilla_ProyAplicado/estilo_visual.tex` aplica los colores al documento.

Para nuevas figuras de Python:

```python
from src.estilo_visual import apply_style, BLUE, ACCENT, line_style
apply_style()
```

Desde la raíz del proyecto, con el ambiente existente:

```powershell
& '.venv/Scripts/python.exe' 'scripts/actualizar_estilo_javeriana.py'
& '.venv/Scripts/python.exe' 'scripts/generar_ejemplo_cv.py'
& '.venv/Scripts/python.exe' 'scripts/figuras_cuerpo.py'
& '.venv/Scripts/python.exe' 'scripts/graficar_contexto_storytelling.py' --corte 28
```

El primer comando regenera siete figuras desde las salidas guardadas, actualiza sus imágenes en los notebooks y genera el tema LaTeX. No reproduce la ejecución analítica completa. Los otros comandos generan el ejemplo didáctico, las ocho figuras añadidas al cuerpo y las seis láminas de contexto. El esquema original no requiere regeneración. Después corresponde compilar el proyecto LaTeX y revisar el PDF a su tamaño final. No se instala ninguna dependencia con estos comandos.

Los scripts de figuras son la fuente de las nuevas salidas. Las copias históricas en `respaldo` y las propuestas visuales anteriores se conservan como evidencia de versiones; no son la referencia de estilo vigente.

## Orientación de comunicación

Se conserva el criterio solicitado de claridad, jerarquía visual, reducción de elementos innecesarios y contexto de los datos. Como orientación se reconocen Knaflic, C. N. (2015), *Storytelling with Data: A Data Visualization Guide for Business Professionals*, Wiley; y Yau, N. (2013), *Data Points: Visualization That Means Something*, Wiley. La consulta disponible fue de los recursos públicos de los autores, no de los libros completos ni de una edición alojada en LibGen: [Storytelling with Data](https://www.storytellingwithdata.com/blog/two-tips-for-better-graphs) y [Data Points](https://flowingdata.com/data-points/).
