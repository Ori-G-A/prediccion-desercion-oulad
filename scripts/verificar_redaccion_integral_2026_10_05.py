"""Verifica conservación editorial y prepara todas las páginas para revisión visual."""
from pathlib import Path
from collections import Counter
import difflib, hashlib, json, re, subprocess
from pypdf import PdfReader
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
P = ROOT/'Plantilla_ProyAplicado'
OLD = ROOT/'respaldo/2026-10-05_pre_revision_redaccion_integral/Plantilla_ProyAplicado'
OUT = ROOT/'reportes/revision_redaccion_integral_2026_10_05'
QA = OUT/'paginas'
QA.mkdir(parents=True, exist_ok=True)
names = sorted(f.name for f in P.glob('*.tex'))
before = {name:(OLD/name).read_text(encoding='utf-8') for name in names}
after = {name:(P/name).read_text(encoding='utf-8') for name in names}
joined = '\n'.join(after.values())

def math(text):
    return Counter(re.sub(r'\s+', '', block) for pattern in
                   [r'\\\[(.*?)\\\]', r'\\begin\{equation\}(.*?)\\end\{equation\}',
                    r'\\begin\{align\}(.*?)\\end\{align\}']
                   for block in re.findall(pattern, text, re.S))

def cites(text):
    return Counter(key.strip() for group in re.findall(r'\\cite\{([^}]+)\}', text)
                   for key in group.split(','))

def table_numbers(text):
    # Solo celdas; títulos y definiciones pueden ampliarse con símbolos explicados.
    blocks = re.findall(r'\\begin\{(?:tabular|longtable)\}.*?\\end\{(?:tabular|longtable)\}', text, re.S)
    result = []
    for block in blocks:
        body = '\n'.join(line for line in block.splitlines()
                         if '&' in line and not line.startswith('\\'))
        result.append(re.findall(r'\d+(?:[,.]\d+)*', body))
    return result

checks = {}
for name in names:
    assert math(before[name]) == math(after[name]), ('formula modificada', name)
    assert cites(before[name]) == cites(after[name]), ('citas modificadas', name)
    assert table_numbers(before[name]) == table_numbers(after[name]), ('celdas numericas', name)
    checks[name] = {'revisado': True, 'modificado': before[name] != after[name],
                    'formulas_conservadas': True, 'citas_conservadas': True,
                    'cifras_tablas_conservadas': True}
assert (P/'biblio.bib').read_bytes() == (OLD/'biblio.bib').read_bytes()
labels = re.findall(r'\\label\{([^}]+)\}', joined)
refs = [value for value in re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}', joined) if '#' not in value]
assert len(labels) == len(set(labels)), 'etiquetas duplicadas'
assert not set(refs)-set(labels), ('remisiones sin destino', set(refs)-set(labels))
bib = set(re.findall(r'@\w+\s*\{\s*([^,]+),', (P/'biblio.bib').read_text(encoding='utf-8')))
assert not set(cites(joined))-bib
images = re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}', joined)
assert all((P/name).exists() for name in images)
assert all((P/name).read_bytes() == (OLD/name).read_bytes() for name in images)
log = (P/'proyecto.log').read_text(encoding='utf-8', errors='replace')
issues = [line for line in log.splitlines() if re.search(r'Overfull|undefined|^!|destination with the same identifier', line)]
warnings = [line for line in log.splitlines() if 'Warning' in line]
diff = '\n'.join(''.join(difflib.unified_diff(before[name].splitlines(True), after[name].splitlines(True),
             fromfile='respaldo/'+name, tofile='vigente/'+name)) for name in names if before[name] != after[name])
(OUT/'cambios.diff').write_text(diff, encoding='utf-8')
doc = PdfReader(P/'proyecto.pdf')
poppler = Path('C:/Users/luisj/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
subprocess.run([str(poppler), '-r', '95', '-png', str(P/'proyecto.pdf'), str(QA/'pagina')], check=True)
tiles = []
pages = []
for i, page in enumerate(doc.pages):
    extracted = page.extract_text()
    pages.append({'pagina_pdf':i+1, 'palabras':len(extracted.split()), 'inicio':extracted[:140]})
    im = Image.open(sorted(QA.glob('pagina-*.png'))[i]).convert('RGB')
    im.thumbnail((306,430))
    tile = Image.new('RGB',(326,455),'#eeeeee')
    tile.paste(im,((326-im.width)//2,2))
    ImageDraw.Draw(tile).text((12,435), f'PDF {i+1}', fill='black')
    tiles.append(tile)
for start in range(0,len(tiles),12):
    sheet = Image.new('RGB',(1304,455*3),'white')
    for j,tile in enumerate(tiles[start:start+12]):
        sheet.paste(tile,((j%4)*326,(j//4)*455))
    sheet.save(QA/f'contacto_{start//12+1:02}.png')
result = {'version':'2026-10-05', 'archivos':checks, 'paginas_pdf':len(doc.pages),
          'bibliografia_conservada':True, 'imagenes_conservadas':True,
          'etiquetas':len(labels), 'remisiones':len(refs), 'citas_distintas':len(cites(joined)),
          'errores_latex':issues, 'advertencias_latex':warnings, 'paginas':pages,
          'sha256_pdf':hashlib.sha256((P/'proyecto.pdf').read_bytes()).hexdigest(),
          'alcance':'Integridad editorial y compilación; no reproduce análisis ni verifica afirmaciones bibliográficas.'}
(OUT/'verificacion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({key:value for key,value in result.items() if key not in ('archivos','paginas')},ensure_ascii=False,indent=2))
assert not issues, 'Incidencias de composición por revisar'
