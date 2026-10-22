"""Integración localizada sobre fuentes activas respaldadas; ejecutar una vez."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'Plantilla_ProyAplicado'
def replace(file,old,new):
    p=D/file;s=p.read_text(encoding='utf-8');assert old in s,(file,old)
    p.write_text(s.replace(old,new),encoding='utf-8')
p=D/'desarrollo3.tex';s=p.read_text(encoding='utf-8')
marker=r'\section{Resultados disponibles y límites}'
assert marker in s
s=s.split(marker)[0]+r'\input{resultados_modelos}'+'\n'
s=s.replace('se congelarán','se congelaron').replace('Se reportarán','Se reportaron').replace('serán descriptivos','se presentan como descriptivos').replace('se declararán','se declararon').replace('se estimará','se estimó').replace('describirán','describen').replace('no incorporarán','no incorporan')
p.write_text(s,encoding='utf-8')
(D/'desarrollo4.tex').write_text('\\label{editorial:shapestado}\n\\input{resultados_shap}\n',encoding='utf-8')
(D/'desarrollo5.tex').write_text(r'''\label{editorial:prototipo}
\section{Prototipo local para consultar predicciones y explicaciones}
Se implementó una primera versión local de consulta, accesible desde un navegador y alimentada por los resultados congelados. Permite elegir el corte temporal, consultar tamaños de población, métricas, intervalos de AP y errores, comparar las familias e inspeccionar la calibración con sus denominadores. La familia principal se distingue de las demás sin permitir sustituirla por resultados de prueba.

La consulta de SHAP presenta magnitudes medias y explicaciones individuales de las cien inscripciones seleccionadas por corte. En cada caso se muestran la probabilidad, el valor de referencia, las contribuciones positivas y negativas y su suma. Los casos usan una numeración local sin exponer identificadores de estudiantes. La interfaz conserva la regla de alerta congelada; no permite alterar umbrales, reajustar modelos ni producir predicciones nuevas.

Esta versión se concentra en predicción e interpretación y no integra todavía toda la exploración del proyecto. Su alcance es académico: no se conecta a un LMS activo ni ejecuta intervenciones. El desarrollo funcional constituye un avance del objetivo de prototipo, pero quedan pendientes su evaluación de comprensión con los autores y usuarios previstos y el cotejo completo de los requisitos. No se presenta como una herramienta institucional validada ni como evidencia de reducción del abandono.
''',encoding='utf-8')
replace('abstract.tex','Los resultados dejan una base documentada para comparar modelos, pero aún no permiten elegir una ventana óptima ni afirmar capacidad predictiva o efectividad educativa. Se fijó una partición por personas para evaluar casos nuevos dentro de las ofertas disponibles y se completó la búsqueda logística. La comparación entre familias está en ejecución; la prueba final, la interpretación mediante SHAP (atribuciones de las variables a las predicciones del modelo) y el prototipo de visualización permanecen pendientes.',
 r'Se compararon cinco familias mediante 3\,200 ajustes con separación por personas, calibración y umbral en conjuntos exclusivos. La prueba reservada mostró AP entre 0,233 y 0,286 en los candidatos principales, por encima de la referencia constante; sin embargo, la precisión de las alertas estuvo entre 22,2\,\% y 29,9\,\%. La interpretación mediante SHAP describió contribuciones de actividad y entregas, sin atribuirles causalidad. Se implementó un prototipo local de consulta pendiente de evaluación con usuarios. Los resultados no permiten elegir una ventana óptima por AP ni afirmar efectividad educativa o generalización a ofertas futuras.')
replace('introduccion.tex','El capítulo de modelos presenta el protocolo y los resultados internos disponibles; los capítulos de SHAP y prototipo distinguen la preparación del trabajo pendiente.',
 'El capítulo de modelos presenta el protocolo y la evaluación reservada; los capítulos de SHAP y prototipo explican las contribuciones de variables y la primera versión local de consulta, junto con sus límites.')
replace('figura_ruta.tex','Modelado predictivo: en ejecución','Modelado predictivo: evaluado')
replace('figura_ruta.tex','Partición por personas y búsqueda logística completas; comparación en curso y prueba final reservada.','Búsquedas y evaluación reservada completas; interpretación de desempeño y límites.')
replace('figura_ruta.tex','Interpretación y comunicación: pendientes','Interpretación y comunicación: avance')
replace('figura_ruta.tex','Explicar el modelo mediante SHAP y desarrollar el prototipo de visualización.','SHAP calculado y prototipo local implementado; evaluación con usuarios pendiente.')
replace('avance_objetivos.tex','La partición por personas y la búsqueda logística están completas; las otras búsquedas y la evaluación final siguen pendientes;',
 'Las búsquedas de cinco familias y la evaluación reservada están completas; falta la revisión académica de la comparación;')
replace('avance_objetivos.tex','Diseño de SHAP y referencia preparados; cálculo y selección comparativa pendientes. El marco teórico no constituye un resultado de interpretación.',
 'Selección por validación y 500 explicaciones SHAP calculadas y verificadas. Se integraron los patrones y límites; la estabilidad de las atribuciones no fue evaluada.')
replace('avance_objetivos.tex','5. Diseñar el prototipo & No iniciado','5. Diseñar el prototipo & Parcial')
replace('avance_objetivos.tex','pendiente de implementación. Las figuras explicativas de la tesis no equivalen al prototipo de predicciones e interpretabilidad previsto.',
 'primera versión local de consulta de predicción e interpretabilidad implementada. Faltan el cotejo completo de requisitos y la evaluación con usuarios; la exploración no está integrada en su totalidad.')
replace('Conclusiones.tex','Se congeló la entrada predictiva y se completó la búsqueda logística, mientras continúa la comparación de modelos. La prueba final, el cálculo de SHAP y el prototipo permanecen pendientes. Por tanto, el objetivo general sigue en desarrollo y no se afirma una reducción del abandono ni capacidad comprobada para predecir casos nuevos.',
 r'Se congeló la entrada predictiva y se completó la comparación con prueba reservada. Los candidatos principales superaron la referencia constante en AP, pero presentaron una precisión de alertas entre 22,2\,\% y 29,9\,\%, con cantidades relevantes de falsas alertas y retiros no detectados. La evidencia apoya una capacidad discriminativa limitada en personas nuevas dentro de las ofertas disponibles; no demuestra utilidad institucional, generalización a periodos futuros ni reducción del abandono. SHAP permitió describir el papel de la actividad y las entregas sin establecer causalidad. Se implementó una primera versión local de consulta; la revisión académica y la evaluación del prototipo con usuarios permanecen pendientes.')
replace('Conclusiones.tex','pero todavía no se ha completado la evaluación del objetivo general.','y ya cuenta con evaluación reservada; el cierre académico del objetivo general sigue pendiente.')
replace('Conclusiones.tex','El siguiente paso es completar las búsquedas bajo el protocolo fijado y evaluar el paquete congelado para personas no vistas dentro de las ofertas disponibles.',
 'El siguiente paso es revisar los hallazgos con los autores y el asesor, completar la evaluación del prototipo y acordar la presentación final. Una posible exploración futura de máquinas de soporte vectorial (SVM) requerirá un protocolo nuevo; la prueba ya observada no podrá reutilizarse como confirmación independiente de cambios motivados por estos resultados.')
replace('proyecto.tex','20 de octubre de 2026','21 de octubre de 2026')
print('Fuentes activas integradas; revisar referencias de estado restantes y compilar.')
