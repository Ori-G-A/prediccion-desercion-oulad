# Narrativa visual del prototipo — 21 de octubre de 2026

Solicitud: aplicar técnicas de Storytelling con datos al prototipo vigente. Veredicto: rediseño implementado y comprobaciones funcionales correctas; revisión visual en navegador y comprensión con usuarios pendientes. No se alteraron datos, modelos ni umbrales.

## Referencia y aplicación

Obra de referencia indicada por el usuario: Knaflic, C. N. (2015). *Storytelling with Data: A Data Visualization Guide for Business Professionals*. Wiley. No se consultó el libro completo ni se atribuyen páginas a esta revisión. Se consultaron el 21 de octubre de 2026 los recursos públicos oficiales:

- Cole Nussbaumer Knaflic, «Two tips for better graphs»: https://www.storytellingwithdata.com/blog/two-tips-for-better-graphs. Reducir distracciones y concentrar la atención mediante contraste selectivo.
- Elizabeth Ricks, «What your audience really wants»: https://www.storytellingwithdata.com/blog/what-your-audience-really-wants. Aplicación del proceso SWD: contexto, elección del gráfico, reducción de ruido, foco y relato. Este artículo es de Ricks, no de Knaflic.

La adaptación sirve a autores y asesor que deben interpretar los resultados y sus límites. No busca persuadir de un desempeño favorable ni omitir resultados adversos.

| Principio | Cambio concreto | Condición de rigor |
|---|---|---|
| Mensaje antes del detalle | Título dinámico con retiros detectados y falsas alertas; recorrido numerado | Denominadores diferentes expresos, sin presentar sensibilidad como precisión |
| Gráfico apropiado | Dos barras de composición: alertas y retiros | Cada barra suma 100 % de su propio grupo; conteos exactos junto al gráfico |
| Foco selectivo | Principal en azul; otros candidatos en gris; primer indicador SHAP destacado | El principal proviene de validación, no del mayor AP de prueba |
| Incertidumbre visible | AP con puntos y segmentos de intervalos del 95 % | Escala común desde cero; no se deduce significancia del solapamiento de intervalos marginales |
| Lectura directa | Probabilidad media y frecuencia observada conectadas; grupo más numeroso descrito | Tamaños visibles, sin afirmar calibración perfecta ni significancia |
| Menos distracciones | Menos bordes, navegación y detalles desplegables | Tablas y definiciones conservadas; límites esenciales visibles |
| Contexto | Barras descriptivas por categoría, porcentajes y tamaños | Escala fija 0–100 %; no se atribuye causalidad ni se confunde población completa con prueba |
| Caso explicado | Título según alerta y desenlace, contribuciones desde cero | Ningún caso se declara representativo; valores observados distintos de contribuciones |

## Verificación

`node prototipo/verificar_funciones.cjs`: cinco cortes, 500 casos, 20 consultas de contexto, límites de posiciones de gráficos, suma de barras de composición, elementos HTML existentes y sintaxis de los dos scripts autónomos. Estructura de etiquetas comprobada con HTMLParser. `datos.js` coincide byte a byte con el respaldo anterior: las 145 filas descriptivas, métricas e intervalos permanecen intactos.

Se conservaron originales en respaldo/2026-10-21_pre_storytelling. El rediseño está en index.html y app.js, incorporados también en OULAD.html. La regeneración habitual conserva el diseño porque incorpora estas fuentes.

## Pendientes

| Severidad | Pendiente | Evidencia necesaria para cierre |
|---|---|---|
| Menor | Composición visual de esta versión en escritorio y pantalla estrecha | Inspección real de navegador; las comprobaciones de DOM mínimo no la sustituyen |
| Mayor de validación | Comprensión por autores y lectores previstos | Aplicar la guía de reportes/mejora_prototipo_2026_10_21/revision.md y registrar respuestas reales |
| Menor documental | Integración del rediseño en descripción final de tesis | Actualizar fuentes activas cuando se consolide la revisión de interfaz y compilar |

La herramienta CUA había fallado al iniciar por error de ruta de recursos. No se declara probado un navegador ni aprobada esta composición mediante capturas de una versión anterior.
