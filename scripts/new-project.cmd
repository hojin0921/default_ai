@echo off
cd /d "%~dp0.."
python "%~dp0new_project.py" %*
exit /b %ERRORLEVEL%
