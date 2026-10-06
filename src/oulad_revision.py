"""Utilidades compartidas de la revisión OULAD; no modifica las fuentes CSV."""
from pathlib import Path
import hashlib
import json
import os
import platform
import importlib.metadata

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

KEY = ['id_student', 'code_module', 'code_presentation']
COURSE = ['code_module', 'code_presentation']
VERSION = 'correcciones_2026_09_10'


def root():
    candidate = Path(os.environ.get('OULAD_ROOT', Path.cwd())).resolve()
    for p in [candidate, *candidate.parents]:
        if (p / 'data' / 'raw' / 'studentInfo.csv').exists():
            return p
    raise FileNotFoundError('Defina OULAD_ROOT con la raíz que contiene data/raw.')


ROOT = root()
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'reportes' / VERSION
PROCESSED = ROOT / 'data' / 'processed' / VERSION
for folder in [OUT / 'tablas', OUT / 'figuras', PROCESSED]:
    folder.mkdir(parents=True, exist_ok=True)


def save_json(name, value):
    def convert(x):
        if isinstance(x, np.generic):
            return x.item()
        if isinstance(x, Path):
            return str(x)
        raise TypeError(type(x).__name__)
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2,
                                     default=convert, allow_nan=False), encoding='utf-8')


def table(name, frame):
    frame.to_csv(OUT / 'tablas' / (name + '.csv'), index=False, encoding='utf-8-sig')
    print(name)
    print(frame.to_string(index=False, max_rows=40))
    return frame


def figure(name):
    plt.tight_layout()
    for ext in ['png', 'pdf']:
        plt.savefig(OUT / 'figuras' / f'{name}.{ext}', dpi=150, bbox_inches='tight')
    plt.show()
    plt.close('all')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def load(name):
    dtypes = {'code_module': 'category', 'code_presentation': 'category'}
    if name == 'studentVle':
        dtypes.update(id_student='int32', id_site='int32', date='int32', sum_click='int64')
    return pd.read_csv(RAW / (name + '.csv'), dtype=dtypes)


def environment():
    packages = ['pandas', 'numpy', 'scipy', 'matplotlib', 'scikit-learn', 'pyarrow']
    return {'python': platform.python_version(),
            'packages': {p: importlib.metadata.version(p) for p in packages}}


def keyset(frame, keys):
    return set(frame[keys].itertuples(index=False, name=None))


try:
    from .estilo_visual import apply_style, BLUE, ACCENT, GRAY
except ImportError:
    from estilo_visual import apply_style, BLUE, ACCENT, GRAY
apply_style()
ORANGE = ACCENT  # Alias conservado para código previo; la paleta vigente usa un acento azul verdoso.


def weighted_rank_effect(values, target, weights):
    """P(X1>X0)-P(X1<X0); los empates reciben peso 1/2 en U."""
    levels, idx = np.unique(values, return_inverse=True)
    a = np.bincount(idx, weights=weights * (target == 1), minlength=len(levels))
    b = np.bincount(idx, weights=weights * (target == 0), minlength=len(levels))
    if a.sum() == 0 or b.sum() == 0:
        return np.nan
    u = np.sum(a * (np.cumsum(b) - .5 * b))
    return 2 * u / (a.sum() * b.sum()) - 1


def cluster_effect_ci(frame, variable, repetitions=5000, seed=20260908, return_draws=False):
    """Bootstrap de personas: conserva juntas todas sus inscripciones observadas.

    Estimando: efecto marginal por inscripción con variable observada, condicionado
    a las presentaciones incluidas. No cubre variabilidad entre instituciones.
    """
    ids, clusters = np.unique(frame.id_student.to_numpy(), return_inverse=True)
    valid = frame[variable].notna().to_numpy()
    x = frame.loc[valid, variable].to_numpy(dtype=float)
    y = frame.loc[valid, 'retiro_futuro'].to_numpy(dtype=int)
    c = clusters[valid]
    # Precalcular categorías ordenadas evita ordenar dentro de cada remuestra.
    levels, bins = np.unique(x, return_inverse=True)
    def effect(w):
        a = np.bincount(bins, weights=w * (y == 1), minlength=len(levels))
        b = np.bincount(bins, weights=w * (y == 0), minlength=len(levels))
        if min(a.sum(), b.sum()) == 0:
            return np.nan
        return 2 * np.dot(a, np.cumsum(b) - .5 * b) / (a.sum() * b.sum()) - 1
    observed = effect(np.ones(len(x)))
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(repetitions):
        multiplicity = np.bincount(rng.integers(0, len(ids), len(ids)), minlength=len(ids))
        draws.append(effect(multiplicity[c]))
    finite = np.asarray(draws)[np.isfinite(draws)]
    low, high = np.quantile(finite, [.025, .975])
    result = (observed, low, high, len(finite))
    return (*result, np.asarray(draws)) if return_draws else result
