"""Verificación de PDF, referencias y renderizado para revisión visual.

Requiere PyMuPDF y Pillow solo para esta comprobación documental.
"""
from pathlib import Path
import hashlib
import json
import re
import fitz
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reportes/correcciones_2026_09_10'
REPORTS=OUT/'informes'
QA=ROOT/'tmp/qa_correcciones_informes'
QA.mkdir(parents=True,exist_ok=True)


def main():
    results=[]
    bib=(REPORTS/'referencias_revision.bib').read_text(encoding='utf-8')
    keys=set(re.findall(r'@\w+\{([^,]+),',bib))
    for stem in ['01_exploracion','02_ingenieria','03_estadistica']:
        tex=(REPORTS/f'{stem}_contenido.tex').read_text(encoding='utf-8')
        citations={v for group in re.findall(r'\\cite\{([^}]+)\}',tex) for v in group.split(',')}
        assert citations<=keys,(stem,'citas inexistentes',citations-keys)
        labels=re.findall(r'\\label\{([^}]+)\}',tex)
        assert len(labels)==len(set(labels)),(stem,'etiquetas repetidas')
        refs=set(re.findall(r'\\ref\{([^}]+)\}',tex))
        assert refs<=set(labels),(stem,'referencias inexistentes')
        log=(REPORTS/f'{stem}.log').read_text(encoding='utf-8',errors='replace')
        warnings=[line for line in log.splitlines() if re.search(r'Overfull|undefined|^!',line)]
        assert not warnings,(stem,warnings)
        doc=fitz.open(REPORTS/f'{stem}.pdf')
        tiles=[]
        for i,page in enumerate(doc):
            words=page.get_text('words')
            assert words,(stem,i,'sin texto extraíble')
            for word in words:
                assert word[0]>=15 and word[1]>=15 and word[2]<=page.rect.width-15 and word[3]<=page.rect.height-15,(stem,i,'texto fuera de zona segura',word)
            pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5))
            pix.save(str(QA/f'{stem}_{i+1:02}.png'))
            image=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
            image.thumbnail((470,665))
            tile=Image.new('RGB',(490,695),'#eeeeee')
            tile.paste(image,((490-image.width)//2,10))
            ImageDraw.Draw(tile).text((12,680),f'{stem} / {i+1}',fill='black')
            tiles.append(tile)
        for start in range(0,len(tiles),6):
            group=tiles[start:start+6]
            sheet=Image.new('RGB',(490*3,695*((len(group)+2)//3)),'white')
            for j,tile in enumerate(group):sheet.paste(tile,((j%3)*490,(j//3)*695))
            sheet.save(QA/f'{stem}_contacto_{start//6+1:02}.png')
        results.append({'informe':stem,'paginas':len(doc),'citas_validas':len(citations),
            'etiquetas_unicas':len(labels),'desbordamientos_latex':0,
            'texto_dentro_margenes':True,'renderizado_paginas':True,
            'sha256_pdf':hashlib.sha256((REPORTS/f'{stem}.pdf').read_bytes()).hexdigest()})
    (OUT/'verificacion_informes.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
