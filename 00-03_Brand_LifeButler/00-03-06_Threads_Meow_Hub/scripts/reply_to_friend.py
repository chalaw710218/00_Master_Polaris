import sys
from pathlib import Path
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from playwright.sync_api import sync_playwright

SESSION_PATH = Path("scripts/threads_session.json")
SCREENSHOT_DIR = Path("scripts/screenshots")

def reply_to_friend(url, comment_text):
    print(f"🌐 前往好友貼文: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        c = browser.new_context(storage_state=str(SESSION_PATH), viewport={"width": 1280, "height": 900})
        page = c.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000)

        # 1. 確保點讚 (愛心)
        for sel in ['div[role="button"]:has(svg[title="Like"])', 'div[role="button"]:has(svg[title="讚"])']:
            loc = page.locator(sel)
            if loc.count() > 0 and loc.first.is_visible():
                print("❤️ 正在按愛心...")
                loc.first.click(force=True)
                page.wait_for_timeout(2000)
                print("🎉 愛心送出成功！")
                break

        # 2. 點擊 Comment 按鈕打開回覆框
        comment_btn = page.locator('div[role="button"]:has(svg[title="Comment"]), div[role="button"]:has(svg[title="留言"]), svg[title="Comment"], svg[title="留言"]').first
        if comment_btn.is_visible():
            print("💬 點擊 Comment 圖標...")
            comment_btn.click(force=True)
            page.wait_for_timeout(2500)
            page.screenshot(path=str(SCREENSHOT_DIR / "reply_box_opened.png"))
            print("📸 已截圖: reply_box_opened.png")

            # 3. 定位文字輸入框
            input_box = page.locator('div[contenteditable="true"], div[role="textbox"], p[data-placeholder]').first
            if input_box.is_visible():
                print("✍️ 正在輸入喵編回覆內容...")
                input_box.click()
                page.wait_for_timeout(500)
                page.keyboard.type(comment_text, delay=25)
                page.wait_for_timeout(1500)
                page.screenshot(path=str(SCREENSHOT_DIR / "comment_ready.png"))
                print("📸 輸入完成截圖: comment_ready.png")

                # 4. 點擊發布按鈕
                post_btns = page.locator('div[role="button"]:has-text("Post"), div[role="button"]:has-text("發布"), div[role="button"]:has-text("回覆")')
                for i in range(post_btns.count()):
                    btn = post_btns.nth(i)
                    if btn.is_visible() and ("Post" in btn.inner_text() or "發布" in btn.inner_text() or "回覆" in btn.inner_text()):
                        print(f"🚀 點擊送出按鈕: '{btn.inner_text().strip()}'")
                        btn.click(force=True)
                        page.wait_for_timeout(6000)
                        page.screenshot(path=str(SCREENSHOT_DIR / "reply_posted_success.png"))
                        print("🎉 留言正式成功送出！截圖已存檔: reply_posted_success.png")
                        break
            else:
                print("⚠️ 找不到輸入框！截圖備查...")
                page.screenshot(path=str(SCREENSHOT_DIR / "reply_box_not_found.png"))

        browser.close()

if __name__ == "__main__":
    reply_to_friend(
        "https://www.threads.com/@travel_zztaitung/post/Dd2obTAE7Yn",
        "活水湖的水波光粼粼的超美喵～✨ 雖然本喵身為貓咪不親自下水泡，但最喜歡揣著爪爪蹲在湖畔草皮上看著大家玩水了！順便偷偷盯著湖裡有沒有肥美的小魚游過去～🐟🐾"
    )
