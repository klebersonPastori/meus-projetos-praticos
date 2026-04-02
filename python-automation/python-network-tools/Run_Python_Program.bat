@echo off
:: AutoEver - Ferramentas de Rede
:: Coloque este .bat na mesma pasta do python-network-tools.py

set PYTHON_EXE=C:\Python314\pythonw.exe
set SCRIPT_PATH=%~dp0python-network-tools.py

if not exist "%SCRIPT_PATH%" (
    echo [ERRO] Script nao encontrado: %SCRIPT_PATH%
    pause
    exit /b 1
)

:: Inicia o GUI e fecha este CMD imediatamente
start "" "%PYTHON_EXE%" "%SCRIPT_PATH%"
exit
