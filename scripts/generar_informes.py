"""Genera fuentes LaTeX migrables desde resultados ya calculados; no recalcula datos."""
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reportes/correcciones_2026_09_10'
DEST=OUT/'informes'
DEST.mkdir(parents=True,exist_ok=True)


def data(name):
    return pd.read_csv(OUT/'tablas'/f'{name}.csv')


def summary(name):
    return json.loads((OUT/f'{name}.json').read_text(encoding='utf-8'))


def esc(value):
    text=str(value)
    return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_\allowbreak{}',
                    '{':r'\{','}':r'\}'}.get(c,c) for c in text)


def number(value,digits=0):
    if pd.isna(value):return 'No aplica'
    if np.isinf(value):return r'$\infty$'
    return f'{value:,.{digits}f}'.replace(',','X').replace('.',',').replace('X',r'\,')


def tab(frame,caption,label,widths=None,digits=2):
    n=len(frame.columns)
    if widths is None: widths=[.48]+[.48/(n-1)]*(n-1) if n>1 else [.96]
    if n >= 5: widths=[w*.90/sum(widths) for w in widths]
    spec=''.join(r'>{\raggedright\arraybackslash}p{'+str(w)+r'\linewidth}' for w in widths)
    header=' & '.join(r'\textbf{'+esc(c)+'}' for c in frame.columns)+r' \\'
    reserve = .30 if len(frame) <= 6 else .42 if len(frame) <= 12 else .20
    lines=[r'\Needspace{'+str(reserve)+r'\textheight}',
           r'\begingroup\small\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.16}',
           r'\begin{longtable}{'+spec+'}', r'\caption{'+caption+r'}\label{'+label+r'}\\',
           r'\toprule',header,r'\midrule\endfirsthead',r'\toprule',header,r'\midrule\endhead',
           r'\bottomrule\endfoot']
    for row in frame.itertuples(index=False,name=None):
        cells=[]
        for x in row:
            if isinstance(x,(int,np.integer)):cells.append(number(x))
            elif isinstance(x,(float,np.floating)):cells.append(number(x,digits))
            else:cells.append(esc(x))
        lines.append(' & '.join(cells)+(r' \\*' if len(frame)<=12 else r' \\'))
    lines += [r'\end{longtable}\endgroup']
    return '\n'.join(lines)+'\n'


def fig(name,caption,label,width='.94'):
    placement = 'H' if name in ['02_calendario_evaluaciones','02_disponibilidad_indicadores'] else 'htbp'
    return '\n'+r'\begin{figure}['+placement+r']\centering'+'\n'+r'\includegraphics[width='+width+r'\linewidth]{../figuras/'+name+r'.pdf}'+'\n'+r'\caption{'+caption+r'}\label{'+label+r'}\end{figure}'+'\n'


def write_report(stem,title,body):
    (DEST/f'{stem}_contenido.tex').write_text(body,encoding='utf-8')
    wrapper=r'''\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{babel}
\babelprovide[import,main]{spanish}
\renewcommand{\tablename}{Tabla}
\usepackage[margin=2.3cm]{geometry}
\usepackage{amsmath,amssymb,graphicx,booktabs,longtable,array,xcolor,hyperref,needspace,float}
\let\originalsection\section
\renewcommand{\section}{\Needspace{.42\textheight}\originalsection}
\definecolor{azul}{RGB}{0,73,118}
\hypersetup{colorlinks=true,linkcolor=azul,urlcolor=azul,citecolor=azul}
\setlength{\parskip}{5pt}
\setlength{\parindent}{0pt}
\setlength{\emergencystretch}{3em}
\title{\color{azul}TITLE}
\author{Oriana Giraldo Arcia \and Luis Javier Rubio Hernández}
\date{Proyecto Aplicado de Ciencia de Datos, PUJ Cali\\Revisión técnica: 10 de septiembre de 2026}
\begin{document}
\renewcommand{\tablename}{Tabla}
\maketitle
\input{STEM_contenido.tex}
\par\vspace{6pt}
\bibliographystyle{plain}
\bibliography{referencias_revision}
\end{document}
'''.replace('TITLE',title).replace('STEM',stem)
    (DEST/f'{stem}.tex').write_text(wrapper,encoding='utf-8')


if __name__=="__main__":
    from generar_multiventana import build
    build()
