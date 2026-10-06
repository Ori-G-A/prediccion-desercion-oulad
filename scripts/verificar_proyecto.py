"""Verifica estructura, bibliografía, figuras y renderiza el documento integrado."""
from pathlib import Path
import collections,hashlib,json,re
import fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'Plantilla_ProyAplicado'
OUT=ROOT/'reportes/correcciones_2026_09_10'
QA=ROOT/'tmp/qa_correcciones_proyecto'

def main():
    OUT.mkdir(exist_ok=True);QA.mkdir(exist_ok=True)
    texts={f.name:f.read_text(encoding='utf-8') for f in P.glob('*.tex')}
    joined='\n'.join(texts.values())
    bibkeys=re.findall(r'@\w+\s*\{\s*([^,]+),',(P/'biblio.bib').read_text(encoding='utf-8'))
    cites={c.strip() for group in re.findall(r'\\cite\{([^}]+)\}',joined) for c in group.split(',')}
    labels=re.findall(r'\\label\{([^}]+)\}',joined)
    refs={r for r in re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',joined) if '#' not in r}
    assert not cites-set(bibkeys),cites-set(bibkeys)
    assert not refs-set(labels),refs-set(labels)
    assert len(labels)==len(set(labels)),'Etiquetas duplicadas'
    assert len(bibkeys)==len(set(bibkeys)),'Claves bibliográficas duplicadas'
    figures=re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',joined)
    assert all((P/f).exists() for f in figures),'Figura faltante'
    migrated=P/'figuras_multiventana'
    assert all(hashlib.sha256(f.read_bytes()).digest()==hashlib.sha256((ROOT/'reportes/correcciones_2026_09_10/figuras'/f.name).read_bytes()).digest() for f in migrated.glob('*.pdf'))
    log=(P/'proyecto.log').read_text(encoding='utf-8',errors='replace')
    serious=[line for line in log.splitlines() if re.search(r'Overfull|undefined|^!|destination with the same identifier',line)]
    warnings=[line for line in log.splitlines() if 'Warning' in line]
    doc=fitz.open(P/'proyecto.pdf');tiles=[];pages=[]
    for i,page in enumerate(doc):
        words=page.get_text('words')
        outside=[w for w in words if w[0]<10 or w[1]<10 or w[2]>page.rect.width-10 or w[3]>page.rect.height-10]
        pages.append({'pagina_pdf':i+1,'palabras':len(words),'fuera_margen_seguro':len(outside),'inicio':page.get_text()[:130]})
        pix=page.get_pixmap(matrix=fitz.Matrix(1.3,1.3))
        pix.save(str(QA/f'pagina_{i+1:03}.png'))
        image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);image.thumbnail((365,510))
        tile=Image.new('RGB',(385,540),'#eeeeee');tile.paste(image,((385-image.width)//2,5))
        ImageDraw.Draw(tile).text((10,520),f'Página PDF {i+1}',fill='black');tiles.append(tile)
    for start in range(0,len(tiles),9):
        sheet=Image.new('RGB',(1155,540*((min(9,len(tiles)-start)+2)//3)),'white')
        for j,tile in enumerate(tiles[start:start+9]):sheet.paste(tile,((j%3)*385,(j//3)*540))
        sheet.save(QA/f'contacto_{start//9+1:02}.png')
    result={'pdf':'Plantilla_ProyAplicado/proyecto.pdf','paginas':len(doc),'citas_con_clave':len(cites),'etiquetas_unicas':len(labels),'figuras_referidas':len(figures),'figuras_migradas_identicas':True,'errores_relevantes_latex':serious,'advertencias_latex':warnings,'paginas_revision':pages,'sha256_pdf':hashlib.sha256((P/'proyecto.pdf').read_bytes()).hexdigest()}
    (OUT/'verificacion_documental.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='paginas_revision'},ensure_ascii=False,indent=2))
    assert not serious,'Revisar errores LaTeX'
    assert not any(p['fuera_margen_seguro'] for p in pages),'Texto fuera de márgenes'

if __name__=='__main__':main()
