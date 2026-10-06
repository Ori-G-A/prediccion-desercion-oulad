"""Integra la revisión editorial desde el respaldo previo, sin alterar análisis.

La fuente anterior se conserva para permitir la reproducción de esta migración.
No ejecutar sobre cambios editoriales posteriores sin reconciliarlos primero.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'Plantilla_ProyAplicado'
OLD = ROOT / 'respaldo/2026-09-13_pre_integracion_editorial/Plantilla_ProyAplicado'


def read(name):
    return (OLD / name).read_text(encoding='utf-8')


def write(name, text):
    (P / name).write_text(text, encoding='utf-8')


def main():
    maintex = read('proyecto.tex').replace('10 de septiembre de 2026', '13 de septiembre de 2026')
    maintex = maintex.replace(r'\mainmatter', '\\input{notacion}\n\\mainmatter')
    write('proyecto.tex', maintex)
    text = read('descripcion.tex')
    # Los cambios de símbolos se limitan a la sección pertinente.
    text = text.replace(r'\sigma(', r'\sigma_{\mathrm{log}}(').replace(r'\sigma\big', r'\sigma_{\mathrm{log}}\big')
    a, b = text.index(r'\paragraph{Regresión logística}'), text.index(r'\paragraph{Random Forest}')
    text = text[:a] + text[a:b].replace(r'\lambda', r'\lambda_{\mathrm{LR}}') + text[b:]
    a, b = text.index(r'\paragraph{Random Forest}'), text.index(r'\paragraph{XGBoost}')
    block = text[a:b].replace('$m$', '$m_{\\mathrm{RF}}$').replace(r'\sigma', r'\sigma_{\mathrm{RF}}').replace(r'\rho', r'\rho_{\mathrm{RF}}')
    proof = re.search(r'\\begin\{proof\}.*?\\end\{proof\}', block, re.S).group()
    block = block.replace(proof, r'La demostración se presenta en el Anexo~\ref{editorial:rf}.')
    text = text[:a] + block + text[b:]
    a, b = text.index(r'\paragraph{XGBoost}'), text.index(r'\paragraph{LightGBM}')
    block = text[a:b].replace(r'\lambda', r'\lambda_{\mathrm{XGB}}').replace(r'\gamma', r'\gamma_{\mathrm{XGB}}')
    block = block.replace('^{(t', '^{(t_{\\mathrm{boost}}').replace('f_{t}', 'f_{t_{\\mathrm{boost}}}').replace('iteración $t$', 'iteración $t_{\\mathrm{boost}}$')
    begin = block.index('con $T$')
    end = block.index('Estas expresiones hacen explícito')
    derivation = block[begin:end]
    replacement = r'''Aquí $T$ es el número de hojas, $\mathbf w$ reúne sus pesos y $t_{\mathrm{boost}}$ identifica la iteración, no el día de predicción. El modelo equilibra dos propósitos: reducir el error de clasificación y limitar la complejidad de los árboles. Esta distinción permite interpretar la regularización antes de examinar su desarrollo algebraico.

La expansión de Taylor, las condiciones del peso óptimo y la ganancia de división se conservan en el Anexo~\ref{editorial:xgb}, ecuaciones~\eqref{eq:xgb-taylor} y~\eqref{eq:xgb-gain}. Allí se detalla por qué las derivadas de la pérdida determinan el ajuste de cada hoja. '''
    block = block[:begin] + replacement + block[end:]
    text = text[:a] + block + text[b:]
    a, b = text.index(r'\paragraph{LightGBM}'), text.index(r'\paragraph{TabNet}')
    block = text[a:b].replace('$k$', '$k_{\\mathrm{bins}}$').replace('O(kp)', 'O(k_{\\mathrm{bins}}p)').replace('$d$', '$d_{\\mathrm{arbol}}$').replace('$2^d$', '$2^{d_{\\mathrm{arbol}}}$')
    text = text[:a] + block + text[b:]
    a, b = text.index(r'\paragraph{TabNet}'), text.index(r'\subsubsection{Metodología CRISP-DM}')
    block = text[a:b].replace(r'\gamma', r'\gamma_{\mathrm{TN}}')
    block = block.replace('paso $i$', 'paso $s_{\\mathrm{TN}}$').replace('[i', '[s_{\\mathrm{TN}}').replace('h_{i}', 'h_{s_{\\mathrm{TN}}}').replace('^{i}', '^{s_{\\mathrm{TN}}}').replace(r'\sum_{i=1}', r'\sum_{s_{\mathrm{TN}}=1}')
    text = text[:a] + block + text[b:]
    theorem = re.search(r'\\begin\{teorema\}\[Unicidad.*?\\end\{teorema\}', text, re.S).group()
    text = text.replace(theorem, r'El resultado formal de unicidad y sus condiciones se conservan en el Anexo~\ref{editorial:shap}. En la lectura aplicada, la propiedad central es que las contribuciones reconstruyen la salida explicada a partir de una referencia fijada.')
    text = text.replace('$I_{j}=n^{-1}', '$I_{\\mathrm{SHAP},j}=n^{-1}')
    write('descripcion.tex', text)
    appendix = '\n\\clearpage\n\\section{Desarrollos matemáticos complementarios}\\label{editorial:matematica}\n'
    appendix += 'Estas derivaciones amplían las formulaciones del marco teórico; su traslado conserva las hipótesis y los resultados. No constituyen evidencia de modelos entrenados.\n'
    appendix += '\n\\subsection{Varianza del promedio en Random Forest}\\label{editorial:rf}\n'
    appendix += 'Bajo las hipótesis de la Proposición~\\ref{prop:rf-var}, se obtiene la ecuación~\\eqref{eq:rf-var} de la siguiente manera.\n' + proof
    appendix += '\n\\subsection{Aproximación y solución por hojas en XGBoost}\\label{editorial:xgb}\n'
    appendix += 'Se parte del objetivo de la ecuación~\\eqref{eq:xgb-obj}, con $\\nu=1$ para el árbol candidato. La expansión utiliza la puntuación acumulada de la etapa anterior.\n'
    # El párrafo inicial dependía de la oración anterior en el cuerpo.
    derivation = derivation.replace('con $T$ el número de hojas del árbol y $\\mathbf{w}$ el vector de sus pesos, y utiliza', 'Con $T$ como número de hojas y $\\mathbf{w}$ como vector de pesos, se utiliza', 1)
    appendix += derivation
    appendix += '\n\\subsection{Condiciones de unicidad de la atribución SHAP}\\label{editorial:shap}\n' + theorem
    appendix += '\nEl enunciado preciso y su demostración se remiten a \\cite{lundberg2017,shapley1953}. El resultado presupone una función de valor, una representación y una salida fijadas; no establece igualdad entre explicaciones construidas con referencias distintas ni identifica relaciones causales. La lectura de las atribuciones conserva la escala de la ecuación~\\eqref{eq:shap-aditivo}.\n'
    write('anexos.tex', read('anexos.tex') + appendix)
    text = read('desarrollo2.tex')
    a = text.index(r'\Needspace{0.42\textheight}')
    b = text.index(r'\begin{align}', a)
    text = text[:a] + r'''La guía preliminar (página~\pageref{editorial:notacion}) reúne la notación del documento. La Figura~\ref{editorial:temporal} permite interpretar las reglas de elegibilidad antes de expresarlas matemáticamente: la información disponible se acumula hasta el corte y el evento se busca únicamente después de él.
\input{figura_temporal}
''' + text[b:]
    text = text.replace('La recencia es $t-\\max A_i(t)$', 'La recencia se denota $R_i(t)=t-\\max A_i(t)$')
    pos = text.index('El sumando 1 de la tendencia')
    example = r'''\paragraph{Lectura de los indicadores mediante un ejemplo}
Considérese una inscripción hipotética elegible al día 28, con 100 clics distribuidos en 10 días activos y última actividad en el día 26. El calendario contiene 29 días; por ello, $V_i(28)=100$, $k_i(28)=10$, $q_i(28)=10/29\simeq0{,}3448$, $m_i(28)=10$ y $R_i(28)=2$. Estas cantidades describen volumen, frecuencia, intensidad y recencia diferentes. Ninguna demuestra motivación ni permite asignar por sí sola el retiro futuro. Si no existieran clics, volumen y días activos serían cero, mientras intensidad y recencia permanecerían sin definición.

La Figura~\ref{editorial:indicadores} representa el paso de registros a indicadores. La unidad resultante continúa siendo la inscripción en un corte; un conteo de filas del registro no se interpreta como número de sesiones.
\input{figura_indicadores}

'''
    text = text[:pos] + example + text[pos:]
    write('desarrollo2.tex', text)
    text = read('desarrollo1.tex').replace(r'\section{Conclusiones y productos de la fase}', r'\section{Balance de la auditoría y productos}')
    text = text.replace('$V=\\sqrt', '$V_C=\\sqrt')
    text += r'''
\Needspace{.25\textheight}\section{Síntesis de la caracterización}
La auditoría permitió distinguir la inscripción de la persona, establecer las limitaciones de los registros y separar el retiro administrativo de las señales de inactividad. La exploración posterior describió asociaciones en poblaciones propias de cada corte; sus magnitudes no constituyen desempeño predictivo ni efectos causales. En conjunto, estos resultados delimitan qué información puede incorporarse a la preparación de datos y qué interpretaciones deben mantenerse condicionadas.

El capítulo siguiente formaliza esa preparación mediante reglas de elegibilidad, ventanas e indicadores. La continuidad entre ambas fases requiere conservar los denominadores, distinguir ausencia de actividad de falta de definición y documentar las variables excluidas antes de evaluar modelos.
'''
    write('desarrollo1.tex', text)
    intro = read('introduccion.tex')
    intro += r'''
La Figura~\ref{editorial:ruta} sitúa los productos disponibles y las etapas pendientes. Para consultar una expresión matemática puede utilizarse la guía preliminar; para relacionarla con una columna del conjunto analítico se dispone del diccionario del Anexo~\ref{corr:anexodiccionario}. Las demostraciones complementarias se reúnen en el Anexo~\ref{editorial:matematica}.
\input{figura_ruta}
'''
    write('introduccion.tex', intro)
    print('Integración editorial aplicada desde el respaldo; análisis conservados.')


if __name__ == '__main__':
    main()
