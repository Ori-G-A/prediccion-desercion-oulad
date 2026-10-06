# Versión documental para revisión del director: 6 de octubre de 2026

El paquete vigente para la primera entrega está en `reportes/entrega_avance_2026_10_06/LEER_PRIMERO.md`: PDF de avance, informe del cronograma y consultas para el director. La actividad cierra el 19 de octubre a las 23:59. La revisión del director y los acuerdos de calendario siguen pendientes; no se ha enviado el paquete ni realizado la entrega.

Las fuentes activas están en `Plantilla_ProyAplicado`; la versión analítica sigue siendo `correcciones_2026_09_10`. Se reejecutaron 49 verificaciones independientes el 6 de octubre, sin repetir todos los notebooks. Para compilar el documento vigente usar `./scripts/compilar_proyecto.ps1`. **No ejecutar los integradores históricos que aparecen más abajo sobre las fuentes actuales:** reconstruyen capítulos y pueden sustituir cambios posteriores. Los apartados siguientes conservan la historia de versiones y sus comandos originales.

# Versión de correcciones del 10 de septiembre de 2026

Entrega ejecutada: tres notebooks, 49 comprobaciones independientes y contraste completo de actividad en cinco cortes. Los cuatro PDF fueron compilados y revisados. Cambios, justificaciones y límites: `reportes/correcciones_2026_09_10/entrega.md`. El registro de hallazgos y el manifiesto identifican el cierre por versión; `actualizacion_asesor.md` complementa el guion anterior de reunión. Los modelos permanecen pendientes.

La versión analítica activa es `correcciones_2026_09_10`. Se conservan los resultados anteriores en sus carpetas y un respaldo de código, notebooks y plantilla en `respaldo/2026-09-10_pre_correcciones`. Los registros de ejecución y validación están en `reportes/correcciones_2026_09_10`.

Se mantiene población, evento y cortes inclusivos. `n_registros_vle` se conserva solo para auditoría; se evalúa `cv_intensidad_activa` como indicador adicional, sin borrar el CV de calendario. El calendario, las cascadas, los atributos de contexto y el diccionario se publican en informes y documento. Diversidad queda explícitamente fuera de esta versión; su utilidad no se presume evaluada.

La ampliación incluye 5.000 remuestreos por persona, comparación de extremos con prefijos de 500 y 2.000, sensibilidad de asociaciones a duplicados, especificaciones de PCA sobre casos comunes y agregación independiente desde toda la fuente. No hay entrenamiento de clasificadores ni selección de ventana. Las diferencias de A3.1/A2.5 y el protocolo de validación requieren ratificación académica.

## Reproducción de la versión actual

```powershell
python scripts/ejecutar_notebooks.py
python scripts/verificar_multiventana.py
python scripts/generar_informes.py
./scripts/compilar_informes.ps1
python scripts/verificar_informes.py
python scripts/integrar_correcciones.py
./scripts/compilar_proyecto.ps1
python scripts/verificar_proyecto.py
python scripts/registrar_entrega_correcciones.py
```

El script de integración reconstruye los capítulos 3, 4 y los anexos desde los informes generados; debe ejecutarse antes de cualquier edición manual posterior de esos capítulos. Los originales de datos no se modifican. La variable VERSION en `src/oulad_revision.py` y las rutas de generación señalan esta entrega; los respaldos permiten recuperar la cadena anterior.

El ajuste de leyenda de la figura de efectos ya está en el notebook. `scripts/ajustar_figura_efectos.py` permite regenerar solo esa figura desde la tabla calculada; no es necesario ejecutarlo al reproducir los notebooks completos. Su registro distingue el ajuste editorial posterior de la ejecución analítica completa previa.

Los documentos históricos siguientes describen exclusivamente las versiones anteriores. Los comprobantes de esta entrega deben consultarse en su carpeta, sin atribuirles comprobaciones aún no registradas.

---

