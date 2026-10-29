import os
import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# 確保 Windows 終端機支援 UTF-8
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

POST_TEXT = """我就問全台灣到底有多少人，
剛剛看新聞才驚覺下週居然就要立冬了？！

氣象說接下來有整整 3 波東北季風接力報到，
低溫直接掉到 1 字頭，
東部跟近山區甚至下探 17 度...

闆仔剛剛一出門倒垃圾，
直接被外面的大風吹到縮著脖子逃回屋裡，
二話不說把剛曬好的厚羊毛毯翻出來。

本喵身為專業貓界氣象官，
早就已經在窗邊折手手縮成一顆大毛球了喵！🐾

大家都把厚棉被跟長袖翻出來了嗎？
還是今天出門已經被冷風吹醒了？👇"""

IMAGE_PATH = ROOT_DIR / "04_Shadow_Kage_Operative" / "images" / "meow_monsoon_lidong_prep.jpg"

print("🔍 [步驟 1] 執行發布前品質審計...")
score, report = evaluate_threads_draft(POST_TEXT)
print(f"🏆 審計得分: {score} / 100")
for r in report:
    print("  ", r)

if score < 90:
    print("❌ 評分未達 90，終止發布！")
    sys.exit(1)

print("\n🚀 [步驟 2] 調用 Meta Threads API 發布新貼文...")
post_id = publish_thread(text=POST_TEXT, image=str(IMAGE_PATH), topic_tag="耍廢日常")

if not post_id:
    print("❌ 發布失敗！")
    sys.exit(1)

print(f"\n🎉 [步驟 3] 貼文發布成功！Post ID: {post_id}")

# 查詢貼文 permalink
import requests
from threads_publisher import THREADS_ACCESS_TOKEN, API_BASE

permalink = None
try:
    info_res = requests.get(f"{API_BASE}/{post_id}?fields=id,text,permalink,timestamp&access_token={THREADS_ACCESS_TOKEN}").json()
    permalink = info_res.get("permalink")
    print(f"🔗 貼文公開永久連結: {permalink}")
except Exception as e:
    print(f"⚠️ 查詢 permalink 提示: {e}")

print("\n📸 [步驟 4] 啟動 Playwright 前台渲染驗收截圖...")
screenshot_path = Path(r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\live_monsoon_dusk_proof.png")
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

# 輸出結果 JSON 供後續整合
result = {
    "post_id": post_id,
    "permalink": permalink,
    "score": score,
    "image_path": str(IMAGE_PATH),
    "screenshot_path": str(screenshot_path)
}
with open(SCRIPT_DIR / "latest_publish_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\n🏁 全部發布與驗收流程完成！")
