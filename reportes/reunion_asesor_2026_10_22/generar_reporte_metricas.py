"""Informe enfocado para reunión: evidencia guardada, decisiones y lectura aplicada."""
import csv, json, hashlib, shutil
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
F=Path(__file__).resolve().parent
S=ROOT/'reportes/cierre_modelado_2026_10_21'
data=json.loads((S/'sintesis.json').read_text(encoding='utf-8'))
selection=json.loads((ROOT/'reportes/continuacion_modelado_2026_10_20/seleccion_validacion.json').read_text())
config=json.loads((ROOT/'reportes/protocolo_validacion_2026_10_19/implementacion/configuracion.json').read_text())
metrics=list(csv.DictReader((S/'metricas_todas.csv').open(encoding='utf-8')))
names={'regresion_logistica':'Logística','random_forest':'Random Forest','lightgbm':'LightGBM','xgboost':'XGBoost','tabnet':'TabNet'}
models=list(names)
def n(v):return f'{int(v):,}'.replace(',','.')
def f(v,k=3):return f'{float(v):.{k}f}'.replace('.',',')
def pct(v):return f(100*v,1)+' %'
def ref(c):return next(r for r in metrics if int(r['corte'])==c and r['modelo']=='referencia')
def ci(p,key):return next(r for r in data['intervalos'] if r['corte']==p['corte'] and r['modelo']==p['modelo'] and r['metrica']==key)
pages=[]
def page(title):pages.append([('title',title)])
def p(text):pages[-1].append(('p',text))
def h(text):pages[-1].append(('h',text))
def table(headers,rows,widths):pages[-1].append(('table',headers,rows,widths))

page('Decisiones y resultados del modelado')
p('Reunión con el asesor · 22 de octubre de 2026. Evidencia disponible al 21 de octubre. Oriana Giraldo Arcia y Luis Javier Rubio Hernández · PUJ Cali.')
h('Qué se completó después de la entrega')
p('Se completaron las búsquedas de cinco familias, la selección por validación, el reajuste, la calibración, la elección de umbrales y la prueba final congelada. Se realizaron 3.200 ajustes de validación cruzada. Este informe concentra las decisiones y resultados; no acredita aprobación académica ni utilidad institucional.')
h('Qué se decidió y por qué')
table(['Decisión ejecutada','Propósito y alcance'],[
['Evento y población','Predecir el retiro registrado después del corte y hasta el cierre de la oferta del módulo. Solo inscripciones vigentes en ese corte; no se atribuye motivo ni voluntariedad. Una persona puede tener varias inscripciones.'],
['Cinco momentos','Modelos separados en días 7, 14, 28, 42 y 56; actividad de 0 al corte, ambos incluidos. Cambian población y horizonte: comparar AP no determina por sí solo el día óptimo.'],
['Separación por personas','Aproximadamente 60 % ajuste, 10 % calibración, 10 % umbral y 20 % prueba. Todas las inscripciones de una persona permanecen juntas. Objetivo: personas nuevas en las ofertas disponibles.'],
['Cinco pliegues (k-fold)','En el conjunto de ajuste, entrenar en cuatro partes y validar en la restante, cinco veces. Se conservan los mismos pliegues por personas para todas las familias; no son cinco pruebas finales.'],
['26 predictores','Indicadores académicos de entregas, actividad y temporalidad. Se excluyeron identificadores, resultado final, fechas de retiro y notas sin disponibilidad temporal acreditada; contexto demográfico no incluido.'],
['Preparación dentro del pliegue','Retirar columnas enteramente ausentes y constantes según entrenamiento; imputar medianas con indicadores de ausencia. Escalar logística y TabNet. Así la parte validada no enseña su distribución al modelo.'],
['Comparación predefinida','8 configuraciones de logística y 30 por cada otra familia, en cada corte. Se exploró ponderación de clases; sin sobremuestreo sintético. Árboles/épocas fijos y sin detención temprana.'],
['Selección y decisiones finales','Mayor AP media interna; después reajuste con todo el ajuste, calibración sigmoidal exclusiva y umbral que maximiza F1 en su conjunto exclusivo. Alerta si probabilidad > umbral; no se impuso 0,5.'],
['Reserva de prueba','Se congelaron modelos, calibradores, umbrales y evaluación antes de abrir la prueba. No se sustituyó al principal por el mejor valor de prueba. Primera apertura registrada: 21 de octubre.']],[125,390])
p('Calibrar busca que las probabilidades concuerden con las frecuencias observadas: entre casos con probabilidad cercana al 20 %, se esperaría una frecuencia de retiro próxima al 20 %. No garantiza acertar cada caso. El umbral convierte esa probabilidad en alerta; bajarlo puede detectar más retiros y producir más falsas alertas.')
p('Semillas conservadas: partición 20261019; validación 20261020; búsqueda 20261021; remuestreo 20261022. Las precisiones metodológicas se presentan al asesor para revisión; no se presume su ratificación.')

