"""Bloques documentales generados exclusivamente desde la nueva ejecución."""
import re
import pandas as pd
from generar_informes import DEST, data, summary, tab, fig, number


FORMAL=r'''
\section{Notación y definición de la tarea temporal}
El día 0 es el inicio de la presentación; las fechas negativas son anteriores a ese origen. La unidad $i$ es la terna de persona, módulo y presentación. Para cada corte $t$, $n_t=t+1$ es la longitud inclusiva del calendario observado, $r_i$ es la fecha de matrícula, $u_i$ la fecha de retiro cuando existe y $L_i$ el final según la convención operativa basada en la longitud registrada de la presentación. La ventana principal es $\{0,\ldots,t\}$ y el horizonte futuro es $(t,L_i]$; los antecedentes preinicio se construyen separadamente.
\begin{align}
\mathcal E(t)&=\{i:r_i\text{ conocida},\ r_i\le t,\ (u_i\text{ ausente o }u_i>t),\ L_i>t\},\label{corr:elegibilidad}\\
N(t)&=|\mathcal E(t)|,\quad Y_i(t)=\mathbf 1\{t<u_i\le L_i\},\label{corr:evento}\\
E(t)&=\sum_{i\in\mathcal E(t)}Y_i(t),\qquad \pi(t)=E(t)/N(t).\label{corr:prevalencia}
\end{align}
La función $\mathbf 1$ vale uno cuando se cumple su condición y cero en otro caso; en particular, una fecha ausente no genera evento. Las barras $|\cdot|$ representan el número de elementos de un conjunto. La clase negativa significa ausencia de retiro registrado dentro del horizonte, no éxito académico ni permanencia acreditada. Los retiros del día del corte ya ocurrieron y quedan excluidos. El horizonte disminuye con $t$ y varía entre presentaciones; la comparación mantiene reglas, no una misma duración de seguimiento.

Sean $c_{id}$ los clics totales del día $d$ y $A_i(t)=\{d\in[0,t]:c_{id}>0\}$. El volumen, los días activos, la proporción activa y la intensidad se definen como
\begin{equation}
V_i(t)=\sum_{d=0}^t c_{id},\quad k_i(t)=|A_i(t)|,\quad q_i(t)=\frac{k_i(t)}{n_t},\quad m_i(t)=\frac{V_i(t)}{k_i(t)}\quad(k_i(t)>0).\label{corr:actividad}
\end{equation}
La recencia es $t-\max A_i(t)$ y su versión relativa divide por $n_t$; ambas permanecen ausentes cuando no hay actividad. El CV de intensidad activa es la desviación estándar muestral de los clics en $A_i(t)$ dividida por su media; requiere $k_i(t)\ge2$. El CV de calendario conserva los ceros. Para abreviar, con $n=n_t$, $k=k_i(t)$ y $q=k/n$,
\begin{equation}
CV_{cal}^{2}=\frac{n}{n-1}\left[\frac{1-q}{q}+\frac{k-1}{kq}CV_{act}^{2}\right],\qquad k\ge2.\label{corr:identidadcv}
\end{equation}
La identidad se obtiene al descomponer la suma de cuadrados de los días activos como $(k-1)s_{act}^{2}+k m^{2}$ y usar la media de calendario $qm$. El primer término recoge la inactividad y el segundo la dispersión de intensidad; solo con intensidad constante se reduce a una función de $q$. Ningún CV se presenta como evidencia independiente de la frecuencia por el solo hecho de tener otro nombre.

El sumando 1 de la tendencia permite cocientes finitos con un bloque nulo. Se trata de un suavizado: intercambiar los bloques invierte exactamente el signo, pero escalar los conteos no conserva necesariamente el valor. Ambos bloques nulos se representan como no observables. La tendencia de siete días requiere $t\ge13$ y la de catorce $t\ge27$; 14 y 28 son los primeros cortes elegidos que cumplen esas condiciones, no los primeros matemáticamente posibles.

\section{Selección de indicadores y diferencias respecto del anteproyecto}
El conteo \texttt{n\_registros\_vle} mide filas originales por inscripción en $[0,t]$, sin identificar sesiones. Su granularidad y sus repeticiones no están explicadas por la fuente. Se conserva para auditoría y se retira del conjunto predictivo principal. Esta decisión evita atribuir a una frecuencia de registro un significado educativo que no ha sido verificado; el VIF documentado aporta una razón adicional de redundancia, pero no es por sí solo una regla universal de exclusión.

La diversidad de recursos y tipos de actividad no se construye en esta versión. El conjunto se delimita a volumen, continuidad, recencia, variación temporal y participación evaluativa, conservando el diseño de indicadores examinado y añadiendo la comparación entre ambos CV. Esta delimitación no demuestra falta de utilidad de diversidad: su evaluación requeriría integrar el catálogo de recursos y considerar oportunidades diferentes entre módulos. La familia se mantiene en el marco como posibilidad derivable, con esta exclusión explícita de la implementación actual.

La actividad A3.1 del anteproyecto interpreta la fecha como retiro voluntario y propone explorar abandono implícito. Los archivos permiten ubicar la baja pero no demostrar su motivo; por ello, se adopta el retiro registrado futuro y se mantiene la inactividad como indicador complementario. La predicción de inactividad en un periodo futuro sería otra tarea, no necesariamente circular; no se adopta como segunda etiqueta en esta versión. A2.5 contempla puntajes, que se conservan solo para auditoría porque falta su fecha de publicación. Estas diferencias y la restricción de población al corte deben ratificarse académicamente; la autorización de trabajo no constituye un acta institucional.

La rejilla se adoptó antes de comparar modelos y conserva hitos de una, dos, cuatro, seis y ocho semanas. Las presentaciones duran entre 234 y 269 días; el corte 56 cae dentro del primer cuarto. La computabilidad y el calendario describen la pertinencia de la rejilla, pero no demuestran que sea óptima ni que se haya seleccionado sin conocimiento previo del desenlace. Los datos de calendario publicados permiten examinar la disponibilidad académica, presente ya al día 14.
'''


