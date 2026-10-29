@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "python '%~dp0tools\login_helper.py'"
pause
