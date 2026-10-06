"""Genera el informe de reunión desde su texto editable y verifica cifras clave."""
from pathlib import Path
import hashlib
import html
import json
import re

import fitz
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reportes/reunion_asesor_2026_09_11'
OUT = ROOT / 'output/pdf/informe_reunion_asesor.pdf'
QA = ROOT / 'tmp/pdfs/reunion_asesor'
OUT.parent.mkdir(parents=True, exist_ok=True)
QA.mkdir(parents=True, exist_ok=True)
SOURCE = REPORT / 'informe_reunion.md'
fontroot = Path('C:/Windows/Fonts')
for name, filename in [('Body', 'calibri.ttf'), ('BodyBold', 'calibrib.ttf'), ('BodyItalic', 'calibrii.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(fontroot / filename)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold', italic='BodyItalic', boldItalic='BodyBold')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Text', fontName='Body', fontSize=10.6, leading=14.0, spaceAfter=8, textColor=colors.HexColor('#233244')))
styles.add(ParagraphStyle(name='TitleCustom', fontName='BodyBold', fontSize=23, leading=26, spaceAfter=13, textColor=colors.HexColor('#143954')))
styles.add(ParagraphStyle(name='SectionCustom', fontName='BodyBold', fontSize=17, leading=20, spaceAfter=12, keepWithNext=True, textColor=colors.HexColor('#143954')))
styles.add(ParagraphStyle(name='SubCustom', fontName='BodyBold', fontSize=11.6, leading=15, spaceBefore=4, spaceAfter=6, keepWithNext=True, textColor=colors.HexColor('#11766E')))
styles.add(ParagraphStyle(name='BulletCustom', parent=styles['Text'], leftIndent=10, firstLineIndent=-7, spaceAfter=6))
styles.add(ParagraphStyle(name='CellCustom', parent=styles['Text'], fontSize=10, leading=13, spaceAfter=0))

def markup(text):
    text = html.escape(text.replace('–', '-').replace('—', '-'))
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

def footer(canvas, doc):
    canvas.saveState()
    w, h = doc.pagesize
    canvas.setStrokeColor(colors.HexColor('#C8D6DF'))
    canvas.line(20*mm, h-16*mm, w-20*mm, h-16*mm)
    canvas.setFont('Body', 8)
    canvas.setFillColor(colors.HexColor('#536879'))
    canvas.drawString(20*mm, h-13*mm, 'PROYECTO OULAD | INFORME PARA ASESORÍA')
    canvas.drawString(20*mm, 12*mm, 'Avance y justificación | 10 septiembre 2026')
    canvas.drawRightString(w-20*mm, 12*mm, str(doc.page))
    canvas.restoreState()

story = []
lines = SOURCE.read_text(encoding='utf-8').splitlines()
i = 0
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1
        continue
    if line == '---':
        story.append(PageBreak())
    elif line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            cells = lines[i].strip('|').split('|')
            if not all(re.fullmatch(r'\s*:?-+:?\s*', x) for x in cells):
                rows.append([Paragraph(markup(x.strip()), styles['CellCustom']) for x in cells])
            i += 1
        table = Table(rows, colWidths=[45*mm, 46*mm, 40*mm, 39*mm], hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E0EBF1')),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F6F8')]),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LINEBELOW',(0,0),(-1,0),.6,colors.HexColor('#9BB2C1')),
        ]))
        story.extend([table, Spacer(1, 12)])
        continue
    elif line.startswith('### '):
        story.append(Paragraph(markup(line[4:]), styles['SubCustom']))
    elif line.startswith('## '):
        story.append(Paragraph(markup(line[3:]), styles['SectionCustom']))
    elif line.startswith('# '):
        story.append(Paragraph(markup(line[2:]), styles['TitleCustom']))
    elif line.startswith('- '):
        story.append(Paragraph('• ' + markup(line[2:]), styles['BulletCustom']))
    else:
        story.append(Paragraph(markup(line), styles['Text']))
    i += 1

