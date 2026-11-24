@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 極星 AI 數位店長 · 子夜零點巡檢自動回覆
echo ========================================================
echo   極星 AI 數位店長 · 子夜零點巡檢與自動回覆啟動中...
echo ========================================================
python "midnight_autopilot.py"
if %errorlevel% neq 0 (
    echo [ERROR] 執行失敗，錯誤代碼：%errorlevel%
    exit /b %errorlevel%
)
echo.
echo 執行完畢！
exit /b 0