# Estado actual: informes integrados en la plantilla

El 9 de septiembre de 2026 se integraron los informes multiventana en `Plantilla_ProyAplicado`. La versión de trabajo compilada es `Plantilla_ProyAplicado/proyecto.pdf`; los cambios, comprobaciones y pendientes se documentan en `reportes/migracion_2026_09_09/entrega.md`.

Para reproducir el documento: `./scripts/compilar_proyecto.ps1` y `python scripts/verificar_proyecto.py`. Los modelos, SHAP y el prototipo permanecen pendientes; la revisión bibliográfica integral del marco de referencia también está identificada como pendiente. Las indicaciones siguientes describen la fase analítica del 8 de septiembre y sus artefactos conservados.

# Revisión de notebooks e informes OULAD — 8 de septiembre de 2026

Se corrigieron los tres notebooks de la raíz y se ejecutaron en secuencia desde los
CSV de `data/raw`. Los originales se conservan en `respaldo/2026-09-08_pre_revision`.
La plantilla definitiva y los informes históricos permanecen como versiones previas;
los productos actuales están en `reportes/multiventana_2026_09_08`.

## Estado metodológico

Se adoptaron los cortes 7, 14, 28, 42 y 56 por autorización del usuario, registrada en `decision_temporal.json`. En cada corte t se observan los días 0..t inclusive: 8, 15, 29, 43 y 57 días de calendario. La población exige matrícula conocida hasta t, ausencia de retiro hasta t y final de presentación posterior a t. El evento es `t < date_unregistration <= module_presentation_length`.

Las calificaciones quedan fuera de los predictores porque no se conoce su fecha de publicación. La inactividad es un indicador complementario, no una etiqueta de abandono. Se supone disponibilidad de registros al cierre del día y del calendario; sus retrasos de publicación no son verificables. La versión anterior de día 28 usaba 0..27; el cambio de cifras se documenta en `02_enlace_corte28.csv`.

Se comparan poblaciones propias de cada corte y una cohorte común retrospectiva de 26.429 inscripciones. Esta última exige elegibilidad hasta 56 y no representa una población operativa de alerta al día 7. Los intervalos son exploratorios y puntuales, mediante 500 remuestreos por persona. No se entrenaron clasificadores, no se identificó una ventana óptima ni se acreditó una prueba final intacta.

## Ejecución

Se utilizó Python 3.11.9 con las versiones de `requirements-revision.txt`.
Desde la raíz del proyecto, en PowerShell:

```powershell
python scripts/ejecutar_notebooks.py
python scripts/verificar_revision.py
python scripts/generar_informes.py
./scripts/compilar_informes.ps1
python scripts/verificar_informes.py
```

El ejecutor inicia un proceso Python nuevo para cada notebook, ejecuta todas sus
celdas en orden y guarda textos e imágenes en el propio `.ipynb`. No utiliza un
servidor ni kernel Jupyter y no admite magias; estos notebooks no las requieren.
También pueden ejecutarse con un kernel Python que tenga las dependencias indicadas.
Si el directorio de inicio es diferente, configurar `$env:OULAD_ROOT` con la raíz.

El script de compilación utiliza MiKTeX y BibTeX instalados localmente; sus rutas
se pueden modificar en `scripts/compilar_informes.ps1`. La compilación no permite
instalar automáticamente paquetes. Se usó `babelprovide` por compatibilidad con
la instalación local. La generación de gráficos y análisis ocurre en los notebooks;
el generador de informes solo lee las tablas y resúmenes exportados.
La última comprobación requiere las dependencias opcionales de
`requirements-verificacion-pdf.txt` y genera imágenes para inspección visual.

## Productos

