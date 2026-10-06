"""Genera el cronograma PDF y verifica el paquete desde las fuentes vigentes."""
from pathlib import Path
from collections import Counter
import difflib
import hashlib
import html
import json
import re
import shutil
import subprocess
from pypdf import PdfReader
from PIL import Image, ImageDraw
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, LongTable, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reportes/entrega_avance_2026_10_06'
P = ROOT / 'Plantilla_ProyAplicado'
OLD = ROOT / 'respaldo/2026-10-06_pre_entrega_avance/Plantilla_ProyAplicado'
QA = OUT / 'paginas'
POPPLER = Path('C:/Users/luisj/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
palette = json.loads((ROOT / 'estilo_visual_javeriana.json').read_text(encoding='utf-8'))

def markup(value):
    return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html.escape(value))

def cronograma():
    blue = colors.HexColor(palette['azul'])
    styles = {
        'p': ParagraphStyle('p', fontName='Times-Roman', fontSize=11, leading=14.3, spaceAfter=8),
        'h1': ParagraphStyle('h1', fontName='Times-Bold', fontSize=20, leading=23, textColor=blue, spaceAfter=13),
        'h2': ParagraphStyle('h2', fontName='Times-Bold', fontSize=14, leading=17, textColor=blue, spaceBefore=12, spaceAfter=8, keepWithNext=True),
        'cell': ParagraphStyle('cell', fontName='Times-Roman', fontSize=9.5, leading=12, alignment=TA_LEFT),
        'head': ParagraphStyle('head', fontName='Times-Bold', fontSize=9.5, leading=12, textColor=colors.white),
    }
    story = []
    lines = (OUT / 'Cronograma_y_avance.md').read_text(encoding='utf-8').splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == '## Propuesta de preparación de la entrega':
            story.append(PageBreak())
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            data = [[Paragraph(markup(c), styles['head' if j == 0 else 'cell']) for c in row] for j, row in enumerate(rows)]
            widths = [119, 62, 96, 226] if rows[0][0] == 'Actividad' else [88, 133, 95, 187]
            table = LongTable(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), blue), ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F1F4F8')]),
                ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LINEBELOW', (0,-1), (-1,-1), 0.5, blue),
            ]))
            story.extend([table, Spacer(1, 10)])
            continue
        style = 'h2' if line.startswith('## ') else 'h1' if line.startswith('# ') else 'p'
        story.append(Paragraph(markup(re.sub(r'^#{1,2} ', '', line)), styles[style]))
        i += 1
    def footer(canvas, doc):
        canvas.setStrokeColor(blue)
        canvas.line(46, 36, A4[0]-46, 36)
        canvas.setFont('Times-Roman', 9)
        canvas.setFillColor(colors.HexColor(palette['texto_secundario']))
        canvas.drawString(46, 24, '6 de octubre de 2026 | Para revisión del director')
        canvas.drawRightString(A4[0]-46, 24, str(doc.page))
    SimpleDocTemplate(str(OUT / 'Cronograma_y_avance_para_revision.pdf'), pagesize=A4,
                      leftMargin=46, rightMargin=46, topMargin=43, bottomMargin=49,
                      title='Avance del cronograma y propuesta de seguimiento',
                      author='Oriana Giraldo Arcia y Luis Javier Rubio Hernández').build(story, onFirstPage=footer, onLaterPages=footer)

def formulas(text):
    return Counter(re.sub(r'\s+', '', b) for pattern in [r'\\\[(.*?)\\\]', r'\\begin\{equation\}(.*?)\\end\{equation\}', r'\\begin\{align\}(.*?)\\end\{align\}'] for b in re.findall(pattern, text, re.S))

def cites(text):
    return Counter(c.strip() for group in re.findall(r'\\cite\{([^}]+)\}', text) for c in group.split(','))

