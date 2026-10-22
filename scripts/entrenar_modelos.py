"""Ejecuta comprobación o búsqueda completa; nunca evalúa prueba final."""
import argparse
import os
from pathlib import Path
import sys

# Límites antes de importar las bibliotecas numéricas.
for variable in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[variable] = '2'
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from entrenamiento_oulad import run_training, MODULES


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--salida', type=Path, required=True, help='Carpeta exclusiva para este contrato')
    parser.add_argument('--modelos', nargs='+', choices=list(MODULES), default=list(MODULES))
    parser.add_argument('--cortes', nargs='+', type=int, default=[7, 14, 28, 42, 56])
    parser.add_argument('--modo', choices=['comprobacion', 'completo'], default='comprobacion')
    parser.add_argument('--finalizar-familias', action='store_true')
    args = parser.parse_args()
    run_training(args.root, args.salida, args.modelos, args.cortes, args.modo, args.finalizar_familias)


if __name__ == '__main__':
    main()