| Producto | Ubicación relativa a la raíz |
|---|---|
| Informes individuales PDF y LaTeX | `reportes/multiventana_2026_09_08/informes` |
| Contenido migrable, sin preámbulo ni bibliografía | `informes/01_exploracion_contenido.tex`, `02_ingenieria_contenido.tex`, `03_estadistica_contenido.tex` dentro de la carpeta anterior |
| Tablas reproducibles y diccionario de roles | `reportes/multiventana_2026_09_08/tablas` |
| Figuras vectoriales PDF y vistas PNG | `reportes/multiventana_2026_09_08/figuras` |
| Dataset analítico y artefactos intermedios | `data/processed/multiventana_2026_09_08` |
| Registro de hallazgos y decisiones | `reportes/multiventana_2026_09_08/registro_hallazgos.csv` |
| Correspondencia con la plantilla | `reportes/multiventana_2026_09_08/migracion.md` |
| Huellas de CSV y entorno | `reportes/multiventana_2026_09_08/fuentes.json`, `entorno.json` |
| Comprobaciones independientes | `reportes/multiventana_2026_09_08/verificaciones_independientes.json` |

El diccionario separa identificadores, desenlace, predictores candidatos, contexto
condicionado y auditoría. **No entrenar con todas las columnas del dataset analítico.**
Utilizar el archivo de candidatos como punto de partida, con selección y tratamiento
de faltantes dentro del entrenamiento. Se documentan identidades entre predictores;
su inclusión conjunta no es una recomendación para regresión logística.

## Alcance de las verificaciones

La ejecución comprende los siete CSV completos. Se verificaron claves y relaciones,
límites temporales, denominadores, exclusión de información retrospectiva y
coherencia de artefactos. Una comprobación independiente releyó `studentVle.csv` por
fragmentos y contrastó la agregación para una muestra reproducible de 60
personas; no es una segunda reconstrucción completa de todas las variables.
El cómputo de entregas se contrastó en toda la fuente y el efecto ponderado se
contrastó con una remuestra materializada que contiene empates.

El bootstrap emplea 500 remuestras de personas y produce intervalos puntuales
exploratorios. No se demostró cobertura exacta ni estabilidad de extremos frente a
otras semillas. Los módulos y presentaciones se consideran fijos. Los diagnósticos
de atípicos no justifican eliminar observaciones ni identifican errores por sí solos.

## Pendientes determinantes

1. Investigar las discordancias de la fuente y mantener explícitos los supuestos de disponibilidad y seguimiento; el protocolo temporal de esta versión ya fue adoptado por el usuario.
2. Definir el protocolo de validación de modelos y la generalización pretendida. La comparación exploratoria de cinco cortes ya está ejecutada; la selección predictiva de ventana permanece pendiente.
3. Migrar el contenido según `migracion.md` y revisar su integración con el anteproyecto y los requisitos institucionales.

La reproducción usa los notebooks de la raíz como fuente de análisis. Los archivos
temporales de construcción, si permanecen en `tmp`, no deben utilizarse para
sobrescribirlos: no constituyen la interfaz de reproducción.

## Conservación y validación de la nueva versión

La revisión anterior permanece en `reportes/revision_2026_09_08` y `data/processed/revision_2026_09_08`. Los notebooks y scripts previos a la ampliación se conservaron en `respaldo/2026-09-08_pre_multiventana`.

Los tres notebooks se ejecutaron completos en procesos nuevos. Se superaron 46 comprobaciones independientes: identidad de fuentes, población y evento por corte, entregas sobre toda la fuente, clics contrastados sobre una muestra reproducible de 60 personas, casos sintéticos de frontera, invariancia ante información futura, faltantes estructurales y bootstrap con empates. El muestreo de clics no constituye una segunda agregación independiente de todas las inscripciones.

El generador requiere la versión anterior conservada para reutilizar la redacción de auditoría invariable y verificar huellas; si cambian las fuentes se detiene. Los análisis actuales y las tablas comparativas se generan desde los CSV actuales. El registro de hallazgos mantiene las limitaciones abiertas de la fuente y separa la preparación de informes de su futura integración en la plantilla.