doc = SimpleDocTemplate(str(OUT), pagesize=(210*mm,297*mm), rightMargin=20*mm, leftMargin=20*mm,
                        topMargin=22*mm, bottomMargin=22*mm, title='Informe de avance para la reunión con el asesor',
                        author='Proyecto aplicado de ciencia de datos - OULAD')
doc.build(story, onFirstPage=footer, onLaterPages=footer)

# Recalcular únicamente los conteos citados: no se ejecuta de nuevo la cadena de notebooks.
base = pd.read_parquet(ROOT/'data/processed/multiventana_2026_09_08/base_auditoria.parquet')
r, u, end = base.date_registration, base.date_unregistration, base.module_presentation_length
known = r.notna()
enrolled = known & (r <= 28)
eligible = enrolled & (u.isna() | (u > 28)) & (end > 28)
counts = {
    'inscripciones_fuente': len(base), 'fechas_retiro_fuente': int(u.notna().sum()),
    'sin_matricula': int((~known).sum()), 'matricula_posterior_28': int((known & (r > 28)).sum()),
    'retiro_previo_filtrado': int((enrolled & (u <= 28)).sum()),
    'elegibles_28': int(eligible.sum()), 'personas_28': int(base.loc[eligible, 'id_student'].nunique()),
    'eventos_28': int((eligible & (u > 28) & (u <= end)).sum()),
    'retiros_hasta_28_fuente': int((u <= 28).sum()),
    'retiros_futuros_fuente': int((u > 28).sum()),
    'futuros_sin_matricula': int(((u > 28) & ~known).sum()),
    'futuros_matricula_tardia': int(((u > 28) & known & (r > 28)).sum()),
    'retiro_fuera_final_elegibles': int((eligible & (u > end)).sum()),
}
expected = [32593,10072,45,16,5017,27515,24826,5012,5055,5017,1,3,1]
assert list(counts.values()) == expected, counts
multi = ROOT/'reportes/multiventana_2026_09_08'
checks = json.loads((multi/'verificaciones_independientes.json').read_text(encoding='utf-8'))
assert len(checks) == 46 and all(x['estado']=='correcta' for x in checks)
math_checks = json.loads((ROOT/'reportes/revision_marco_2026_09_09/verificacion_matematica.json').read_text(encoding='utf-8'))
assert len(math_checks) == 11 and all(x['estado']=='correcta' for x in math_checks)

pdf = fitz.open(OUT)
page_info = []
for page in pdf:
    pix = page.get_pixmap(matrix=fitz.Matrix(1.35,1.35), alpha=False)
    pix.save(QA/f'pagina_{page.number+1:02}.png')
    text = page.get_text()
    page_info.append({'pagina':page.number+1, 'palabras':len(text.split()), 'seccion':next((l for l in text.splitlines() if re.match(r'^\d+\. ',l)),None)})
assert len(pdf) == 10, page_info
for idx, page in enumerate(pdf):
    assert re.search(rf'(?m)^{idx+1}\. ', page.get_text()), page_info
    for word in page.get_text('words'):
        assert word[0] >= 20 and word[2] <= page.rect.width-20 and word[1] >= 15 and word[3] <= page.rect.height-15
manifest = {'fecha':'2026-09-10','conteos_recalculados':counts,'porcentaje_global':10072/32593*100,
            'porcentaje_futuro_28':5012/27515*100,'verificaciones_analiticas_previas':len(checks),
            'verificaciones_matematicas_previas':len(math_checks),'paginas':page_info,
            'pdf':str(OUT),'sha256_pdf':hashlib.sha256(OUT.read_bytes()).hexdigest(),
            'fuente_editable':str(SOURCE),'sha256_texto':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'alcance':'Se consultaron ejecuciones previas; se recalcularon conteos de prevalencia, sin reejecutar notebooks.',
            'revision_visual':'pendiente de inspección de renderizados'}
(REPORT/'verificacion_informe.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pdf':str(OUT),'paginas':page_info,'verificacion_cifras':'correcta'},ensure_ascii=False))
