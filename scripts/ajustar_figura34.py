"""Regenera solo la Figura 3.4 desde los cinco conjuntos guardados.

Comprueba las coordenadas de las diez curvas y actualiza la imagen del notebook;
no ejecuta su análisis estadístico completo ni modifica los datos.
"""
from pathlib import Path
import base64
import hashlib
import json
import shutil
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.estilo_visual import apply_style
from src.figuras_oulad import distribuciones_cortes


def main():
    report=ROOT/'reportes/ajuste_figura34_2026_10_05'
    report.mkdir(parents=True,exist_ok=True)
    processed=ROOT/'data/processed/correcciones_2026_09_10'
    paths=[processed/f'dataset_corte_{cut:02}.parquet' for cut in [7,14,28,42,56]]
    paths+=list((ROOT/'reportes/correcciones_2026_09_10/tablas').glob('*.csv'))
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    before={str(p.relative_to(ROOT)):sha(p) for p in paths}
    datasets={cut:pd.read_parquet(processed/f'dataset_corte_{cut:02}.parquet',columns=['proporcion_dias_activos','recencia_relativa']) for cut in [7,14,28,42,56]}
    apply_style(); fig=distribuciones_cortes(datasets); fig.tight_layout()
    for ax,variable in zip(fig.axes,['proporcion_dias_activos','recencia_relativa']):
        assert len(ax.lines)==5 and len(ax.texts)==0
        for line,(cut,frame) in zip(ax.lines,sorted(datasets.items())):
            values=frame[variable].dropna().sort_values().to_numpy()
            assert line.get_linestyle()=='-' and line.get_marker() in [None,'None','']
            assert np.array_equal(line.get_xdata(),values)
            assert np.array_equal(line.get_ydata(),np.arange(1,len(values)+1)/len(values))
    assert len(fig.legends)==1
    assert len({line.get_color() for line in fig.axes[0].lines})==5
    colors={str(cut):line.get_color() for cut,line in zip(sorted(datasets),fig.axes[0].lines)}
    directory=ROOT/'reportes/correcciones_2026_09_10/figuras'
    for ext in ['pdf','png']:
        path=directory/f'03_distribuciones_cortes.{ext}'
        fig.savefig(path,dpi=180,bbox_inches='tight')
        shutil.copy2(path,ROOT/'Plantilla_ProyAplicado/figuras_multiventana'/path.name)
    plt.close(fig)
    notebook_path=ROOT/'03_analisis_estadistico.ipynb'
    nb=json.loads(notebook_path.read_text(encoding='utf-8'))
    original_sources=[c['source'] for c in nb['cells']]
    cells=[c for c in nb['cells'] if c['cell_type']=='code' and "figure('03_distribuciones_cortes')" in ''.join(c['source'])]
    assert len(cells)==1
    outputs=[o for o in cells[0].get('outputs',[]) if 'image/png' in o.get('data',{})]
    assert len(outputs)==1
    png=directory/'03_distribuciones_cortes.png'
    outputs[0]['data']['image/png']=base64.b64encode(png.read_bytes()).decode('ascii')
    cells[0].setdefault('metadata',{})['actualizacion_visual']={'fecha':'2026-10-05','origen':'salidas analíticas guardadas','analisis_repetido':False,'cambio':'Figura 3.4: líneas continuas, sin marcadores ni anotaciones sobre las curvas; leyenda común exterior.'}
    assert original_sources==[c['source'] for c in nb['cells']]
    notebook_path.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    assert before=={str(p.relative_to(ROOT)):sha(p) for p in paths}
    result={'fecha':'2026-10-05','curvas_verificadas':10,'coordenadas_identicas_a_datos_guardados':True,
            'lineas_continuas_sin_marcadores':True,'sin_anotaciones_sobre_curvas':True,'leyendas':1,'colores_por_corte':colors,
            'archivos_analiticos_sin_cambios':len(paths),'codigo_notebook_sin_cambios':True,'ejecucion_analitica_completa':False,
            'sha256_analiticos':before,'sha256_png_notebook':sha(png),'revision_pdf':'pendiente de compilación e inspección'}
    (report/'verificacion.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='sha256_analiticos'},ensure_ascii=False,indent=2))


if __name__=='__main__': main()
