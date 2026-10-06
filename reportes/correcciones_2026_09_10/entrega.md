# Entrega de correcciones analíticas y documentales

Versión: `correcciones_2026_09_10`. Fecha: 10 de septiembre de 2026.

## Veredicto y alcance

Se implementaron las tres correcciones centrales confirmadas por el usuario y las ampliaciones analíticas asociadas. Las cascadas completas y los atributos de contexto se publican dentro del trabajo de grado; `n_registros_vle` se retiró del conjunto candidato y se conserva exclusivamente para auditoría; la ausencia de diversidad se justifica expresamente. La caracterización y la ingeniería cuentan con evidencia reproducida y una nueva entrega documental. Esto no constituye la terminación del proyecto ni una validación predictiva.

La contrarrevisión inicial confundió la existencia de exportables con el cierre del pendiente de publicación. Se reconoce y corrige ese criterio: el cierre documental exige resultados, denominadores, interpretación y remisiones accesibles en el propio documento.

## Productos

El trabajo integrado se encuentra en `Plantilla_ProyAplicado/proyecto.pdf`, con fuentes editables en esa carpeta. Los informes independientes y sus fuentes migrables están en `reportes/correcciones_2026_09_10/informes`: `01_exploracion`, `02_ingenieria` y `03_estadistica`. Los datos analíticos nuevos se conservan en `data/processed/correcciones_2026_09_10`; las tablas y figuras se encuentran en la carpeta de esta entrega. `version_entregada.json` identifica los archivos mediante SHA-256 y registra el resultado de las comprobaciones.

Los resultados previos permanecen en sus carpetas. El respaldo anterior a las modificaciones está en `respaldo/2026-09-10_pre_correcciones`, incluidos los tres notebooks, código, scripts y plantilla. No se encontró un repositorio Git inicializado en esta carpeta; no se presenta la entrega como un commit ni se presume sincronización con GitHub.

## Cambios y justificación

| Cambio | Justificación | Evidencia y ubicación estable |
|---|---|---|
| Publicación de las cinco cascadas | Un exportable no sustituye su presentación al jurado. Los filtros deben ser secuenciales para evitar doble conteo. | Capítulo 4, `corr:flujos`; tabla `02_flujos.csv`; partición adicional `02_particion_exclusiones.csv`. |
| Contexto ampliado | La exposición previa omitía región, discapacidad, edad e IMD. Se agregan créditos e intentos previos con denominadores explícitos. | Capítulo 3, `corr:numericos`; Anexo 9.2, `corr:niveles`, con remisión desde el capítulo. |
| Retiro del conteo de filas | La frecuencia de registro no tiene una interpretación educativa verificada y presenta redundancia en la especificación examinada. Cambiar el nombre no resuelve ese problema. | `src/ventanas_oulad.py`, `PREDICTORS`; archivos de predictores de los cinco cortes; `corr:vif` y `corr:diccionario`. |
| VIF con tamaño efectivo | El valor depende de las variables y casos incluidos. Al día 28, el VIF de filas es 10,929; se conserva como diagnóstico histórico, no como selección final. | `03_vif.csv`; capítulo 4, `corr:vif`. |
| Diversidad fuera de la implementación | Se explicita la delimitación a las cinco familias construidas. No se ha demostrado que diversidad carezca de utilidad; evaluarla requeriría integrar el catálogo y las oportunidades por módulo. | Capítulo 4, «Selección de indicadores y diferencias respecto del anteproyecto». |
| Comparación de dos CV | El CV de calendario combina inactividad e intensidad. El CV activo describe dispersión entre días activos y requiere al menos dos; mide otra propiedad y pierde observabilidad. | Identidad general `corr:identidadcv`; diccionario; `03_comparacion_cv.csv`; `03_efectos.csv`. |
| Sensibilidad a duplicados exactos | Se examina la dependencia descriptiva de la representación de la fuente sin presumir que deduplicar descubre los registros verdaderos. | Eliminación sobre todas las columnas antes de agregar; `03_sensibilidad_duplicados_efectos.csv`; `corr:duplicadosefectos`. |
| Tres especificaciones de PCA | Se compara redundancia sobre los mismos casos. Cambiar las variables cambia la varianza total; un porcentaje mayor no acredita mejor predicción del abandono. | `03_sensibilidad_pca.csv`; `corr:pcasens`. |
| 5.000 remuestreos por persona | La dependencia entre inscripciones de una persona debe preservarse al evaluar incertidumbre. Se verifica sensibilidad numérica de los extremos. | `03_estabilidad_bootstrap.csv`; `03_estabilidad_resumen.csv`; `corr:bootstrap`. |
| Definiciones, símbolos y figuras | Se separan prevalencia, probabilidad individual, calendario, población y seguimiento; se evita interpretar asociaciones como desempeño longitudinal. | Capítulo 4, ecuaciones `corr:elegibilidad` a `corr:identidadcv`; figuras de retiro, evolución agregada, calendario y observabilidad. |
| Diferencias con A3.1 y A2.5 | La fuente no prueba voluntariedad ni fecha de publicación de notas. Se documentan retiro registrado, inactividad complementaria y puntajes solo para auditoría. | `decision_temporal.json`; capítulo 4. La ratificación académica permanece pendiente. |

## Resultados de la ampliación

