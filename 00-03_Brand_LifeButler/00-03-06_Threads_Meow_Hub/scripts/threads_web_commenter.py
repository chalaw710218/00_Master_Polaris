import os
import sys
import time
import argparse
from pathlib import Path

# 確保 Windows 終端機支援 Emoji
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"
SCREENSHOT_DIR = SCRIPT_DIR / "screenshots"

def post_comment(post_url, comment_text, headless=True):
    """
    使用 Playwright 攜帶登入憑證，自動進入指定 Threads 貼文網址並發表留言
    :param post_url: 貼文完整 URL (例如 https://www.threads.net/@hattcoffee/post/Deniyw6iQ9J)
    :param comment_text: 欲回覆的留言文字
    :param headless: 是否使用無頭模式 (預設 True，若除錯可設為 False)
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ 請先安裝 Playwright: pip install playwright && playwright install chromium")
        return False

    if not SESSION_PATH.exists():
        print(f"⚠️ 找不到登入憑證檔案: {SESSION_PATH}")
        print("💡 請先執行: python scripts/threads_web_login.py 登入一次帳號並保存憑證！")
        return False

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    print(f"🤖 [Threads 智能留言機] 正在前往目標貼文: {post_url}")
    print(f"💬 預定留言內容: {comment_text}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            storage_state=str(SESSION_PATH),
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            locale="zh-TW",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()

        try:
            # 導航至貼文
            page.goto(post_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_timeout(3000)

            # 尋找回覆按鈕或輸入框
            # 策略 1: 直接點擊「回覆」圖示或回覆區域
            reply_trigger = None
            for sel in [
                'svg[aria-label="回覆"]',
                'svg[aria-label="Reply"]',
                'div[role="button"]:has(svg[aria-label="回覆"])',
                'div[role="button"]:has(svg[aria-label="Reply"])',
                'div[aria-label="留下回覆..."]',
                'div[aria-label="Post a reply..."]'
            ]:
                if page.locator(sel).first.is_visible():
                    reply_trigger = sel
                    break

            if reply_trigger:
                print(f"🎯 點擊回覆按鈕: {reply_trigger}")
                page.locator(reply_trigger).first.click()
                page.wait_for_timeout(2000)

            # 策略 2: 定位輸入文字框 (contenteditable 或 textarea)
            input_box = None
            for sel in [
                'div[contenteditable="true"]',
                'div[role="textbox"]',
                'textarea',
                'p[data-placeholder]'
            ]:
                if page.locator(sel).first.is_visible():
                    input_box = sel
                    break

            if not input_box:
                print("❌ 無法定位回覆文字輸入框！截圖記錄中...")
                page.screenshot(path=str(SCREENSHOT_DIR / "error_no_input.png"))
                browser.close()
                return False

            print(f"✍️ 正在輸入留言...")
            page.locator(input_box).first.click()
            page.wait_for_timeout(500)
            # 模擬人類自然打字
            page.keyboard.type(comment_text, delay=25)
            page.wait_for_timeout(1500)

            # 策略 3: 定位並點擊「發布 / 回覆 / Post」按鈕
            submit_btn = None
            for sel in [
                'div[role="button"]:has-text("發布")',
                'div[role="button"]:has-text("Post")',
                'div[role="button"]:has-text("回覆")',
                'div[role="button"]:has-text("Reply")',
                'button:has-text("發布")',
                'button:has-text("Post")'
            ]:
                # 排除剛才的回覆圖標按鈕，尋找文字發布按鈕
                locator = page.locator(sel)
                for i in range(locator.count()):
                    btn = locator.nth(i)
                    if btn.is_visible() and btn.is_enabled():
                        submit_btn = btn
                        break
                if submit_btn:
                    break

            if not submit_btn:
                print("⚠️ 未找到明確的發布按鈕，嘗試 Enter 或快速搜尋...")
                page.screenshot(path=str(SCREENSHOT_DIR / "error_no_submit.png"))
                browser.close()
                return False

            print("🚀 點擊送出留言按鈕！")
            submit_btn.click()
            page.wait_for_timeout(5000) # 等待送出完成

            # 截圖存檔作為成功憑證
            success_shot = SCREENSHOT_DIR / "latest_reply_success.png"
            page.screenshot(path=str(success_shot))
            print(f"🎉 留言成功！憑證已截圖存檔: {success_shot}")
            browser.close()
            return True

        except Exception as e:
            print(f"❌ 留言過程中發生異常: {e}")
            try:
                page.screenshot(path=str(SCREENSHOT_DIR / "exception.png"))
            except Exception:
                pass
            browser.close()
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Threads 自動化留言機")
    parser.add_argument("--url", required=True, help="目標貼文完整 URL")
    parser.add_argument("--text", required=True, help="欲回覆的留言文字")
    parser.add_argument("--headed", action="store_true", help="顯示瀏覽器視窗 (方便除錯)")

    args = parser.parse_args()
    post_comment(post_url=args.url, comment_text=args.text, headless=not args.headed)
