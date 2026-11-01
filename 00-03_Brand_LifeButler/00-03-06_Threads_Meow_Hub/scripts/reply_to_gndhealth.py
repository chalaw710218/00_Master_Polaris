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

COMMENT_ID = "17924439264216679"
USERNAME = "gndhealth"
POST_URL = "https://www.threads.com/@hellotaitung/post/De9vdgZkzDI"

REPLY_TEXT = "（喵編在沙發上抬頭眨眨眼）沒錯～手手折好就是全家最高打烊宣告，連闆仔都不敢催我讓位🤣 每天認真經營真的辛苦了！薄荷薑油聽起來超適合舒緩一整天疲勞，今晚也早點休息好好放鬆喵 🌿🐾💤"

print(f"🚀 [喵編秒回任務] 正在回覆網友 @{USERNAME} (Comment ID: {COMMENT_ID})...")
print(f"💬 回覆內容:\n{REPLY_TEXT}")

reply_post_id = publish_thread(text=REPLY_TEXT, reply_to_id=COMMENT_ID)

if reply_post_id:
    print(f"\n🎉 回覆成功！Reply Post ID: {reply_post_id}")
    print(f"🔗 前台連結: https://www.threads.com/@hellotaitung/post/{reply_post_id}")
else:
    print("❌ API 回覆失敗！")
    sys.exit(1)

# 記錄到 replied_ids.json
state_file = SCRIPT_DIR / "replied_ids.json"
replied_ids = []
if state_file.exists():
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            replied_ids = json.load(f)
    except Exception:
        pass
if COMMENT_ID not in replied_ids:
    replied_ids.append(COMMENT_ID)
with open(state_file, "w", encoding="utf-8") as f:
    json.dump(replied_ids, f, ensure_ascii=False, indent=2)
print("✅ 已將 Comment ID 登記至 replied_ids.json")

# 前台驗收截圖 & 點愛心
print("\n📸 [前台驗收] 正在打開貼文頁面點讚並截取留言驗收截圖...")
screenshot_path = Path(r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\verified_reply_to_gndhealth.png")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SCRIPT_DIR / "threads_session.json"),
        viewport={"width": 1280, "height": 950},
        locale="zh-TW"
    )
    page = context.new_page()
    page.goto(POST_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(4000)

    # 為網友 @gndhealth 的留言按愛心
    try:
        like_btns = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])')
        for i in range(1, like_btns.count()):
            like_btns.nth(i).click(force=True)
            print(f"❤️ 成功為留言點亮愛心！")
            page.wait_for_timeout(1000)
            break
    except Exception as e:
        print("點讚留言提示:", e)

    page.screenshot(path=str(screenshot_path))
    browser.close()

print(f"✅ 前台驗收截圖已儲存至: {screenshot_path}")
print("🏁 回覆任務圓滿達成！")
