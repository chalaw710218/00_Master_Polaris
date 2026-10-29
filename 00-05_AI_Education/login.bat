@echo off
chcp 65001 >nul
echo ========================================================
echo  Polaris Gemini Notebook / NotebookLM 備用重新登入入口
echo ========================================================
echo.
python -m notebooklm login
echo.
echo 登入完成！憑證已更新至 ~/.notebooklm/profiles/default/storage_state.json
pause
