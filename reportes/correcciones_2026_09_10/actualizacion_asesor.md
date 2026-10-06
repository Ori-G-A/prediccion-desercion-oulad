# Actualización para la reunión con el asesor

Fecha: 10 de septiembre de 2026. Complemento del informe de reunión preparado antes de cerrar las correcciones de la bitácora. Este texto actualiza lo ejecutado; no reemplaza la ratificación académica de los cambios respecto del anteproyecto.

## Mensaje principal

La revisión posterior permitió corregir una diferencia entre disponer de resultados calculados y presentarlos efectivamente en el trabajo de grado. Se publicaron las cascadas de elegibilidad de los cinco cortes y los resultados de región, discapacidad, edad e IMD; se añadieron créditos e intentos previos y se incorporaron remisiones explícitas a los anexos. También se resolvió el uso del conteo de filas VLE antes del modelado y se amplió la sensibilidad estadística. El proyecto dispone de una versión analítica reproducida, tres informes actualizados y su integración en la plantilla; los clasificadores, SHAP y el prototipo siguen pendientes.

## Preguntas y respuestas sustentadas

**¿Por qué la prevalencia pasó de 30,9 % a 18 %?** La primera cifra es 10.072 fechas de retiro entre 32.593 inscripciones de toda la fuente. Incluye retiros anteriores al inicio y al día de predicción. La segunda corresponde a 5.012 retiros futuros entre 27.515 inscripciones elegibles al cierre del día 28: 18,22 %. Se corrigió la correspondencia entre pregunta predictiva, evento y denominador. No se observó una disminución causada por una intervención. En esta nueva entrega esos valores se mantienen respecto de la versión multiventana.

**¿Por qué cinco ventanas y no una?** Los cortes 7, 14, 28, 42 y 56 permiten examinar el intercambio entre anticipación e información disponible. La ventana 0..t incluye t+1 días. Las tendencias requieren historia suficiente y el calendario de evaluaciones cambia entre presentaciones: hay entregas anticipadas al día 7 aunque no haya vencimientos en esa ventana. La rejilla permite comparar estas condiciones, pero no se ha demostrado que cinco sea el número óptimo ni que alguna ventana sea superior. También cambian población y seguimiento; una cohorte común retrospectiva complementa la comparación sin convertirse en población operativa de alerta temprana.

**¿Por qué todavía no hay modelo?** La prioridad ejecutada fue corregir la tarea temporal, la disponibilidad de predictores y la coherencia entre código y documento. Ahora debe fijarse un protocolo de evaluación que atienda a estudiantes repetidos y a la generalización buscada. No corresponde afirmar que los diagnósticos exploratorios ya validaron la predicción. Tampoco se plantea esperar a terminar toda mejora bibliográfica para preparar una línea base: el requisito inmediato es una evaluación definida y honesta sobre la exploración previa de los datos.

**¿Sirve el retiro administrativo si no se sabe si fue voluntario?** Permite definir un evento registrado y fechado, útil para estudiar la anticipación de esa baja. No permite atribuir motivos ni equiparar la baja de una inscripción al abandono institucional. A3.1 del anteproyecto hablaba de voluntariedad y exploración de abandono implícito; por ello, esta diferencia debe presentarse expresamente al asesor y ratificarse. La inactividad permanece como indicador complementario. Predecir inactividad futura sería otra tarea posible, que no se ha adoptado como segunda etiqueta.

**¿Qué se decidió sobre `n_registros_vle`?** Se retiró de los predictores y se conservó para auditoría. Cuenta filas, sin identificador de sesión; la procedencia de las repeticiones no está verificada. El VIF de 10,929 al día 28 muestra redundancia en la especificación examinada, pero la decisión no se basa solo en un umbral estadístico: también responde a la interpretación no resuelta de la medida. Los cinco archivos de predictores y el diccionario reflejan la exclusión.

**¿Se eliminaron todos los registros repetidos de la fuente principal?** No. La fuente original se preservó y se calculó una alternativa que retira duplicados exactos sobre todas las columnas antes de agregar. En las siete asociaciones estudiadas, el mayor cambio absoluto fue aproximadamente 0,00244. Esto indica sensibilidad pequeña en esos resultados concretos; no permite identificar qué registro es verdadero ni anticipar que todos los modelos serán robustos. Los 787.170 exactos y las 2.195.960 repeticiones de clave no son categorías disjuntas que puedan sumarse.

**¿Por qué se agregó otro coeficiente de variación?** El CV de calendario mezcla continuidad e intensidad, porque incorpora días sin actividad. El CV activo describe variación entre días con clics y requiere al menos dos. Se verificó la identidad algebraica que los relaciona y se compararon observabilidad y asociaciones. En los cortes 7 y 14, los intervalos del CV activo incluyen cero. No se afirma independencia estadística ni superioridad predictiva. Ambos siguen siendo candidatos que deberán tratarse adecuadamente durante la selección posterior.

**¿Qué cambió en el PCA?** Se compararon tres especificaciones sobre los mismos casos: la original, otra sin volumen y otra que además utiliza CV activo. El porcentaje de varianza resumida cambia con las variables incluidas. Ninguno de esos porcentajes mide cuánto abandono se explica ni justifica elegir automáticamente un conjunto para el clasificador.

**¿Por qué aumentar el remuestreo?** Se buscó evaluar la estabilidad numérica de los intervalos, manteniendo agrupadas las inscripciones de cada persona. Se pasó de 500 a 5.000 remuestreos y se compararon prefijos de 500 y 2.000. Las 66 comparaciones entre 2.000 y 5.000 quedaron dentro de 0,005 unidades del efecto; el cambio máximo fue 0,00299394. No es una garantía universal de convergencia: los prefijos comparten secuencia y los intervalos siguen siendo puntuales y exploratorios.

**¿Qué ocurrió con la familia diversidad?** El marco enumera seis familias derivables, pero esta implementación desarrolla cinco. Su ausencia ahora está justificada expresamente como delimitación del conjunto estudiado. No se presenta como una variable calculada ni como una familia cuya falta de utilidad haya sido probada. Una ampliación exigiría integrar tipos de recursos y sus oportunidades por módulo.

**¿Qué puede afirmarse que fue verificado?** Se ejecutaron los tres notebooks en procesos Python nuevos, pasaron 49 comprobaciones independientes y se contrastaron clics, días activos y CV activo con la fuente completa para las cinco poblaciones elegibles. Se comprobaron referencias y figuras de los cuatro documentos y se revisó su presentación. La reproducción analítica no equivale a una revisión bibliográfica exhaustiva ni a validar un modelo inexistente.

## Decisiones que conviene dejar documentadas en la reunión

1. Ratificación del retiro registrado futuro y de la población elegible al corte, reconociendo las diferencias con A3.1.
2. Tratamiento de puntajes previsto en A2.5 cuando no se dispone de fecha de publicación; mantenimiento de inactividad como predictor complementario.
3. Escenario de generalización prioritario: otras personas, nuevas presentaciones o ambos; de él dependen las particiones.
4. Protocolo para comparar ventanas y modelos, incluyendo calibración, anticipación, métricas y selección de umbral dentro del entrenamiento.

La evidencia consultable se encuentra en `entrega.md`, los registros de ejecución y los tres informes de `correcciones_2026_09_10`. La versión anterior del informe de reunión conserva valor histórico, pero sus referencias a 500 remuestreos y a resultados aún no publicados deben actualizarse con este complemento.
