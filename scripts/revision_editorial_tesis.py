"""Informe editorial y propuesta propia; no modifica tesis ni resultados analíticos."""
from pathlib import Path
import json, hashlib, html
import fitz
import matplotlib
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reportes/revision_editorial_2026_09_13';OUT.mkdir(parents=True,exist_ok=True)
PDF=ROOT/'output/pdf/revision_editorial_tesis_aprobadas.pdf'
inventory=json.loads((ROOT/'tmp/revision_tesis_aprobadas/inventario.json').read_text(encoding='utf-8'))
selection=json.loads((ROOT/'tmp/revision_tesis_aprobadas/seleccion_visual.json').read_text(encoding='utf-8'))
extra={'T02':[22,35],'T05':[13],'T08':[22],'T09':[58],'T11':[55],'T12':[8,33],'T15':[50]}
for r in inventory:r['paginas_revision_visual']=sorted(set(selection[r['id']]+extra.get(r['id'],[])))

# Referencias editoriales: páginas físicas del PDF, no páginas impresas.
examples=[
('T01','Expansión urbana y pobreza en Bogotá','40','Flujo de preprocesamiento junto a su explicación.','Adaptar un flujo de las fuentes OULAD a la inscripción por corte.'),
('T02','Cuantificación en toxicología forense','22, 35, 75','Ciclo metodológico, caso trabajado y gráficos comparables.','Un ejemplo de inscripción ayuda a seguir filtros e indicadores.'),
('T03','Matrícula de aspirantes admitidos','16–17','Fórmula, definición próxima de términos y matriz de errores.','Explicar el significado educativo de cada expresión antes de su desarrollo.'),
('T04','Fraudes y anomalías en agua potable','39–40','Vincula errores de clasificación con el problema aplicado.','Traducir falso positivo y falso negativo al retiro registrado, sin atribuir motivos.'),
('T05','EUR/USD con LSTM y sentimiento','13, 28–29','CRISP-DM adaptado y lectura organizada de hallazgos.','Usar un mapa propio; no trasladar su arquitectura ni criterios estadísticos.'),
('T06','Identificación de pólipos','20, 38','Matriz de confusión interpretada y tablas de comparación.','Preparar esta presentación para cuando existan modelos evaluados.'),
('T07','Islas de calor en tres ciudades','33–34','Diagramas de operaciones con referencias al código.','Conectar fases con entradas, salidas y controles; evitar dibujar cada instrucción.'),
('T08','Digitalización del sector cacaocultor','22, 30','Flujo por etapas y representación visual de productos.','Mostrar cómo los registros se convierten en indicadores, sin copiar imágenes.'),
('T09','Humedad del suelo en el CIAT','15, 44, 58','Esquema de modelo, panel de resultados y flujo de modelado.','Adoptar la lógica expositiva; su división de datos no justifica una partición OULAD.'),
('T10','Resiliencia escolar y conflicto armado','17, 49','Interpretación de métricas y procedimiento enumerado.','Separar procedimiento, resultado y consecuencia; no trasladar decisiones de validación.'),
('T11','Homicidios, eficiencia y resiliencia','43, 55','Definiciones operativas y figura SHAP junto al texto.','Reservar SHAP para el modelo evaluado; interpretar atribuciones, no causalidad.'),
('T12','Salud mental en comunidad universitaria','8, 33','Glosario preliminar y resumen metodológico.','Justifica estudiar una ayuda de consulta; no equivale a tabla matemática completa.'),
('T13','Contratistas y publicaciones de corrupción','14, 50','Apartados breves con transiciones entre procedimientos.','Retener la organización temática, sin convertir afirmaciones ajenas en evidencia propia.'),
('T14','ClientMinds: experiencia del cliente y PLN','60','Diagrama que explicita particiones y estructura del registro.','Dibujar la partición solo después de definir el protocolo propio.'),
('T15','Supervivencia en cáncer de estómago','24, 50, 55','Ejemplo de calibración identificado como ilustración y discusión de faltantes.','Distinguir figuras didácticas de resultados; no importar etiquetas o supuestos de supervivencia.'),
]
findings=[
('E01','Mayor','Guía parcial y tardía','Tabla 4.1, p. PDF 45; fórmulas desde p. 19.','Crear índice general de símbolos antes de la introducción; conservar definiciones locales.'),
('E02','Mayor','Símbolos con varios usos','Cap. 2: t, i, m, k, γ y σ; cap. 4: índices temporales.','Separar índices y añadir contexto/dominio. La reutilización local no prueba error algebraico.'),
('E03','Mayor','Desarrollo formal difícil de recorrer','Cap. 2, Random Forest, XGBoost y SHAP; pp. PDF 21–29.','Mantener fórmula y supuestos esenciales; trasladar derivaciones extensas con remisión explícita.'),
('E04','Mayor','Falta un esquema de la tarea temporal','Cap. 4.1, pp. PDF 45–46.','Añadir línea temporal con población elegible, corte, evento y horizonte variable.'),
('E05','Menor','Las figuras existentes no cubren todas las preguntas','Figuras 3.1–3.4 y 4.1–4.3; anexo relacional.','Conservar resultados útiles; añadir ayudas conceptuales sin duplicar tablas completas.'),
('E06','Menor','Conclusión de auditoría antes del resto del capítulo','Cap. 3.6 precede al histograma y a las asociaciones.','Renombrar como balance de auditoría; cerrar capítulo 3 con síntesis integradora.'),
('E07','Menor','Nombres de código y detalle de versión interrumpen lectura','Cap. 3.1 y diccionario del anexo.','Usar nombres legibles en el relato y mantener correspondencia con código en diccionario.'),
('E08','Mayor','Antecedente editorial no equivale a regla institucional','Carpeta aportada y materiales locales de plantilla.','Conservar jerarquía institucional y consultar reglamento para cambios obligatorios; aprobación de estos archivos aportada por usuario.'),
]
visuals=[
('V01','Mapa del estudio','Introducción o apertura metodológica','Datos → unidad de análisis → cinco cortes → indicadores → modelos → SHAP/prototipo. Diferenciar ejecutado y pendiente.','Prioridad 1'),
('V02','Línea temporal y cuatro casos','Antes de elegibilidad, cap. 4.1','Mostrar día 0, t, L y cuatro inscripciones hipotéticas; distinguir registro tardío, retiro previo y futuro.','Prioridad 1'),
('V03','Del registro al indicador','Construcción de variables','Ejemplo pequeño de clics diarios que produzca volumen, días activos, proporción y recencia.','Prioridad 1'),
('V04','Flujo de elegibilidad al día 28','Junto a la cascada completa','Construir desde 02_flujos.csv. No sumar categorías solapadas ni sustituir la tabla de cinco cortes.','Prioridad 2'),
('V05','Comparación de ambos CV','Sección de variabilidad','Dos secuencias hipotéticas con igual frecuencia y distinta intensidad; señalar qué mide cada CV.','Prioridad 2'),
('V06','Particiones y evaluación','Capítulo de modelos','Personas/presentaciones, ajustes internos y evaluación reservada. Esquema aún pendiente de protocolo.','Posterior'),
('V07','Resultados predictivos y SHAP','Resultados de modelos','Curvas de calibración y precisión–recobrado, matriz de errores y explicación de riesgo; solo resultados ejecutados.','Posterior'),
]

