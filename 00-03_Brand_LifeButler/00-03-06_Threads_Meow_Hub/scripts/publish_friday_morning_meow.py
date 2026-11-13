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

draft_file = Path("data/draft_friday_morning_meow.txt")
image_file = Path("images/meow_friday_morning_tgif.jpg")

with open(draft_file, "r", encoding="utf-8") as f:
    post_text = f.read().strip()

first_reply = "（偷偷用肉球推了推熱咖啡）選 2 的朋友別硬撐，小編剛剛已經把今天早上的熱壓吐司跟熱美式送到門口啦喵～個人檔案有生活管家任意門，熱早餐直送門口，吃飽喝足，今天下午四點就可以開始倒數放假了！🥪☕"

print(f"🚀 [喵編週五早晨號] 開始正式推送【帶圖貼文】至 Threads...")
print(f"🖼️ 配圖確認: {image_file.name} (大小: {image_file.stat().st_size} bytes)")

post_id = publish_thread(text=post_text, image=str(image_file), topic_tag="台東生活")
if not post_id:
    print("❌ 發布失敗！")
    sys.exit(1)

print(f"🎉 帶圖貼文發布成功！Post ID: {post_id}")

# 透過 API 獲取準確短網址
permalink = None
try:
    info_url = f"{API_BASE}/{post_id}?fields=id,permalink&access_token={THREADS_ACCESS_TOKEN}"
    r = requests.get(info_url, timeout=10).json()
    permalink = r.get("permalink")
    print(f"🔗 取得官方準確短代碼網址: {permalink}")
except Exception as e:
    print(f"⚠️ 獲取 short permalink 失敗: {e}")

if not permalink:
    permalink = f"https://www.threads.net/@hellotaitung/post/{post_id}"

# 發布首回覆
print("💬 發布首回覆橋接（搶佔黃金 60 分鐘推薦池）...")
time.sleep(2)
reply_id = publish_thread(text=first_reply, reply_to_id=post_id)
print(f"✅ 首回覆發布成功！Reply ID: {reply_id}")

# 登記圖片防重複
reg_path = Path("data/published_image_registry.json")
if reg_path.exists():
    try:
        reg = json.load(open(reg_path, encoding='utf-8'))
        reg["published_images"].append({
            "filename": image_file.name,
            "published_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "post_id": post_id,
            "topic": "喵編週五TGIF早晨熱早餐生活服務篇"
        })
        json.dump(reg, open(reg_path, "w", encoding='utf-8'), ensure_ascii=False, indent=2)
        print("✅ 已成功登記圖片至 published_image_registry.json！")
    except Exception as e:
        print(f"⚠️ 登記圖片異常: {e}")

# Playwright 前台截圖存證
session_path = Path("scripts/threads_session.json")
screenshot_dir = Path("scripts/screenshots")
screenshot_dir.mkdir(parents=True, exist_ok=True)
proof_path = screenshot_dir / f"walk_v3_{post_id}_meow_friday_morning_verified.png"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(session_path),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = context.new_page()
    print(f"📸 前往公開貼文詳情截圖: {permalink}")
    page.goto(permalink, wait_until="domcontentloaded", timeout=25000)
    page.wait_for_timeout(4000)
    page.screenshot(path=str(proof_path))
    print(f"✅ 成功截圖存證: {proof_path}")
    browser.close()

# 輸出最新 walk 結果
result_path = Path("scripts/latest_walk_v3_result.json")
with open(result_path, "w", encoding="utf-8") as f:
    json.dump({
        "post_id": post_id,
        "permalink": permalink,
        "reply_id": reply_id,
        "image": image_file.name,
        "proof_screenshot": str(proof_path)
    }, f, ensure_ascii=False, indent=2)
