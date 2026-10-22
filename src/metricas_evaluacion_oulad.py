"""Métricas y remuestreo pareado por personas, sin ajuste de modelos."""
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

from entrenamiento_oulad import require


def metrics(y, p, threshold, weights=None):
    y, p = np.asarray(y), np.asarray(p, dtype=float)
    w = np.ones(len(y)) if weights is None else np.asarray(weights, dtype=float)
    require(len(y) == len(p) == len(w) and len(y) > 0, 'Tamaños inválidos')
    require(np.isin(y, [0, 1]).all(), 'Etiqueta no binaria')
    require(np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all(), 'Probabilidades inválidas')
    require(np.isfinite(w).all() and (w >= 0).all() and w.sum() > 0, 'Pesos inválidos')
    require(np.isfinite(threshold), 'Umbral no finito')
    alert = p > threshold
    tp, fp = w[(y == 1) & alert].sum(), w[(y == 0) & alert].sum()
    fn, tn = w[(y == 1) & ~alert].sum(), w[(y == 0) & ~alert].sum()
    both = tp + fn > 0 and tn + fp > 0
    ratio = lambda a, b: float(a / b) if b else None
    return {
        'ap': float(average_precision_score(y, p, sample_weight=w)) if both else None,
        'roc_auc': float(roc_auc_score(y, p, sample_weight=w)) if both else None,
        'brier': float(np.average((y - p) ** 2, weights=w)),
        'prevalencia': ratio(tp + fn, w.sum()),
        'tn': float(tn), 'fp': float(fp), 'fn': float(fn), 'tp': float(tp),
        'sensibilidad': ratio(tp, tp + fn), 'especificidad': ratio(tn, tn + fp),
        'precision': ratio(tp, tp + fp), 'f1': ratio(2 * tp, 2 * tp + fp + fn),
        'exactitud': ratio(tp + tn, w.sum()), 'proporcion_alertas': ratio(tp + fp, w.sum())}


def person_weights(ids, universe, rng):
    """Una multiplicidad por persona; conserva juntas sus inscripciones."""
    universe = np.asarray(universe)
    require(len(universe) > 0 and len(np.unique(universe)) == len(universe), 'Universo de personas inválido')
    locations = pd.Index(universe).get_indexer(ids)
    require((locations >= 0).all(), 'Persona ajena al universo de remuestreo')
    counts = np.bincount(rng.integers(0, len(universe), len(universe)), minlength=len(universe))
    return counts[locations]


def paired_bootstrap(ids, y, predictions, thresholds, universe, repetitions=2000, seed=20261022):
    """Mismas muestras en todas las familias; diferencias a menos b."""
    names = list(predictions)
    require(set(names) == set(thresholds), 'Faltan umbrales')
    rng = np.random.default_rng(seed)
    records = []
    for replicate in range(repetitions):
        weights = person_weights(ids, universe, rng)
        for name in names:
            values = metrics(y, predictions[name], thresholds[name], weights) if weights.sum() else {}
            records.append({'replica': replicate, 'modelo': name, **values})
    frame = pd.DataFrame(records)
    fields = list(metrics(y, predictions[names[0]], thresholds[names[0]]))
    intervals, comparisons = [], []
    for name in names:
        subset = frame.loc[frame.modelo.eq(name)]
        for field in fields:
            valid = subset[field].dropna()
            bounds = np.percentile(valid, [2.5, 97.5]).tolist() if len(valid) else [None, None]
            intervals.append({'modelo': name, 'metrica': field, 'inferior': bounds[0], 'superior': bounds[1], 'replicas_validas': len(valid), 'replicas_excluidas': repetitions - len(valid)})
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            first = frame.loc[frame.modelo.eq(a)].set_index('replica')
            second = frame.loc[frame.modelo.eq(b)].set_index('replica')
            for field in fields:
                delta = (first[field] - second[field]).dropna()
                bounds = np.percentile(delta, [2.5, 97.5]).tolist() if len(delta) else [None, None]
                comparisons.append({'a': a, 'b': b, 'metrica': field, 'inferior_a_menos_b': bounds[0], 'superior_a_menos_b': bounds[1], 'replicas_validas': len(delta), 'replicas_excluidas': repetitions - len(delta)})
    return frame, intervals, comparisons
