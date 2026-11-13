import os
import sys
import time
import json
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

sys.path.append("scripts")
from threads_publisher import publish_thread, THREADS_ACCESS_TOKEN, API_BASE

image_file = Path("images/meow_friday_midnight_box.jpg")
draft_file = Path("scripts/test_friday_midnight_draft.txt")
SESSION_PATH = Path("scripts/threads_session.json")
PROOF_DIR = Path("scripts/screenshots")
PROOF_DIR.mkdir(parents=True, exist_ok=True)

with open(draft_file, "r", encoding="utf-8") as f:
    post_text = f.read().strip()

first_reply = "（輕手輕腳幫紙箱蓋上一角小毛毯，並把走廊的夜燈調暗）辛苦了一整個星期，今天就別再給自己任何壓力了。明天不用上班，把手機放遠一點，好好睡個沒有負擔的大飽覺吧。晚安～🍵🌙"

print("==================================================")
print("🚀 [週五午夜深夜專場 · 喵編隨筆記發布啟動]")
print(f"🖼️ 配圖確認: {image_file.name} (大小: {image_file.stat().st_size} bytes)")
print("==================================================")

post_id = publish_thread(text=post_text, image=str(image_file), topic_tag="週五晚上")
if not post_id:
    print("❌ 發布失敗！")
    sys.exit(1)

print(f"🎉 帶圖貼文發布成功！Post ID: {post_id}")

permalink = None
try:
    info_url = f"{API_BASE}/{post_id}?fields=id,permalink&access_token={THREADS_ACCESS_TOKEN}"
    r = requests.get(info_url, timeout=10).json()
    permalink = r.get("permalink")
    print(f"🔗 官方短代碼永久網址: {permalink}")
except Exception as e:
    print(f"⚠️ 獲取 permalink 失敗: {e}")

if not permalink:
    permalink = f"https://www.threads.net/@hellotaitung/post/{post_id}"

# 發布首回覆
print("\n💬 發布作者公開首回覆橋接（搶佔黃金 60 分鐘推薦池）...")
time.sleep(3)
reply_id = publish_thread(text=first_reply, reply_to_id=post_id)
print(f"✅ 首回覆發布成功！Reply ID: {reply_id}")

# 登記圖片防重複
reg_path = Path("data/published_image_registry.json")
if reg_path.exists():
    try:
        reg = json.load(open(reg_path, encoding='utf-8'))
        reg["published_images"].append({
            "filename": image_file.name,
            "post_id": post_id,
            "published_at": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        json.dump(reg, open(reg_path, "w", encoding='utf-8'), ensure_ascii=False, indent=2)
        print("📝 圖片已登錄至 published_image_registry.json 防重複資產庫！")
    except Exception as e:
        print(f"⚠️ 註冊圖片失敗: {e}")

# 前台截圖存證
proof_path = PROOF_DIR / f"walk_v3_{post_id}_meow_friday_midnight_verified.png"
if permalink and SESSION_PATH.exists():
    print("\n📸 前往前台進行實景存證截圖...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                storage_state=str(SESSION_PATH),
                viewport={"width": 1280, "height": 900},
                locale="zh-TW"
            )
            page = context.new_page()
            page.goto(permalink, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(4000)
            page.screenshot(path=str(proof_path))
            browser.close()
            print(f"✅ 實景截圖存證完成: {proof_path}")
    except Exception as e:
        print(f"⚠️ 截圖異常 (貼文仍已成功發布): {e}")

out_result = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "persona": "Meow Editor (店貓喵編) ✕ Shadow (生活管家 影)",
    "theme": "週五午夜大赦免 ✕ 週末不用設鬧鐘 ✕ 喵編睡翻紙箱",
    "post_id": post_id,
    "permalink": permalink,
    "reply_id": reply_id,
    "proof_screenshot": str(proof_path) if proof_path.exists() else ""
}
with open("scripts/latest_friday_midnight_result.json", "w", encoding="utf-8") as f:
    json.dump(out_result, f, ensure_ascii=False, indent=2)

print("\n🎉 週五午夜深夜陪伴專場漫遊隨筆記閉環大成功！")