page('Resultados de la búsqueda y la selección')
p('Entrenar es ajustar el modelo. Validar es medirlo en personas excluidas de ese ajuste. La tabla siguiente muestra la AP media de los cinco pliegues para la mejor configuración de cada familia; sirvió para seleccionar, por lo que no es una evaluación independiente del ganador.')
table(['Día']+list(names.values()),[[c]+[f(next(x['ap_media'] for x in selection['seleccion_por_familia'] if x['corte']==c and x['modelo']==m),4) for m in models] for c in [7,14,28,42,56]],[35,96,96,96,96,96])
p('Principal seleccionado: XGBoost en días 7, 28, 42 y 56; Random Forest en día 14. Las diferencias internas son pequeñas y la regla de selección no prueba superioridad estadística. Empate a seis decimales: logística, Random Forest, LightGBM, XGBoost y TabNet; dentro de familia, orden congelado.')
h('Configuraciones principales conservadas')
table(['Corte / familia','Configuración seleccionada'],[
['7 / XGBoost','200 árboles; profundidad 2; tasa de aprendizaje 0,03; fracción de filas 1,0 y de variables por árbol 0,8; regularización L2 = 1; pesos balanceados.'],
['14 / Random Forest','600 árboles; profundidad sin límite explícito; mínimo 30 inscripciones por hoja; raíz cuadrada del número de variables en cada división; pesos balanceados.'],
['28, 42 y 56 / XGBoost','200 árboles; profundidad 2; tasa 0,03; fracción de filas 0,8 y de variables 0,8; regularización L2 = 1; sin ponderación.']],[125,390])
h('AP en prueba final: comparación posterior, sin nueva selección')
table(['Día']+list(names.values()),[[c]+[f(next(float(x['ap']) for x in metrics if int(x['corte'])==c and x['modelo']==m),4) for m in models] for c in [7,14,28,42,56]],[35,96,96,96,96,96])
p('AP resume la precisión al recuperar progresivamente más retiros; no equivale al porcentaje de aciertos. Las páginas 4 a 8 explican todos los resultados del principal de cada corte. El archivo CSV adjunto conserva las demás métricas de las cinco familias y dos referencias en los cinco cortes.')

page('Cómo leer las métricas y la matriz')
p('La clase positiva es retiro futuro. La predicción positiva es una alerta al superar el umbral. “Negativo” significa ausencia de alerta o de retiro, según el eje; no significa una valoración del estudiante. Las métricas cuentan inscripciones, no personas únicas.')
table(['Real / predicho','Alerta','Sin alerta'],[
['Retiro posterior','VP: verdadero positivo. Retiro detectado.','FN: falso negativo. Retiro que no se detectó.'],
['Sin retiro posterior','FP: falso positivo. Falsa alerta.','VN: verdadero negativo. Ausencia de retiro correctamente clasificada.']],[125,195,195])
p('Se leen filas por desenlace real y columnas por decisión del modelo. N = VP + FP + FN + VN. Las matrices siguientes conservan ese orden; la diagonal correcta es VP y VN.')
table(['Medida y cálculo','Qué indica y qué no indica'],[
['Accuracy / exactitud\n(VP + VN) / N','Fracción total de clasificaciones correctas. Puede ser alta por acertar la clase mayoritaria sin detectar retiros. No equivale a precisión.'],
['Precisión\nVP / (VP + FP)','De las alertas, qué proporción corresponde a retiros. El complemento es la proporción de falsas alertas entre alertas, no la tasa FP/(FP+VN).'],
['Recall / sensibilidad\nVP / (VP + FN)','De los retiros que ocurrieron, qué proporción se detectó. No informa cuántas falsas alertas se produjeron.'],
['Especificidad\nVN / (VN + FP)','De las inscripciones sin retiro, qué proporción quedó sin alerta. Su complemento es la tasa de falsos positivos.'],
['F1\n2VP / (2VP + FP + FN)','Media armónica de precisión y sensibilidad. Va de 0 a 1; mayor es mejor bajo este criterio. No es porcentaje de aciertos y no considera VN. Depende del umbral.'],
['AP / precisión promedio','Resume precisión a lo largo de cambios de sensibilidad al variar el umbral; pondera por incrementos de sensibilidad. Mayor es mejor, con la prevalencia como referencia constante. No es área trapezoidal ni precisión al umbral elegido.'],
['ROC-AUC','Capacidad de ordenar mayor riesgo a un retiro que a un no retiro (empates aportan la mitad). 0,5 indica ausencia de discriminación; 1, orden perfecto. No es accuracy.'],
['Brier\nPromedio de (probabilidad - desenlace)²','Error cuadrático de las probabilidades frente a desenlaces 0/1. En este problema va de 0 a 1; menor es mejor. No se lee como porcentaje de error y no mide solo calibración.'],
['Proporción de alertas\n(VP + FP) / N','Fracción que recibiría alerta con la regla congelada. Describe volumen potencial de atención, no eficacia educativa.'],
['Anticipación mediana','Tiempo desde el corte hasta el retiro entre VP. La mitad tiene tiempos iguales o menores y la otra mitad iguales o mayores. No representa a los FN ni demuestra que una intervención funcione.']],[155,360])
p('Accuracy, precisión, sensibilidad, especificidad y F1 usan la matriz y el umbral. AP, ROC-AUC y Brier usan las probabilidades. Fuentes técnicas: documentación oficial de scikit-learn 1.8; referencias al final.')

