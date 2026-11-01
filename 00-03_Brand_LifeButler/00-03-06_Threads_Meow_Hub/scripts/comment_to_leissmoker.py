import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"
POST_URL = "https://www.threads.net/@956leissmoker/post/DfEuzpXkiKt"

COMMENT_TEXT = "（喵編默默舉起肉球）這題本喵懂！這種員工主要負責提供『精神支持與監督眼神』，薪水直接用煙燻肉肉結算就對了🐾🍖🤣"

print("==================================================")
print(f"🚀 [友店互動・走心回覆] 前往 @956leissmoker 貼文: {POST_URL}")
print(f"💬 回覆內容:\n{COMMENT_TEXT}")
print("==================================================")

screenshot_proof = Path(r"C:\Users\lenovo\.gemini\antigravity\brain\62615c83-54cd-4585-ac6a-95745b9ac34a\live_reply_to_956leissmoker.png")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        storage_state=str(SESSION_PATH),
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        locale="zh-TW",
        viewport={"width": 1280, "height": 900}
    )
    page = context.new_page()

    try:
        page.goto(POST_URL, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000)

        # 1. 點讚
        like_btn = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').first
        if like_btn.is_visible(timeout=3000):
            like_btn.click(force=True)
            print("❤️ 已點亮愛心！")
            page.wait_for_timeout(1500)

        # 2. 定位或打開回覆框
        reply_trigger = page.locator('div[role="button"]:has(svg[title="Reply"]), div[role="button"]:has(svg[title="回覆"]), svg[title="Reply"], svg[title="回覆"]').first
        if reply_trigger.is_visible(timeout=3000):
            print("💬 點擊回覆按鈕...")
            reply_trigger.click(force=True)
            page.wait_for_timeout(2000)

        input_box = page.locator('div[contenteditable="true"]').first
        if input_box.is_visible(timeout=5000):
            print("✍️ 成功定位輸入框，正在輸入內容 (使用 force=True)...")
            input_box.click(force=True)
            page.wait_for_timeout(500)
            page.keyboard.type(COMMENT_TEXT, delay=30)
            page.wait_for_timeout(2000)

            # 點擊「發布」或「回覆」或「Post」
            post_btn = None
            for sel in [
                'div[role="button"]:has-text("Post")',
                'div[role="button"]:has-text("發布")',
                'div[role="button"]:has-text("回覆")',
                'button:has-text("發布")',
                'button:has-text("Post")'
            ]:
                candidate = page.locator(sel)
                for i in range(candidate.count()):
                    btn = candidate.nth(i)
                    if btn.is_visible() and btn.is_enabled():
                        post_btn = btn
                        break
                if post_btn:
                    break

            if post_btn:
                print(f"🚀 點擊送出按鈕: '{post_btn.inner_text().strip()}'")
                post_btn.click(force=True)
                page.wait_for_timeout(6000)
                print("🎉 留言已成功送出！")
            else:
                print("⚠️ 未找到送出按鈕，嘗試按 Control+Enter 送出...")
                page.keyboard.press("Control+Enter")
                page.wait_for_timeout(6000)

            page.screenshot(path=str(screenshot_proof))
            print(f"📸 驗收截圖已儲存至: {screenshot_proof}")

        else:
            print("❌ 未能定位輸入框！截圖記錄中...")
            page.screenshot(path=str(screenshot_proof))

    except Exception as e:
        print("❌ 異常:", e)
        page.screenshot(path=str(screenshot_proof))
    finally:
        browser.close()
