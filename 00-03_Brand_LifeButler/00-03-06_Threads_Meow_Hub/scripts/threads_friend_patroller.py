import sys
import json
import time
import random
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.sync_api import sync_playwright

SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"
SCREENSHOT_DIR = SCRIPT_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

def like_and_reply_post(post_url, comment_text, headless=True):
    """
    全自動好友貼文巡邏、按讚與高情商回覆引擎
    """
    print("==================================================")
    print(f"🌊 [北極星 Threads 好友巡邏引擎] 目標: {post_url}")
    print(f"💬 回覆內容: {comment_text}")
    print("==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            storage_state=str(SESSION_PATH),
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            locale="zh-TW",
            viewport={"width": 1280, "height": 900}
        )
        page = context.new_page()

        try:
            page.goto(post_url, wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(3000)

            # 1. 檢查並點讚 (愛心)
            liked = False
            for sel in ['div[role="button"]:has(svg[title="Unlike"])', 'div[role="button"]:has(svg[title="收回讚"])']:
                if page.locator(sel).count() > 0 and page.locator(sel).first.is_visible():
                    liked = True
                    print("💖 此貼文已在愛心名單中！")
                    break

            if not liked:
                for sel in ['div[role="button"]:has(svg[title="Like"])', 'div[role="button"]:has(svg[title="讚"])']:
                    loc = page.locator(sel)
                    if loc.count() > 0 and loc.first.is_visible():
                        print("❤️ 正在按愛心...")
                        time.sleep(random.uniform(1.2, 2.5))
                        loc.first.click(force=True)
                        page.wait_for_timeout(2000)
                        print("🎉 愛心成功送出！")
                        break

            # 2. 定位輸入框或點擊 Reply 打開
            input_box = page.locator('div[contenteditable="true"]').first
            if not input_box.is_visible():
                reply_btn = page.locator('div[role="button"]:has(svg[title="Reply"]), div[role="button"]:has(svg[title="回覆"])').first
                if reply_btn.is_visible():
                    reply_btn.click(force=True)
                    page.wait_for_timeout(2000)

            input_box = page.locator('div[contenteditable="true"]').first
            if input_box.is_visible():
                print("✍️ 正在輸入回覆內容...")
                input_box.click()
                page.wait_for_timeout(500)
                input_box.press("Enter")
                page.keyboard.type(comment_text, delay=25)
                page.wait_for_timeout(1500)

                # 按 Enter 送出
                print("🚀 正在按下 Enter 送出留言...")
                input_box.press("Enter")
                page.wait_for_timeout(6000)

                shot = SCREENSHOT_DIR / "latest_friend_reply_proof.png"
                page.screenshot(path=str(shot))
                print(f"🎉 留言發布任務完成！截圖已存檔: {shot}")
                return True
            else:
                print("❌ 未能定位回覆輸入框！")
                return False

        except Exception as e:
            print(f"❌ 執行過程異常: {e}")
            return False
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python threads_friend_patroller.py <post_url> <comment_text>")
        sys.exit(1)
    like_and_reply_post(sys.argv[1], sys.argv[2])
