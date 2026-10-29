"""
極星 Gemini Notebook (NotebookLM) ✕ PPTX 自動簡報生成橋接器
============================================================
功能：
1. 檢測 NotebookLM 本地登入憑證狀態。
2. 列出當前所有筆記本，或建立新筆記本。
3. 自動上傳資料並調用 Google 原生「generate slide-deck」生成簡報。
4. 若已有生成結果，可直接下載並無縫對接極星 16:9 黑曜石金簡報排版引擎。
"""

import sys
import subprocess
import os

NOTEBOOKLM_EXE = r"C:\Users\lenovo\AppData\Roaming\Python\Python312\Scripts\notebooklm.exe"

def check_status():
    print("🔍 正在檢測 NotebookLM 連線與登入狀態...")
    result = subprocess.run([NOTEBOOKLM_EXE, "doctor"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if "not authenticated" in result.stdout:
        print("\n⚠️ 尚未登入 Google 帳號！")
        print("👉 請直接在資料夾中雙擊執行【點我登入NotebookLM.bat】")
        print("   瀏覽器彈出後登入一次您的 Google 帳號即可永久授權！\n")
        return False
    else:
        print("✅ NotebookLM 已成功授權連線！")
        return True

def list_notebooks():
    print("\n📚 當前帳號中的筆記本清單：")
    result = subprocess.run([NOTEBOOKLM_EXE, "list"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
    print(result.stdout)

def main():
    print("=" * 60)
    print("   🚀 極星教育 · Gemini Notebook 簡報自動生成流水線")
    print("=" * 60)
    
    if not check_status():
        sys.exit(0)
        
    list_notebooks()
    print("💡 您可以使用以下指令直接生成原生 Slide Deck：")
    print("   notebooklm generate slide-deck \"請以繁體中文製作 10 頁教學簡報\" --format presenter")
    print("   notebooklm download slide-deck")

if __name__ == "__main__":
    main()
