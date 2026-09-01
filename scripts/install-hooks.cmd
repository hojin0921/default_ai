@echo off
cd /d "%~dp0.."
python "%~dp0install_hooks.py" %*
exit /b %ERRORLEVEL%
