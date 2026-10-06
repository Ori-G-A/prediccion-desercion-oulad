"""Integra bloques de informes verificados; preserva el marco y la plantilla."""
from pathlib import Path
import re
import shutil
from generar_informes import OUT, DEST

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'Plantilla_ProyAplicado'


def sections(text):
    starts=list(re.finditer(r'\\section\{([^}]+)\}',text))
    return {m.group(1):text[m.start():starts[j+1].start() if j+1<len(starts) else len(text)] for j,m in enumerate(starts)}


def adapt(text):
    text=text.replace('../figuras/','figuras_multiventana/')
    text=text.replace('El presente\ninforme','Este capítulo').replace('El presente informe','Este capítulo')
    text=text.replace('Por ello, se retiró la afirmación de que corresponden necesariamente a sesiones separadas.',
                      'Los registros no incluyen identificador de sesión ni hora; el origen de las repeticiones no puede establecerse a partir de estos campos.')
    # Las tablas reservan espacio según su tamaño; evitar encabezados aislados.
    text=text.replace('\\section{', '\\Needspace{.42\\textheight}\\section{')
    text=text.replace('\\subsection{', '\\Needspace{.32\\textheight}\\subsection{')
    return text


def main():
    b1=(DEST/'01_exploracion_contenido.tex').read_text(encoding='utf-8')
    b2=sections((DEST/'02_ingenieria_contenido.tex').read_text(encoding='utf-8'))
    b3=sections((DEST/'03_estadistica_contenido.tex').read_text(encoding='utf-8'))
    # Resultados y denominadores visibles; listados extensos se publican en anexos referidos.
    context=b3['Resultados ampliados de las variables de contexto']
    table_start=context.index('\\Needspace',context.index('Los créditos representan'))
    levels=context[table_start:]
    context=context[:table_start]+'Los conteos por nivel se publican en el Anexo~\\ref{corr:anexocontexto}, Tabla~\\ref{corr:niveles}.\n'
    c1='\\label{cap:caracterizacion}\n'+b1
    c1+='\n\\section{Exploración estadística por corte}\n'
    for key in ['Propósito y alcance estadístico','Asociaciones e incertidumbre dentro de cada corte','Disponibilidad, distribución y heterogeneidad']:
        c1+=b3[key].replace('\\section{','\\subsection{',1)
    c1+=context
    c2='\\label{cap:ingenieria}\n'
    c2+=b2['Notación y definición de la tarea temporal']
    c2+=b2['Selección de indicadores y diferencias respecto del anteproyecto']
    c2+=b2['Población elegible y cambio de composición']
    c2+=b2['Cascadas completas de elegibilidad']
    c2+=b2['Construcción y disponibilidad de indicadores']
    c2+=b2['Disponibilidad y calendario']
    c2+='Los nombres, dominios y reglas de ausencia de los candidatos se publican en el Anexo~\\ref{corr:anexodiccionario}, Tabla~\\ref{corr:diccionario}.\n'
    for key in ['Redundancia y estructura multivariada','VIF publicado y decisión sobre el conteo de filas','Sensibilidad de variabilidad y componentes principales','Sensibilidad de asociaciones a los duplicados exactos','Estabilidad de los intervalos por remuestreo','Sensibilidad con población y evento comunes','Conclusiones y continuidad']:
        c2+=b3[key]
    (P/'desarrollo1.tex').write_text(adapt(c1),encoding='utf-8')
    (P/'desarrollo2.tex').write_text(adapt(c2),encoding='utf-8')
    annex=r'''\markboth{Anexos}{Anexos}
\section{Reproducibilidad y decisiones de la versión}\label{anexo:reproducibilidad}
La versión \texttt{correcciones\_2026\_09\_10} conserva el protocolo temporal de la versión multiventana anterior. Los tres notebooks se ejecutaron en procesos Python nuevos. Los CSV originales se preservan; el respaldo previo de código, notebooks y plantilla está identificado en el registro de entrega. La autorización de trabajo y las diferencias de A3.1 y A2.5 se documentan sin presumir ratificación institucional.

Se contrastaron clics, días activos y CV activo sobre toda la fuente para las inscripciones elegibles de los cinco cortes; también se comprobaron fronteras de fechas, conjuntos candidatos, etiquetas e invariancia frente a información futura. La alternativa sin exactos conserva población y evento. Los intervalos utilizan 5\,000 remuestreos de personas y su estabilidad se describe comparando prefijos de 500 y 2\,000; no se presenta esta comparación como prueba de convergencia universal.

El archivo \texttt{README\_\allowbreak{}REVISION.md} documenta los comandos de generación, comprobación e integración. Los registros independientes y los hashes identifican la ejecución y los artefactos. No se entrenaron clasificadores ni se eligió una ventana óptima. La revisión bibliográfica del marco continúa parcial y el protocolo de validación predictiva permanece pendiente.

\section{Resultados por nivel de las variables de contexto}\label{corr:anexocontexto}
Cada celda informa retiros futuros sobre inscripciones elegibles y el porcentaje correspondiente. Las categorías no disponibles permanecen explícitas y el análisis no atribuye causalidad ni certifica equidad.
'''+levels+'\n'+b2['Diccionario reconciliado de indicadores'].replace('\\section{Diccionario reconciliado de indicadores}',r'\section{Diccionario reconciliado de indicadores}\label{corr:anexodiccionario}')
    annex+='\n'+b2['Enlace con la versión anterior y productos']
    annex+=r'''
\clearpage
\section{Esquema relacional OULAD}
\begin{figure}[H]\centering
\includegraphics[width=.95\textwidth]{model.png}
\caption{Esquema relacional de OULAD. Fuente: \cite{sdata2017171}.}\label{fig:esquema-oulad}
\end{figure}
'''
    (P/'anexos.tex').write_text(adapt(annex),encoding='utf-8')
    for f in (OUT/'figuras').glob('*'):
        if f.suffix in ['.pdf','.png']:shutil.copy2(f,P/'figuras_multiventana'/f.name)
    # Precisar el significado de la probabilidad en la deducción de costes.
    path=P/'descripcion.tex';text=path.read_text(encoding='utf-8')
    text=text.replace('la comparación entre $c_{FP}(1-\\pi)$ y $c_{FN}\\pi$',
                      'con $p(\\mathbf x)=\\Pr(Y=1\\mid\\mathbf X=\\mathbf x)$, la comparación entre $c_{FP}(1-p(\\mathbf x))$ y $c_{FN}p(\\mathbf x)$')
    text=text.replace('proporción $\\hat{\\pi}$ de la clase positiva es $G=2\\hat{\\pi}(1-\\hat{\\pi})$',
                      'proporción $\\hat p_{\\mathrm{nodo}}$ de la clase positiva es $G=2\\hat p_{\\mathrm{nodo}}(1-\\hat p_{\\mathrm{nodo}})$')
    text=text.replace('y la equidad de sus predicciones constituye un criterio de evaluación adicional al desempeño agregado',
                      'y la equidad de sus predicciones constituiría un criterio adicional al desempeño agregado en una ampliación del estudio; su evaluación exhaustiva queda fuera del alcance actual')
    path.write_text(text,encoding='utf-8')
    path=P/'conclusiones.tex';text=path.read_text(encoding='utf-8')
    text=text.replace('Los dos primeros objetivos cuentan con evidencia reproducida en esta fase; su consolidación académica depende de la revisión integral del documento.',
                      'La caracterización y la ingeniería disponen de evidencia reproducida, con publicación de los flujos, atributos de contexto y diccionario. La selección de variables base para el modelado sigue pendiente. Se excluyó el conteo de filas como candidato y se documentaron sensibilidad a duplicados, variabilidad activa y especificaciones de PCA; estos diagnósticos no acreditan ganancia predictiva.')
    path.write_text(text,encoding='utf-8')
    path=P/'abstract.tex';text=path.read_text(encoding='utf-8')
    text=text.replace('500 remuestreos','5\\,000 remuestreos').replace('46 comprobaciones','comprobaciones')
    text=text.replace('siete tablas que contienen', 'siete tablas; las de información y matrícula contienen')
    text=text.replace('con contrastes de clics sobre una muestra reproducible y de entregas sobre toda la fuente',
                      'con contrastes completos de clics, días activos y CV activo en las poblaciones elegibles, además de las entregas')
    path.write_text(text,encoding='utf-8')
    print('Capítulos 3 y 4 y anexos integrados desde la nueva ejecución.')


if __name__=='__main__':main()
