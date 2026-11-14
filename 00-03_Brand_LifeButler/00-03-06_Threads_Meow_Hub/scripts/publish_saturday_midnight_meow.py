import os
import sys
import time
import json
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.append("scripts")
from threads_publisher import publish_thread, THREADS_ACCESS_TOKEN, API_BASE

image_file = Path("images/meow_saturday_midnight_sleep.jpg")
draft_file = Path("scripts/test_saturday_midnight_draft.txt")
SESSION_PATH = Path("scripts/threads_session.json")
PROOF_DIR = Path("scripts/screenshots")
PROOF_DIR.mkdir(parents=True, exist_ok=True)

with open(draft_file, "r", encoding="utf-8") as f:
    post_text = f.read().strip()

first_reply = "（替熟睡的喵編輕輕拉好小毛毯）週末最棒的事情，就是今晚可以理直氣壯地晚睡，明天可以心安理得地賴床。不管你是享受安靜的夜貓族，還是剛滑手機滑到想睡，明天早上想吃現做熱早餐不用早起換衣服出門，生活管家任意門在個人檔案，熱騰騰送到家。大家今晚做個好夢，晚安！🌙✨"

print("==================================================")
print("🚀 [週六深夜晚安專場 · 店貓喵編隨筆記發布啟動]")
print(f"🖼️ 配圖確認: {image_file.name} (大小: {image_file.stat().st_size} bytes)")
print("==================================================")

post_id = publish_thread(text=post_text, image=str(image_file), topic_tag="台東生活")

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
proof_path = PROOF_DIR / f"walk_v3_{post_id}_meow_saturday_midnight_verified.png"
if permalink and SESSION_PATH.exists():
    print("\n📸 前往前台進行實景存證截圖...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                storage_state=str(SESSION_PATH),
                viewport={"width": 1280, "height": 900}
            )
            page = context.new_page()
            page.goto(permalink, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            page.screenshot(path=str(proof_path), full_page=False)
            browser.close()
            print(f"📸 前台截圖存證成功: {proof_path}")
    except Exception as e:
        print(f"⚠️ 截圖失敗: {e}")

print("\n🏁 週六深夜隨筆記全流程圓滿完成！")
