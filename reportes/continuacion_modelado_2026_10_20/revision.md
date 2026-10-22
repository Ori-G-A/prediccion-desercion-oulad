# Reanudación del 20 de octubre de 2026

Se comprobó que no quedaban procesos Python de la sesión anterior. Había 85 ajustes de Random Forest y cinco de referencia, cinco más que en la última revisión del día anterior. Se reanudó el contrato completo sin modificar el entrenador, dependencias, particiones ni configuración. La ejecución produjo ajustes nuevos. La espera anterior durante la importación de pandas dejó de reproducirse; no se determinó su causa raíz.

Las pruebas del evaluador detectaron acceso denegado al reemplazar archivos en el directorio temporal del entorno restringido. Se trasladaron sus archivos sintéticos a tmp/pruebas_evaluador dentro del proyecto. También se corrigió la comparación de rutas con separadores de Windows en la verificación de huellas. Pasaron cuatro pruebas: rechazo previo a lectura, huellas obligatorias, manifiesto de 25 candidatos y detección de alteración, y flujo sintético sin ajuste con anticipación y restricción de reapertura. El flujo usa veinte réplicas solo para comprobar código; no constituye la evaluación reservada de 2.000 réplicas.

La prueba real permanece reservada. El congelador no se ejecutará antes de resolver las búsquedas, consolidar selección y verificar los candidatos. La integración documental y SHAP siguen pendientes.

## Preparación de interpretación sin abrir prueba

Se incorporaron SHAP 0.51.0, numba 0.68.0, llvmlite 0.50.0 y slicer 0.0.8, sin actualizar dependencias ya instaladas. pip check pasó. Las versiones se conservan en requirements-interpretacion.txt y en el inventario de esta carpeta. La prueba sintética de SHAP reprodujo contribuciones analíticas conocidas y verificó aditividad.

El diseño se conserva en shap/diseno.json: predictor calibrado principal por corte, escala de probabilidad y enmascaramiento marginal con cincuenta inscripciones de ajuste elegidas con semilla fija. Se explicarán hasta cien inscripciones de prueba por corte, elegidas sin desenlace ni puntuación; veinte ciclos de permutaciones. Este presupuesto corresponde a interpretación aproximada, no a una búsqueda ni a un criterio de selección. Los indicadores dependientes pueden producir combinaciones poco realistas al enmascararse; las contribuciones no son causales. La referencia está guardada con claves y huellas, y no se ha leído la prueba.

Fuentes técnicas consultadas: documentación oficial de SHAP, PermutationExplainer (https://shap.readthedocs.io/en/latest/generated/shap.PermutationExplainer.html) e Independent (https://shap.readthedocs.io/en/latest/generated/shap.maskers.Independent.html). La consulta orienta el diseño; el cálculo real sigue pendiente.

## Auditoría y nueva reanudación de la tarde

Se confirmó la ausencia de procesos Python antes de reanudar el contrato completo en la sesión 95305, sin cambiar el entrenador. Se conservaron 458 ajustes: 150 de Random Forest, 150 de XGBoost, 150 de LightGBM y ocho de TabNet. No se determinó la causa de terminación del proceso anterior; no se atribuye a un error de modelado sin evidencia.

La auditoría de familias disponibles terminó correctamente. Recalculó AP y verificó huellas, claves, etiquetas y cobertura de los cinco pliegues de cada configuración: 200 ajustes logísticos de cinco cortes y 450 de las otras tres familias en el corte siete. El archivo auditoria_disponibles.json conserva las huellas y las lecturas de ajuste. No realiza selección global ni abre prueba. TabNet y los otros cortes continúan pendientes.

## Integración documental parcial y composición

Las fuentes activas incorporan el protocolo ejecutable, la búsqueda logística terminada y el diseño previsto de evaluación e interpretación, distinguiéndolos de resultados aún pendientes. Se conservaron originales en respaldo/2026-10-20_pre_integracion_modelado. El flujo ordinario scripts/compilar_proyecto.ps1 produjo proyecto.pdf de 93 páginas; el registro confirma compilación terminada. Se revisaron visualmente las páginas 2, 14, 17, 27, 68, 69, 70, 71, 73, 74, 80 y 92, sin recortes ni solapamientos observados. Esta comprobación no equivale a revisión integral de todo el documento ni a aprobación académica. La integración de resultados de las búsquedas restantes, prueba y SHAP sigue pendiente.

## Continuación persistente del protocolo

Se añadió scripts/continuar_protocolo_modelado.py y se comprobaron tres condiciones de control con procesos simulados: exclusión de supervisores duplicados, interrupción antes de congelación y prueba cuando falla la selección, y rechazo de nuevo entrenamiento si existe primera apertura de prueba. No son pruebas de desempeño predictivo. El supervisor se inició oculto, esperando el proceso de entrenamiento 8496; no inicia una segunda búsqueda mientras ese proceso exista. Al terminar, reanuda idempotentemente el contrato para comprobar pliegues persistidos, consolida todas las búsquedas, verifica el evaluador, congela candidatos y ejecuta evaluación y SHAP solo si cada paso anterior termina correctamente. Los errores detienen las etapas dependientes y quedan registrados.

El estado operativo está en continuacion_actual.json, el historial en continuacion.jsonl y las salidas de cálculos en continuacion_calculos.log. El supervisor actualiza el conteo cada minuto durante entrenamiento. No declara cierre académico automático: la interpretación de resultados, integración final del documento y revisión de composición requieren continuar después de esos cálculos. No se atribuye aprobación académica ni se modifican particiones, configuraciones o criterios.

## Incidencia del contador y recuperación, 16:40

El supervisor terminó a las 16:07:53 por TimeoutExpired del contador de progreso (límite de 30 segundos). El entrenador 8496 permaneció activo y siguió guardando ajustes; el registro viejo de 484 no representaba el progreso posterior. Se corrigió progress() para registrar y reintentar fallos del contador sin detener la supervisión. Las verificaciones de selección, congelación y evaluación siguen siendo obligatorias y sus fallos detienen las etapas dependientes. Pasaron cuatro pruebas, incluida la nueva prueba de demora del contador. Se reanudó únicamente el supervisor, conservando el entrenador y sus artefactos. A las 16:40:26 había 503 ajustes registrados correctos, incluidos 53 de TabNet. La prueba permanece reservada.

## Decisión del 21 de octubre de 2026: SVM como opción futura

Por solicitud explícita del usuario, se registró SVM como opción de exploración futura en PROTOCOLO_EJECUCION_MODELOS.md. Se mantiene la comparación actual de cinco candidatos, sin cambiar contratos, particiones ni configuraciones. No se inicia entrenamiento SVM ni se infiere aprobación académica. La decisión complementa el alcance vigente; no sustituye ninguna regla de ejecución. Su eventual incorporación necesitará un diseño documentado que no reutilice una prueba ya observada como confirmación independiente. La integración de esta opción en trabajos futuros del documento queda para la siguiente actualización de los capítulos.
