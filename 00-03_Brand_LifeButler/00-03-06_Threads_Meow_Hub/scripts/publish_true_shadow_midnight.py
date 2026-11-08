import sys
import time
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

post_text = """週日深夜十一點多，把整週奔波的行事曆合上。
在台東的老木桌前熱了一小壺水，慢慢泡開鹿野紅烏龍。

看著茶葉在陶壺裡舒展，
窗外的夜風帶著太平洋安靜的味道。
生活的大多數焦慮，往往在肯給自己一段完全安靜的呼吸時光時，
就慢慢沉澱落下了。

大家今晚都準備睡了嗎？
不管明天週一有什麼硬仗要打，今晚把心安頓在枕頭上，好好睡上一覺。晚安！🍵✨ #台東生活"""

first_reply = "（輕輕遞上一只溫熱的茶杯）如果腦袋還在轉、還睡不著也沒關係，把燈光調暗，喝口溫水。今晚的生活管家在後排替大家守夜，願你好夢。🍵✨"
image_path = Path("images/shadow_sunday_midnight_tea_desk_v2.jpg")

print(f"🚀 開始正式推送【真正的生活管家（影）】帶圖貼文至 Threads...")
print(f"🖼️ 配圖確認: {image_path.name} (大小: {image_path.stat().st_size} bytes)")

post_id = publish_thread(text=post_text, image=str(image_path), topic_tag="台東生活")
if not post_id:
    print("❌ 發布失敗！")
    sys.exit(1)

print(f"🎉 正式發布成功！Threads Post ID: {post_id}")

# 查詢正確的公開 permalink
time.sleep(2)
info_res = requests.get(f"{API_BASE}/{post_id}?fields=id,permalink,media_type&access_token={THREADS_ACCESS_TOKEN}").json()
permalink = info_res.get("permalink", f"https://www.threads.net/@hellotaitung/post/{post_id}")
print(f"🔗 官方短網址: {permalink} (媒體類型: {info_res.get('media_type')})")

# 發布首回覆
print("💬 發布首回覆橋接...")
reply_id = publish_thread(text=first_reply, reply_to_id=post_id)
print(f"✅ 首回覆發布成功！Reply ID: {reply_id}")

# Playwright 前台截圖驗收
session_path = Path("scripts/threads_session.json")
screenshot_dir = Path("scripts/screenshots")
screenshot_dir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(session_path),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = context.new_page()
    print(f"📸 前往公開詳情截圖驗收: {permalink}")
    page.goto(permalink, wait_until="domcontentloaded", timeout=25000)
    page.wait_for_timeout(4000)
    
    proof_path = screenshot_dir / f"true_shadow_midnight_{post_id}_verified.png"
    page.screenshot(path=str(proof_path))
    
    artifact_proof = Path(r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\true_shadow_midnight_verified.png")
    page.screenshot(path=str(artifact_proof))
    print("📸 驗收截圖完成並同步成功！")
    
    browser.close()

print(f"🏁 影的真正定裝照發布與驗收圓滿完成！網址: {permalink}")
