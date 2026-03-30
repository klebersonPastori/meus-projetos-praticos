@echo off
title CSIRT WebSec Phishing Scanner
chcp 65001 > nul
cls

echo.
echo   ============================================================
echo                 CSIRT WebSec Phishing Scanner
echo            Ambiente: Isolado (Virtual Environment)
echo   ============================================================
echo.

cd /d "%~dp0"

:: Verifica Python
set PYTHON_CMD=

for /f "delims=" %%i in ('where python 2^>nul') do (
    if not defined PYTHON_CMD set PYTHON_CMD=python
)

if not defined PYTHON_CMD (
    for /f "delims=" %%i in ('where py 2^>nul') do (
        if not defined PYTHON_CMD set PYTHON_CMD=py
    )
)

if not defined PYTHON_CMD (
    if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
        set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
    )
)

if not defined PYTHON_CMD (
    echo   [ERRO] Python nao encontrado no sistema.
    echo          Instale em: https://www.python.org/downloads/
    echo          Marque "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

echo   [+] Python encontrado: %PYTHON_CMD%
echo.

:: Primeira execucao: cria venv e instala dependencias
if not exist "venv\Scripts\activate.bat" (
    echo   [*] Primeira execucao detectada.
    echo.

    echo   [+] Criando atalho na Area de Trabalho...
    powershell -Command "$wshell = New-Object -ComObject WScript.Shell; $shortcut = $wshell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\CSIRT Web Scanner.lnk'); $shortcut.TargetPath = '%~dpnx0'; $shortcut.WorkingDirectory = '%~dp0'; $shortcut.IconLocation = $env:windir + '\System32\SecurityHealthSystray.exe,0'; $shortcut.Save()" > nul 2>&1
    echo   [!] Atalho criado.
    echo.

    echo   [+] Criando ambiente virtual isolado...
    %PYTHON_CMD% -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo   [ERRO] Falha ao criar ambiente virtual.
        pause
        exit /b 1
    )
    echo   [!] Ambiente virtual criado.
    echo.

    call venv\Scripts\activate.bat

    echo   [+] Instalando python-whois. Aguarde...
    pip install python-whois --disable-pip-version-check --quiet
    if %ERRORLEVEL% NEQ 0 (
        echo   [ERRO] Falha ao instalar python-whois.
        pause
        exit /b 1
    )
    echo   [!] python-whois instalado.
    echo.
    echo   ------------------------------------------------------------
    echo   [*] Ambiente configurado. Iniciando scanner...
    echo   ------------------------------------------------------------
    echo.
) else (
    call venv\Scripts\activate.bat
)

:: A chave do VirusTotal e gerenciada pelo proprio scanner (cli.py).
:: Na primeira execucao ele pede a chave e oferece salvar em venv\.vt_api_key.
:: Nas execucoes seguintes ele carrega automaticamente sem perguntar.
python -m websec_recon.cli %* --html evidencia_phishing.html

set EXIT_CODE=%ERRORLEVEL%
call deactivate

:: Pausa so em caso de erro
if %EXIT_CODE% NEQ 0 (
    echo.
    echo   ------------------------------------------------------------
    echo   [ERRO] Scanner encerrou com erro (codigo %EXIT_CODE%).
    echo          Verifique se todos os arquivos do pacote estao presentes.
    echo   ------------------------------------------------------------
    echo.
    pause
)