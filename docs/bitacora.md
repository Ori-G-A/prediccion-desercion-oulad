# Bitácora de desarrollo

Proyecto: Predicción de deserción estudiantil · OULAD · CRISP-DM

Esta bitácora registra **decisiones y su justificación**, no avances diarios. El código
documenta *qué* se hizo; aquí queda el *por qué*. Cada entrada debe poder defenderse ante
el jurado y alimenta directamente la redacción del documento final.

---

## Cómo se usa

- **Cuándo escribir una entrada:** cuando se toma una decisión que habría que justificar en la
  sustentación, o cuando se resuelve un problema relevante. No es un diario de progreso.
- **Código de actividad:** usar el mismo del tablero/cronograma (`F0.x`, `A1.x` … `A5.x`).
- **Condición primero:** describir la observación que disparó la decisión *antes* que la decisión.
  Las decisiones se enmarcan como respuestas a condiciones detectadas, no como pasos asumidos.
- **Git:** idealmente una decisión = un commit; anotar el hash en `Commit`.
- **Destino:** indicar a qué sección del documento alimenta la salida, para que el informe se
  ensamble desde lo ya documentado.
- **Orden:** entradas más recientes al final (append-only). No reescribir entradas pasadas;
  si una decisión cambia, se registra una nueva entrada que la reemplaza y se enlaza.

### Plantilla de entrada (copiar y rellenar)

```
### [AAAA-MM-DD] · <CÓDIGO> — <título corto de la decisión>

- **Condición detectada:** <qué se observó que motivó la decisión>
- **Decisión:** <qué se decidió hacer>
- **Justificación:** <por qué esta opción>
- **Alternativas descartadas:** <opción A — motivo; opción B — motivo>
- **Salida → destino:** <archivo / figura / tabla>  →  <sección del documento>
- **Commit:** <hash o "—">
```

### Mapa rápido entrada → capítulo

| Tipo de decisión                                  | Sección destino habitual          |
|---------------------------------------------------|-----------------------------------|
| Comprensión del fenómeno, definición del problema | Comprensión del área / Metodología|
| Hallazgos del EDA, calidad de datos               | Resultados / Comprensión de datos |
| Ingeniería de variables, ventanas temporales      | Metodología (preparación)         |
| Particionado, transformaciones, desbalance        | Metodología (modelado)            |
| Métricas, comparación, interpretabilidad          | Resultados / Evaluación           |
| Diseño y validación del prototipo                 | Resultados / Despliegue           |

---

## Entradas

### [2026-06-05] · F0.0 — Adopción de CRISP-DM como marco del proceso

- **Condición detectada:** el programa recomienda explícitamente CRISP-DM como marco de
  referencia, por su orientación formativa hacia la práctica profesional; el borrador inicial
  describía el flujo en términos de KDD.
- **Decisión:** adoptar CRISP-DM y mapear cada objetivo específico a una de sus fases.
- **Justificación:** las seis fases de CRISP-DM (comprensión del área, comprensión de los datos,
  preparación, modelado, evaluación, despliegue) se alinean casi uno a uno con los cinco
  objetivos, y el marco es el sugerido por el programa.
- **Alternativas descartadas:** KDD — válido pero menos orientado a la práctica profesional y no
  recomendado por el programa.
- **Salida → destino:** párrafo introductorio del capítulo → Metodología.
- **Commit:** —

### [2026-06-05] · A1.0 — Definición dual de la deserción (comprensión del área)

- **Condición detectada:** el fenómeno de abandono no se manifiesta de una sola forma en los
  datos de OULAD; existe abandono administrativo y abandono efectivo sin trámite.
- **Decisión:** definir la deserción desde dos perspectivas complementarias: retiro formal
  (registrado en `date_unregistration`) y abandono implícito (inactividad prolongada en la
  plataforma).
- **Justificación:** la distinción nace del entendimiento del fenómeno educativo, no de los datos
  en sí; capturarla evita subestimar el abandono real. Evidencia de la fase de comprensión del
  área aunque no figure como objetivo explícito.
- **Alternativas descartadas:** usar solo `date_unregistration` — dejaría fuera a quienes
  abandonan sin tramitar el retiro.
- **Salida → destino:** definición operacional del target → Metodología (comprensión del área y
  modelado A3.1).
- **Commit:** —

### [2026-06-06] · A1.3 — Estandarización a tres categorías de variables

- **Condición detectada:** distintos archivos del documento listaban cuatro categorías
  (incluyendo sociodemográficas) y otros solo tres, generando inconsistencia entre secciones.
- **Decisión:** estandarizar a tres categorías —académicas, conductuales y temporales— en todo
  el documento y en el análisis exploratorio.
- **Justificación:** coherencia interna del documento y alineación con el alcance real del
  análisis previsto.
- **Alternativas descartadas:** mantener cuatro categorías — obligaba a sostener un eje
  sociodemográfico que no se explota de forma central en los objetivos.
