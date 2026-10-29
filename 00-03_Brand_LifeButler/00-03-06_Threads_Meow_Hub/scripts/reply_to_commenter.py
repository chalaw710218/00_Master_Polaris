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

COMMENT_ID = "18458909932192625"
REPLY_TEXT = "（拍拍旁邊溫暖的木地板）下午那塊太陽真的太有催眠瓦斯了！眼睛睜不開就放過自己趴個10分鐘，靈魂先午睡一下再回來工作喵 ☕🐾"

print(f"🚀 [喵編秒回任務] 正在回覆網友 @mmasisou (Comment ID: {COMMENT_ID})...")
print(f"💬 回覆內容: {REPLY_TEXT}")

reply_post_id = publish_thread(text=REPLY_TEXT, reply_to_id=COMMENT_ID)

if reply_post_id:
    print(f"🎉 回覆成功！Reply Post ID: {reply_post_id}")
    print(f"🔗 前台連結: https://www.threads.com/@hellotaitung/post/{reply_post_id}")
else:
    print("❌ API 回覆失敗！")
    sys.exit(1)

# 前台驗收截圖
print("\n📸 [前台驗收] 正在截取貼文留言區驗收截圖...")
POST_URL = "https://www.threads.com/@hellotaitung/post/DfEOY2kn06S"
screenshot_path = Path(r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\verified_reply_to_mmasisou.png")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SCRIPT_DIR / "threads_session.json"),
        viewport={"width": 1280, "height": 900},
        locale="zh-TW"
    )
    page = context.new_page()
    page.goto(POST_URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(4000)

    # 順便給對方的留言點愛心 ❤️
    try:
        like_btn = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').nth(1)
        if like_btn.is_visible(timeout=3000):
            like_btn.click(force=True)
            print("❤️ 已順便為 @mmasisou 的留言點亮愛心！")
            page.wait_for_timeout(1000)
    except Exception as e:
        print("點讚留言提示:", e)

    page.screenshot(path=str(screenshot_path))
    browser.close()

print(f"✅ 留言回覆與互動驗收截圖已存至: {screenshot_path}")
