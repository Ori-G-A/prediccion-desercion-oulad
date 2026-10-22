import json
import statistics
import hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
rows=[]
for source in ['logistica','restantes_completo']:
    for path in (ROOT/'reportes/entrenamiento_2026_10_19'/source).glob('corte_*/*/config_*_fold_*.json'):
        row=json.loads(path.read_text(encoding='utf-8'))
        if row['modelo']=='referencia': continue
        row['fuente']=str(path.relative_to(ROOT))
        rows.append(row)
assert len(rows)==3200 and all(r['estado']=='correcto' for r in rows)
assert len({(r['modelo'],r['corte'],r['configuracion'],r['pliegue']) for r in rows})==3200
stats=[]
for name in ['regresion_logistica','random_forest','xgboost','lightgbm','tabnet']:
    group=[r for r in rows if r['modelo']==name]
    times=[r['segundos'] for r in group]
    stats.append(dict(modelo=name,ajustes=len(times),segundos=sum(times),media=statistics.mean(times),
                      mediana=statistics.median(times),minimo=min(times),maximo=max(times),
                      por_corte={str(c):sum(r['segundos'] for r in group if r['corte']==c) for c in [7,14,28,42,56]}))
folder=ROOT/'reportes/continuacion_modelado_2026_10_20'
first=ROOT/'reportes/continuacion_modelado_2026_10_19/primera_apertura_prueba.json'
data={'fecha':datetime.now(ZoneInfo('America/Bogota')).isoformat(),'tiempos':stats,
      'total_segundos':sum(r['segundos'] for r in rows),
      'estado':json.loads((ROOT/'estado_ejecucion_modelos.json').read_text(encoding='utf-8')),
      'operacion':json.loads((folder/'continuacion_actual.json').read_text(encoding='utf-8')),
      'seleccion':json.loads((folder/'seleccion_validacion.json').read_text(encoding='utf-8'))['principales'],
      'primera_apertura':json.loads(first.read_text(encoding='utf-8')) if first.exists() else None,
      'evaluacion_cierre':json.loads((folder/'evaluacion/cierre.json').read_text(encoding='utf-8')) if (folder/'evaluacion/cierre.json').exists() else None,
      'cortes_intervalos':[c for c in [7,14,28,42,56] if (folder/f'evaluacion/corte_{c:02d}/intervalos.json').exists()],
      'cortes_shap':[c for c in [7,14,28,42,56] if (folder/f'shap/resultados/corte_{c:02d}/verificacion.json').exists()]}
closure=data['evaluacion_cierre']
if closure:
    for rel, expected in closure['huellas_salidas'].items():
        assert hashlib.sha256((folder/'evaluacion'/rel).read_bytes()).hexdigest()==expected, rel
    assert closure['paquete_sha256']==hashlib.sha256((folder/'paquete_evaluacion.json').read_bytes()).hexdigest()
data['huellas_evaluacion_verificadas']=len(closure['huellas_salidas']) if closure else 0
(OUT/'evidencia.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'registros_tiempos.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:data[k] for k in ['fecha','tiempos','total_segundos','operacion','cortes_intervalos','cortes_shap']},ensure_ascii=False,indent=2))
