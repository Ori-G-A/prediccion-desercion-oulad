"""Verifica búsquedas completas y selecciona por AP interna, sin leer prueba."""
import argparse
import importlib.metadata
import json
import os
import sys
from pathlib import Path

for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[variable] = '2'
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from entrenamiento_oulad import TrainingData, KEY, ORDER, require, sha, save_json


def consolidate(root, sources, output, audit_only=False):
    loader = TrainingData(root)
    origins = {}
    evidence = {}
    for source in sources:
        contract_path = source / 'contrato.json'
        contract = json.loads(contract_path.read_text(encoding='utf-8'))
        require(contract['modo'] == 'completo', 'No se admite una comprobación reducida')
        require(contract['configuracion_sha256'] == sha(loader.folder / 'configuracion.json'), 'Configuración incompatible')
        require(contract['manifiesto_sha256'] == sha(loader.folder / 'personas.csv'), 'Partición incompatible')
        require(contract['cortes'] == loader.config['cortes'], 'Cortes incompletos')
        packages = ['numpy', 'pandas', 'scikit-learn', 'pyarrow', 'joblib']
        if 'xgboost' in contract['modelos']:
            packages.append('xgboost')
        if 'lightgbm' in contract['modelos']:
            packages.append('lightgbm')
        if 'tabnet' in contract['modelos']:
            packages += ['torch', 'pytorch-tabnet']
        for package in packages:
            require(contract['entorno'][package] == importlib.metadata.version(package), f'Entorno requiere revisión: {package}')
        allowed_code = [root / 'src/entrenamiento_oulad.py', root / 'reportes/entrenamiento_2026_10_19/codigo_inicial/entrenamiento_oulad.py']
        require(contract['codigo_sha256'] in [sha(p) for p in allowed_code], 'Código no revisado')
        evidence[str(contract_path.relative_to(root))] = sha(contract_path)
        for name in contract['modelos']:
            require(name not in origins, 'Familia duplicada entre ejecuciones')
            origins[name] = source
    require(set(origins) == set(ORDER), 'Faltan familias completas')
    selected = []
    for cut in loader.config['cortes']:
        expected = loader.load(cut, 'ajuste')
        for name in ORDER:
            folder = origins[name] / f'corte_{cut:02d}' / name
            if audit_only:
                summary = folder/'seleccion.json'
                if not summary.exists() or not json.loads(summary.read_text(encoding='utf-8'))['busqueda_completa']:
                    continue
            candidates = []
            for index, params in enumerate(loader.config['configuraciones'][name]):
                aps = []
                for fold in range(5):
                    marker = folder / f'config_{index:02d}_fold_{fold}.json'
                    require(marker.exists(), f'Búsqueda incompleta: {marker}')
                    row = json.loads(marker.read_text(encoding='utf-8'))
                    require(row['estado'] == 'correcto', f'Pliegue inválido: {marker}')
                    require((row['modelo'], row['corte'], row['configuracion'], row['pliegue'], row['parametros']) == (name, cut, index, fold, params), 'Identidad o parámetros incompatibles')
                    pred_path = marker.with_suffix('.parquet')
                    require(sha(pred_path) == row['predicciones_sha256'], 'Predicciones alteradas')
                    pred = pd.read_parquet(pred_path).sort_values(KEY).reset_index(drop=True)
                    valid = expected.loc[expected.pliegue_interno.eq(fold)].sort_values(KEY).reset_index(drop=True)
                    require(pred[KEY + ['retiro_futuro']].equals(valid[KEY + ['retiro_futuro']]), 'Cobertura, etiquetas o pliegue incorrectos')
                    p = pred.probabilidad.to_numpy()
                    require(np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all(), 'Probabilidades inválidas')
                    ap = float(average_precision_score(pred.retiro_futuro, p))
                    require(abs(ap - row['ap']) < 1e-12, 'AP no reproducible')
                    aps.append(ap)
                    evidence[str(marker.relative_to(root))] = sha(marker)
                    evidence[str(pred_path.relative_to(root))] = sha(pred_path)
                candidates.append({'configuracion': index, 'ap_media': float(np.mean(aps))})
            best = min(candidates, key=lambda c: (-round(c['ap_media'], 6), c['configuracion']))
            saved_selection = json.loads((folder/'seleccion.json').read_text(encoding='utf-8'))
            require(saved_selection['mejor_configuracion']['configuracion'] == best['configuracion'], 'Selección guardada no reproducible')
            selected.append({'corte': cut, 'modelo': name, **best, 'carpeta': str(folder.relative_to(root)), 'candidatos': candidates})
    if audit_only:
        save_json(output, {'estado':'auditoria_de_familias_disponibles', 'familias_cortes_verificados':selected,
                          'evidencias_sha256':evidence, 'prueba_final_leida':False,
                          'seleccion_global_realizada':False, 'lecturas':loader.read_log})
        return selected
    principals = {}
    for cut in loader.config['cortes']:
        winner = min([s for s in selected if s['corte'] == cut], key=lambda s: (-round(s['ap_media'], 6), ORDER.index(s['modelo'])))
        principals[str(cut)] = winner['modelo']
    save_json(output, {'estado': 'seleccion_completa', 'principales': principals, 'seleccion_por_familia': selected, 'evidencias_sha256': evidence, 'criterio': 'AP media interna; empate a seis decimales, orden preestablecido', 'prueba_final_leida': False, 'lecturas': loader.read_log})
    return selected


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--fuentes', type=Path, nargs='+', required=True)
    parser.add_argument('--salida', type=Path, required=True)
    parser.add_argument('--auditar-disponibles', action='store_true', help='Solo verifica familias-corte ya terminadas; no selecciona ganador global')
    args = parser.parse_args()
    consolidate(args.root.resolve(), [p.resolve() for p in args.fuentes], args.salida, args.auditar_disponibles)
