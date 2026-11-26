@echo off
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  py -3 lab.py
) else (
  python lab.py
)
if errorlevel 1 (
  echo Python 3.10 or newer is required. Check errors above.
  pause
  exit /b 1
)
start "" "%~dp0results\report.html"
pause