- **Salida → destino:** lista de categorías y EDA por categoría → Metodología / Resultados.
- **Commit:** —

### [2026-06-06] · A3.4 — Tratamiento del desbalance como actividad condicional

- **Condición detectada:** la deserción suele ser la clase minoritaria; aún no se ha medido la
  proporción real en el dataset preparado.
- **Decisión:** planificar el tratamiento del desbalance como una actividad **condicional**, que
  se ejecuta solo si se detecta desbalance tras el particionado, y siempre sobre el conjunto de
  entrenamiento.
- **Justificación:** evita asumir un resultado no verificado; la decisión queda enmarcada como
  respuesta a una condición que se comprobará empíricamente. El particionado estratificado
  (A3.2) preserva la proporción de clases para poder medirla.
- **Alternativas descartadas:** aplicar remuestreo por defecto — introduciría un tratamiento sin
  evidencia de que sea necesario, con riesgo de distorsionar la distribución.
- **Salida → destino:** descripción de la actividad A3.4 → Metodología (modelado).
- **Commit:** —

<!-- Nueva entrada debajo de esta línea -->


### [2026-10-06] · A1-A3 — Integración de la etapa local y actualización de decisiones

- **Condición detectada:** main conserva el trabajo hasta el 6 de septiembre. La versión local incorpora revisiones posteriores de temporalidad, variables y documentación. La bitácora inicial no las recoge.
- **Decisión:** conservar el historial y añadir la versión local en una rama para revisión. Los tres notebooks activos se ubican en la raíz, y los cuatro anteriores se conservan sin modificación en `notebooks/historico_2026_09_06/`.
- **Justificación:** permite enlazar el trabajo previo y los cambios posteriores sin borrar la evidencia. La selección de rutas mantiene el flujo de ejecución ya utilizado localmente.
- **Cambios metodológicos:** se utilizan cinco cortes inclusivos; se seleccionan inscripciones vigentes al corte y se define retiro futuro hasta el final de la presentación. Las notas permanecen para auditoría y la inactividad es complementaria. Se separan 26 indicadores candidatos y atributos de contexto. La definición dual registrada en junio se conserva como antecedente; esta versión no implementa inactividad como segunda etiqueta. La autorización de implementación del usuario no se presenta como ratificación académica del director.
- **Evidencia:** `decision_temporal.json`, `src/ventanas_oulad.py`, `reportes/correcciones_2026_09_10/` y `reportes/entrega_avance_2026_10_06/`. Los 49 controles del 6 de octubre no equivalen a reejecutar todos los notebooks.
- **Salida → destino:** fuentes y resultados locales → caracterización, ingeniería, conclusiones y anexos. Modelos, SHAP y prototipo siguen pendientes.
- **Commit:** véase el historial de esta entrada en la rama `actualizacion/avance-local-2026-10-06`.

### [2026-10-06] · Seguimiento — Calendario continuo y revisión del plan

- **Condición detectada:** los autores aclararon el inicio previsto el 27 de julio de 2026 y la intención de finalizar en mayo de 2027, trabajando en el receso.
- **Decisión:** proponer diez bloques mensuales consecutivos hasta el 26 de mayo de 2027 y revisar el plan al finalizar el semestre, según la orientación del director comunicada por el usuario.
- **Justificación:** permite relacionar los bloques M1-M10 con fechas estimadas sin esperar el calendario académico de 2027 ni confundir la entrega final del curso de noviembre con la terminación del proyecto.
- **Límite:** las fechas detalladas y el cierre estimado de mayo no se presentan como aprobados. Los commits de junio y julio documentan antecedentes, no modifican automáticamente el inicio previsto.
- **Salida → destino:** `docs/cronograma_estimado.md` → seguimiento y próxima actualización de la entrega.
- **Commit:** véase el historial de esta entrada.

### [2026-10-06] · Organización — Notebooks vigentes en su carpeta

- **Solicitud:** organizar los notebooks activos dentro de `notebooks/` y conservar el funcionamiento del proyecto.
- **Decisión que sustituye la ubicación anterior:** los tres notebooks vigentes pasan de la raíz a `notebooks/`. Se conserva la subcarpeta histórica sin cambios. El traslado se aplica también a la carpeta de trabajo local.
- **Cambios:** se actualizan siete scripts que localizan notebooks, la orientación del lanzador de Jupyter y las guías de uso. No se modifica el código ni las salidas de los notebooks.
- **Validación:** identidad de archivos antes y después, sintaxis, arranque desde la nueva carpeta, prueba aislada del ejecutor y 49 comprobaciones independientes. No se repiten todos los análisis. Evidencia en `docs/validacion_estructura_notebooks_2026_10_06.json`.
- **Guías locales:** `AGENTS.md`, `EJECUCION_LOCAL.md` y `ESTILO_VISUAL.md` permanecen fuera del seguimiento por solicitud del usuario; el README público contiene las instrucciones de reproducción.
