"""Cascada desde exportables y cierre editorial desde respaldo versionado."""
from pathlib import Path
import csv
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'Plantilla_ProyAplicado'
OLD=ROOT/'respaldo/2026-09-13_pre_cierre_editorial/Plantilla_ProyAplicado'
OUT=ROOT/'reportes/revision_editorial_2026_09_13/cierre'
TABLES=ROOT/'reportes/correcciones_2026_09_10/tablas'


def rows(name):
    with (TABLES/name).open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))


def cascade():
    flow=[r for r in rows('02_flujos.csv') if r['corte']=='28']
    assert [r['etapa'] for r in flow]==['Fuente','Matrícula conocida','Matriculada al corte','Sin retiro hasta corte','Final posterior al corte']
    n=[int(r['inscripciones']) for r in flow]
    people=[int(r['personas']) for r in flow]
    exclusions=[int(r['excluidas']) for r in flow]
    for j in range(1,5):
        assert n[j-1]-exclusions[j]==n[j]
        assert 0<people[j]<=n[j]
    assert n[0]-sum(exclusions)==n[-1]
    summary=next(r for r in rows('02_comparacion_cortes.csv') if r['corte']=='28')
    assert int(summary['inscripciones'])==n[-1] and int(summary['personas'])==people[-1]
    events=int(summary['retiros'])
    assert abs(100*events/n[-1]-float(summary['prevalencia_pct']))<1e-10
    manifest=json.loads((TABLES.parent/'version_entregada.json').read_text(encoding='utf-8'))['archivos']
    hashes={}
    for name in ['02_flujos.csv','02_comparacion_cortes.csv']:
        file=TABLES/name
        key=file.relative_to(ROOT).as_posix()
        digest=hashlib.sha256(file.read_bytes()).hexdigest()
        assert key in manifest and manifest[key]['sha256']==digest, key
        hashes[key]=digest
    template=r'''\begin{figure}[H]\centering
\begin{tikzpicture}[font=\small,>=Stealth,
 etapa/.style={draw,rounded corners,align=center,text width=6.2cm,minimum height=1.03cm,inner sep=5pt}]
\node[etapa] (a) at (0,0) {\textbf{Fuente completa}\\@N0@ inscripciones; @P0@ personas};
\node[etapa] (b) at (0,-1.55) {\textbf{Fecha de matrícula conocida}\\@N1@ inscripciones; @P1@ personas};
\node[etapa] (c) at (0,-3.1) {\textbf{Matrícula hasta el día 28}\\@N2@ inscripciones; @P2@ personas};
\node[etapa] (d) at (0,-4.65) {\textbf{Sin retiro hasta el día 28 incluido}\\@N3@ inscripciones; @P3@ personas};
\node[etapa,fill=blue!6] (e) at (0,-6.2) {\textbf{Final posterior al día 28: elegibles}\\@N4@ inscripciones; @P4@ personas};
\draw[->] (a)--(b);\draw[->] (b)--(c);\draw[->] (c)--(d);\draw[->] (d)--(e);
\node[anchor=west,align=left,text width=4.3cm] at (3.45,-.77) {Se excluyen @X1@\\sin fecha de matrícula};
\node[anchor=west,align=left,text width=4.3cm] at (3.45,-2.32) {Se excluyen @X2@\\con matrícula posterior};
\node[anchor=west,align=left,text width=4.3cm] at (3.45,-3.87) {Se excluyen @X3@\\con retiro hasta el corte};
\node[anchor=west,align=left,text width=4.3cm] at (3.45,-5.42) {Se excluyen @X4@\\por final no posterior};
\node[draw,fill=green!6,align=center,text width=10.4cm,inner sep=8pt] (f) at (1.7,-8) {\textbf{Evento posterior al corte, entre las elegibles}\\@EVENTS@ retiros futuros / @N4@ inscripciones = @RATE@\,\%\\@NEGATIVE@ inscripciones sin retiro registrado dentro del horizonte};
\draw[->] (e.south)--(0,-7.05)--(f.north);
\end{tikzpicture}
\caption{Cascada secuencial de elegibilidad en el corte 28. Elaboración propia desde los exportables de la versión analítica del 10 de septiembre; las exclusiones cuentan inscripciones en cada etapa.}\label{editorial:cascada28}
\end{figure}
'''
    fmt=lambda x:f'{x:,}'.replace(',',r'\,')
    for j in range(5):
        template=template.replace(f'@N{j}@',fmt(n[j])).replace(f'@P{j}@',fmt(people[j])).replace(f'@X{j}@',fmt(exclusions[j]))
    template=template.replace('@EVENTS@',fmt(events)).replace('@NEGATIVE@',fmt(n[-1]-events)).replace('@RATE@',f'{100*events/n[-1]:.2f}'.replace('.',','))
    assert '@' not in template
    (P/'figura_cascada28.tex').write_text(template,encoding='utf-8')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'verificacion_cascada.json').write_text(json.dumps({'fuentes_sha256_verificadas_con_entrega_analitica':hashes,'flujo':flow,'retiros_futuros':events,'sin_evento':n[-1]-events,'prevalencia_pct':100*events/n[-1],'alcance':'Aritmética y trazabilidad de exportables; no se reprodujeron los análisis OULAD.'},ensure_ascii=False,indent=2),encoding='utf-8')


