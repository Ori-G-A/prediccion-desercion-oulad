"""Esquema vectorial resumido, con claves cotejadas con cabeceras CSV locales."""
from pathlib import Path
import csv
import json
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.estilo_visual import apply_style, BLUE, ACCENT, INK, MUTED, PALE


def main():
    apply_style()
    required = {
        'courses': ['code_module', 'code_presentation', 'module_presentation_length'],
        'studentInfo': ['code_module', 'code_presentation', 'id_student', 'final_result'],
        'studentRegistration': ['code_module', 'code_presentation', 'id_student', 'date_registration', 'date_unregistration'],
        'assessments': ['code_module', 'code_presentation', 'id_assessment', 'assessment_type', 'date', 'weight'],
        'studentAssessment': ['id_assessment', 'id_student', 'date_submitted', 'score'],
        'vle': ['code_module', 'code_presentation', 'id_site', 'activity_type'],
        'studentVle': ['code_module', 'code_presentation', 'id_student', 'id_site', 'date', 'sum_click'],
    }
    for table, columns in required.items():
        with (ROOT / 'data/raw' / f'{table}.csv').open(encoding='utf-8-sig', newline='') as f:
            header = next(csv.reader(f))
        assert set(columns) <= set(header), (table, header)

    fig, ax = plt.subplots(figsize=(10, 8.4))
    fig.subplots_adjust(left=.01, right=.99, top=.99, bottom=.01)
    ax.set(xlim=(0, 10), ylim=(0, 8.4)); ax.axis('off')
    def box(x, y, w, h, title, lines, accent=False):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=.06',
                                   linewidth=1,edgecolor=BLUE,facecolor=PALE,zorder=3))
        ax.text(x+.15,y+h-.23,title,fontsize=11,weight='bold',color=BLUE,va='top',zorder=4)
        ax.plot([x+.15,x+w-.15],[y+h-.57]*2,color=ACCENT if accent else BLUE,lw=2,zorder=4)
        ax.text(x+.15,y+h-.76,'\n'.join(lines),fontsize=9.5,color=INK,va='top',linespacing=1.55,zorder=4)
    def link(points, label=None, at=None):
        ax.plot(*zip(*points), color=BLUE, linewidth=1.2,zorder=1)
        if label:
            ax.text(*at,label,fontsize=9,color=BLUE,ha='center',va='center',
                    bbox=dict(facecolor='white',edgecolor='none',pad=2),zorder=5)
    box(3.5,6.8,3,1.4,'courses',['Módulo y presentación (MP)','Duración del curso'])
    box(.1,4.2,2.8,1.75,'assessments',['MP + id_assessment','Tipo, fecha y peso','de cada evaluación'])
    box(3.5,4.2,3,1.75,'studentInfo',['Inscripción (I)','Características del estudiante','y resultado final'],True)
    box(7.1,4.2,2.8,1.75,'vle',['MP + id_site','Tipo de recurso','y semanas previstas'])
    box(.1,1.7,2.8,1.8,'studentAssessment',['id_student + id_assessment','Fecha de entrega','y calificación'])
    box(3.5,1.7,3,1.8,'studentRegistration',['Inscripción (I)','Fechas de registro','y retiro'])
    box(7.1,1.7,2.8,1.8,'studentVle',['I + id_site','Día de interacción','y número de clics'])
    link([(5,6.8),(5,5.95)],'MP',(5,6.35))
    link([(3.5,7.3),(1.5,7.3),(1.5,5.95)],'MP',(1.5,6.35))
    link([(6.5,7.3),(8.5,7.3),(8.5,5.95)],'MP',(8.5,6.35))
    link([(1.5,4.2),(1.5,3.5)],'id_assessment',(1.5,3.85))
    link([(5,4.2),(5,3.5)],'I',(5,3.85))
    link([(8.5,4.2),(8.5,3.5)],'MP + id_site',(8.5,3.85))
    # Vínculos hacia la inscripción. En las entregas, MP se obtiene de assessments.
    link([(2.9,2.6),(3.2,2.6),(3.2,4.55),(3.5,4.55)],'I*',(3.2,3.15))
    link([(7.1,2.6),(6.8,2.6),(6.8,4.55),(6.5,4.55)],'I',(6.8,3.15))
    ax.text(.1,1.16,'MP = code_module + code_presentation',fontsize=10,color=BLUE,weight='bold')
    ax.text(.1,.87,'I = id_student + code_module + code_presentation',fontsize=10,color=BLUE,weight='bold')
    ax.text(.1,.5,'* Para vincular las entregas con la inscripción, módulo y presentación se recuperan desde assessments.',fontsize=9,color=MUTED)
    ax.text(.1,.18,'Las líneas indican campos de enlace. Se muestran contenidos resumidos, sin detallar todos los campos.',fontsize=9,color=MUTED)
    output = ROOT/'Plantilla_ProyAplicado/figuras_editoriales/esquema_oulad'
    output.parent.mkdir(parents=True,exist_ok=True)
    for ext in ['pdf','svg','png']:
        fig.savefig(output.with_suffix('.'+ext),dpi=180)
    plt.close(fig)
    report=ROOT/'reportes/identidad_visual_2026_09_30/verificacion_esquema.json'
    report.write_text(json.dumps({'cabeceras_verificadas':required,'imagen_original_conservada':True,
                                 'alcance':'Síntesis de contenidos y campos de enlace; no expresa cardinalidades.'},ensure_ascii=False,indent=2),encoding='utf-8')


if __name__ == '__main__':
    main()