verified=[]
for r in data['principales']:
 c=r['corte'];tp,fp,fn,tn=[int(r[k]) for k in ['tp','fp','fn','tn']];N=r['inscripciones'];alerts=tp+fp;neg=tn+fp
 checks={'exactitud':(tp+tn)/N,'precision':tp/alerts,'sensibilidad':tp/(tp+fn),'especificidad':tn/neg,'f1':2*tp/(2*tp+fp+fn),'proporcion_alertas':alerts/N}
 assert tp+fp+fn+tn==N and tp+fn==r['eventos']
 for k,v in checks.items():assert abs(v-r[k])<1e-12,(c,k)
 verified.append({'corte':c,'matriz_y_metricas_coinciden':True})
 page(f'Día {c}: {names[r["modelo"]]} en prueba final')
 p(f'{n(N)} inscripciones de {n(r["personas"])} personas; {n(r["eventos"])} retiros posteriores ({pct(r["prevalencia"])}). Alerta cuando p > {f(r["umbral"],6)} (aproximadamente {pct(r["umbral"])}). El umbral se eligió antes de observar esta prueba.')
 table(['Desenlace real / decisión','Alerta','Sin alerta','Total real'],[
 ['Retiro posterior',f'VP = {n(tp)}\nRetiros detectados',f'FN = {n(fn)}\nRetiros no detectados',n(tp+fn)],
 ['Sin retiro posterior',f'FP = {n(fp)}\nFalsas alertas',f'VN = {n(tn)}\nSin retiro y sin alerta',n(tn+fp)],
 ['Total predicho',n(alerts),n(tn+fn),n(N)]],[145,135,135,100])
 p(f'Lectura de la matriz: de {n(alerts)} alertas, {n(tp)} correspondieron a retiros y {n(fp)} no. De {n(tp+fn)} retiros reales, {n(fn)} quedaron sin alerta.')
 interval=ci(r,'ap');br=float(ref(c)['brier'])
 rows=[
 ['Accuracy',pct(r['exactitud']),f'{n(tp+tn)} de {n(N)} inscripciones se clasificaron correctamente.'],
 ['Precisión',pct(r['precision']),f'{n(tp)} / {n(alerts)} alertas fueron correctas; {pct(1-r["precision"])} de las alertas fueron falsas.'],
 ['Sensibilidad',pct(r['sensibilidad']),f'{n(tp)} / {n(tp+fn)} retiros se detectaron; se omitió el {pct(1-r["sensibilidad"])}.'],
 ['Especificidad',pct(r['especificidad']),f'{n(tn)} / {n(neg)} inscripciones sin retiro quedaron sin alerta; {pct(1-r["especificidad"])} recibió falsa alerta.'],
 ['F1',f(r['f1']),f'2 × {n(tp)} / (2 × {n(tp)} + {n(fp)} + {n(fn)}). Resume conjuntamente precisión y sensibilidad; no significa {pct(r["f1"])} de aciertos.'],
 ['AP',f(r['ap']),f'Frente a {f(r["prevalencia"])} de la referencia constante. IC 95 %: [{f(interval["inferior"])}; {f(interval["superior"])}]. Resume la ordenación al variar el umbral, no el porcentaje de alertas correctas.'],
 ['ROC-AUC',f(r['roc_auc']),f'Equivale a {pct(r["roc_auc"])} de concordancia al comparar pares retiro/no retiro, contando medio acierto en empates. Discriminación limitada; no es exactitud.'],
 ['Brier',f(r['brier'],4),f'Error probabilístico menor que la referencia constante ({f(br,4)}). No significa {pct(r["brier"])} de predicciones equivocadas.'],
 ['Alertas',pct(r['proporcion_alertas']),f'{n(alerts)} / {n(N)} inscripciones superaron el umbral; este sería el volumen de alertas de la regla evaluada.'],
 ['Anticipación',f(r['anticipacion_tp']['mediana'],1)+' días',f'Mediana entre los {n(tp)} retiros detectados; el 50 % central está entre {f(r["anticipacion_tp"]["q25"],1)} y {f(r["anticipacion_tp"]["q75"],1)} días.']]
 table(['Métrica','Resultado','Interpretación aplicada'],rows,[85,70,360])
 p(f'Control de lectura: predecir “sin retiro” para todos obtendría {pct(1-r["prevalencia"])} de accuracy y 0 % de sensibilidad. Por ello, la exactitud aislada no responde al objetivo de detectar retiros. Se reportan ambas consecuencias, sin ocultar los errores del modelo.')

