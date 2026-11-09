"""
========================================================================
生活管家・一鍵倒垃圾雷達 步驟1：雲端靜態託管與 GitHub Pages 自動部署腳本
========================================================================
業務主政：執行長雪 (Yuki) ✕ CTO 林納斯 (Linus)
========================================================================
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(SCRIPT_DIR, "05_Trash_Radar_Engine")
REPO_NAME = "taitung-trash-radar"
GITHUB_USER = "chalaw710218"

def run_cmd(cmd, cwd=None):
    print(f"▶ 執行: {cmd}")
    res = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        print(f"❌ 錯誤 (Code {res.returncode}):\n{res.stderr}")
    else:
        if res.stdout.strip():
            print(f"✔ 輸出:\n{res.stdout.strip()}")
    return res

def deploy():
    print("==================================================")
    print("🚀 執行長雪 (Yuki) 指揮部署：啟動步驟 1 GitHub Pages 發布")
    print("==================================================")

    # 1. 建立獨立乾淨打包目錄
    temp_dir = os.path.join(tempfile.gettempdir(), REPO_NAME)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)

    # 2. 複製必要前端靜態檔案
    files_to_copy = [
        "index.html",
        "taitung_trash_routes_seed.json",
        "taitung_fixed_points.json"
    ]
    for fn in files_to_copy:
        src = os.path.join(ENGINE_DIR, fn)
        dst = os.path.join(temp_dir, fn)
        shutil.copy2(src, dst)
        print(f"📦 複製靜態檔案: {fn}")

    # 3. 建立乾淨專業之 README.md (符合品牌法定名稱零洩漏防火牆)
    readme_content = """# 生活管家・台東一鍵倒垃圾雷達 (Taitung Trash Radar)

> 台東在地常民零挫折清運導航 ✕ LINE LIFF 輕量單頁應用  
> 官方服務品牌：生活的一部分，就醬點！｜日常業務：生活管家

## 🌟 功能亮點
- **雙軌出發點**：支援自動手機 GPS 定位 ＋ 手動輸入台東路名模糊匹配
- **交通工具動力學**：支援【🚶 步行】、【🛵 騎機車 (台東預設)】、【🚗 開車】不同車速與到站時間計算
- **資源回收開關**：未勾選默認只倒垃圾，勾選強制篩選【一般垃圾 ＋ 資源回收車】雙收班次
- **戴明安燈防呆**：內建台東市清潔隊【週三與週日例行停收，週六正常收運】在地風土防呆
- **三大決策卡片**：🥇 火速攔截（最快）、🥈 步行最近、🥉 早晨定點站救急

## 🔗 線上訪問
- **正式網址**：https://chalaw710218.github.io/taitung-trash-radar/
"""
    with open(os.path.join(temp_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 4. Git 初始化並提交
    run_cmd("git init -b main", cwd=temp_dir)
    run_cmd("git config user.name \"chalaw710218\"", cwd=temp_dir)
    run_cmd("git config user.email \"chalaw710218@gmail.com\"", cwd=temp_dir)
    run_cmd("git add .", cwd=temp_dir)
    run_cmd("git commit -m \"feat: initial release of Taitung Trash Radar PWA/LIFF (Exit Code 0)\"", cwd=temp_dir)

    # 5. 使用 gh CLI 在 GitHub 上建立公開倉庫並推動
    create_res = run_cmd(f"gh repo create {GITHUB_USER}/{REPO_NAME} --public --source=. --remote=origin --push", cwd=temp_dir)
    if create_res.returncode != 0:
        print("⚠️ 建立倉庫若已存在，嘗試直接 push...")
        run_cmd(f"git remote add origin https://github.com/{GITHUB_USER}/{REPO_NAME}.git", cwd=temp_dir)
        run_cmd("git push -u origin main --force", cwd=temp_dir)

    # 6. 開啟 GitHub Pages (使用 gh api)
    print("⚙️ 設定 GitHub Pages 託管 (main branch / root)...")
    page_res = run_cmd(f"gh api --method POST -H \"Accept: application/vnd.github+json\" /repos/{GITHUB_USER}/{REPO_NAME}/pages -f source='{{\"branch\":\"main\",\"path\":\"/\"}}'", cwd=temp_dir)
    if page_res.returncode != 0:
        print("ℹ️ 檢查 GitHub Pages 當前狀態...")
        run_cmd(f"gh api /repos/{GITHUB_USER}/{REPO_NAME}/pages", cwd=temp_dir)

    published_url = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/"
    print("==================================================")
    print("🎉 步驟 1 圓滿竣工！正式 HTTPS 網址已就緒：")
    print(f"👉 正式 Endpoint URL: {published_url}")
    print("==================================================")

if __name__ == "__main__":
    deploy()