Se mantienen población, evento, cinco cortes y ventana inclusiva de la versión multiventana. Al día 28 se conservan 27.515 inscripciones elegibles y 5.012 retiros futuros, equivalentes a 18,22 %. La proporción global de fechas de retiro sigue siendo 10.072/32.593 = 30,90 %. No se trata de una reducción del abandono causada por el estudio: cambian evento y denominador.

La alternativa sin duplicados exactos conserva las poblaciones y etiquetas. El mayor cambio absoluto de los efectos examinados es aproximadamente 0,00244, correspondiente al CV activo del corte 7. Este resultado se limita a siete asociaciones descriptivas en cinco cortes; no acredita robustez de un clasificador ni resuelve la procedencia de las repeticiones.

Los intervalos puntuales del CV activo incluyen cero en los cortes 7 y 14. Su asociación difiere de la observada con el CV de calendario, por lo que no se sustituye una medida por otra como si fueran equivalentes. En la especificación de PCA con CV activo, dos componentes resumen aproximadamente 68,57 % a 70,76 % de la varianza de las cuatro variables estandarizadas; esos porcentajes no expresan la fracción explicada del abandono.

Las 66 comparaciones de extremos entre 2.000 y 5.000 remuestreos quedaron dentro de la tolerancia descriptiva de 0,005 unidades del efecto. El cambio máximo fue 0,00299394. Los prefijos comparten secuencia aleatoria: se trata de estabilidad numérica exploratoria, no de convergencia universal ni de un contraste entre ventanas.

## Ejecución y comprobaciones

Los tres notebooks se ejecutaron secuencialmente en procesos Python nuevos, sin kernel Jupyter: aproximadamente 138,2; 36,3 y 354,5 segundos. Los registros individuales `*_ejecucion.json` documentan ese alcance. Después se ajustaron texto y presentación; la leyenda de la figura de efectos se regeneró desde su CSV, sin repetir cálculos estadísticos. `ajuste_editorial_figura.json` distingue este ajuste de la ejecución completa previa y verifica que la tabla permaneció idéntica.

Pasaron 49 comprobaciones independientes. La ampliación leyó las 10.655.280 filas de `studentVle.csv` y contrastó clics, días activos y CV activo para todas las inscripciones elegibles en los cinco cortes. También comprobó la identidad de los CV, la exclusión del conteo de filas de candidatos y la invariancia de población y evento frente a deduplicación. Las pruebas de información futura, claves y fronteras temporales se conservan en `verificaciones_independientes.json`.

Los cuatro PDF se compilaron y renderizaron. Los verificadores revisan referencias, etiquetas, archivos gráficos, desbordamientos y márgenes; la revisión visual complementa esas comprobaciones. La plantilla conserva advertencias de clase y paquetes documentadas en `verificacion_documental.json`; no equivalen a errores numéricos. La correspondencia de las figuras migradas se comprobó mediante hash. La bibliografía tiene claves resolubles, lo que no acredita por sí solo la verificación de cada pasaje citado.

La entrega final contiene 79 páginas de proyecto y 6, 10 y 10 páginas en los informes 01, 02 y 03. No se detectaron desbordamientos ni referencias sin resolver. Se revisaron las páginas renderizadas y se corrigieron leyendas, tablas cortas, símbolos y encabezados de anexos. Las páginas en blanco entre capítulos obedecen al formato a dos caras. Las ubicaciones principales son la Tabla 4.4 para las cascadas; la Tabla 3.10 para créditos e intentos; la Tabla 9.1, expresamente referida desde el capítulo 3, para niveles de contexto; y la sección 4.2 para conteo de filas, diversidad y diferencias con el anteproyecto.

## Pendientes revalidados

| Pendiente | Severidad | Condición para su cierre |
|---|---|---|
| Protocolo de validación predictiva | Bloqueante para una comparación interpretable de modelos | Fijar generalización, separación por personas/tiempo, selección dentro de entrenamiento, métricas, calibración y reglas de umbral. Declarar la exploración previa de toda la fuente; no llamar intacta a una prueba sin evidencia. |
| Ratificación de diferencias con A3.1/A2.5 | Mayor | Acuerdo académico documentado sobre evento, población, papel de inactividad y tratamiento de puntajes; no se presume acta ni formato institucional obligatorio. |
| Selección predictiva, modelos base y comparación | Mayor; no iniciado en esta versión | Ejecutar el protocolo acordado sin reutilizar la prueba para decidir ventanas o modelos. |
| SHAP y prototipo | Mayor; no iniciado | Modelo evaluado, explicación con variante, referencia y escala explícitas; prototipo con alcance definido. |
| Revisión bibliográfica integral y PDF anotado | Mayor; parcial/no verificable | Contrastar pasajes, ediciones y las anotaciones del archivo concreto. La corrección de claves no sustituye ese trabajo. |
| Motivo de retiro, disponibilidad de notas y origen de repeticiones | Limitaciones de fuente | Evidencia externa de procedencia y disponibilidad; no se infieren estas propiedades de asociaciones observadas. |

El siguiente trabajo analítico es concretar el protocolo de validación y preparar las líneas base. La justificación de diversidad no obliga a incorporarla antes de comenzar esa etapa. El guion complementario para el asesor está en `actualizacion_asesor.md`; debe leerse junto con el informe histórico de reunión, cuyas cifras de remuestreo y estado documental corresponden a la versión anterior.
