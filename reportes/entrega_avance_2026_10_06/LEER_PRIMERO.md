# Versión preparada para revisión del director

Fecha: 6 de octubre de 2026. La actividad está habilitada hasta el 19 de octubre de 2026 a las 23:59. Se toma como evidencia la captura del usuario, sin atribuir acceso directo a la plataforma.

## Archivos para compartir

- `Proyecto_avance_para_revision.pdf`: documento actualizado de 94 páginas; copia de las fuentes activas de `Plantilla_ProyAplicado` compiladas en esta revisión.
- `Cronograma_y_avance_para_revision.pdf`: informe de 3 páginas, con actividades, estados, evidencia y propuesta de preparación de la entrega. Su fuente editable es `Cronograma_y_avance.md`.
- `Consultas_para_el_director.md`: texto sugerido para acompañar los dos archivos; no enviado.

El usuario aclaró que todavía no ha tratado estos acuerdos con el director y que desea enviar primero el documento para recibir sugerencias. Por eso, el paquete está preparado para esa revisión previa. El cronograma general sigue por acordar; no se presenta como aprobado ni como una entrega ya realizada. La meta del 16 de octubre es una propuesta de cierre de la versión candidata y permite seguir mejorando la claridad hasta integrar las observaciones.

## Qué se corrigió

Se explicitó la selección de variables base y su diferencia frente a la selección durante el entrenamiento; se corrigieron los estados de A1.3 y A2.7; y se armonizaron la tabla CRISP-DM y el capítulo de modelado. La estratificación propuesta en A3.2 del anteproyecto se conserva como referencia, con una explicación de los aspectos que faltan precisar. No se ejecutó una partición ni se cambió el evento, la población, los cortes o las cifras.

Se mantuvo la voz académica e impersonal. Los nuevos pasajes explican para qué se seleccionan las variables, qué información se utiliza y qué no puede concluirse todavía. La revisión integral del 5 de octubre se conserva como antecedente; esta sesión revisó y corrigió los apartados afectados, no se presenta como una nueva auditoría bibliográfica o matemática completa.

Verificaciones, límites y hallazgos: `Revision_y_pendientes.md`. Comprobaciones ejecutadas: `verificaciones_independientes.json`, `cotejo_seleccion_y_poblaciones.json` y `verificacion_documental.json`. Diferencias frente al respaldo: `cambios.diff`.

## Siguiente paso

Compartir ambos PDF con el director y recoger sus observaciones. Antes de la entrega institucional, integrar los acuerdos del cronograma, revisar los recursos de estructura y plantilla del curso y realizar la lectura de ambos autores. No hace falta esperar una rúbrica inexistente para solicitar esta revisión.

## Reproducción

Desde la raíz, ejecutar las verificaciones con `.venv/Scripts/python.exe scripts/verificar_entrega_2026_10_06.py`. Compilar las fuentes activas con `./scripts/compilar_proyecto.ps1`. El script `scripts/preparar_paquete_avance_2026_10_06.py` genera el cronograma, copia el PDF activo y verifica el paquete; requiere Python con reportlab, pypdf y Pillow, y la ruta Poppler indicada en su cabecera. Se usó el Python integrado de Codex para este último script.

No ejecutar integradores antiguos para recompilar: reconstruyen fuentes y podrían sustituir correcciones posteriores. Se preservó el estado previo en `respaldo/2026-10-06_pre_entrega_avance/Plantilla_ProyAplicado`.
