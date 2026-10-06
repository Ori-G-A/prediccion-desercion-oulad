"""Figuras para impresión en el cuerpo de la tesis, desde tablas ya calculadas.

No estima modelos ni contrastes. Comprueba los datos contra las tablas LaTeX.
"""
from pathlib import Path
import hashlib
import json
import re
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import Normalize
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.estilo_visual import apply_style, BLUE, ACCENT, INK, MUTED, GRAY, GRID, PALE, SEQUENTIAL, sequential_text, line_style
from graficar_contexto import verify, label, entero, porcentaje, VARIABLES

SOURCE = ROOT/'reportes/correcciones_2026_09_10/tablas'
OUTPUT = ROOT/'Plantilla_ProyAplicado/figuras_contexto'
REPORT = ROOT/'reportes/figuras_cuerpo_2026_10_04'
CUTS = [7, 14, 28, 42, 56]
NAMES = {'age_band':'Edad', 'disability':'Discapacidad registrada', 'imd_band':'Privación del área (IMD)', 'region':'Región',
         'code_module':'Módulo', 'code_presentation':'Presentación', 'gender':'Género', 'highest_education':'Educación previa'}


def decimal(x, places=1):
    return f'{x:.{places}f}'.replace('.', ',')


def save(fig, stem):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for artist in fig.findobj(matplotlib.text.Text):
        if not artist.get_visible() or not artist.get_text():
            continue
        bounds = artist.get_window_extent(renderer)
        assert bounds.x0 >= -1 and bounds.y0 >= -1 and bounds.x1 <= fig.bbox.width+1 and bounds.y1 <= fig.bbox.height+1, (stem, artist.get_text())
    for ext in ['pdf','png','svg']:
        fig.savefig(OUTPUT/f'{stem}.{ext}',dpi=180)
    plt.close(fig)


def bars(data, variable):
    d=data[(data.corte==28)&(data.variable==variable)].copy()
    if variable=='region':
        d=d.sort_values('tasa_pct',ascending=False,kind='stable')
    if variable=='age_band':
        d=d.set_index('nivel').loc[['0-35','35-55','55<=']].reset_index()
    if variable=='disability':
        d=d.set_index('nivel').loc[['N','Y']].reset_index()
    n, events=int(d.n.sum()), int(d.retiros.sum())
    reference=100*events/n
    height=max(2.25,1.35+.29*len(d))
    fig=plt.figure(figsize=(6.8,height))
    ax=fig.add_axes([.40,.52/height,.54,(height-1.15)/height])
    y=np.arange(len(d))
    focus=np.zeros(len(d),dtype=bool)
    if variable=='age_band': focus=d.nivel.eq('55<=').to_numpy()
    elif variable=='disability': focus=d.nivel.eq('Y').to_numpy()
    elif variable=='region': focus[[0,-1]]=True
    colors=[ACCENT if f else BLUE for f in focus]
    if variable=='imd_band': colors=[GRAY if v=='No disponible' else BLUE for v in d.nivel]
    plotted=ax.barh(y,d.tasa_pct,color=colors,height=.53)
    assert np.array_equal([p.get_width() for p in plotted],d.tasa_pct.to_numpy())
    names=[]
    for row in d.itertuples():
        text=label(variable,row.nivel).replace('\n',' ').replace(' Region','')
        if variable=='disability': text=text.replace(' registrada','\nregistrada')
        names.append(f'{text} (n = {entero(row.n)})')
    ax.set_yticks(y,names,fontsize=9)
    ax.tick_params(axis='y',length=0,pad=9)
    ax.set_ylim(len(d)-.4,-.6); ax.set_xlim(0,35)
    ax.set_xticks([0,10,20,30],['0 %','10 %','20 %','30 %'],fontsize=9)
    ax.grid(axis='x',color=GRID); ax.set_axisbelow(True)
    ax.axvline(reference,color=MUTED,lw=.9,ls=(0,(3,3)))
    ax.text(reference,1.025,f'Total: {porcentaje(reference)}',transform=ax.get_xaxis_transform(),ha='center',fontsize=8,color=MUTED)
    for row_y, rate in zip(y,d.tasa_pct):
        ax.text(rate+.4,row_y,porcentaje(rate),va='center',fontsize=9,color=INK,zorder=4,
                bbox={'facecolor':'white','edgecolor':'none','pad':.4})
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.text(.015,.97,f'{NAMES[variable]} · corte 28',va='top',color=BLUE,weight='bold',fontsize=11)
    fig.text(.40,.045,'Retiro posterior al corte, dentro de cada categoría',fontsize=9,color=MUTED)
    return fig