# Cada entrada: escritura propuesta, significado/dominio, ámbito. Los cambios son propuestas, no sustituciones ejecutadas.
notation=[
('A. Población y tiempo',[
('i','Inscripción: persona × módulo × presentación.','Unidad de análisis'),
('d; t','Día relativo al inicio; corte de predicción. t pertenece a {7,14,28,42,56}.','Corte y actividad'),
('n_t = t + 1','Cantidad de días del calendario inclusivo 0..t. No es tamaño muestral.','Ventana'),
('r_i; u_i','Fecha de matrícula y fecha de retiro, en días relativos. Pueden faltar en la fuente.','Elegibilidad'),
('L_i','Final operativo según longitud de presentación; no fecha de última observación individual verificada.','Horizonte'),
('ℰ(t)','Conjunto de inscripciones elegibles. Mantener la letra caligráfica en LaTeX para distinguirlo del conteo E(t).','Conjunto'),
('N(t)','Número de inscripciones elegibles: cardinalidad de ℰ(t).','Denominador'),
('Y_i(t)','Indicador 0/1 de retiro en t < u_i ≤ L_i. Una fecha ausente no genera evento.','Etiqueta'),
('E(t)','Número de retiros futuros entre elegibles; distinto del conjunto ℰ(t).','Numerador'),
('π(t)','Prevalencia E(t)/N(t), entre 0 y 1. No probabilidad individual.','Población'),
('1{condición}','Función indicadora: 1 si la condición se cumple, 0 en otro caso.','Operador'),
('|S|; ∈; ∅','Número de elementos; pertenencia; conjunto vacío.','Conjuntos'),
('[0,t]; (t,L_i]','Extremos incluidos; extremo inicial excluido y final incluido.','Intervalos temporales'),
]),
('B. Actividad e indicadores',[
('c_id','Total de clics de inscripción i en día d; entero no negativo.','Actividad diaria'),
('A_i(t)','Conjunto de días con al menos un clic entre 0 y t.','Días activos'),
('V_i(t)','Suma de clics entre 0 y t.','Volumen'),
('k_i(t)','Número de días activos: |A_i(t)|; 0..n_t.','Frecuencia'),
('q_i(t)','Proporción k_i(t)/n_t; 0..1.','Continuidad'),
('m_i(t)','Intensidad V_i(t)/k_i(t); no definida si k_i(t)=0.','Intensidad'),
('R_i(t); R_i(t)/n_t','Propuesta para recencia t − max A_i(t) y recencia relativa; ausentes sin actividad.','Recencia'),
('CV_cal; CV_act','Desviación muestral/media de clics: calendario completo o solo días activos. CV_act requiere k_i≥2.','Variabilidad'),
('s_act; q; k; n','Desviación activa y abreviaturas locales q_i(t), k_i(t), n_t en la identidad de CV.','Identidad, cap. 4'),
('s; T_i,s(t)','Longitud del bloque (7 o 14) y logaritmo del cociente suavizado de dos bloques; ausente con historia insuficiente o ambos nulos.','Tendencia'),
('ln; log; exp','Logaritmo natural en las expresiones de esta versión; exponencial inversa. Especificar otra base si se introduce.','Funciones'),
('Σ; max; ≥; ≤','Suma; máximo; comparaciones inclusivas.','Operadores'),
]),
('C. Estadística descriptiva y asociaciones',[
('Q25; Q50; Q75','Cuartiles 25, 50 (mediana) y 75 por variable y corte.','Distribución'),
('IQR; MAD','Rango intercuartílico y desviación absoluta mediana; documentar factor de normalización usado.','Dispersión'),
('r_rb; U_1','Efecto biserial por rangos y estadístico de Mann–Whitney del grupo con retiro futuro.','Asociación numérica'),
('n_1; n_0','Casos observados de cada grupo para el indicador; no siempre todos los elegibles.','Denominadores efectivos'),
('ρ_S','Propuesta para correlación de Spearman, distinguida de la correlación común ρ_RF de árboles.','Correlación'),
('V_C; χ²','Propuesta para V de Cramér y estadístico de la tabla de contingencia. Evitar confundir V_C con volumen V_i.','Asociación categórica'),
('N_cont; f; g','Total de casos de contingencia y cantidades de filas/columnas; en el texto se utiliza N.','V de Cramér'),
('B_boot; IC95 %','Cantidad de remuestreos (5.000) e intervalo puntual exploratorio del 95 %. Separar B_boot del número de árboles.','Remuestreo'),
('Var; Cov','Varianza y covarianza; sus argumentos identifican las variables aleatorias.','Operadores'),
('PCA; VIF; MCD','Componentes principales; inflación de varianza; determinante mínimo de covarianza. Desarrollar en glosario.','Siglas metodológicas'),
]),
('D. Clasificación, regresión logística y árboles',[
('D; n_ent; p','Conjunto de entrenamiento, número de filas y número de características. D representa la actual letra caligráfica.','Formulación general'),
('x_i; x_ij; y_i','Vector de características, componente j y etiqueta binaria de inscripción i en un corte fijado.','Entrenamiento'),
('p(x); p̂(x); ŷ','Probabilidad condicional, estimación del modelo y clase asignada. El sombrero indica estimación.','Predicción'),
('τ; c_FP; c_FN','Umbral y costes positivos de falso positivo/negativo. No están fijados operativamente aún.','Decisión'),
('σ_log; η; β_0; β_j','Función logística, predictor lineal, intercepto y coeficientes. σ_log evita confusión con desviación estándar.','Regresión logística'),
('ℓ; λ_LR; C','Log-verosimilitud, penalización logística y parámetro de implementación; relación depende de normalización.','Ajuste'),
('π_i → p̂_i','Cambio propuesto para probabilidad individual estimada, distinguida de prevalencia π(t).','LR y boosting'),
('B_RF; b_RF; m_RF','Número de árboles, índice de árbol y predictores candidatos en un corte de árbol.','Random Forest'),
('T_b; σ_RF²; ρ_RF','Estimador por árbol, varianza común y correlación común en la proposición idealizada.','Proposición RF'),
('p̂_nodo; Gini','Proporción positiva en un nodo e impureza binaria.','Árboles'),
('ℝ^p; xᵀβ; ||β||²_2','Espacio real p-dimensional, producto escalar y norma euclídea al cuadrado.','Álgebra'),
]),
('E. Boosting, LightGBM y TabNet',[
('h_boost; z_i; f_h; ν','Índice propuesto de iteración (actual t), puntuación previa a logística, árbol y tasa de aprendizaje.','Boosting'),
('L_obj; l; Ω','Objetivo, pérdida individual y penalización del árbol; conservar letras caligráficas en LaTeX.','XGBoost'),
('T_hojas; w_j; I_j','Número de hojas, peso de hoja y conjunto de observaciones asignadas.','XGBoost'),
('g_i; h_i; G_j; H_j','Derivadas primera y segunda de pérdida y sus sumas por hoja. h_i no es índice h_boost.','Taylor'),
('λ_XGB; γ_XGB; G_corte','Penalización de pesos, coste de hoja y ganancia del corte. Añadir subíndices evita ambigüedad entre modelos.','XGBoost'),
('I_L; I_R; w_j*','Observaciones de ramas izquierda/derecha y peso óptimo de hoja, bajo los supuestos indicados.','XGBoost'),
('a_GOSS; b_GOSS; k_bins; d_arbol','Fracciones GOSS del total, intervalos del histograma y profundidad. Distinguir k_bins de días activos.','LightGBM'),
('N_s; s_TN; N_b; b_lote','Número e índice de pasos de decisión, tamaño e índice del lote. Actual i en TabNet no es inscripción.','TabNet'),
('M[s]; P[s]; a[s]; h_s','Máscara, prior, estado y transformación entrenable. Dimensiones según arquitectura.','TabNet'),
('γ_TN; λ_disp; ε; L_disp','Reutilización, penalización de dispersión, estabilizador positivo y término de entropía.','TabNet'),
('⊙; Π; sparsemax','Producto elemento a elemento, producto indexado y transformación de máscara dispersa.','Operadores'),
]),
('F. SHAP y consulta transversal',[
('F; S; j','Conjunto de características, subconjunto y característica explicada. j es local al ámbito.','Shapley'),
('v(S); φ_j; φ_0','Valor de coalición, atribución y referencia/base. Definir distribución y escala al implementar.','SHAP'),
('f(x); v_x(∅)','Salida explicada y valor de la coalición vacía para la observación x; este último fija φ_0.','Explicación aditiva'),
('E[·]; E[·|·]','Esperanza y esperanza condicional; no número de eventos E(t).','Referencia SHAP'),
('p = |F|; B_SHAP; L_SHAP; D_SHAP','Cantidad de características, árboles, máximo de hojas y profundidad máxima en el coste computacional. L_SHAP no es final de curso L_i.','TreeSHAP'),
('I_SHAP,j','Propuesta para importancia global: promedio de |φ_j| sobre casos. El texto usa I_j, también usado como conjunto de hoja en XGBoost.','SHAP global'),
('X_S; x_S; X_−S','Subvector aleatorio, valores observados de las características de S y características complementarias.','Referencia SHAP'),
('!; ⊆; ∪; ∖','Factorial, subconjunto, unión y diferencia de conjuntos en la fórmula de Shapley.','Operadores'),
('∂; ≈; O(·)','Derivada parcial, aproximación y orden de coste asintótico; contexto y supuestos locales.','Operadores'),
('LMS; VLE; OULAD; CRISP-DM','Separar siglas de notación matemática y de nombres de columnas en el diccionario.','Glosario'),
])]

