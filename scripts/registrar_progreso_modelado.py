"""Registra progreso observado sin confundir marcadores con validación integral."""
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / 'reportes/entrenamiento_2026_10_19/restantes_completo'
    records = [json.loads(p.read_text(encoding='utf-8')) for p in folder.glob('corte_*/*/config_*_fold_*.json')]
    records = [r for r in records if r['modelo'] != 'referencia']
    progress = {'fecha': datetime.now(ZoneInfo('America/Bogota')).isoformat(), 'previstos': 3000,
                'marcadores': len(records), 'estados': dict(Counter(r['estado'] for r in records)),
                'por_familia': dict(Counter(r['modelo'] for r in records)),
                'segundos_ajustes_terminados': sum(r['segundos'] for r in records),
                'advertencia': 'Conteo de marcadores; el cierre exige verificar predicciones, cobertura y contratos.',
                'prueba_final_abierta': (ROOT / 'reportes/continuacion_modelado_2026_10_19/primera_apertura_prueba.json').exists()}
    destination = ROOT / 'reportes/continuacion_modelado_2026_10_19'
    (destination / 'progreso.json').write_text(json.dumps(progress, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    with (destination / 'historial_progreso.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(progress, ensure_ascii=False)+'\n')
    state_path = ROOT / 'estado_ejecucion_modelos.json'
    state = json.loads(state_path.read_text(encoding='utf-8'))
    state['progreso_observado'] = progress
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(progress, ensure_ascii=False))


if __name__ == '__main__':
    main()
