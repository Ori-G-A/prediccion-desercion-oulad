"""Comprueba dependencias, datos y un kernel; no ejecuta el análisis completo."""
from pathlib import Path
import importlib.metadata
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ['OULAD_ROOT'] = str(ROOT)
for name, folder in {
    'JUPYTER_CONFIG_DIR': 'config',
    'JUPYTER_RUNTIME_DIR': 'runtime',
    'IPYTHONDIR': 'ipython',
    'MPLCONFIGDIR': 'matplotlib',
}.items():
    path = ROOT / '.jupyter' / folder
    path.mkdir(parents=True, exist_ok=True)
    os.environ[name] = str(path)


def main():
    from jupyter_client import KernelManager
    import pandas as pd

    expected_python = ROOT / '.venv' / 'Scripts' / 'python.exe'
    if Path(sys.executable).resolve() != expected_python.resolve():
        raise RuntimeError('Ejecutar con .venv/Scripts/python.exe')
    versions = {}
    for line in (ROOT / 'requirements-revision.txt').read_text().splitlines():
        if '==' in line and not line.lstrip().startswith('#'):
            name, expected = line.strip().split('==')
            actual = importlib.metadata.version(name)
            if actual != expected:
                raise RuntimeError(f'{name}: se esperaba {expected}, se encontró {actual}')
            versions[name] = actual
    for name in ['jupyterlab', 'ipykernel']:
        versions[name] = importlib.metadata.version(name)
    files = ['courses', 'assessments', 'vle', 'studentInfo',
             'studentRegistration', 'studentAssessment', 'studentVle']
    sources = {}
    for name in files:
        path = ROOT / 'data' / 'raw' / f'{name}.csv'
        sample = pd.read_csv(path, nrows=3)
        sources[name] = {'bytes': path.stat().st_size, 'columnas': list(sample.columns)}

    notebooks = {}
    first_cell = None
    for name in ['01_carga_exploracion.ipynb', '02_feature_engineering.ipynb',
                 '03_analisis_estadistico.ipynb']:
        nb = json.loads((ROOT / 'notebooks' / name).read_text(encoding='utf-8'))
        code = [c for c in nb['cells'] if c['cell_type'] == 'code']
        for i, cell in enumerate(code):
            compile(''.join(cell['source']), f'{name}:code{i}', 'exec')
        notebooks[name] = {'celdas_codigo_sintaxis_valida': len(code)}
        if first_cell is None:
            first_cell = ''.join(code[0]['source'])

    km = KernelManager(kernel_name='python3')
    kc = None
    try:
        km.start_kernel(cwd=str(ROOT / 'notebooks'), env=os.environ.copy())
        kc = km.client()
        kc.start_channels()
        kc.wait_for_ready(timeout=90)
        verification_code = first_cell + '\n' + (
            'from pathlib import Path\n'
            f'assert Path(sys.executable).resolve() == Path({str(expected_python)!r}).resolve()\n'
            'import ventanas_oulad, ampliacion_oulad\n'
            'assert pd.read_csv(ROOT / "data/raw/studentInfo.csv", nrows=3).shape[0] == 3\n'
        )
        reply = kc.execute_interactive(verification_code, timeout=90,
                                       output_hook=lambda message: None)
        if reply['content']['status'] != 'ok':
            raise RuntimeError(reply['content'])
    finally:
        if kc is not None:
            kc.stop_channels()
        if km.has_kernel:
            km.shutdown_kernel(now=True)

    report = {
        'estado': 'correcto',
        'python': sys.version,
        'ejecutable': sys.executable,
        'versiones': versions,
        'datos_lectura_muestra': sources,
        'notebooks': notebooks,
        'kernel_real_y_celda_inicial': 'correcto',
        'analisis_completo_ejecutado': False,
    }
    output = ROOT / 'reportes' / 'entorno_local_2026_09_30'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'verificacion.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Entorno, siete CSV, sintaxis y kernel comprobados. No se ejecutó el análisis completo.')


if __name__ == '__main__':
    main()
