"""Ajuste editorial reproducible desde la tabla calculada, sin repetir bootstrap."""
from pathlib import Path
import base64
import hashlib
import json
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'src'))
from src.oulad_revision import OUT, GRAY, figure, save_json
from src.figuras_oulad import efectos_cortes

path=ROOT/'03_analisis_estadistico.ipynb'
notebook=json.loads(path.read_text(encoding='utf-8'))
cell=next(c for c in notebook['cells'] if c['cell_type']=='code' and "table('03_efectos',effects)" in ''.join(c['source']))
table_path=OUT/'tablas/03_efectos.csv'
before=hashlib.sha256(table_path.read_bytes()).hexdigest()
effects=pd.read_csv(table_path)
CUTS=sorted(effects.corte.unique())
efectos_cortes(effects, CUTS)
figure('03_efectos_cortes')
png=base64.b64encode((OUT/'figuras/03_efectos_cortes.png').read_bytes()).decode('ascii')
for output in cell.get('outputs',[]):
    if 'image/png' in output.get('data',{}):output['data']['image/png']=png
path.write_text(json.dumps(notebook,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
assert before==hashlib.sha256(table_path.read_bytes()).hexdigest()
save_json('ajuste_editorial_figura.json',{'cambio':'Leyenda fuera de las curvas; celda gráfica regenerada desde la tabla ejecutada',
          'tabla_sha256_antes_y_despues':before,'recalculo_estadistico':False,
          'ejecucion_completa_previa':'Consultar 03_analisis_estadistico_ejecucion.json; el ajuste posterior solo afecta la figura y su salida guardada.'})
