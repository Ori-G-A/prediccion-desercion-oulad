"""Actualiza únicamente la presentación y regenera figuras desde salidas guardadas.

No ejecuta bootstrap, entrenamiento ni reconstrucción de los CSV originales.
"""
from pathlib import Path
import ast
import base64
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'src'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from estilo_visual import apply_style, CONFIG
import figuras_oulad as plots

REPORT = ROOT / 'reportes/figuras_cuerpo_2026_10_04'
SOURCE = ROOT / 'reportes/correcciones_2026_09_10'
PROCESSED = ROOT / 'data/processed/correcciones_2026_09_10'
DEST = ROOT / 'Plantilla_ProyAplicado'
CUTS = [7, 14, 28, 42, 56]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def latex_theme():
    text = r'''% Generado desde estilo_visual_javeriana.json; no cambia el cuerpo ni las ecuaciones.
\definecolor{PUJAzul}{HTML}{BLUE}
\definecolor{PujAcento}{HTML}{ACCENT}
\definecolor{PUJGris}{HTML}{GRAY}
\definecolor{PUJTexto}{HTML}{TEXT}
\colorlet{PUJClaro}{PUJAzul!6!white}
\colorlet{PUJResalte}{PujAcento!18!white}
% etoolbox ya está disponible mediante hyperref; sin nuevas dependencias tipográficas.
\makeatletter
\patchcmd{\@makechapterhead}{\normalfont}{\normalfont\color{PUJAzul}}{}{}
\patchcmd{\@makeschapterhead}{\normalfont}{\normalfont\color{PUJAzul}}{}{}
\patchcmd{\section}{\normalfont\Large\bfseries}{\normalfont\Large\bfseries\color{PUJAzul}}{}{}
\patchcmd{\subsection}{\normalfont\large\bfseries}{\normalfont\large\bfseries\color{PUJAzul}}{}{}
\patchcmd{\subsubsection}{\normalfont\normalsize\bfseries}{\normalfont\normalsize\bfseries\color{PUJAzul}}{}{}
\makeatother
\colorlet{linkcol}{PUJAzul}
\colorlet{citecol}{PUJAzul}
\arrayrulecolor{PUJAzul}
\renewcommand{\headrule}{\color{PUJAzul}\headruleORIG}
\tikzset{puj base/.style={draw=PUJAzul,text=PUJTexto},
  puj etapa/.style={draw=PUJAzul,text=PUJTexto,rounded corners,line width=.6pt}}
'''
    for token, key in [('BLUE','azul'),('ACCENT','acento'),('GRAY','gris'),('TEXT','texto')]:
        text = text.replace(token, CONFIG[key].lstrip('#'))
    (DEST / 'estilo_visual.tex').write_text(text, encoding='utf-8')
    p = DEST / 'format.tex'; text = p.read_text(encoding='utf-8')
    if r'\input{estilo_visual}' not in text:
        text += '\n% Estilo visual del proyecto, basado en la identidad institucional.\n' + r'\input{estilo_visual}' + '\n'
    p.write_text(text, encoding='utf-8')
    for name in ['figura_ruta.tex','figura_indicadores.tex','figura_cascada28.tex','figura_temporal.tex']:
        p = DEST / name; text = p.read_text(encoding='utf-8')
        text = text.replace(r'font=\small,', r'font=\small\sffamily,')
        text = text.replace('etapa/.style={draw,', 'etapa/.style={draw=PUJAzul,text=PUJTexto,')
        text = text.replace('fill=blue!6', 'fill=PUJClaro').replace('fill=green!6', 'fill=PUJResalte')
        text = text.replace('[blue!9]', '[PUJClaro]').replace('[green!9]', '[PUJResalte]')
        text = text.replace('[red!70!black]', '[PUJGris]').replace('[blue!70!black]', '[PUJAzul]')
        text = text.replace(r'\draw[->]', r'\draw[->,PUJAzul]')
        text = text.replace(r'\node[draw,fill=', r'\node[draw=PUJAzul,fill=')
        p.write_text(text, encoding='utf-8')


