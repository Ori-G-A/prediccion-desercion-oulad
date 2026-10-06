"""Comprueba conservación de ecuaciones, tablas y notebooks tras la edición."""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import importlib.util
import json
import re

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'Plantilla_ProyAplicado'
OLD = ROOT / 'respaldo/2026-09-13_pre_integracion_editorial/Plantilla_ProyAplicado'
OUT = ROOT / 'reportes/revision_editorial_2026_09_13/integracion'


def normalize(text):
    # Renombramientos editoriales, sin cambiar operadores ni coeficientes.
    for new, old in [
        (r't_{\mathrm{boost}}', 't'), (r's_{\mathrm{TN}}', 'i'),
        (r'\sigma_{\mathrm{log}}', r'\sigma'),
        (r'\sigma_{\mathrm{RF}}', r'\sigma'),
        (r'\rho_{\mathrm{RF}}', r'\rho'),
        (r'\lambda_{\mathrm{LR}}', r'\lambda'),
        (r'\lambda_{\mathrm{XGB}}', r'\lambda'),
        (r'\gamma_{\mathrm{XGB}}', r'\gamma'),
        (r'\gamma_{\mathrm{TN}}', r'\gamma'),
    ]:
        text = text.replace(new, old)
    return re.sub(r'\s+', '', text)


def displayed_math(folder):
    text = '\n'.join((folder / name).read_text(encoding='utf-8') for name in
                     ['descripcion.tex', 'desarrollo1.tex', 'desarrollo2.tex', 'anexos.tex'])
    blocks = re.findall(r'\\\[(.*?)\\\]', text, re.S)
    blocks += re.findall(r'\\begin\{equation\}(.*?)\\end\{equation\}', text, re.S)
    blocks += re.findall(r'\\begin\{align\}(.*?)\\end\{align\}', text, re.S)
    return Counter(normalize(b) for b in blocks)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    before, after = displayed_math(OLD), displayed_math(P)
    assert before == after, {'eliminadas': list((before-after)), 'nuevas': list((after-before))}
    tables = []
    for name in ['descripcion.tex', 'desarrollo1.tex', 'desarrollo2.tex', 'anexos.tex']:
        get = lambda folder: re.findall(r'\\begin\{(?:longtable|tabular)\}.*?\\end\{(?:longtable|tabular)\}', (folder/name).read_text(encoding='utf-8'), re.S)
        old_tables = [t for t in get(OLD) if r'\label{corr:simbolos}' not in t]
        assert old_tables == get(P), name
        tables.extend(old_tables)
    saved = json.loads((ROOT / 'reportes/revision_editorial_2026_09_13/notebooks_pre_integracion.json').read_text(encoding='utf-8-sig'))
    notebooks = {Path(row['Path']).name: hashlib.sha256(Path(row['Path']).read_bytes()).hexdigest().upper() == row['Hash'] for row in saved}
    assert all(notebooks.values())
    assert (P/'biblio.bib').read_bytes() == (OLD/'biblio.bib').read_bytes()
    result = {
        'bloques_matematicos_conservados_tras_renombrar': sum(before.values()),
        'tablas_previas_conservadas_excepto_guia_sustituida': len(tables),
        'notebooks_sin_cambios': notebooks,
        'bibliografia_sin_cambios': True,
        'alcance': 'Integridad editorial; no se reprodujeron análisis ni se revalidaron fuentes bibliográficas.'
    }
    (OUT/'conservacion.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    spec = importlib.util.spec_from_file_location('qa', ROOT/'scripts/verificar_proyecto.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.OUT = OUT
    module.QA = ROOT/'tmp/qa_editorial_integrada'
    module.main()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='reportes/revision_editorial_2026_09_13/integracion')
    args = parser.parse_args()
    OUT = ROOT / args.output
    main()