def append(stem,text):
    p=DEST/f'{stem}_contenido.tex'
    p.write_text(p.read_text(encoding='utf-8')+'\n'+text,encoding='utf-8')


def ampliar_informes():
    append('01_exploracion',r'\section{Distribución temporal del retiro}'+
           '\nLa figura presenta las 10\\,072 inscripciones con fecha de retiro de toda la fuente. Los 2\\,678 retiros preinicio no son eventos futuros de las ventanas examinadas; este denominador no debe mezclarse con la población filtrada por matrícula.\n'+
           fig('01_fechas_retiro','Distribución de fechas de retiro; líneas en el inicio y en los cortes 7, 14, 28, 42 y 56.','corr:histograma'))
    flows=data('02_flujos').rename(columns={'corte':'Corte','etapa':'Etapa','inscripciones':'Inscripciones','personas':'Personas','excluidas':'Excluidas'})
    symbols=pd.DataFrame([
        ('i','Inscripción: persona, módulo y presentación'),('d, t','Día relativo al inicio y corte de predicción'),
        ('n_t','Número de días observados: t+1'),('r_i, u_i, L_i','Matrícula, retiro y final de presentación'),
        ('c_id, A_i(t)','Clics diarios y conjunto de días activos'),('V_i, k_i, q_i, m_i','Volumen, días activos, proporción activa e intensidad'),
        ('N(t), E(t), pi(t)','Inscripciones elegibles, eventos futuros y prevalencia'),
        ('Y_i(t)','Evento binario posterior al corte y hasta el final'),
        ('p(x), tau','Probabilidad condicional y umbral de clasificación'),
        ('phi_j','Contribución de Shapley en una escala y referencia fijadas')],columns=['Símbolo en las ecuaciones','Significado'])
    symbol_table=tab(symbols,'Guía de símbolos; los índices de modelos se definen localmente en su formulación.','corr:simbolos',[.27,.67])
    math_symbols=[r'i',r'd,t',r'n_t',r'r_i,u_i,L_i',r'c_{id},A_i(t)',r'V_i,k_i,q_i,m_i',r'N(t),E(t),\pi(t)',r'Y_i(t)',r'p(\mathbf{x}),\tau',r'\phi_j']
    from generar_informes import esc
    for plain,math in zip(symbols.iloc[:,0],math_symbols):
        symbol_table=symbol_table.replace('\n'+esc(plain)+' &','\n$'+math+'$ &')
    formal=FORMAL.replace('\\begin{align}',symbol_table+'\\begin{align}',1)
    b=formal+r'\section{Cascadas completas de elegibilidad}'+'\n'
    b+='La Tabla~\\ref{corr:flujos} publica cada filtro y sus denominadores. Las exclusiones son secuenciales, no categorías superpuestas. Después del filtro de matrícula quedan 2\\,643 retiros preinicio; los 35 restantes de la fuente completa ya fueron excluidos por matrícula.\n'
    b+=tab(flows,'Flujo secuencial en cada corte; las exclusiones corresponden a la etapa indicada.','corr:flujos',[.07,.34,.20,.18,.15])
    b+=r'\section{Disponibilidad y calendario}'+'\nEl primer vencimiento continuo varía entre los días 12 y 61 según la presentación. En el corte 7 hay entregas anticipadas aunque no haya vencimientos. La falta de oportunidad no equivale a incumplimiento.\n'
    b+=fig('02_calendario_evaluaciones','Primer vencimiento no Exam por módulo y presentación.','corr:calendario')
    b+=fig('02_disponibilidad_indicadores','Observabilidad de cada indicador; porcentaje de inscripciones elegibles en cada corte.','corr:observabilidad')
    dic=data('02_diccionario');dic=dic.loc[dic.rol.eq('predictor_candidato')|dic.variable.eq('n_registros_vle')]
    dic=dic[['variable','definicion','dominio']].rename(columns={'variable':'Variable','definicion':'Definición','dominio':'Dominio y ausencia'})
    b+=r'\section{Diccionario reconciliado de indicadores}'+'\nSe documentan 26 candidatos, incluidos ambos CV; no se han seleccionado variables mediante desempeño predictivo. El conteo de filas aparece únicamente como auditoría. Los identificadores, el contexto y los desenlaces permanecen separados.\n'
    b+=tab(dic,'Diccionario de candidatos y conteo de filas de auditoría; nombres idénticos al código.','corr:diccionario',[.29,.43,.22])
    append('02_ingenieria',b)
    b=r'\section{Resultados ampliados de las variables de contexto}'+'\n'
    b+='Las categorías se analizan en las mismas poblaciones de cada corte. La Tabla~\\ref{corr:niveles} publica conteos y tasas por nivel; la categoría No disponible preserva los faltantes de IMD. Los resultados no se interpretan como efectos causales ni como una evaluación exhaustiva de equidad.\n'
    numeric=data('03_contexto_numerico')[['corte','variable','observados','faltantes','mediana','q25','q75','efecto']].copy()
    numeric['variable']=numeric.variable.map({'studied_credits':'Créditos','num_of_prev_attempts':'Intentos previos'})
    numeric['intervalo']=numeric.apply(lambda r:f'{number(r.q25)}--{number(r.q75)}',axis=1)
    numeric=numeric[['corte','variable','observados','faltantes','mediana','intervalo','efecto']]
    numeric.columns=['Corte','Variable','Observados','Ausentes','Mediana','Q25--Q75','Efecto']
    b+=tab(numeric,'Distribución y asociación de créditos e intentos previos; efecto biserial por rangos.','corr:numericos',[.08,.19,.14,.12,.12,.15,.12],digits=3)
    b+='Los créditos representan la carga registrada y los intentos previos describen antecedentes de inscripción. Sus asociaciones no permiten distinguir mecanismos educativos ni efectos de modificar la carga. Se mantienen como contexto condicionado, sin incorporarlos automáticamente al conjunto de predictores conductuales.\n'
    levels=data('03_niveles');levels=levels.loc[levels.variable.isin(['region','disability','age_band','imd_band'])]
    # Una fila por nivel; publicar n y retiros por los cinco cortes sin esconder denominadores.
    lev=levels[['variable','nivel','corte','n','retiros']].copy()
    lev['celda']=lev.apply(lambda r:f'{number(r.retiros)}/{number(r.n)} ({number(100*r.retiros/r.n,1)}%)',axis=1)
    wide=lev.pivot(index=['variable','nivel'],columns='corte',values='celda').reset_index()
    wide['variable']=wide.variable.map({'region':'Región','disability':'Discapacidad','age_band':'Edad','imd_band':'IMD'})
    wide['Nivel']=wide.variable+' / '+wide.nivel.astype(str);wide=wide[['Nivel',7,14,28,42,56]];wide.columns=['Nivel','7','14','28','42','56']
    b+=tab(wide,'Retiros futuros / inscripciones elegibles (porcentaje) por nivel y corte.','corr:niveles',[.25,.15,.15,.15,.15,.15])
    b+=r'\section{VIF publicado y decisión sobre el conteo de filas}'+'\n'
    vif=data('03_vif');w=vif.pivot(index='corte',columns='variable',values='VIF').reset_index()
    w['n']=vif.groupby('corte')['n'].first().to_numpy();w=w[['corte','n','total_clics','proporcion_dias_activos','n_registros_vle','n_evaluaciones_entregadas']]
    w.columns=['Corte','n','Clics','Proporción activa','Filas VLE','Entregas']
    b+=tab(w,'VIF con intercepto en la especificación de auditoría de cuatro indicadores.','corr:vif',[.09,.18,.16,.19,.16,.16],digits=3)
    b+='El mayor VIF corresponde al conteo de filas en cada corte y llega a 10,929 al día 28. Se conserva esta especificación como diagnóstico de la decisión de exclusión; no es el conjunto predictivo final. La redundancia y la procedencia no resuelta del conteo se consideran conjuntamente, sin imponer un umbral universal para todos los modelos.\n'
    b+=r'\section{Sensibilidad de variabilidad y componentes principales}'+'\n'
    cv=data('03_comparacion_cv')[['corte','observados_calendario','observados_activos','rho_calendario_q_mismos','rho_activo_q']]
    cv.columns=['Corte','CV calendario observable','CV activo observable','Rho calendario','Rho activo']
    b+=tab(cv,'Correlación con proporción activa en los mismos casos con al menos dos días activos.','corr:cv',[.10,.24,.23,.19,.18],digits=3)
    b+='El CV activo separa mejor la dispersión de intensidad de la frecuencia en estos datos, a costa de una menor observabilidad. No se identifica independencia estadística ni ganancia predictiva. El CV de calendario combina ambos componentes y no se descarta retrospectivamente como cálculo erróneo.\n'
    effects=data('03_efectos');active=effects.loc[effects.variable.eq('cv_intensidad_activa')]
    early=active.loc[active.corte.isin([7,14])]
    if ((early.IC95_inferior<0)&(early.IC95_superior>0)).all():
        b+='En los cortes 7 y 14, los intervalos puntuales del CV activo incluyen cero y no respaldan una dirección clara. Esta diferencia respecto del CV de calendario muestra que cambiar la definición modifica la interpretación del indicador; no prueba ausencia de utilidad conjunta en un clasificador.\n'
    pca=data('03_sensibilidad_pca');wide=pca.pivot(index=['corte','n'],columns='especificacion',values='varianza_2_pct').reset_index()
    wide=wide[['corte','n','original_mismos_casos','sin_volumen','intensidad_activa']];wide.columns=['Corte','n común','Original (5)','Sin volumen (4)','CV activo (4)']
    b+=tab(wide,'Varianza porcentual de dos componentes; comparación descriptiva sobre la misma población.','corr:pcasens',[.10,.19,.23,.23,.19])
    b+='La especificación original incluye logaritmos de volumen e intensidad, proporción activa, recencia relativa y CV de calendario. La segunda retira volumen; la tercera sustituye además el CV por su versión activa. Todas se ajustan separadamente por corte y se estandarizan. Cambiar el número y significado de las variables cambia el total de varianza: un porcentaje mayor no acredita una representación superior ni explica mayor proporción del abandono.\n'
    b+=r'\section{Sensibilidad de asociaciones a los duplicados exactos}'+'\n'
    dup=data('03_sensibilidad_duplicados_efectos');d=dup.pivot(index='variable',columns='corte',values='diferencia').reset_index()
    names={'total_clics':'Clics','proporcion_dias_activos':'Proporción activa','recencia_relativa':'Recencia','coef_variacion_clics':'CV calendario','cv_intensidad_activa':'CV activo','log_ratio_7d':'Tendencia 7','log_ratio_14d':'Tendencia 14'}
    d['variable']=d.variable.map(names);d.columns=['Indicador','7','14','28','42','56']
    b+=tab(d,'Cambio del efecto biserial al retirar exactos: alternativa menos fuente original.','corr:duplicadosefectos',[.28,.13,.13,.13,.13,.13],digits=4)
    b+='La alternativa elimina repeticiones en todas las columnas de la fuente antes de agregar; conserva población y evento. La actividad original sigue siendo el análisis principal. Estas diferencias cuantifican sensibilidad descriptiva, no identifican cuál registro es verdadero ni prueban robustez de un modelo aún no entrenado.\n'
    stability=data('03_estabilidad_resumen');s=stability.groupby('corte').agg(comparaciones=('variable','size'),max_cambio=('cambio_max_frente_5000','max'),dentro=('dentro_tolerancia','sum')).reset_index()
    s.columns=['Corte','Indicadores','Cambio máximo','Dentro de 0,005']
    b+=r'\section{Estabilidad de los intervalos por remuestreo}'+'\n'
    b+=tab(s,'Cambio máximo de extremos entre 2.000 y 5.000 remuestreos; comparación numérica, no contraste de hipótesis.','corr:bootstrap',[.14,.25,.29,.26],digits=4)
    b+='Se compararon los primeros 500 y 2\\,000 remuestreos con los 5\\,000 de la misma secuencia reproducible. Se fijó una tolerancia descriptiva de 0,005 unidades del efecto para comparar extremos. Las secuencias son anidadas: este diagnóstico no demuestra convergencia con semillas independientes ni elimina error Monte Carlo. Los intervalos publicados utilizan 5\\,000 remuestreos y permanecen puntuales y exploratorios.\n'
    append('03_estadistica',b)
    # La síntesis cierra también el informe individual, después de las ampliaciones.
    p=DEST/'03_estadistica_contenido.tex'
    content=p.read_text(encoding='utf-8')
    start=content.index(r'\section{Conclusiones y continuidad}')
    stop=content.index(r'\section{Resultados ampliados',start)
    content=content[:start]+content[stop:]+'\n'+content[start:stop]
    p.write_text(content,encoding='utf-8')