def main():
    QA.mkdir(parents=True, exist_ok=True)
    after = {f.name: f.read_text(encoding='utf-8') for f in P.glob('*.tex')}
    before = {n: (OLD/n).read_text(encoding='utf-8') for n in after}
    changed = [n for n in after if after[n] != before[n]]
    for n in after:
        assert formulas(after[n]) == formulas(before[n]), n
        assert cites(after[n]) == cites(before[n]), n
    assert (P/'biblio.bib').read_bytes() == (OLD/'biblio.bib').read_bytes()
    joined = '\n'.join(after.values())
    labels = re.findall(r'\\label\{([^}]+)\}', joined)
    refs = [x for x in re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}', joined) if '#' not in x]
    assert len(labels) == len(set(labels))
    assert not set(refs) - set(labels)
    bib = set(re.findall(r'@\w+\s*\{\s*([^,]+),', (P/'biblio.bib').read_text(encoding='utf-8')))
    assert not set(cites(joined)) - bib
    for image in re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}', joined):
        assert (P/image).read_bytes() == (OLD/image).read_bytes()
    log = (P/'proyecto.log').read_text(encoding='utf-8', errors='replace')
    issues = [l for l in log.splitlines() if re.search(r'Overfull|undefined|^!|destination with the same identifier', l)]
    assert not issues, issues
    current = PdfReader(P/'proyecto.pdf')
    fulltext = '\n'.join(p.extract_text() for p in current.pages)
    assert 'La actividad A3.2 del anteproyecto' in fulltext
    assert 'La selección inicial busca conservar' in fulltext
    assert '6 de octubre de 2026' in fulltext
    cronograma()
    shutil.copy2(P/'proyecto.pdf', OUT/'Proyecto_avance_para_revision.pdf')
    shutil.copy2(P/'compilacion_proyecto.txt', OUT/'compilacion.txt')
    (OUT/'cambios.diff').write_text('\n'.join(''.join(difflib.unified_diff(before[n].splitlines(True), after[n].splitlines(True), fromfile='previo/'+n, tofile='vigente/'+n)) for n in changed), encoding='utf-8')
    result = {'fecha': '2026-10-06', 'archivos_modificados': changed,
              'formulas_y_citas_conservadas': True, 'bibliografia_e_imagenes_conservadas': True,
              'etiquetas': len(labels), 'remisiones': len(refs), 'errores_latex': issues,
              'advertencias_latex': [l for l in log.splitlines() if 'Warning' in l], 'archivos': []}
    for name in ['Proyecto_avance_para_revision', 'Cronograma_y_avance_para_revision']:
        path = OUT/f'{name}.pdf'
        dest = QA/name
        dest.mkdir(exist_ok=True)
        subprocess.run([str(POPPLER), '-r', '85', '-png', str(path), str(dest/'pagina')], check=True)
        doc = PdfReader(path)
        pages = []
        tiles = []
        for j, png in enumerate(sorted(dest.glob('pagina-*.png'))[:len(doc.pages)]):
            im = Image.open(png).convert('RGB')
            im.thumbnail((306, 430))
            tile = Image.new('RGB', (326, 455), '#EEEEEE')
            tile.paste(im, ((326-im.width)//2, 2))
            ImageDraw.Draw(tile).text((12,435), f'PDF {j+1}', fill='black')
            tiles.append(tile)
            text = doc.pages[j].extract_text()
            if any(term in text for term in ['La selección inicial busca', 'La actividad A3.2', 'Definición de particiones', 'La selección base de A1.3']):
                pages.append(j+1)
        for start in range(0,len(tiles),12):
            sheet = Image.new('RGB', (1304, 1365), 'white')
            for j, tile in enumerate(tiles[start:start+12]):
                sheet.paste(tile, ((j%4)*326,(j//4)*455))
            sheet.save(dest/f'contacto_{start//12+1:02}.png')
        result['archivos'].append({'nombre': path.name, 'paginas': len(doc.pages), 'paginas_cambios': pages,
                                   'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    (OUT/'verificacion_documental.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
