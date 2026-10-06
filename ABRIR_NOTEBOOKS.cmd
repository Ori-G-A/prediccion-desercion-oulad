@echo off
setlocal
cd /d "%~dp0"
set "OULAD_ROOT=%CD%"
set "JUPYTER_CONFIG_DIR=%CD%\.jupyter\config"
set "JUPYTER_RUNTIME_DIR=%CD%\.jupyter\runtime"
set "IPYTHONDIR=%CD%\.jupyter\ipython"
set "MPLCONFIGDIR=%CD%\.jupyter\matplotlib"
if not exist ".venv\Scripts\python.exe" (
  echo No se encuentra el entorno .venv. Consulte EJECUCION_LOCAL.md.
  pause
  exit /b 1
)
echo Abriendo JupyterLab con el entorno del proyecto.
echo Ejecute los notebooks en orden: 01, 02 y 03.
echo Mantenga esta ventana abierta mientras trabaja.
".venv\Scripts\python.exe" -m jupyterlab --ServerApp.ip=127.0.0.1 --ServerApp.root_dir="%CD%"
if errorlevel 1 pause
endlocal
