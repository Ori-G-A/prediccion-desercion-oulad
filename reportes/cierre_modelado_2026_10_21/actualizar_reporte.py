from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
folder=ROOT/'reportes/reunion_asesor_2026_10_22'
p=folder/'reporte_base.md';s=p.read_text(encoding='utf-8')
s=s.replace('La revisión académica de esos resultados, su integración final en la tesis y el prototipo siguen pendientes.','Se revisaron las salidas, se integraron los hallazgos y límites en las fuentes activas y se implementó una primera versión local del prototipo. La revisión con el asesor y la evaluación del prototipo con usuarios siguen pendientes.')
s=s.replace('su situación actual se distingue del prototipo, todavía no iniciado.','se implementó una primera versión local del prototipo de predicción e interpretación.')
s=s.replace('**Esa versión de la tesis aún no contiene el cierre de cálculos del 21 de octubre.**','El 21 de octubre se incorporaron posteriormente la evaluación final, la interpretación de SHAP y sus límites. Se conserva el respaldo de la versión previa.')
s=s.replace('Falta revisión e interpretación académica de los resultados.','Métricas e intervalos revisados desde salidas guardadas; falta discusión con el asesor.')
s=s.replace('Integración parcial compilada el 20 de octubre. Falta incorporar y revisar los resultados finales, discusión, conclusiones y composición.','Resultados y límites integrados el 21 de octubre; revisión académica de los autores y el asesor pendiente.')
s=s.replace('No iniciado según la evidencia documental consultada; sigue siendo un producto pendiente.','Primera versión local implementada: métricas, calibración y explicaciones por corte. Evaluación con usuarios y cobertura completa de requisitos pendientes.')
s=s.replace('El siguiente trabajo es revisar conjuntamente discriminación, calibración, errores, intervalos y anticipación; interpretar SHAP con sus límites; integrar la evidencia en los capítulos y construir el prototipo previsto.','Se revisaron conjuntamente discriminación, calibración, errores, intervalos y anticipación, se interpretó SHAP y se integraron resultados en los capítulos. El siguiente trabajo es discutir las conclusiones con el asesor y evaluar el prototipo con sus usuarios previstos.')
s=s.replace('Actualmente se trabaja en las explicaciones y en la revisión de resultados; faltan su integración final en la tesis y el prototipo.','Las explicaciones ya se calcularon y revisaron; se integraron los resultados en la tesis y se preparó una primera versión local del prototipo. Quedan pendientes su evaluación con usuarios y la discusión académica de los hallazgos.')
data=json.loads((ROOT/'reportes/cierre_modelado_2026_10_21/sintesis.json').read_text(encoding='utf-8'))
def f(x):return f'{x:.3f}'.replace('.',',')
table=['| Día | Principal | AP e intervalo del 95 % | Precisión | Sensibilidad |','| --- | --- | --- | --- | --- |']
for r in data['principales']:
    ci=next(x for x in data['intervalos'] if x['corte']==r['corte'] and x['modelo']==r['modelo'] and x['metrica']=='ap')
    name='Random Forest' if r['modelo']=='random_forest' else 'XGBoost'
    table.append(f"| {r['corte']} | {name} | {f(r['ap'])} [{f(ci['inferior'])}; {f(ci['superior'])}] | {100*r['precision']:.1f} % | {100*r['sensibilidad']:.1f} % |".replace('.',','))
s+='''

<!-- PAGE -->
## 7. Hallazgos revisados para discutir en la reunión
La tabla resume los candidatos principales elegidos antes de observar la prueba. AP describe la ordenación de casos a distintos niveles de recuperación de retiros; precisión y sensibilidad corresponden al umbral congelado de cada candidato.

'''+ '\n'.join(table)+'''

**Hay señal predictiva, pero también límites importantes.** La AP de los principales supera la referencia constante en los cinco cortes; los intervalos pareados de la diferencia quedaron por encima de cero. No obstante, los intervalos de la diferencia de AP entre principal y logística incluyen cero en los cinco cortes. No corresponde afirmar una superioridad concluyente de los principales sobre logística, ni equivalencia entre modelos.

**Las falsas alertas requieren atención.** Al día 7 se detectan 964 de 1.327 retiros posteriores y se generan 2.756 falsas alertas; se alertaría sobre el 64,0 % de las inscripciones. Al día 28 se detectan 358 retiros, se omiten 645 y se generan 841 falsas alertas; se alertaría sobre el 21,8 %. Detectar más retiros y concentrar mejor las alertas son objetivos distintos. El criterio F1 usado para comparar no reemplaza una política institucional de atención.

**La probabilidad no equivale a certeza.** Los principales tienen menor Brier que la referencia constante, pero la diferencia es pequeña. No se demuestra calibración perfecta, utilidad educativa ni mejora atribuible exclusivamente a calibrar. Las medianas de anticipación, de 61,5 a 88 días, describen únicamente alertas correctas; no prueban que una intervención hubiera evitado esos retiros.

**SHAP describe el modelo, no las causas.** En el primer corte destacan los clics recientes; desde el día 28 domina la proporción entregada de evaluaciones con vencimiento hasta el corte. Las contribuciones dependen de la referencia y de indicadores relacionados. Se verificaron 500 explicaciones, pero no su estabilidad ante otras muestras. Las cinco poblaciones y sus horizontes cambian, por lo que no se propone un día óptimo comparando solamente AP.

La revisión reprodujo las métricas desde las predicciones, verificó 56 huellas de salidas, recalculó los percentiles desde las réplicas guardadas y comprobó las sumas SHAP. No repitió entrenamientos ni utilizó la prueba para cambiar los candidatos. El prototipo muestra estas mismas cifras y permite consultar casos sin identificadores de estudiantes; sus pruebas funcionales no sustituyen una evaluación con usuarios.
'''
p.write_text(s,encoding='utf-8')
p=folder/'generar_reporte.py';s=p.read_text(encoding='utf-8')
s=s.replace("count=len(rows[0]);widths=([116,72,145,150] if count==4 else [145,338])","count=len(rows[0]);widths=({2:[145,338],4:[116,72,145,150],5:[30,90,175,90,98]}[count])")
s=s.replace('len(reader.pages)==6','len(reader.pages)==7').replace('se esperaban seis páginas','se esperaban siete páginas')
s=s.replace('su revisión e interpretación académica están pendientes.','sus salidas y patrones se revisaron; la discusión con el asesor está pendiente.')
p.write_text(s,encoding='utf-8')
print('Reporte actualizado con hallazgos y estado; regenerar desde evidencia vigente.')
