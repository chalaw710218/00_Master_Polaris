@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command "python '%~dp0tools\harvest_yihua_catalog.py' --limit 15"
pause
