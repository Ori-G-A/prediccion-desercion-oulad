# Orden de ejecución del modelado OULAD

Decisión persistente del proyecto, 19 de octubre de 2026. El usuario solicitó verificar el orden, conservarlo y crear una skill que lo ejecute. Esta regla concreta la secuencia del protocolo de validación; no modifica población, evento, cortes, particiones, predictores ni espacios de búsqueda, y no acredita aprobación del director.

## Secuencia vigente y condiciones para avanzar

| Etapa | Actividad y propósito | Evidencia de cierre |
|---|---|---|
| 0. Comprobar el estado | Leer AGENTS.md, el protocolo, configuración y manifiesto congelados, contratos y resultados. Identificar ejecuciones completas, fallidas y pendientes antes de iniciar trabajo. | Huellas válidas, entorno documentado, separación por personas y ejecución compatible; el estado resumido no sustituye los artefactos. |
| 1. Completar las búsquedas | Ejecutar las configuraciones previstas de Random Forest, XGBoost, LightGBM y TabNet con los mismos cinco pliegues por personas y cinco cortes. Reutilizar la búsqueda logística completa cuando su contrato sea compatible. | Cada configuración tiene sus cinco ajustes válidos, predicciones verificables y AP media. Las comprobaciones reducidas no cuentan como búsquedas completas. |
| 2. Seleccionar por validación | Elegir la configuración de cada familia y la familia principal de cada corte mediante AP media interna y los desempates ya establecidos. Mantener también los candidatos por familia para la comparación prevista. | Tabla de selección y `seleccion_validacion.json`, con rutas y huellas de los resultados que sustentan cada decisión. No usar métricas del conjunto de umbral ni de prueba para escoger la familia. |
| 3. Preparar los candidatos finales | Reajustar las configuraciones en todo el conjunto de ajuste, calibrar en el conjunto exclusivo de calibración y elegir el umbral en su conjunto exclusivo, en ese orden. | Modelos guardados y recargables, base inmutable durante calibración, umbrales reproducibles y conjuntos separados. No reajustar después con calibración o umbral. |
| 4. Congelar la evaluación | Fijar qué modelos de cada familia y corte se evaluarán, cuál es principal, sus probabilidades, umbrales, métricas, comparaciones, remuestreo por personas y análisis de anticipación. Verificar el evaluador sin utilizar la prueba real. | `paquete_evaluacion.json` con huellas de modelos, selección, datos, particiones y código; pruebas del evaluador con datos sintéticos o de desarrollo. |
| 5. Evaluar la prueba reservada | Ejecutar el paquete predefinido sin seleccionar ni reajustar a partir de sus resultados. Reportar métricas, incertidumbre y tamaños por corte y oferta según el protocolo. | Predicciones finales guardadas, métricas e intervalos reproducibles y registro de primera evaluación. Un fallo técnico se corrige conservando evidencias y el paquete; no autoriza una nueva búsqueda. |
| 6. Interpretar y cerrar | Realizar las explicaciones SHAP y el análisis académico, integrar resultados y límites en las fuentes activas y verificar la composición. | Variante, referencia, escala y objeto explicado documentados; capítulos integrados y compilados, con revisión visual o pendiente explícito. No presentar SHAP como causalidad. |

La documentación y el registro de incidencias acompañan todas las etapas. No se espera hasta la etapa 6 para conservar evidencia. Cada avance se registra en `estado_ejecucion_modelos.json` con rutas de respaldo; el archivo orienta la continuación y debe revalidarse contra las salidas.

## Precisiones metodológicas

La selección entre familias se realiza antes de mirar la prueba. La calibración y el umbral pueden haberse calculado para una familia cuya configuración ya fue seleccionada, como ocurrió con logística, sin esperar a las demás. Esas salidas pueden reutilizarse si su contrato es compatible y no orientan la selección entre familias. El paquete de evaluación solo se cierra cuando todas las búsquedas previstas están resueltas.

La evaluación final puede incluir el candidato congelado de cada familia para la comparación prevista. Una familia que obtenga mejores cifras en prueba no reemplaza retrospectivamente a la principal seleccionada por validación. No se elegirá una ventana óptima comparando únicamente AP entre cortes: sus poblaciones y horizontes cambian.

