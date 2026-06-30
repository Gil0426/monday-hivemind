@echo off
setlocal
:: Launch the hivemind remote server + cloudflared tunnel.
:: Double-click this, or run it from a terminal. Leave the window open.
set DIR=%~dp0
cd /d "%DIR%"

if not exist .venv\Scripts\python.exe (
    echo Error: .venv not found. Rebuild it with Windows Python first.
    pause
    exit /b 1
)

.venv\Scripts\python.exe serve_remote.py
pause