page('Qué comunicar al asesor y qué queda por discutir')
h('Resultado central')
p('El protocolo completo ya se ejecutó. Los modelos principales superan la referencia constante en AP, pero la discriminación es limitada y se producen numerosas falsas alertas. La selección interna eligió XGBoost en cuatro cortes y Random Forest en uno; eso no permite afirmar que superen concluyentemente a logística en prueba.')
for r in data['principales']:
 matches=[x for x in data['diferencias'] if x['corte']==r['corte'] and x['metrica']=='ap' and {x['a'],x['b']}=={r['modelo'],'regresion_logistica'}]
 assert len(matches)==1 and matches[0]['inferior_a_menos_b']<=0<=matches[0]['superior_a_menos_b']
p('Los intervalos pareados de diferencia de AP entre principal y logística incluyen cero en los cinco cortes. Esto no demuestra equivalencia. Los intervalos se obtuvieron con 2.000 remuestreos de personas, manteniendo sus inscripciones juntas; describen incertidumbre condicional a modelos y ofertas observados, no toda la variación del entrenamiento ni de futuras ofertas.')
h('Por qué tomó tiempo')
p('Cada configuración se ajustó cinco veces por corte: logística 8 × 5 × 5 = 200; cada otra familia 30 × 5 × 5 = 750. Total: 3.200 ajustes. Un ajuste aprende parámetros; una configuración especifica, por ejemplo, profundidad o número de árboles. TabNet repite el aprendizaje durante 100 o 200 épocas por ajuste.')
ev=json.loads((F/'evidencia.json').read_text(encoding='utf-8'))
def duration(sec):
 sec=round(sec);return f'{sec//3600:02d}:{sec%3600//60:02d}:{sec%60:02d}'
