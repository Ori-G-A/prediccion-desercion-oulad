# Revisión e integración del cierre de modelado

Fecha: 21 de octubre de 2026. Se aplicó el protocolo vigente sin volver a entrenar, seleccionar candidatos, recalibrar ni cambiar umbrales después de la prueba.

## Veredicto

Se verificaron las salidas congeladas y se integraron resultados y límites en las fuentes activas. Las familias principales superan la referencia constante en AP, pero presentan precisión de alertas limitada. Los intervalos pareados de AP entre principal y logística incluyen cero en los cinco cortes. No se afirma superioridad concluyente, equivalencia, causalidad ni utilidad institucional demostrada. El cierre técnico del modelado no equivale al cierre académico del proyecto.

| Severidad / tipo | Evidencia | Corrección o pendiente |
| --- | --- | --- |
| Mayor / límite analítico | Precisión principal 22,2 % a 29,9 %; falsas alertas y retiros omitidos | Se incorporaron métricas, denominadores, errores y límites en capítulo, reporte y prototipo. No se cambió el umbral al observar prueba. |
| Mayor / interpretación | Intervalos pareados principal menos logística incluyen cero en todos los cortes | Se evitó declarar superioridad concluyente; no se infiere equivalencia. |
| Menor / estado desactualizado, corregido | Capítulos indicaban entrenamiento y prueba pendientes; contador mantenía apertura falsa | Se actualizaron capítulos, resumen, ruta y objetivos. El contador consulta ahora el registro real de apertura. Se preservan los registros históricos. |
| Menor / verificación pendiente | CUA no pudo iniciar por error de escritura de kernel; HTTP local no respondió | Prototipo autónomo OULAD.html creado y enviado al navegador predeterminado. Pruebas funcionales con DOM mínimo pasaron; visualización real y comprensión con usuarios no verificadas. |
| Mayor / alcance del prototipo parcial | Primera versión comunica predicción e interpretación, pero no toda la exploración | Se mantiene el objetivo parcial y la evaluación de requisitos y usuarios pendiente. |
| Pendiente académico | Ratificación del alcance y revisión de los autores/asesor no acreditadas | No se sustituyen por pruebas de software ni por la compilación. |

## Comprobaciones ejecutadas

`scripts/revisar_cierre_modelado.py` comprobó el paquete, 56 huellas de salidas, 35 combinaciones de modelo/referencia y corte, métricas y anticipación desde predicciones, percentiles y diferencias pareadas desde réplicas guardadas, así como 500 contribuciones SHAP y su correspondencia con las predicciones reservadas. No repite entrenamientos ni los 2.000 remuestreos. La aditividad no prueba estabilidad de atribuciones. Resultado: verificacion.json.

`scripts/generar_resultados_finales.py` genera seis tablas LaTeX, dos figuras científicas y datos del prototipo sin identificadores de estudiantes. La aplicación conserva modelos y umbrales, muestra todos los candidatos y distingue el principal definido por validación. `prototipo/verificar_funciones.cjs` comprobó controles de cinco cortes y 500 casos mediante DOM mínimo; no es una prueba visual de navegador. La versión autónoma permite abrir un único archivo sin servidor.

Se conservaron fuentes y PDF anteriores en respaldo/2026-10-21_pre_cierre_modelado. Se integraron capítulos de modelos, SHAP y prototipo, resumen, introducción, contextualización, ruta, objetivos y conclusiones. No se modificaron datos, contratos ni código incluido en el paquete congelado. El informe para el asesor pasó a siete páginas e incluye hallazgos, tiempos y hardware, con estado fechado.

La compilación usa scripts/compilar_proyecto.ps1 y fuentes activas. Se revisaron las páginas afectadas, tablas, figuras y cambios de estado; no se declara revisión integral de toda la tesis. Los registros de composición y huellas finales se conservan en verificacion_entrega.json. Quedan pendientes la revisión académica, la comprobación visual del prototipo y su evaluación con usuarios.
