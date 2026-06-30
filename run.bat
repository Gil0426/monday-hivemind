@echo off
setlocal

:: Resolve script directory so this works from anywhere
set DIR=%~dp0
cd /d "%DIR%"

:: Load .env if present
if exist .env (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
        if not "%%A"=="" if not "%%A:~0,1%"=="#" set "%%A=%%B"
    )
)

:: Guard: API key must be set
if "%ANTHROPIC_API_KEY%"=="" (
    echo Error: ANTHROPIC_API_KEY is not set.
    echo Copy .env.example to .env and add your key.
    exit /b 1
)

:: Activate venv if present
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

python -m manager.manager %*