def matrix(data, variables):
    entries=[]
    for variable in variables:
        entries.append(('heading',NAMES[variable],None))
        d=data[data.variable.eq(variable)]
        levels=d.nivel.drop_duplicates().tolist()
        if variable=='region': levels=sorted(levels)
        pivot=d.pivot(index='nivel',columns='corte',values='tasa_pct').loc[levels,CUTS]
        for level in levels:
            name=label(variable,level).replace('\n',' ').replace(' Region','')
            entries.append(('data',name,pivot.loc[level].to_numpy()))
    total=data[data.variable.eq('age_band')].groupby('corte')[['n','retiros']].sum().loc[CUTS]
    entries.append(('total','Total del corte',(100*total.retiros/total.n).to_numpy()))
    count=len(entries)
    height=1.38+count*.255
    fig=plt.figure(figsize=(6.8,height))
    ax=fig.add_axes([.41,.58/height,.57,(height-1.34)/height])
    ax.set(xlim=(-.5,4.5),ylim=(count-.4,-.6)); ax.axis('off')
    for j,cut in enumerate(CUTS):
        ax.text(j,-1.18,f'Día {cut}',ha='center',fontsize=9,weight='bold',clip_on=False)
        ax.text(j,-.70,f'n = {entero(total.loc[cut,"n"])}',ha='center',fontsize=7.4,color=MUTED,clip_on=False)
    for i,(kind,name,values) in enumerate(entries):
        ax.text(-.66,i,name,ha='right',va='center',fontsize=8.6,color=BLUE if kind=='heading' else INK,weight='bold' if kind!='data' else 'normal',clip_on=False)
        if values is None: continue
        for j,value in enumerate(values):
            fill=PALE if kind=='total' else SEQUENTIAL(value/40)
            ax.add_patch(Rectangle((j-.47,i-.42),.94,.84,facecolor=fill,edgecolor='none'))
            ax.text(j,i,porcentaje(value),ha='center',va='center',fontsize=8.7,color=INK if kind=='total' else sequential_text(value,40),weight='bold' if kind=='total' else 'normal')
    cax=fig.add_axes([.46,.26/height,.46,.07/height])
    cb=fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(0,40),cmap=SEQUENTIAL),cax=cax,orientation='horizontal',ticks=[0,20,40])
    cb.ax.set_xticklabels(['0 %','20 %','40 %'],fontsize=8); cb.ax.tick_params(length=0,pad=1); cb.outline.set_visible(False)
    fig.text(.015,.985,'Retiro futuro por categoría y corte',va='top',fontsize=11,color=BLUE,weight='bold')
    return fig


def verify_table_rows(frame, source, mapping, columns):
    for key, name in mapping.items():
        lines=[line for line in source.splitlines() if line.startswith(name+' &')]
        assert len(lines)==1,name
        printed=[float(x.replace(',','.')) for x in re.findall(r'-?\d+,\d+',lines[0])]
        if isinstance(columns,str):
            values=frame[frame.variable.eq(key)].set_index('corte').loc[CUTS,columns].to_numpy()
        else:
            values=frame[frame.corte.eq(key)][columns].to_numpy().ravel()
        assert np.allclose(values,printed[-len(values):],atol=.00050001,rtol=0),(key,values,printed)