fontdir=Path(matplotlib.get_data_path())/'fonts/ttf'
pdfmetrics.registerFont(TTFont('Arial',str(fontdir/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('ArialB',str(fontdir/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialB',italic='Arial',boldItalic='ArialB')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyX',fontName='Arial',fontSize=10,leading=14,spaceAfter=9,textColor=colors.HexColor('#243746')))
styles.add(ParagraphStyle(name='TitleX',fontName='ArialB',fontSize=23,leading=28,spaceAfter=18,textColor=colors.HexColor('#134E67')))
styles.add(ParagraphStyle(name='HeadX',fontName='ArialB',fontSize=15,leading=19,spaceAfter=12,textColor=colors.HexColor('#134E67')))
styles.add(ParagraphStyle(name='CellX',fontName='Arial',fontSize=9,leading=12.2,spaceAfter=0))
styles.add(ParagraphStyle(name='SmallX',fontName='Arial',fontSize=8,leading=11,spaceAfter=7,textColor=colors.HexColor('#52636A')))
story=[];md=[]
def para(s,style='BodyX'):
    story.append(Paragraph(s,styles[style]));md.append(s.replace('<b>','**').replace('</b>','**'))
def head(s):para(s,'HeadX');md[-1]='## '+md[-1]
def page():story.append(PageBreak());md.append('')
def table(headers,rows,widths):
    vals=[[Paragraph(html.escape(str(x)),styles['CellX']) for x in row] for row in [headers,*rows]]
    t=Table(vals,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DDEDF2')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#134E67')),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#CBD5DA'))]))
    story.append(t);story.append(Spacer(1,10));md.append('| '+' | '.join(headers)+' |\n|'+ '|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(str(x).replace('|','/') for x in row)+' |' for row in rows))

para('Una tesis más clara, con el mismo rigor','TitleX')
para('Revisión editorial comparada y propuesta de notación<br/>Proyecto OULAD · PUJ Cali · 13 de septiembre de 2026','SmallX')
head('Veredicto')
para('La necesidad de mejorar la lectura está sustentada en la organización del documento actual. El trabajo dispone de resultados y controles metodológicos, pero la guía de símbolos llega después del marco matemático, varias letras cambian de significado y faltan esquemas que expliquen la tarea temporal. La prioridad es orientar al lector antes de exigirle seguir una derivación.')
para('Los referentes aportados muestran recursos compatibles con una exposición académica aplicada: diagramas metodológicos, ejemplos trabajados, glosarios y tablas de comparación. Se propone adaptar esas funciones comunicativas mediante contenido propio, conservando cifras, supuestos, referencias y trazabilidad del proyecto.')
head('Alcance de la revisión')
para(f'Se inventariaron los 15 PDF, que suman {sum(r["paginas"] for r in inventory)} páginas. Se extrajo su texto para localizar estructura, índices, notación y recursos didácticos, y se examinaron visualmente páginas seleccionadas de cada trabajo. Es una revisión editorial dirigida; no una auditoría integral de todos sus resultados ni una lectura crítica de cada página. Las páginas citadas en este informe son páginas físicas del PDF.')
para('La condición de «aprobadas» corresponde a la información aportada por el usuario; no se verificaron actas. Una práctica presente en estos trabajos constituye un antecedente de presentación, no una autorización normativa general. No se localizó en lo examinado una regla institucional específica sobre extensión o ubicación obligatoria de la notación.')
para('La entrega propone cambios y muestra ejemplos propios. El documento activo, los notebooks y los resultados analíticos permanecen como base de contraste. La existencia de un recurso visual en otra tesis no valida trasladar su división de datos, criterios de eliminación, supuestos o conclusiones.')

page();head('1. Qué aportan los referentes: estructura y explicación')
table(['Ref. / tema','PDF','Recurso observado y adaptación propuesta'],[(x[0]+' · '+x[1],x[2],x[3]+' '+x[4]) for x in examples[:8]],[135,45,315])
para('Se retiene el propósito de cada recurso, no su diseño literal. La apariencia también debe revisarse: texto pequeño dentro de un diagrama o la acumulación de gráficas pueden dificultar la lectura aunque aparezcan en un trabajo aprobado.','SmallX')
page();head('2. Qué aportan los referentes: consulta y resultados')
table(['Ref. / tema','PDF','Recurso observado y adaptación propuesta'],[(x[0]+' · '+x[1],x[2],x[3]+' '+x[4]) for x in examples[8:]],[135,45,315])
para('La identificación completa de los archivos T01–T15 y las páginas examinadas acompaña este informe en inventario_fuentes.json y en la versión Markdown. El glosario de T12 es un antecedente de consulta inicial; no se presenta como una tabla de notación matemática equivalente a la que requiere OULAD.','SmallX')

page();head('3. Hallazgos en el documento OULAD')
table(['ID / severidad','Evidencia','Corrección propuesta'],[(x[0]+' · '+x[1]+'\n'+x[2],x[3],x[4]) for x in findings],[142,145,208])
para('La tabla actual contiene diez entradas agrupadas; no cubre todas las familias de símbolos del marco ni dispone de una columna de dominio y remisión. Su existencia no cierra la necesidad de una ayuda general. Las colisiones aquí identificadas son dificultades de lectura; no se equiparan automáticamente a errores de cálculo.','SmallX')

page();head('4. Recursos visuales que responden preguntas concretas')
table(['Recurso','Ubicación / prioridad','Pregunta o contenido'],[(x[0]+' · '+x[1],x[2]+'\n'+x[4],x[3]) for x in visuals],[132,135,228])
para('Se propone comenzar con tres ayudas: mapa del estudio, línea temporal y ejemplo de indicador. Las figuras actuales de fechas de retiro, población por corte, observabilidad y asociaciones ya aportan evidencia y deben conservarse cuando respondan preguntas distintas. No se fija una cuota de figuras ni se usan imágenes decorativas para llenar páginas.')
para('Cada figura deberá tener título informativo, unidades y denominador cuando corresponda, leyenda legible, procedencia, remisión en el texto y un párrafo que explique su aporte y sus límites. Los ejemplos didácticos se rotularán como hipotéticos; los resultados se generarán desde las tablas verificadas.')

page();head('5. Ejemplo propio: qué significa predecir al día 28')
para('El esquema siguiente es didáctico. Se fija hipotéticamente L = 100 para facilitar la lectura; en el análisis real el final varía entre presentaciones. La matrícula es conocida y vale r = 0 salvo en el cuarto caso.')
d=Drawing(495,175)
for x,w,label,col in [(15,130.2,'Observación: [0,28]','#DDEDF2'),(145.2,334.8,'Seguimiento: (28,100]','#E4F0E7')]:
 d.add(Rect(x,83,w,38,fillColor=colors.HexColor(col),strokeColor=None));d.add(String(x+8,98,label,fontName='ArialB',fontSize=9))
d.add(Line(15,77,480,77,strokeColor=colors.HexColor('#134E67'),strokeWidth=2))
for x,label in [(15,'Día 0'),(145.2,'Corte t = 28'),(480,'L = 100')]:
 d.add(Line(x,67,x,130,strokeColor=colors.HexColor('#134E67')));d.add(String(x if x<400 else x-44,48,label,fontName='Arial',fontSize=10))
d.add(String(15,18,'El retiro del propio día 28 ya ocurrió: no es un evento futuro.',fontName='Arial',fontSize=10))
story.append(d)
table(['Caso hipotético','¿Elegible?','Etiqueta al corte 28 / razón'],[('Retiro u = 20','No','El retiro antecede al corte; no se utiliza como positivo futuro.'),('Retiro u = 40','Sí','Y = 1 porque 28 < 40 ≤ 100.'),('Sin fecha de retiro','Sí','Y = 0 según regla operativa; no demuestra éxito académico.'),('Matrícula r = 30; sin retiro','No','La inscripción aún no estaba matriculada al corte.')],[185,65,245])
head('Del comportamiento observado al indicador')
para('En otro ejemplo hipotético, una inscripción acumula 100 clics en 10 días activos dentro de 0..28 y su última actividad ocurre el día 26. El volumen es 100; la frecuencia es 10 días; la proporción activa es 10/29 = 34,48 %; la intensidad media es 100/10 = 10 clics por día activo y la recencia es 28 − 26 = 2 días. Ninguna de estas medidas equivale por sí sola a motivación o abandono.')
para('Si no hay actividad, el volumen y la proporción pueden ser cero, pero intensidad, recencia y CV no se definen con esas reglas. Este contraste explica por qué no todos los faltantes deben completarse automáticamente con cero.')

page();head('6. Cómo organizar la consulta de símbolos')
para('Se propone una lista general de notación después de los índices y antes de la introducción, accesible desde el índice. Cada fila debe incluir símbolo, significado, dominio o unidad y enlace a su definición. En el primer uso se conserva una explicación breve: la tabla no debe obligar a interrumpir continuamente la lectura.')
para('La notación matemática, las siglas y el diccionario de variables cumplen funciones distintas. La primera explica las ecuaciones; el glosario desarrolla LMS, OULAD, PCA o SHAP; el diccionario vincula nombre legible, columna del código, fórmula y regla de ausencia. Se propone mantener las tres ayudas y conectarlas mediante remisiones.')
table(['Uso actual','Distinción propuesta','Motivo'],[('t: corte y boosting','t para tiempo; h_boost para iteración','Separar tiempo educativo y ajuste del modelo.'),('i: inscripción y paso TabNet','i para inscripción; s_TN para paso','Evitar mezclar unidad muestral y arquitectura.'),('m, k, d en varios ámbitos','m_RF, k_bins, d_arbol','Distinguir parámetros de árboles de intensidad, días activos y tiempo.'),('γ y λ entre modelos','γ_XGB, γ_TN; λ_LR, λ_XGB','Los parámetros no representan una única cantidad compartida.'),('σ logística y σ² de RF','σ_log y σ_RF²','Función y varianza son objetos distintos.'),('π_i frente a π(t)','p̂_i frente a π(t)','Separar probabilidad estimada individual y prevalencia.')],[150,155,190])
para('Estas escrituras son propuestas editoriales. Deben sustituirse de forma coherente en ecuaciones, demostraciones y tablas; no mediante reemplazos globales de letras. Las letras caligráficas y vectoriales se conservarán en LaTeX. Las seis tablas siguientes conforman un borrador de cobertura, sujeto a comprobación de cada expresión y a enlaces automáticos al integrarlo.')

for name,rows in notation:
 page();head('Notación · '+name)
 table(['Símbolo o grupo propuesto','Significado y dominio','Ámbito'],rows,[125,280,90])
 para('Estado: propuesta de consulta y desambiguación. No se han modificado todavía las fórmulas del documento activo. Cuando una fila agrupa símbolos, la integración podrá separarlos para ofrecer búsqueda y enlace individual.','SmallX')

page();head('7. Hacer más amable la prosa sin perder precisión')
para('Cada sección puede seguir una progresión breve: qué pregunta responde, por qué importa en OULAD, cómo se define o calcula, qué se observó y qué permite concluir. La fórmula se introduce después de explicar su función; las excepciones se mantienen junto al procedimiento al que afectan.')
head('Ejemplo de redacción para abrir la tarea temporal')
para('Para que una predicción sea temprana, debe referirse a un retiro que todavía no ha ocurrido. Por ello, en cada corte se consideran las inscripciones cuya matrícula ya está registrada y que continúan sin retiro hasta ese día. La información utilizada comprende únicamente la historia disponible al cierre del corte; el seguimiento comienza después y llega hasta el final de la presentación. Esta separación permite distinguir las señales previas del evento que se busca anticipar.')
para('En particular, al predecir al día 28 se observan los días 0 a 28, incluidos ambos extremos. Un retiro registrado el día 20 queda fuera de la población elegible; uno registrado el día 40 puede constituir el evento futuro si ocurre antes del final de la presentación. La línea temporal introduce estas reglas y las ecuaciones posteriores precisan su definición para todas las inscripciones.')
head('Qué conservar en el cuerpo y qué llevar al anexo')
table(['Cuerpo principal','Anexo técnico con remisión'],[('Evento, población, ventana y horizonte; supuestos de disponibilidad.','Detalles de verificación y controles reproducibles.'),('Significado de cada modelo, fórmula central y limitaciones pertinentes.','Desarrollo completo de varianza de RF, Taylor y ganancia de XGBoost, y teorema de Shapley.'),('Resultados principales con denominadores e incertidumbre.','Desgloses extensos y análisis complementarios que ya están publicados.'),('Qué distingue CV de calendario y CV activo.','Demostración detallada de su identidad si interrumpe la lectura del resultado.')],[247,248])
para('Trasladar una demostración no implica eliminarla ni retirar sus hipótesis. El cuerpo debe conservar la ecuación necesaria para interpretar el método y un enlace inequívoco a la derivación. La propuesta mantiene la estructura principal del proyecto y no incorpora modelos, variables o poblaciones nuevas.')

page();head('8. Orden de implementación y criterios de cierre')
table(['Paso','Trabajo','Cómo comprobarlo'],[('1','Inventario de ecuaciones, símbolos y sus usos; fijar desambiguaciones.','Toda expresión tiene definición próxima y entrada de consulta; no hay cambios de significado inadvertidos.'),('2','Mapa del estudio, línea temporal y ejemplo de indicadores.','Ejemplos rotulados; conteos y límites concuerdan con el código; sin resultados predictivos inventados.'),('3','Reescritura de aperturas, enlaces y síntesis de capítulos.','Se distingue procedimiento, hallazgo e interpretación; se conserva voz del planteamiento.'),('4','Reubicar demostraciones y completar remisiones.','Cada derivación permanece accesible y las hipótesis necesarias siguen en el cuerpo.'),('5','Integrar y renderizar una nueva versión preservando la actual.','Referencias y enlaces válidos; tabla legible; cifras intactas; revisión visual de todas las páginas modificadas.')],[38,227,230])
head('Límites y decisiones pendientes')
para('La revisión no acredita una norma institucional específica ni revisa el mérito estadístico de las quince tesis. Tampoco sustituye la ratificación pendiente del evento y el protocolo de validación OULAD. Su utilidad es establecer una propuesta editorial concreta sin alterar el alcance analítico.')
para('El PDF llamado Plantilla_ProyAplicado.pdf en la raíz contiene una versión histórica del propio proyecto; no se utilizó como reglamento institucional. El contraste principal utiliza Plantilla_ProyAplicado/proyecto.pdf y sus fuentes activas. Se conservan los títulos de capítulos de la plantilla; una reorganización institucional mayor requeriría contraste específico con las directrices vigentes.')
para('El siguiente paso recomendado es integrar la notación general y las tres ayudas visuales prioritarias, junto con una edición del marco teórico que conserve sus fundamentos. La revisión bibliográfica y el protocolo de modelado pueden continuar por sus propias líneas de trabajo.')

for start in [0,8]:
 page();head('Fuentes locales · identificación de los referentes')
 para('Identificadores usados en las tablas comparativas. Los archivos se encuentran en la carpeta TESIS APROBADAS del proyecto. Las páginas corresponden al PDF, no a la numeración impresa.','SmallX')
 table(['ID','Archivo aportado / páginas revisadas visualmente'],[(r['id'],r['archivo']+'\nPDF: '+', '.join(map(str,r['paginas_revision_visual']))) for r in inventory[start:start+8]],[35,460])

def footer(c,doc):
 c.saveState();c.setStrokeColor(colors.HexColor('#CBD5DA'));c.line(50,43,545,43);c.setFont('Arial',8);c.setFillColor(colors.HexColor('#52636A'));c.drawString(50,29,'Revisión editorial · OULAD · Propuesta del 13/09/2026');c.drawRightString(545,29,str(doc.page));c.restoreState()
PDF.parent.mkdir(exist_ok=True,parents=True)
SimpleDocTemplate(str(PDF),pagesize=(595.28,841.89),rightMargin=50,leftMargin=50,topMargin=48,bottomMargin=60,title='Revisión editorial de tesis aprobadas y propuesta OULAD',author='Revisión del proyecto OULAD').build(story,onFirstPage=footer,onLaterPages=footer)
md.append('## Identificación de fuentes locales\nLas páginas indicadas son posiciones físicas en los PDF. No se reproducen sus imágenes o redacciones.')
for r in inventory:
 md.append(f"- **{r['id']}**: [{r['archivo']}](<{(ROOT/'TESIS APROBADAS'/r['archivo']).as_posix()}>). Páginas examinadas visualmente: {', '.join(map(str,r['paginas_revision_visual']))}.")
(OUT/'revision_y_propuesta.md').write_text('\n\n'.join(md),encoding='utf-8')
(OUT/'notacion_propuesta.json').write_text(json.dumps(notation,ensure_ascii=False,indent=2),encoding='utf-8')
for r in inventory:
 r['sha256']=hashlib.sha256((ROOT/'TESIS APROBADAS'/r['archivo']).read_bytes()).hexdigest()
(OUT/'inventario_fuentes.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'hallazgos.json').write_text(json.dumps([dict(zip(['id','severidad','hallazgo','ubicacion','correccion'],x),version='editorial_2026_09_13',estado='propuesto') for x in findings],ensure_ascii=False,indent=2),encoding='utf-8')
print(PDF)
print('Páginas:',len(fitz.open(PDF)))
