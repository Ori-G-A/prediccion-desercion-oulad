"""Revalida la evidencia de avance sin sobrescribir registros históricos."""
from pathlib import Path
import importlib.util
import json
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reportes/entrega_avance_2026_10_06'
sys.path.insert(0, str(ROOT / 'src'))
from ventanas_oulad import PREDICTORS, CONTEXT

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('comprobaciones', ROOT / 'scripts/verificar_multiventana.py')
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)
    def save_current(name, value):
        # La lectura de celdas guardadas no demuestra una nueva ejecución del notebook.
        for item in value:
            item['verificacion'] = item['verificacion'].replace('Ejecución completa:', 'Celdas guardadas con contador y sin error:')
        (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    checks.save_json = save_current
    checks.main()
    dictionary = pd.read_csv(ROOT / 'reportes/correcciones_2026_09_10/tablas/02_diccionario.csv')
    assert set(dictionary.loc[dictionary.rol.eq('predictor_candidato'), 'variable']) == set(PREDICTORS)
    assert len(PREDICTORS) == 26
    assert set(dictionary.loc[dictionary.rol.eq('contexto_condicionado'), 'variable']) == set(CONTEXT)
    populations = []
    for cut in [7, 14, 28, 42, 56]:
        d = pd.read_parquet(ROOT / f'data/processed/correcciones_2026_09_10/dataset_corte_{cut:02}.parquet')
        populations.append({'corte': cut, 'inscripciones': len(d), 'personas': int(d.id_student.nunique()),
                            'retiros_futuros': int(d.retiro_futuro.sum())})
    (OUT / 'cotejo_seleccion_y_poblaciones.json').write_text(json.dumps({
        'fecha': '2026-10-06', 'candidatos': PREDICTORS, 'contexto_condicionado': CONTEXT,
        'diccionario_coincide_con_codigo': True, 'poblaciones': populations,
        'alcance': 'Reejecución de verificaciones independientes; no reejecución integral de notebooks ni entrenamiento.'
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Diccionario, código y poblaciones cotejados.')

if __name__ == '__main__':
    main()