def association(data):
    order=['code_module','code_presentation','disability','highest_education','imd_band','gender','region','age_band']
    mat=data.pivot(index='variable',columns='corte',values='V_cramer').loc[order,CUTS].to_numpy()
    fig,ax=plt.subplots(figsize=(6.8,3.5))
    fig.subplots_adjust(left=.27,right=.97,top=.80,bottom=.25)
    im=ax.imshow(mat,cmap=SEQUENTIAL,vmin=0,vmax=.20,aspect='auto')
    ax.set_yticks(range(8),[NAMES[x] for x in order],fontsize=9)
    ax.set_xticks(range(5),[f'Día {x}' for x in CUTS],fontsize=9)
    ax.tick_params(length=0); ax.xaxis.tick_top()
    for spine in ax.spines.values(): spine.set_visible(False)
    for (i,j),value in np.ndenumerate(mat):
        ax.text(j,i,decimal(value,3),ha='center',va='center',fontsize=9,color=sequential_text(value,.20))
    cax=fig.add_axes([.40,.13,.47,.026])
    cb=fig.colorbar(im,cax=cax,orientation='horizontal',ticks=[0,.1,.2]); cb.ax.set_xticklabels(['0,00','0,10','0,20'],fontsize=8)
    cb.ax.tick_params(length=0); cb.outline.set_visible(False)
    fig.text(.015,.96,'Asociación descriptiva con el retiro futuro',fontsize=11,color=BLUE,weight='bold',va='top')
    fig.text(.40,.015,'V de Cramér · escala mostrada de 0,00 a 0,20',fontsize=8.5,color=MUTED)
    return fig


def cv_relationship(data):
    fig,ax=plt.subplots(figsize=(6.8,3.5))
    fig.subplots_adjust(left=.12,right=.96,top=.78,bottom=.20)
    for i,(column,name) in enumerate([('rho_calendario_q_mismos','CV de calendario'),('rho_activo_q','CV entre días activos')]):
        ax.plot(data.corte,data[column],label=name,**line_style(i))
        for x,y in zip(data.corte,data[column]):
            ax.annotate(decimal(y,3),(x,y),xytext=(0,9),textcoords='offset points',ha='center',fontsize=8.5,color=INK)
    ax.set(xlim=(4,59),ylim=(-1.08,.38),xlabel='Día del corte',ylabel='Correlación de Spearman')
    ax.set_xticks(CUTS); ax.set_yticks([-1,-.5,0],['-1,0','-0,5','0,0'])
    ax.axhline(0,color=GRAY,lw=.8,ls='--'); ax.grid(axis='y'); ax.set_axisbelow(True)
    ax.legend(loc='upper center',bbox_to_anchor=(.5,1.25),ncol=2,fontsize=9)
    fig.text(.015,.97,'Relación de cada CV con la proporción de días activos',fontsize=11,color=BLUE,weight='bold',va='top')
    return fig


def main():
    apply_style(10); OUTPUT.mkdir(parents=True,exist_ok=True); REPORT.mkdir(parents=True,exist_ok=True)
    sources=[SOURCE/n for n in ['03_niveles.csv','03_categoricas.csv','03_comparacion_cv.csv']]
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    levels=pd.read_csv(sources[0],keep_default_na=False)
    checks=verify(levels,(ROOT/'Plantilla_ProyAplicado/anexos.tex').read_text(encoding='utf-8'))
    exported=[]
    for variable in VARIABLES:
        stem=f'contexto_{variable}_28'; save(bars(levels,variable),stem); exported.append(stem)
    for variables,stem in [(VARIABLES[:3],'contexto_cortes'),(['region'],'contexto_region_cortes')]:
        save(matrix(levels,variables),stem); exported.append(stem)
    cramer=pd.read_csv(sources[1]); cv=pd.read_csv(sources[2])
    table_names={k:('Discapacidad' if k=='disability' else 'Privación (IMD)' if k=='imd_band' else v) for k,v in NAMES.items()}
    verify_table_rows(cramer,(ROOT/'Plantilla_ProyAplicado/desarrollo1.tex').read_text(encoding='utf-8'),table_names,'V_cramer')
    cv_table=(ROOT/'Plantilla_ProyAplicado/desarrollo2.tex').read_text(encoding='utf-8').split(r'\label{corr:cv}')[1].split(r'\end{longtable}')[0]
    verify_table_rows(cv,cv_table,{cut:str(cut) for cut in CUTS},['rho_calendario_q_mismos','rho_activo_q'])
    save(association(cramer),'asociaciones_contexto'); exported.append('asociaciones_contexto')
    save(cv_relationship(cv),'relacion_cv_actividad'); exported.append('relacion_cv_actividad')
    assert before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    checks.update({'fecha':'2026-10-04','figuras':exported,'sha256_fuentes':before,'celdas_cramer_cotejadas':40,
                   'correlaciones_cv_cotejadas':10,'tablas_analiticas_modificadas':False,'ejecucion_analitica_completa':False,
                   'tamano_diseno_pulgadas':6.8,'textos_dentro_del_lienzo':True})
    (REPORT/'verificacion_figuras.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(checks,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
