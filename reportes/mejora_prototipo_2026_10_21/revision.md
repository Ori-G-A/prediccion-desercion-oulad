# Revisión del prototipo — 21 de octubre de 2026

Veredicto: ampliación implementada; validación de comprensión pendiente. Las cuatro capturas aportadas por el usuario acreditan la apertura de la versión anterior y permiten revisar sus secciones visibles del día 7. No prueban todos los controles ni la composición de la versión ampliada.

## Requisitos y cobertura

Fuente activa: Plantilla_ProyAplicado/descripcion.tex, objetivo específico de prototipo y alcance del despliegue; desarrollo5.tex. La matriz traduce el objetivo en comprobaciones de implementación, sin atribuir aprobación adicional del asesor.

| Requisito | Estado y evidencia | Pendiente |
|---|---|---|
| Comunicar exploración | Incorporada consulta de cuatro características en cinco cortes; numeradores y denominadores cotejados con el anexo | Cobertura parcial: no integra toda la exploración académica, conductual y temporal |
| Comunicar predicciones | Probabilidades, errores, población, intervalos y comparación de candidatos congelados | Lectura por usuarios previstos |
| Comunicar explicaciones | Magnitudes globales y 500 casos; valores observados y contribuciones con signo | Estabilidad de SHAP no evaluada; no se afirma causalidad |
| Lectura educativa clara | Glosario de métricas, ejemplo hipotético y explicación de indicadores | Comprobar comprensión con autores y asesor |
| Consulta local | Archivo autónomo sin dependencias externas; apertura anterior confirmada por usuario | Revisión visual de la nueva versión y controles en navegador |
| Conservar alcance | Sin conexión a LMS, intervención, nuevos ajustes ni umbrales | No constituye herramienta institucional validada |

## Hallazgos y correcciones

| Severidad | Evidencia | Corrección |
|---|---|---|
| Menor | Etiquetas sin tildes y nombres técnicos en capturas | Etiquetas legibles de los 26 predictores |
| Menor | ROC-AUC y F1 sin definición | Glosario desplegable, AP y Brier explicados, ejemplo hipotético de precisión y sensibilidad |
| Menor | Cuatro intervalos visibles frente a diez anunciados | Aclaración: se omiten grupos vacíos |
| Mayor de comunicación | Caso sin valores de los indicadores y barras negativas hacia la derecha | Valores originales y eje centrado en cero; ausente separado de cero |
| Mayor de cobertura | Exploración ausente en la primera versión | Consulta descriptiva por cuatro variables, con población y límites explícitos; cobertura restante no declarada completa |
| Limitación técnica | CUA falla al escribir recursos de inicio, error de ruta 3 | Verificación funcional mediante DOM mínimo; no presentada como prueba real de navegador |

## Guía para autores y asesor

1. Abrir OULAD.html y cambiar entre los cinco días. Comprobar que cambian población, modelo principal y resultados. En día 14 el principal es Random Forest; en los demás, XGBoost.
2. Elegir las cuatro características de contexto. Explicar por qué el número de inscripciones es mayor que en la prueba y por qué las diferencias descriptivas no explican causas.
3. Leer precisión y sensibilidad con sus denominadores. Explicar por qué muchas alertas pueden ser falsas aunque se detecten numerosos retiros.
4. Elegir casos distintos. Distinguir valor observado del indicador, contribución SHAP, probabilidad y desenlace. Explicar que una contribución negativa disminuye la predicción respecto de la referencia.
5. Identificar qué población y horizonte cambia al seleccionar otro corte y por qué AP no basta para escoger un día óptimo.

Registrar para cada actividad: fecha, participante, versión del archivo, respuesta observada, dificultad y corrección necesaria. Ninguna de estas actividades se registra como realizada sin evidencia. Para la reunión, revisar límites predictivos, alcance académico pendiente de ratificación y requisitos de comunicación; no solicitar nuevos ajustes a partir de la prueba ya observada.

Fuentes y comprobaciones reproducibles: prototipo/verificacion_datos.json y prototipo/verificacion_funcional.json. Respaldo previo: respaldo/2026-10-21_pre_mejora_prototipo. La tesis compilada anterior conserva su descripción de primera versión; la integración documental de esta ampliación y la revisión visual posterior quedan pendientes.
