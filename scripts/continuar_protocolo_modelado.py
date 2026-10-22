"""Continúa el protocolo autorizado con comprobaciones entre etapas y registro persistente."""
import argparse
import ctypes
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reportes/continuacion_modelado_2026_10_20'
PYTHON = ROOT / '.venv/Scripts/python.exe'


def record(stage, status, **details):
    item = {'fecha': datetime.now(ZoneInfo('America/Bogota')).isoformat(),
            'etapa': stage, 'estado': status, 'pid_supervisor': os.getpid(), **details}
    with (REPORT/'continuacion.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(item, ensure_ascii=False)+'\n')
    (REPORT/'continuacion_actual.json').write_text(json.dumps(item, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(item, ensure_ascii=False), flush=True)


def progress():
    try:
        subprocess.run([str(PYTHON), 'scripts/registrar_progreso_modelado.py'], cwd=ROOT, check=True,
                       stdout=subprocess.DEVNULL, timeout=30)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, OSError) as error:
        # El contador es informativo: su fallo no invalida ni detiene el entrenador.
        # Las verificaciones obligatorias de cada etapa conservan su fallo estricto.
        record(1, 'incidencia_registro_progreso', causa=f'{type(error).__name__}: {error}',
               accion='Continuar supervisión y reintentar el contador en el siguiente ciclo.')


def checkpoint(completed, **updates):
    path = ROOT/'estado_ejecucion_modelos.json'
    state = json.loads(path.read_text(encoding='utf-8'))
    state.update(updates)
    state['ultima_etapa_completa_global'] = completed
    state['proxima_etapa'] = completed+1
    state['actualizado'] = datetime.now(ZoneInfo('America/Bogota')).isoformat()
    state['continuacion_persistente'] = 'reportes/continuacion_modelado_2026_10_20/continuacion_actual.json'
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def run(stage, script, *args):
    record(stage, 'ejecutando', script=script)
    with (REPORT/'continuacion_calculos.log').open('a', encoding='utf-8') as log:
        process = subprocess.Popen([str(PYTHON), '-u', script, *map(str, args)], cwd=ROOT,
                                   stdout=log, stderr=subprocess.STDOUT)
        while process.poll() is None:
            try:
                process.wait(timeout=60)
            except subprocess.TimeoutExpired:
                if stage == 1:
                    progress()
        if stage == 1:
            progress()
        if process.returncode:
            raise RuntimeError(f'{script}: código de salida {process.returncode}; consultar continuacion_calculos.log')
    record(stage, 'comando_terminado', script=script)


def wait_existing(pid):
    # Un handle identifica el proceso original aunque Windows reutilice después su PID.
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    handle = kernel.OpenProcess(0x00100000, False, pid)
    if not handle:
        if ctypes.get_last_error() == 87:  # Ya terminó.
            return
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        record(1, 'esperando_entrenador_existente', pid_entrenador=pid)
        while True:
            result = kernel.WaitForSingleObject(handle, 60000)
            progress()
            if result == 0:
                break
            if result != 258:
                raise ctypes.WinError(ctypes.get_last_error())
    finally:
        kernel.CloseHandle(handle)


def main(pid):
    lock = REPORT/'continuacion.lock'
    with lock.open('x', encoding='utf-8') as stream:
        stream.write(str(os.getpid()))
    stage = 1
    try:
        if (ROOT/'reportes/continuacion_modelado_2026_10_19/primera_apertura_prueba.json').exists():
            raise RuntimeError('La prueba ya fue abierta; revisar paquete y resultados antes de cualquier continuación')
        if pid:
            wait_existing(pid)
        # Reanudar es idempotente bajo el contrato: verifica y conserva pliegues guardados.
        run(1, 'scripts/entrenar_modelos.py', '--salida', 'reportes/entrenamiento_2026_10_19/restantes_completo',
            '--modelos', 'random_forest', 'xgboost', 'lightgbm', 'tabnet', '--modo', 'completo', '--finalizar-familias')
        stage = 2
        selection = REPORT/'seleccion_validacion.json'
        package = REPORT/'paquete_evaluacion.json'
        if package.exists():
            raise RuntimeError('Ya existe paquete: revisar su estado antes de repetir la continuación integral')
        run(2, 'scripts/consolidar_validacion.py', '--fuentes', 'reportes/entrenamiento_2026_10_19/logistica',
            'reportes/entrenamiento_2026_10_19/restantes_completo', '--salida', selection)
        checkpoint(2, busquedas={name:'completa_cinco_cortes_verificada' for name in
                   ['regresion_logistica','random_forest','xgboost','lightgbm','tabnet']},
                   seleccion_entre_familias=str(selection.relative_to(ROOT)))
        stage = 4
        run(4, 'scripts/verificar_metricas_evaluacion.py')
        run(4, 'scripts/verificar_evaluador_reservado.py')
        run(4, 'scripts/verificar_shap.py')
        run(4, 'scripts/congelar_evaluacion.py', '--seleccion', selection,
            '--diseno-shap', REPORT/'shap/diseno.json', '--verificacion',
            ROOT/'reportes/continuacion_modelado_2026_10_19/pruebas_evaluador.json', '--salida', package)
        checkpoint(4, calibracion_umbral='25_candidatos_verificados', paquete_evaluacion=str(package.relative_to(ROOT)))
        stage = 5
        evaluation = REPORT/'evaluacion'
        run(5, 'scripts/evaluar_prueba.py', '--paquete', package, '--salida', evaluation)
        checkpoint(5, prueba_final='evaluacion_completa_paquete_congelado', evaluacion=str(evaluation.relative_to(ROOT)))
        stage = 6
        run(6, 'scripts/explicar_modelos.py', '--paquete', package, '--evaluacion', evaluation,
            '--salida', REPORT/'shap/resultados')
        checkpoint(5, shap='calculado_pendiente_revision_e_integracion_academica')
        record(6, 'calculos_terminados_integracion_academica_pendiente',
               pendiente='Revisar resultados, integrar capítulos y verificar composición; no declarar cierre integral.')
    except Exception as error:
        record(stage, 'bloqueo_tecnico', causa=f'{type(error).__name__}: {error}',
               regla='Conservar evidencias y corregir causa; no alterar selección por resultados de prueba.')
        raise
    finally:
        lock.unlink(missing_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--esperar-pid', type=int)
    args = parser.parse_args()
    main(args.esperar_pid)
