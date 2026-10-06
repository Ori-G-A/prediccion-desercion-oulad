# Instrucciones para código y notebooks

Estas reglas complementan el AGENTS.md de la raíz; no sustituyen sus criterios académicos ni su estilo.

## Antes de modificar
- Lee los archivos afectados, sus dependencias, la configuración del entorno y las decisiones metodológicas documentadas.
- Identifica la unidad de análisis, claves, evento, población elegible y corte temporal vigentes. No asumas que el día 28 está ratificado.
- Respeta nombres, estructura y librerías existentes. No reorganices el repositorio sin necesidad.
- Usa rutas relativas a una raíz configurable y documenta versiones relevantes.

## Datos y temporalidad
- Conserva las fuentes originales. Comprueba unicidad y cardinalidad de claves antes y después de cada unión.
- Agrega por estudiante, módulo y presentación cuando la unidad sea la inscripción; no mezcles cursos de una persona.
- Documenta filtros con conteos de entrada, salida y exclusiones. Distingue ausencia de registro, cero e información desconocida.
- Separa el instante de disponibilidad de una variable de la fecha del hecho que representa. No uses notas o registros aún desconocidos al predecir.
- Excluye eventos ya ocurridos de la población en riesgo para una predicción futura, según la definición ratificada.
- Construye etiquetas con seguimiento suficiente; no uses variables que revelen directa o indirectamente el desenlace como predictores.
- Para ventanas repetidas, controla dependencia y solapamiento; evita contaminación entre conjuntos.

## Entrenamiento y evaluación
- Ajusta transformaciones aprendidas y selección de variables dentro de cada fold de entrenamiento mediante pipelines adecuados.
- Aplica remuestreo solo a entrenamiento. No impongas SMOTE ni escalado a todos los algoritmos.
- Justifica división por persona, presentación o tiempo según el escenario de generalización. La estratificación no resuelve por sí sola la dependencia.
- Reserva el conjunto de prueba hasta terminar selección de modelo, hiperparámetros, calibración y umbral.
- Incluye un modelo base simple. Compara con particiones comunes y presupuesto de ajuste documentado.
- Registra semillas, configuración, clase positiva, prevalencia, métricas y matriz de confusión. Explicita cómo calculas el área PR o average precision.
- Estima incertidumbre con un procedimiento compatible con las dependencias de los datos.
- En SHAP registra modelo, variante, referencia, escala de salida y tratamiento de dependencia.

## Notebooks y artefactos
- Mantén un orden de ejecución claro y evita dependencias de variables creadas manualmente fuera del flujo.
- No presentes salidas antiguas como resultados de código recién modificado. Señala salidas pendientes de regeneración.
- Exporta métricas, auditorías, tablas y figuras a archivos reproducibles; documenta cómo se generan.
- Conserva el formato .ipynb y evita cambios masivos de metadatos o salidas ajenas a la tarea.
- El texto explicativo de las celdas Markdown aplica la sección 3 del AGENTS.md principal: voz académica, explicaciones directas, términos definidos y ejemplos identificados. Las figuras siguen ESTILO_VISUAL.md y reutilizan los generadores compartidos; no recuperes paletas históricas.
- Extrae funciones a módulos existentes cuando evite duplicación real, sin convertir cambios pequeños en refactorizaciones generales.

## Verificación y entrega
- Ejecuta comprobaciones pertinentes: integridad de claves, exclusiones, límites temporales y separación entre conjuntos.
- Usa muestras para verificar el flujo cuando el procesamiento completo sea costoso; identifica la validación como parcial.
- No instales dependencias o ejecutes entrenamientos largos sin valorar necesidad y recursos disponibles.
- Si hace falta ejecución local, entrega comando, entorno requerido y lista de salidas que debe aportar el autor.
- Resume cambios, comprobaciones efectivamente ejecutadas, resultados y limitaciones.
