"""Enriquece la comunicación local desde salidas guardadas, sin ajustar modelos."""
import json
import hashlib
import sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from graficar_contexto import verify
P = ROOT / 'prototipo'
S = ROOT / 'reportes/continuacion_modelado_2026_10_20'
KEY = ['id_student', 'code_module', 'code_presentation']

def main():
    data = json.loads((P/'datos.js').read_text(encoding='utf-8').removeprefix('const DATA = ').rstrip(';'))
    labels = ['Clics acumulados','Días con actividad','Proporción de días con actividad','Promedio de clics por día activo','Variabilidad de clics en todos los días','Variabilidad de clics en días activos','Días desde la última interacción','Recencia relativa','Semanas completas con actividad','Proporción de semanas completas con actividad','Clics antes del inicio','Clics en los últimos 7 días','Clics en los 7 días anteriores','Cambio de actividad entre semanas','Cambio de actividad entre quincenas','Sin actividad acumulada','Sin actividad en los últimos 7 días','Sin actividad en los últimos 14 días','Sin actividad en los últimos 28 días','Evaluaciones entregadas','Entregas anteriores al inicio','Evaluaciones con vencimiento hasta el corte','Evaluaciones vencidas entregadas hasta el corte','Proporción entregada de evaluaciones vencidas','Sin evaluaciones con vencimiento hasta el corte','Sin entregas acumuladas']
    package = json.loads((S/'paquete_evaluacion.json').read_text())
    predictors = package['predictores']
    assert len(labels) == len(predictors)
    data['labels'].update(dict(zip(predictors, labels)))
    sources = {}
    for cut in package['cortes']:
        folder = S/f'shap/resultados/corte_{cut:02d}'
        c = pd.read_parquet(folder/'contribuciones.parquet')
        x = pd.read_parquet(folder/'inscripciones_explicadas.parquet')
        values = c[KEY].merge(x, on=KEY, validate='one_to_one', how='left')
        assert len(values) == len(data['casos'][str(cut)]) == 100
        for i, row in values.iterrows():
            case = data['casos'][str(cut)][i]
            assert abs(case['probabilidad'] - c.iloc[i].probabilidad) < 1e-12
            case['valores'] = {k: None if pd.isna(row[k]) else float(row[k]) for k in predictors}
        sources[str(cut)] = hashlib.sha256((folder/'inscripciones_explicadas.parquet').read_bytes()).hexdigest()
    path = ROOT/'reportes/correcciones_2026_09_10/tablas/03_niveles.csv'
    eda = pd.read_csv(path, keep_default_na=False)
    eda = eda[eda.variable.isin(['age_band','disability','imd_band','region'])]
    checks = verify(eda, (ROOT/'Plantilla_ProyAplicado/anexos.tex').read_text(encoding='utf-8'))
    data['exploracion'] = eda.to_dict('records')
    text = 'const DATA = '+json.dumps(data, ensure_ascii=False, allow_nan=False)+';'
    assert 'id_student' not in text
    (P/'datos.js').write_text(text, encoding='utf-8')
    html = (P/'index.html').read_text(encoding='utf-8')
    for name in ['datos.js','app.js']:
        html = html.replace(f'<script src="{name}"></script>', '<script>'+ (P/name).read_text(encoding='utf-8')+'</script>')
    (P/'OULAD.html').write_text(html, encoding='utf-8')
    checks.update(valores_individuales=500, fuentes_valores_sha256=sources, fuente_eda_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), modelos_reajustados=False)
    (P/'verificacion_datos.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(checks, ensure_ascii=False))

if __name__ == '__main__':
    main()
