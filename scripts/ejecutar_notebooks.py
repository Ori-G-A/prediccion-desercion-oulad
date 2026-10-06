"""Ejecuta celdas Python en orden, en un proceso nuevo por notebook.

No necesita un servidor Jupyter. Captura stdout, stderr, última expresión e imágenes
de matplotlib como salidas ipynb. No admite magias; estos notebooks no las usan.
"""
import ast
import base64
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ['01_carga_exploracion.ipynb', '02_feature_engineering.ipynb',
             '03_analisis_estadistico.ipynb']


def execute(name):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    path = ROOT / name
    nb = json.loads(path.read_text(encoding='utf-8'))
    namespace = {'__name__': '__main__'}
    count = 0
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            cell['outputs'], cell['execution_count'] = [], None
    started = time.time()
    for index, cell in enumerate(nb['cells']):
        if cell['cell_type'] != 'code':
            continue
        count += 1
        cell['execution_count'] = count
        outputs = cell['outputs']
        def show(*args, **kwargs):
            for number in plt.get_fignums():
                buf = io.BytesIO()
                plt.figure(number).savefig(buf, format='png', bbox_inches='tight', dpi=110)
                outputs.append({'output_type': 'display_data', 'metadata': {},
                                'data': {'image/png': base64.b64encode(buf.getvalue()).decode('ascii')}})
        plt.show = show
        stream = io.StringIO()
        print(f'{name}: celda {index + 1}', flush=True)
        try:
            tree = ast.parse(''.join(cell['source']))
            last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
            with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
                exec(compile(tree, f'{name}:celda{index + 1}', 'exec'), namespace)
                if last:
                    result = eval(compile(ast.Expression(last.value), name, 'eval'), namespace)
                    if result is not None:
                        print(result)
        except Exception as error:
            outputs.insert(0, {'output_type': 'stream', 'name': 'stdout', 'text': stream.getvalue()})
            outputs.append({'output_type': 'error', 'ename': type(error).__name__,
                            'evalue': str(error), 'traceback': traceback.format_exc().splitlines()})
            path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
            raise
        if stream.getvalue():
            outputs.insert(0, {'output_type': 'stream', 'name': 'stdout', 'text': stream.getvalue()})
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
    duration = time.time() - started
    logdir = ROOT / 'reportes' / 'correcciones_2026_09_10'
    logdir.mkdir(parents=True, exist_ok=True)
    (logdir / (path.stem + '_ejecucion.json')).write_text(json.dumps({
        'notebook': name, 'celdas_codigo': count, 'segundos': duration,
        'estado': 'completo', 'python': sys.version, 'proceso_limpio': True,
        'ejecutor': 'Python secuencial; no kernel Jupyter',
    }, indent=2), encoding='utf-8')
    print(f'Completado: {name} ({duration:.1f} s)', flush=True)


if __name__ == '__main__':
    os.chdir(ROOT)
    os.environ['OULAD_ROOT'] = str(ROOT)
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) == 3 and sys.argv[1] == '--uno':
        execute(sys.argv[2])
    else:
        for name in NOTEBOOKS:
            subprocess.run([sys.executable, __file__, '--uno', name], cwd=ROOT, check=True)