Antes de abrir la prueba se fijará también el diseño de las explicaciones: modelo base o predictor calibrado, escala de salida, referencia tomada del ajuste, tratamiento de dependencia y regla de muestreo. El cálculo final de SHAP y su interpretación pueden realizarse después. Si SHAP motiva cambios de variables o del modelo tras observar la prueba, esos cambios pertenecen a un nuevo estudio exploratorio y no reutilizan esa prueba como confirmación independiente.

Las correcciones de código y de incoherencias metodológicas necesarias sí se permiten antes de la prueba: se documentan, se conserva la versión anterior y se reejecuta lo afectado con una versión nueva. Esto sustituye una lectura absoluta de «no cambiar variables o ampliar la búsqueda»: no se modifica el protocolo solo para perseguir cifras favorables, pero tampoco se conserva un error conocido. Los cambios sustantivos de alcance, población, evento o criterio de selección requieren la decisión explícita correspondiente, conforme a AGENTS.md.

## Situación comprobada al guardar esta regla

La búsqueda logística está completa para los cinco cortes; las otras cuatro familias solo tienen comprobaciones funcionales. El entrenador actual elige configuraciones dentro de cada familia y puede calibrarlas, pero no selecciona entre familias ni evalúa la prueba. Por ello, la ejecución integral deberá implementar y comprobar la consolidación de selección, el manifiesto de evaluación, el evaluador reservado y SHAP cuando llegue a esas etapas. La skill no debe afirmar que esos componentes ya existen.

La etiqueta `estado: parcial` del resumen actual no basta para decidir si una familia terminó: una ejecución que contiene solo logística sigue marcada como parcial respecto de las cinco familias. Se revisan los resultados y los pliegues de cada familia y corte, no solo esa etiqueta.

Fuentes de implementación: `reportes/protocolo_validacion_2026_10_19/protocolo.md`, su carpeta `implementacion/`, `src/entrenamiento_oulad.py` y `reportes/entrenamiento_2026_10_19/revision.md`. Los artefactos de entrenamiento previos se conservan; esta decisión no inicia nuevas búsquedas por sí sola.

## Opción de exploración futura: SVM

Decisión del usuario del 21 de octubre de 2026: conservar las máquinas de soporte vectorial (SVM) como una opción para explorar en un trabajo futuro. La ejecución actual mantiene los cinco candidatos y sus configuraciones congeladas; esta decisión no incorpora entrenamientos adicionales ni modifica la selección vigente. No se ha evaluado SVM en esta comparación y no se afirma que su desempeño sea inferior o superior al de los candidatos incluidos. Su posible incorporación requerirá definir y documentar un protocolo propio de comparación. Si la prueba actual ya fue observada, no podrá reutilizarse como confirmación independiente para seleccionar o validar esa ampliación. El registro de esta opción no acredita aprobación académica ni obliga a ejecutarla.

## Sustento y límites de la verificación

Se contrastó el orden con documentación oficial consultada el 19 de octubre de 2026:

- Scikit-learn developers. [Cross-validation: evaluating estimator performance, versión 1.8](https://scikit-learn.org/1.8/modules/cross_validation.html): selección con validación y reserva de prueba; transformaciones aprendidas dentro del entrenamiento.
- Scikit-learn developers. [Probability calibration, versión 1.8](https://scikit-learn.org/1.8/modules/calibration.html): calibración de un estimador congelado con datos separados de su ajuste.
- Scikit-learn developers. [Tuning the decision threshold, versión 1.8](https://scikit-learn.org/1.8/modules/classification_threshold.html): elección del umbral separada del ajuste del clasificador.
- SHAP developers. [TreeExplainer](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html): importancia de la referencia, la dependencia entre variables y la escala explicada. No implica que TreeExplainer sirva para todas las familias o para cualquier envoltura calibrada.

Veredicto: el orden es metodológicamente coherente para la generalización acordada, con las condiciones anteriores. Esta verificación del diseño y de su correspondencia con el código no demuestra desempeño futuro ni elimina las limitaciones ya documentadas.