def insert_after(text, target, paragraph):
    assert text.count(target)==1,target
    return text.replace(target,target+'\n'+paragraph,1)


def main():
    cascade()
    text=(OLD/'desarrollo1.tex').read_text(encoding='utf-8')
    text=text.replace('sus resultados se obtuvieron mediante una\nejecución nueva y no mediante la reutilización de salidas históricas.',
        'sus resultados proceden de la ejecución documentada en la versión analítica del 10 de septiembre de 2026. Las revisiones editoriales posteriores conservan esa evidencia y no constituyen nuevas ejecuciones.')
    text=insert_after(text,r'\section{Estructura y unidad de análisis}',
        r'La Tabla~\ref{rev01:dimensiones} permite distinguir el tamaño de las fuentes de la cantidad de unidades analizadas. Las filas de interacciones y entregas describen registros asociados a una inscripción; no representan personas adicionales.')
    text=text.replace('no se aplica este desglose histórico como filtro común.',r'no se aplica este desglose histórico como filtro común. La definición operativa y la cascada del día 28 se presentan en el Capítulo~\ref{cap:ingenieria}, Figura~\ref{editorial:cascada28}.')
    text=text.replace('en el segundo informe;',r'en el Capítulo~\ref{cap:ingenieria};')
    text=text.replace('La figura presenta las 10',r'La Figura~\ref{corr:histograma} presenta las 10')
    text=insert_after(text,r'\subsection{Asociaciones e incertidumbre dentro de cada corte}',
        r'La pregunta de esta comparación es si los valores observados de cada indicador difieren entre inscripciones con y sin retiro futuro. La Tabla~\ref{multi03:efectos} resume la dirección y magnitud de esas asociaciones; la Figura~\ref{multi03:figefectos} añade intervalos para una selección de indicadores. Su lectura conjunta distingue una estimación puntual de su incertidumbre.')
    text=text.replace('ni proporción de cumplimiento observable sin evaluaciones programadas.', 'ni proporción entregada de evaluaciones programadas cuando no existen evaluaciones en ese calendario.')
    text=text.replace('La asociación con el módulo evidencia heterogeneidad contextual que debe considerarse al diseñar la validación.',
        r'En la Tabla~\ref{multi03:categorias}, el módulo presenta los mayores valores de V de Cramér entre los atributos publicados en todos los cortes. Esta heterogeneidad contextual debe considerarse al diseñar la validación.')
    text=text.replace('Las tasas por nivel y los conteos se exportan por separado;',r'Las tasas por nivel y los conteos se publican en el Anexo~\ref{corr:anexocontexto}, Tabla~\ref{corr:niveles};')
    (P/'desarrollo1.tex').write_text(text,encoding='utf-8')
    text=(OLD/'desarrollo2.tex').read_text(encoding='utf-8')
    text=insert_after(text,r'\section{Población elegible y cambio de composición}',
        r'La Tabla~\ref{multi02:poblacion} responde cuántas inscripciones siguen siendo elegibles y cuántos retiros ocurren después de cada corte. La Tabla~\ref{multi02:transiciones} identifica entradas y salidas entre cortes consecutivos; por ello, la disminución del total no debe interpretarse como seguimiento de una población fija.')
    text=insert_after(text,r'\section{Cascadas completas de elegibilidad}',r'''La Figura~\ref{editorial:cascada28} resume la aplicación de los filtros al día 28. Cada exclusión se calcula sobre las inscripciones que superaron la etapa anterior, de modo que las cantidades no se suman como categorías superpuestas. El evento futuro se cuenta únicamente después de completar la elegibilidad.
\input{figura_cascada28}
La proporción de 30,90\,\% describe fechas de retiro en la fuente completa; el 18,22\,\% utiliza 5\,012 retiros futuros entre 27\,515 inscripciones elegibles. El cambio responde a otra población y otro intervalo del evento, no a una reducción del abandono producida por el estudio. Las 5\,017 exclusiones por retiro hasta el corte coinciden numéricamente con los 5\,017 retiros posteriores al día 28 de la Tabla~\ref{rev01:retiro}; son conjuntos distintos, definidos en etapas y poblaciones diferentes.
''')
    text=insert_after(text,r'\section{Disponibilidad y calendario}',
        r'La Figura~\ref{corr:calendario} muestra el primer vencimiento de evaluación según módulo y presentación, no la fecha en que cada actividad se hizo accesible. La Figura~\ref{corr:observabilidad} permite examinar qué indicadores pueden calcularse en cada corte; un porcentaje menor indica falta de observabilidad y no menor riesgo de abandono.')
    text=insert_after(text,r'\section{Redundancia y estructura multivariada}',
        r'Los siguientes diagnósticos examinan cuánto se solapan los indicadores y cómo se resume su variación conjunta. La correlación describe asociaciones entre variables, el VIF examina dependencia lineal dentro de una especificación y el PCA resume variabilidad de los predictores. Ninguno mide por sí solo la capacidad de anticipar el retiro.')
    text=insert_after(text,r'\section{VIF publicado y decisión sobre el conteo de filas}',
        r'La Tabla~\ref{corr:vif} conserva la especificación utilizada para auditar la redundancia del conteo de filas. Su publicación permite justificar la decisión de exclusión sin presentar ese conjunto de cuatro variables como el diseño definitivo del clasificador.')
    text=insert_after(text,r'\section{Sensibilidad de variabilidad y componentes principales}',
        r'La Tabla~\ref{corr:cv} contrasta los dos CV con la proporción de días activos. Las dos columnas de observabilidad informan tamaños distintos, pero ambas correlaciones se calcularon sobre los mismos casos con al menos dos días activos. Esta precisión evita comparar correlaciones como si procedieran de las dos poblaciones observables completas.')
    text=text.replace('El CV activo separa mejor la dispersión de intensidad de la frecuencia en estos datos, a costa de una menor observabilidad.',
        r'La asociación con la proporción activa es menor en valor absoluto para el CV activo que para el CV de calendario en todos los cortes de la Tabla~\ref{corr:cv}. Esta diferencia es compatible con sus definiciones, ilustradas en la Figura~\ref{editorial:cv}, y se obtiene a costa de una menor observabilidad.')
    text=text.replace('En los cortes 7 y 14, los intervalos puntuales del CV activo incluyen cero',
        'En los cortes 7 y 14, los intervalos puntuales del efecto biserial del CV activo frente al retiro futuro incluyen cero')
    text=insert_after(text,r'\section{Sensibilidad de asociaciones a los duplicados exactos}',
        r'La Tabla~\ref{corr:duplicadosefectos} muestra cuánto cambia cada asociación al retirar filas exactamente repetidas antes de agregar la actividad. El signo corresponde a alternativa menos fuente original; un valor próximo a cero indica un cambio descriptivo pequeño en esa comparación, no la validación de una política general de deduplicación.')
    text=insert_after(text,r'\section{Estabilidad de los intervalos por remuestreo}',
        r'La Tabla~\ref{corr:bootstrap} examina cuánto cambian los extremos de los intervalos al ampliar el número de remuestreos. Las 66 comparaciones publicadas permanecen dentro de la tolerancia descriptiva de 0,005; este resultado caracteriza la secuencia utilizada y no una garantía general de convergencia.')
    (P/'desarrollo2.tex').write_text(text,encoding='utf-8')
    conclusions=(OLD/'Conclusiones.tex').read_text(encoding='utf-8')
    conclusions=conclusions.replace(r'\section{Continuidad y trabajos futuros}',r'''\section{Correspondencia con los objetivos}
La Tabla~\ref{editorial:avance} distingue la evidencia disponible de la terminación de cada objetivo. La comprensión de datos y la ingeniería tienen productos ejecutados; su existencia no implica que se haya fijado el conjunto predictivo final ni evaluado el objetivo general. Los estados se refieren a esta versión, sin asignar porcentajes de avance.
\input{avance_objetivos}
\section{Continuidad y trabajos futuros}''')
    (P/'Conclusiones.tex').write_text(conclusions,encoding='utf-8')
    for name,label in [('desarrollo3.tex','editorial:modelos'),('desarrollo4.tex','editorial:shapestado'),('desarrollo5.tex','editorial:prototipo')]:
        (P/name).write_text(r'\label{'+label+'}\n'+(OLD/name).read_text(encoding='utf-8'),encoding='utf-8')
    print('Cascada verificada, resultados aclarados y trazabilidad integrada.')


if __name__=='__main__':
    main()