table(['Familia','Ajustes CV','Suma de tiempos (hh:mm:ss)'],[[names[t['modelo']],str(t['ajustes']),duration(t['segundos'])] for t in ev['tiempos']],[170,100,245])
p('Son sumas de tiempos registrados de ajustes CV terminados, incluyendo preparación, predicción, métricas y escritura de cada ajuste; no son la duración total del proyecto. Excluyen arranque, interrupciones sin marcador, reajustes finales, calibración, prueba y SHAP. Equipo registrado: Core i5-9300H, 4 núcleos/8 hilos, aproximadamente 8 GB de RAM; entrenamiento en CPU, máximo dos hilos, sin búsquedas concurrentes. La GPU no se utilizó; no se demostró un cuello de botella específico de memoria o disco.')
h('Discusión propuesta para la reunión')
p('Revisar las decisiones de agrupación por personas y alcance temporal; discutir el compromiso entre retiros detectados y falsas alertas; confirmar cómo presentar las limitaciones. Maximizar F1 fue una regla académica predefinida, no una política institucional: no se conocen costos de error ni capacidad de atención. No corresponde volver a escoger modelos o umbrales mirando esta prueba.')
h('Fuentes y trazabilidad')
p('Resultados: seleccion_validacion.json; paquete_evaluacion.json; evaluación/metricas.json; sintesis.json y metricas_todas.csv del cierre del 21 de octubre. Las matrices y seis métricas derivadas se recalcularon desde sus conteos para este informe; no se repitieron entrenamientos. CSV complementario: metricas_completas_reunion.csv.')
p('Scikit-learn developers (2025-2026), documentación 1.8: <link href="https://scikit-learn.org/1.8/modules/model_evaluation.html" color="#2C5697">Metrics and scoring</link>; <link href="https://scikit-learn.org/1.8/modules/generated/sklearn.metrics.confusion_matrix.html" color="#2C5697">confusion_matrix</link>; <link href="https://scikit-learn.org/1.8/modules/generated/sklearn.metrics.f1_score.html" color="#2C5697">f1_score</link>; <link href="https://scikit-learn.org/1.8/modules/generated/sklearn.metrics.average_precision_score.html" color="#2C5697">average_precision_score</link>; <link href="https://scikit-learn.org/1.8/modules/generated/sklearn.metrics.brier_score_loss.html" color="#2C5697">brier_score_loss</link>. Consulta: 21 de octubre de 2026.')

# Dos representaciones desde la misma estructura: PDF y texto editable.
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleReport',fontName='Helvetica-Bold',fontSize=21,leading=25,textColor=HexColor('#2C5697'),spaceAfter=14))
styles.add(ParagraphStyle(name='TextReport',fontName='Helvetica',fontSize=10,leading=13.5,spaceAfter=8))
styles.add(ParagraphStyle(name='HeadReport',fontName='Helvetica-Bold',fontSize=12,leading=16,textColor=HexColor('#2C5697'),spaceBefore=8,spaceAfter=7))
styles.add(ParagraphStyle(name='CellReport',fontName='Helvetica',fontSize=9,leading=11.5))
story=[];md=[]
for ix,blocks in enumerate(pages):
 if ix:story.append(PageBreak())
 for block in blocks:
  kind=block[0]
  if kind=='table':
   headers,rows,widths=block[1:];arr=[[Paragraph(escape(str(v)).replace('\n','<br/>'),styles['CellReport']) for v in row] for row in [headers]+rows]
   t=Table(arr,colWidths=widths,repeatRows=1,hAlign='LEFT')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#eaf0f7')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.7,HexColor('#2C5697')),('LINEBELOW',(0,1),(-1,-1),.3,HexColor('#dbe2ea'))]))
   story.extend([t,Spacer(1,9)]);md.extend(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(v).replace('\n','; ') for v in row)+' |' for row in rows]+[''])
  else:
   sty={'title':'TitleReport','h':'HeadReport','p':'TextReport'}[kind];story.append(Paragraph(block[1],styles[sty]));md.extend([('# ' if kind=='title' else '## ' if kind=='h' else '')+block[1],''])
out=ROOT/'output/pdf/Reporte_entrenamiento_metricas_asesor_22_octubre_2026.pdf'
def footer(canvas,doc):
 canvas.setStrokeColor(HexColor('#2C5697'));canvas.line(40,40,555,40);canvas.setFont('Helvetica',8);canvas.setFillColor(HexColor('#595959'));canvas.drawString(40,27,'OULAD | Decisiones, evaluación y lectura de métricas | 22/10/2026');canvas.drawRightString(555,27,str(doc.page))
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=40,rightMargin=40,topMargin=35,bottomMargin=52,title='Decisiones de entrenamiento y resultados OULAD',author='Oriana Giraldo Arcia y Luis Javier Rubio Hernández')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
count=len(PdfReader(out).pages)
(F/'Reporte_entrenamiento_metricas.md').write_text('\n'.join(md),encoding='utf-8')
shutil.copyfile(S/'metricas_todas.csv',F/'metricas_completas_reunion.csv')
v={'paginas':count,'cortes_verificados':verified,'matrices':'Filas: realidad; columnas: alerta / sin alerta','pdf_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'revision_visual':'pendiente'}
(F/'verificacion_metricas_reunion.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(v,ensure_ascii=False))
