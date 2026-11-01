import os
import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.append(str(SCRIPT_DIR))

from threads_publisher import publish_thread
from evaluate_threads_draft import evaluate_threads_draft

POST_TEXT = """剛剛看了一眼牆上的時鐘，
九點過後的週日夜晚總是走得特別快。

身後的闆仔一邊嘆氣，
一邊默默把明天要用的行事曆收進後背包。
本喵早就把兩隻小前腳收進胸口，
在地毯上折好最標準的毛毛吐司麵包，
呼嚕呼嚕準備進入深度充電模式。

（對貓咪來說，週一根本只是日曆上的兩個字而已喵）

明天的事情明天再煩惱，
今晚先把一整週的疲勞好好睡掉吧。

大家現在已經躺平在被窩裡、
還是捨不得睡正在滑手機抗議週一呢？🛌🐾"""

IMAGE_PATH = ROOT_DIR / "04_Shadow_Kage_Operative" / "images" / "meow_sunday_night_loaf.jpg"

print("🔍 [步驟 1] 執行發布前品質審計...")
score, report = evaluate_threads_draft(POST_TEXT)
print(f"🏆 審計得分: {score} / 100")
for r in report:
    print("  ", r)

if score < 90:
    print("❌ 評分未達 90，終止發布！")
    sys.exit(1)

print("\n🚀 [步驟 2] 調用 Meta Threads API 發布週日收假夜間貼文...")
post_id = publish_thread(text=POST_TEXT, image=str(IMAGE_PATH), topic_tag="耍廢日常")

if not post_id:
    print("❌ 發布失敗！")
    sys.exit(1)

print(f"\n🎉 [步驟 3] 貼文發布成功！Post ID: {post_id}")

import requests
from threads_publisher import THREADS_ACCESS_TOKEN, API_BASE

permalink = None
try:
    info_res = requests.get(f"{API_BASE}/{post_id}?fields=id,text,permalink,timestamp&access_token={THREADS_ACCESS_TOKEN}").json()
    permalink = info_res.get("permalink")
    print(f"🔗 貼文公開永久連結: {permalink}")
except Exception as e:
    print(f"⚠️ 查詢 permalink 提示: {e}")

# 登記新圖片至 published_image_registry.json
registry_path = ROOT_DIR / "data" / "published_image_registry.json"
try:
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)
    registry["published_images"].append({
        "filename": "meow_sunday_night_loaf.jpg",
        "published_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "post_id": post_id,
        "topic": "耍廢日常"
    })
    registry["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    print("✅ 成功登記全新照片至 published_image_registry.json")
except Exception as e:
    print(f"⚠️ 登記圖片提示: {e}")

print("\n📸 [步驟 4] 啟動 Playwright 前台渲染驗收截圖...")
screenshot_path = Path(r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\live_sunday_night_proof.png")
target_url = permalink if permalink else "https://www.threads.com/@hellotaitung"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SCRIPT_DIR / "threads_session.json"),
        viewport={"width": 1280, "height": 900}
    )
    page = context.new_page()
    page.goto(target_url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    page.screenshot(path=str(screenshot_path))
    browser.close()

print(f"✅ 前台驗收截圖已儲存至: {screenshot_path}")

result = {
    "post_id": post_id,
    "permalink": permalink,
    "score": score,
    "image_path": str(IMAGE_PATH),
    "screenshot_path": str(screenshot_path)
}
with open(SCRIPT_DIR / "latest_sunday_night_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\n🏁 全部發布與驗收流程完成！")
