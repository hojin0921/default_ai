@echo off
setlocal
cd /d "%~dp0.."
set "PYTHONPATH=%CD%\scripts"
python "%~dp0_gate_cli.py" %*
if errorlevel 1 exit /b %ERRORLEVEL%
exit /b 0
