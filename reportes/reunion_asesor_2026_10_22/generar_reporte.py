import json
import re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader

FOLDER=Path(__file__).resolve().parent
ROOT=FOLDER.parents[1]
evidence=json.loads((FOLDER/'evidencia.json').read_text(encoding='utf-8'))
assert evidence['evaluacion_cierre']['estado']=='evaluacion_completa'
assert evidence['huellas_evaluacion_verificadas']>0
config=json.loads((ROOT/'reportes/protocolo_validacion_2026_10_19/implementacion/configuracion.json').read_text(encoding='utf-8'))
assert {x['max_epochs'] for x in config['configuraciones']['tabnet']}=={100,200}
names={'regresion_logistica':'Regresión logística','random_forest':'Random Forest','xgboost':'XGBoost','lightgbm':'LightGBM','tabnet':'TabNet'}
def duration(seconds):
    seconds=round(seconds)
    h,rem=divmod(seconds,3600)
    m,s=divmod(rem,60)
    return f'{h:02d}:{m:02d}:{s:02d}'
table=['| Familia | Ajustes | Tiempo acumulado (h:min:s) | Promedio por ajuste |',
       '| --- | --- | --- | --- |']
for row in evidence['tiempos']:
    table.append(f"| {names[row['modelo']]} | {row['ajustes']} | {duration(row['segundos'])} | {row['media']:.2f} s |".replace('.',','))
shap=evidence['cortes_shap']
shap_status=('El cálculo SHAP terminó en los cinco cortes; sus salidas y patrones se revisaron; la discusión con el asesor está pendiente.' if len(shap)==5 else
             f'El cálculo SHAP está en ejecución; hay salidas de verificación en {len(shap)} de cinco cortes, pendientes de revisión académica.')
text=(FOLDER/'reporte_base.md').read_text(encoding='utf-8')
values={'FECHA':evidence['fecha'][:19].replace('T',' '),'TABLA_TIEMPOS':'\n'.join(table),
        'TIEMPO_TOTAL':duration(evidence['total_segundos'])+' (h:min:s)',
        'PORCENTAJE_TABNET':f"{100*evidence['tiempos'][-1]['segundos']/evidence['total_segundos']:.1f}".replace('.',','),
        'SHAP_ESTADO':shap_status,'HUELLAS':str(evidence['huellas_evaluacion_verificadas'])}
for key,value in values.items(): text=text.replace('{{'+key+'}}',value)
assert '{{' not in text
(FOLDER/'Reporte_avance_reunion_22_octubre.md').write_text(text,encoding='utf-8')

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportBody',fontName='Times-Roman',fontSize=11,leading=14.7,spaceAfter=9,textColor=HexColor('#202020')))
styles.add(ParagraphStyle(name='ReportTitle',fontName='Times-Bold',fontSize=22,leading=25,spaceAfter=14,textColor=HexColor('#2C5697')))
styles.add(ParagraphStyle(name='ReportHeading',fontName='Times-Bold',fontSize=15,leading=18,spaceBefore=5,spaceAfter=11,textColor=HexColor('#2C5697')))
styles.add(ParagraphStyle(name='Cell',fontName='Times-Roman',fontSize=10,leading=12.5,spaceAfter=0))
styles.add(ParagraphStyle(name='HeadCell',parent=styles['Cell'],fontName='Times-Bold',textColor=white))
def markup(s):
    s=escape(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`(.+?)`',r'<i>\1</i>',s)
    return s
story=[]
lines=text.splitlines()
i=0
while i<len(lines):
    line=lines[i].strip()
    if not line:
        i+=1;continue
    if line=='<!-- PAGE -->':
        story.append(PageBreak());i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[-: ]+',c) for c in cells): rows.append(cells)
            i+=1
        count=len(rows[0]);widths=({2:[145,338],4:[116,72,145,150],5:[30,90,175,90,98]}[count])
        data=[[Paragraph(markup(c),styles['HeadCell' if n==0 else 'Cell']) for c in row] for n,row in enumerate(rows)]
        t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#2C5697')),
                              ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),
                              ('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),
                              ('BOTTOMPADDING',(0,0),(-1,-1),7),
                              ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#F0F4F8')]),
                              ('LINEBELOW',(0,-1),(-1,-1),.5,HexColor('#347B83'))]))
        story.extend([t,Spacer(1,12)]);continue
    style='ReportBody'
    if line.startswith('# '):style='ReportTitle';line=line[2:]
    elif line.startswith('## '):style='ReportHeading';line=line[3:]
    story.append(Paragraph(markup(line),styles[style]));i+=1
out=ROOT/'output/pdf/Reporte_avance_reunion_22_octubre_2026.pdf'
out.parent.mkdir(parents=True,exist_ok=True)
def page(canvas,doc):
    canvas.saveState()
    canvas.setStrokeColor(HexColor('#347B83'));canvas.line(56,801,539,801)
    canvas.setFont('Times-Roman',9);canvas.setFillColor(HexColor('#595959'))
    canvas.drawString(56,813,'PUJ Cali | Proyecto aplicado | Reporte para el asesor')
    canvas.drawString(56,31,'Corte de evidencia: '+evidence['fecha'][:16].replace('T',' ')+' · Colombia')
    canvas.drawRightString(539,31,str(doc.page));canvas.restoreState()
doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=56,leftMargin=56,topMargin=54,bottomMargin=53,
                      title='Avance del proyecto y explicación del modelado',
                      author='Oriana Giraldo Arcia y Luis Javier Rubio Hernández')
doc.build(story,onFirstPage=page,onLaterPages=page)
reader=PdfReader(out)
print(json.dumps({'pdf':str(out),'paginas':len(reader.pages),'caracteres_por_pagina':[len(p.extract_text()) for p in reader.pages]},ensure_ascii=False))
assert len(reader.pages)==7, 'Revisar paginación: se esperaban siete páginas'
