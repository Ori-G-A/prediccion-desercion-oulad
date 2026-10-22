"""Fija referencia y muestreo de explicaciones antes de abrir la prueba."""
import os
import sys
from pathlib import Path

for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[variable] = '2'
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from entrenamiento_oulad import TrainingData, KEY, require, sha, save_json


def main():
    output = ROOT/'reportes/continuacion_modelado_2026_10_20/shap'
    require(not (output/'diseno.json').exists(), 'Diseño existente: conservar y verificar, no sobrescribir')
    loader = TrainingData(ROOT)
    references = {}
    for cut in loader.config['cortes']:
        fit = loader.load(cut, 'ajuste')
        reference = fit.sample(n=min(50, len(fit)), random_state=20261023 + cut)[KEY+loader.predictors]
        path = output/f'referencia_{cut:02d}.parquet'
        path.parent.mkdir(parents=True, exist_ok=True)
        reference.to_parquet(path, index=False)
        references[str(cut)] = {'archivo':str(path.relative_to(ROOT)), 'sha256':sha(path), 'filas':len(reference)}
    save_json(output/'diseno.json', {
        'objeto':'Predictor calibrado principal de cada corte, elegido exclusivamente por validación interna.',
        'escala':'Probabilidad de retiro futuro; enlace identidad. Las contribuciones suman p(x) menos la media en la referencia.',
        'variante':'shap.PermutationExplainer con masker Independent; 20 ciclos completos hacia delante y atrás.',
        'referencia':references,
        'muestreo':'Hasta 100 inscripciones elegibles de prueba por corte; ordenar por claves y sample(random_state=20261024+corte), sin estratificar por desenlace ni puntuación.',
        'dependencia':'Enmascaramiento marginal con filas de ajuste. No estima expectativas condicionales; puede formar combinaciones incompatibles entre indicadores derivados y redistribuir contribuciones entre predictores dependientes. No permite inferencia causal.',
        'n_explicaciones':100, 'ciclos':20, 'semilla':20261025,
        'limite':'Aproximación sobre una muestra; no representa certeza de cada contribución ni importancia causal. No se usa para modificar modelos o predictores.',
        'fuentes':['https://shap.readthedocs.io/en/latest/generated/shap.PermutationExplainer.html',
                   'https://shap.readthedocs.io/en/latest/generated/shap.maskers.Independent.html'],
        'prueba_final_abierta':False})


if __name__ == '__main__':
    main()
