"""Figura didáctica reproducible; no utiliza ni modifica observaciones OULAD."""
from pathlib import Path
import json
import math
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from estilo_visual import apply_style, BLUE, MUTED
OUT = ROOT / 'reportes/revision_editorial_2026_09_13/cv_y_lectura'
FIG = ROOT / 'Plantilla_ProyAplicado/figuras_editoriales'
CASES = {
    'A. Actividad diaria constante': [5, 5, 5, 5, 5, 5, 5, 5],
    'B. Días activos alternados': [10, 0, 10, 0, 10, 0, 10, 0],
    'C. Intensidad activa variable': [2, 0, 6, 0, 12, 0, 20, 0],
    'D. Actividad inicial concentrada': [10, 10, 10, 10, 0, 0, 0, 0],
}


def metrics(values):
    x = np.asarray(values, dtype=float)
    active = x[x > 0]
    cal = float(x.std(ddof=1) / x.mean()) if x.mean() > 0 and len(x)>1 else None
    act = float(active.std(ddof=1) / active.mean()) if len(active)>1 else None
    return {'clics': values, 'n':len(x), 'volumen': int(x.sum()), 'dias_activos':len(active),
            'q':len(active)/len(x), 'cv_cal':cal, 'cv_act':act,
            'recencia':int(len(x)-1-np.flatnonzero(x>0)[-1]) if len(active) else None}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(exist_ok=True)
    rows = {name:metrics(x) for name,x in CASES.items()}
    for row in rows.values():
        n,k,q = row['n'],row['dias_activos'],row['q']
        rhs = n/(n-1)*((1-q)/q+(k-1)/(k*q)*row['cv_act']**2)
        assert math.isclose(row['cv_cal']**2,rhs,abs_tol=1e-12)
        assert row['volumen']==40
    a,b,c,d = rows.values()
    assert a['cv_cal']==a['cv_act']==b['cv_act']==0
    assert c['cv_cal']>b['cv_cal'] and c['cv_act']>b['cv_act']
    assert b['cv_cal']==d['cv_cal'] and b['cv_act']==d['cv_act'] and b['recencia']!=d['recencia']
    assert metrics([0]*8)['cv_cal'] is None and metrics([0]*8)['cv_act'] is None
    assert metrics([10]+[0]*7)['cv_act'] is None
    apply_style()
    fig, axes = plt.subplots(2,2,figsize=(7.4,6.8),sharey=True)
    for ax,(name,row) in zip(axes.flat,rows.items()):
        x=np.asarray(row['clics'])
        ax.bar(range(8),x,color=BLUE,width=.68)
        ax.scatter(np.flatnonzero(x==0),np.zeros(sum(x==0)),marker='o',s=15,facecolors='white',edgecolors=MUTED,zorder=3,clip_on=False)
        ax.set_title(name,fontsize=10.5,fontweight='bold',pad=12)
        ax.set_xticks(range(8));ax.set_xlabel('Día relativo al inicio');ax.set_ylim(0,23)
        ax.set_yticks([0,5,10,15,20]);ax.set_ylabel('Clics diarios')
        ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
        ax.spines[['top','right']].set_visible(False)
        fmt=lambda v:f'{v:.3f}'.replace('.',',')
        annotation=(f"{row['dias_activos']}/8 días activos; volumen = 40\n"
                    f"CV calendario = {fmt(row['cv_cal'])}\nCV activo = {fmt(row['cv_act'])}; recencia = {row['recencia']} {'día' if row['recencia']==1 else 'días'}")
        ax.text(0,-.31,annotation,transform=ax.transAxes,va='top',fontsize=9.5,linespacing=1.5)
    fig.subplots_adjust(left=.10,right=.99,top=.94,bottom=.16,hspace=.9,wspace=.32)
    fig.savefig(FIG/'comparacion_cv.pdf',bbox_inches='tight')
    fig.savefig(OUT/'comparacion_cv.png',dpi=160,bbox_inches='tight')
    plt.close(fig)
    result={'alcance':'Ejemplos hipotéticos en 8 días (corte 7), con desviación muestral ddof=1; no resultados OULAD.',
            'casos':rows,'verificaciones':'Identidad de CV, volumen común, invariancia ante permutación y faltantes estructurales comprobados.'}
    (OUT/'ejemplos_cv.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Cuatro ejemplos calculados y verificados; figura vectorial generada.')


if __name__=='__main__':
    main()