def update_notebooks(figures):
    records = []
    mapping = {
        '01_carga_exploracion.ipynb': [('01_momento_retiro', 'momento_retiro(segments)')],
        '02_feature_engineering.ipynb': [('02_poblacion_cortes', 'poblacion_cortes(population)')],
        '03_analisis_estadistico.ipynb': [('03_distribuciones_cortes','distribuciones_cortes(datasets)'), ('03_efectos_cortes','efectos_cortes(effects, CUTS)')]
    }
    for name, calls in mapping.items():
        p = ROOT / name; notebook = json.loads(p.read_text(encoding='utf-8'))
        before_sources = [c.get('source') for c in notebook['cells']]
        for figure_name, call in calls:
            candidates = [c for c in notebook['cells'] if c['cell_type']=='code' and f"figure('{figure_name}')" in ''.join(c['source'])]
            assert len(candidates)==1, figure_name
            cell = candidates[0]; source = ''.join(cell['source'])
            marker = 'from figuras_oulad import '
            if marker in source:
                start = source.index(marker)
            else:
                start = min(i for i in [source.find('fig, ax = plt.subplots'), source.find('fig,ax=plt.subplots'), source.find('fig,axes=plt.subplots')] if i>=0)
            prefix = source[:start]
            function_name = call.split('(')[0]
            cell['source'] = (prefix + f'from figuras_oulad import {function_name}\n{call}\nfigure({figure_name!r})\n').splitlines(keepends=True)
            ast.parse(''.join(cell['source']))
            png_outputs = [o for o in cell.get('outputs',[]) if 'image/png' in o.get('data',{})]
            assert len(png_outputs)==1, (name,figure_name,len(png_outputs))
            png_outputs[0]['data']['image/png'] = base64.b64encode(figures[figure_name].read_bytes()).decode('ascii')
            cell.setdefault('metadata',{})['actualizacion_visual'] = {'fecha':CONFIG['version'],'origen':'salidas analíticas guardadas','analisis_repetido':False}
            records.append({'notebook':name,'figura':figure_name,'prefijo_analitico_sha256':hashlib.sha256(prefix.encode()).hexdigest()})
        for cell in notebook['cells']:
            if cell['cell_type']=='code' and 'ejecutar_ampliacion(datasets)' in ''.join(cell['source']):
                png_outputs = [o for o in cell.get('outputs',[]) if 'image/png' in o.get('data',{})]
                names = ['01_fechas_retiro','02_calendario_evaluaciones','02_disponibilidad_indicadores']
                assert len(png_outputs)==len(names), (name,len(png_outputs))
                for output, figure_name in zip(png_outputs,names):
                    output['data']['image/png'] = base64.b64encode(figures[figure_name].read_bytes()).decode('ascii')
                cell.setdefault('metadata',{})['actualizacion_visual'] = {'fecha':CONFIG['version'],'analisis_repetido':False,'figuras':names}
        notebook.setdefault('metadata',{})['estilo_visual'] = {'version':CONFIG['version'],'paleta':'Azul Javeriana y tonos complementarios sin amarillo','nota':'Se regeneraron las figuras desde salidas guardadas; no se repitió la ejecución analítica completa.'}
        p.write_text(json.dumps(notebook,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    return records


def main():
    REPORT.mkdir(parents=True, exist_ok=True)
    paths = list((SOURCE/'tablas').glob('*.csv')) + list(PROCESSED.glob('*.parquet'))
    before = {str(p.relative_to(ROOT)):sha(p) for p in paths}
    family = apply_style()
    datasets = {cut:pd.read_parquet(PROCESSED/f'dataset_corte_{cut:02}.parquet') for cut in CUTS}
    population = pd.read_csv(SOURCE/'tablas/02_comparacion_cortes.csv')
    for row in population.itertuples():
        d = datasets[row.corte]
        assert len(d)==row.inscripciones and d.retiro_futuro.sum()==row.retiros
    jobs = [
        ('01_momento_retiro', lambda:plots.momento_retiro(pd.read_csv(SOURCE/'tablas/01_momento_retiro.csv'))),
        ('01_fechas_retiro', lambda:plots.fechas_retiro(pd.read_parquet(PROCESSED/'base_auditoria.parquet'),CUTS)),
        ('02_poblacion_cortes', lambda:plots.poblacion_cortes(population)),
        ('02_calendario_evaluaciones', lambda:plots.calendario_evaluaciones(pd.read_csv(SOURCE/'tablas/02_primera_evaluacion.csv'),CUTS)),
        ('02_disponibilidad_indicadores', lambda:plots.disponibilidad_indicadores(datasets)),
        ('03_distribuciones_cortes', lambda:plots.distribuciones_cortes(datasets)),
        ('03_efectos_cortes', lambda:plots.efectos_cortes(pd.read_csv(SOURCE/'tablas/03_efectos.csv'),CUTS))]
    exported = {}
    for name, function in jobs:
        fig = function(); fig.tight_layout()
        for ext in ['pdf','png']:
            p = SOURCE/'figuras'/f'{name}.{ext}'
            fig.savefig(p,dpi=160,bbox_inches='tight')
            shutil.copy2(p, DEST/'figuras_multiventana'/p.name)
        plt.close(fig)
        exported[name] = SOURCE/'figuras'/f'{name}.png'
    records = update_notebooks(exported)
    latex_theme()
    after = {str(p.relative_to(ROOT)):sha(p) for p in paths}
    assert before==after, 'Se modificaron salidas analíticas.'
    result = {'fuente_tipografica':family,'figuras_regeneradas':list(exported),'notebooks':records,
              'archivos_analiticos_sin_cambio':len(paths),'sha256_analiticos':before,
              'analisis_completo_repetido':False,'comprobacion_conteos_por_corte':True,
              'logo_y_esquema_fuente_conservados':True}
    (REPORT/'verificacion_regeneracion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='sha256_analiticos'},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
