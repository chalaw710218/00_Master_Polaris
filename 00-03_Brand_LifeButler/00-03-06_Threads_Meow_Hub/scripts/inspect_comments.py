import os
import sys
import json
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = ROOT_DIR / ".secrets.env"

def load_env(env_path):
    if not env_path.exists():
        return {}
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()
    return env_vars

ENV = load_env(ENV_PATH)
TOKEN = ENV.get("THREADS_ACCESS_TOKEN")
API_BASE = "https://graph.threads.net/v1.0"
POST_ID = "18637505857005596"

print(f"🔍 正在查詢貼文 {POST_ID} 的回覆對象與留言內容...")

# 1. 嘗試透過 Meta Threads API 抓取 conversation
try:
    url = f"{API_BASE}/{POST_ID}/conversation?fields=id,text,timestamp,username,permalink&access_token={TOKEN}"
    res = requests.get(url).json()
    print("API 回覆清單:", json.dumps(res, ensure_ascii=False, indent=2))
except Exception as e:
    print("API 查詢異常:", e)

# 2. 透過 Playwright 前台精確截圖並讀取留言內容
SESSION_PATH = Path(__file__).resolve().parent / "threads_session.json"
POST_URL = "https://www.threads.com/@hellotaitung/post/DfEOY2kn06S"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = context.new_page()
    print(f"🌐 前往貼文頁面: {POST_URL}")
    page.goto(POST_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    page.screenshot(path="scripts/screenshots/comment_check_sunnap.png")
    print("📸 已截圖：scripts/screenshots/comment_check_sunnap.png")

    # 提取頁面上的回覆文字
    items = page.locator('div[data-pressable-container="true"], div[dir="auto"]').all_inner_texts()
    print("頁面文字節選:")
    for t in items[:15]:
        if len(t.strip()) > 5:
            print("  -", t.strip().replace("\n", " "))
    browser.close()
