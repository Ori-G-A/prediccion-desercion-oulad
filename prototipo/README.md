# Prototipo local de consulta

Rediseño narrativo del 21 de octubre: resultado y errores → comparación → probabilidades → explicaciones → casos → contexto. Incorpora gráficos con etiquetas directas y tablas desplegables, siguiendo orientaciones públicas de Storytelling with Data. Datos sin modificaciones. Fuentes, comprobaciones y pendientes: `reportes/storytelling_prototipo_2026_10_21/revision.md`. Recargar con Ctrl+F5 después de sustituir el archivo.

Abrir `OULAD.html` con un navegador mediante doble clic. Es un archivo autónomo con datos y código incorporados: no necesita servidor, conexión a internet ni instalación. Se añadió esta opción después de que el acceso HTTP local no respondiera. `index.html` es la versión de desarrollo y requiere conservar `app.js` y `datos.js` en la misma carpeta.

Permite consultar los cinco cortes, métricas de las cinco familias y dos referencias, calibración con tamaños de grupo, importancia media SHAP y cien casos explicados por corte. Los identificadores de estudiantes no se exportan. La tabla distingue el principal elegido antes de la prueba. No permite reajustar, cambiar umbrales ni generar nuevas predicciones.

Los datos se generan con `scripts/generar_resultados_finales.py` después de `scripts/revisar_cierre_modelado.py`. El generador llama a `scripts/completar_prototipo.py`, que también puede ejecutarse por separado para actualizar la interfaz y sus datos adicionales. La fuente predictiva es el paquete congelado de octubre de 2026.

La versión ampliada del 21 de octubre incorpora contexto por edad, discapacidad registrada, privación del área y región desde `03_niveles.csv`; se cotejan numeradores, denominadores y porcentajes con el anexo activo. Es la población elegible completa, distinta del conjunto de prueba. No representa la totalidad de la exploración del proyecto. Las explicaciones individuales incorporan valores observados antes del preprocesamiento y barras divergentes desde cero. No se exportan identificadores personales.

Verificación: `.venv/Scripts/python.exe scripts/completar_prototipo.py` y `node prototipo/verificar_funciones.cjs`. El segundo comprueba eventos con un DOM mínimo, no con un navegador real. El usuario confirmó apertura y aportó capturas de la versión anterior. La revisión visual de esta ampliación y la evaluación de comprensión siguen pendientes. Matriz de requisitos y guía: `reportes/mejora_prototipo_2026_10_21/revision.md`.
