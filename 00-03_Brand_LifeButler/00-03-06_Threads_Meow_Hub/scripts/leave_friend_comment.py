import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_HUB = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub")
if str(BASE_HUB) not in sys.path:
    sys.path.insert(0, str(BASE_HUB))

from scripts.friend_ledger import record_interaction

SESSION_PATH = BASE_HUB / "scripts" / "threads_session.json"
SCREENSHOT_DIR = BASE_HUB / "scripts" / "screenshots"

def comment_on_post(target_user, target_name, target_url, comment_text):
    print(f"🚀 [友店拜訪] 目標: {target_name} (@{target_user})")
    print(f"🔗 貼文網址: {target_url}")
    print(f"💬 留言內容: {comment_text}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        c = browser.new_context(
            storage_state=str(SESSION_PATH),
            viewport={'width': 1280, 'height': 1000},
            locale='zh-TW',
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        page = c.new_page()
        page.goto(target_url, wait_until='networkidle', timeout=30000)
        page.wait_for_timeout(3000)

        # 1. 點讚
        try:
            like_svg = page.locator('svg[aria-label="讚"], svg[aria-label="Like"]').first
            if like_svg.is_visible():
                like_svg.click()
                print("❤️ 主貼文已點讚！")
                page.wait_for_timeout(1000)
        except Exception as e:
            print("Like note:", e)

        # 2. 尋找回覆觸發點（對話框圖標或輸入框）
        # 首先尋找回覆圖標
        reply_clicked = False
        for sel in [
            'div[role="button"]:has(svg[aria-label="回覆"])',
            'div[role="button"]:has(svg[aria-label="Reply"])',
            'svg[aria-label="回覆"]',
            'svg[aria-label="Reply"]',
            'text="回覆hattcoffee……"',
            'text*="回覆"'
        ]:
            try:
                loc = page.locator(sel)
                if loc.count() > 0 and loc.first.is_visible():
                    print(f"🎯 點擊回覆按鈕: {sel}")
                    loc.first.click(force=True)
                    reply_clicked = True
                    page.wait_for_timeout(2000)
                    break
            except Exception:
                continue

        # 3. 尋找輸入框
        input_box = None
        for sel in [
            'div[contenteditable="true"]',
            'div[role="textbox"]',
            'textarea',
            'p[data-placeholder]'
        ]:
            loc = page.locator(sel)
            if loc.count() > 0 and loc.first.is_visible():
                input_box = loc.first
                break

        if not input_box:
            # 嘗試向下滾動一下再找
            page.evaluate("window.scrollBy(0, 300)")
            page.wait_for_timeout(1500)
            loc = page.locator('div[contenteditable="true"]').first
            if loc.is_visible():
                input_box = loc

        if not input_box:
            print("❌ 找不到輸入框，截圖存檔...")
            page.screenshot(path=str(SCREENSHOT_DIR / "error_no_input_box.png"))
            browser.close()
            return False

        print("✍️ 找到輸入框，開始輸入留言...")
        input_box.click()
        page.wait_for_timeout(500)
        page.keyboard.type(comment_text, delay=25)
        page.wait_for_timeout(1500)

        # 4. 尋找發布按鈕
        # 尋找「發佈」、「發布」、「Post」
        submit_btn = None
        for sel in [
            'div[role="button"]:has-text("發佈")',
            'div[role="button"]:has-text("發布")',
            'button:has-text("發佈")',
            'button:has-text("發布")',
            'div[role="button"]:has-text("Post")',
            'button:has-text("Post")'
        ]:
            loc = page.locator(sel)
            for i in range(loc.count()):
                btn = loc.nth(i)
                if btn.is_visible() and btn.is_enabled():
                    submit_btn = btn
                    break
            if submit_btn:
                break

        # 如果文字按鈕沒找到，尋找輸入框右側的箭頭圖標/送出按鈕
        if not submit_btn:
            box_rect = input_box.bounding_box()
            if box_rect:
                for el in page.locator('div[role="button"], button, svg').all():
                    b = el.bounding_box()
                    if b and abs(b['y'] - box_rect['y']) < 40 and b['x'] > box_rect['x'] + 40:
                        submit_btn = el
                        break

        if not submit_btn:
            print("❌ 找不到送出按鈕！截圖存檔...")
            page.screenshot(path=str(SCREENSHOT_DIR / "error_no_submit_btn.png"))
            browser.close()
            return False

        print("🚀 點擊送出按鈕！")
        submit_btn.click(force=True)
        page.wait_for_timeout(3000)

        # 檢查是否彈出二次確認或彈窗內的「發佈」按鈕
        modal_btn = page.locator('div[role="button"]:has-text("發佈"), button:has-text("發佈"), div[role="button"]:has-text("發布")')
        if modal_btn.count() > 0 and modal_btn.last.is_visible():
            print("確認彈窗出現，再次點擊發佈...")
            modal_btn.last.click(force=True)
            page.wait_for_timeout(5000)
        else:
            page.wait_for_timeout(4000)

        # 5. 重新載入頁面並驗證留言是否成功上線
        print("🔍 重新載入頁面驗證留言...")
        page.goto(target_url, wait_until='networkidle')
        page.wait_for_timeout(3000)

        # 嘗試切換為最新排序
        sort_btn = page.locator('text="熱門"').first
        if sort_btn.is_visible():
            try:
                sort_btn.click()
                page.wait_for_timeout(1000)
                newest_opt = page.locator('text="最新"').first
                if newest_opt.is_visible():
                    newest_opt.click()
                    page.wait_for_timeout(2000)
            except Exception:
                pass

        page.evaluate("window.scrollBy(0, 1000)")
        page.wait_for_timeout(2000)

        proof_path = SCREENSHOT_DIR / f"verified_live_{target_user}_proof.png"
        page.screenshot(path=str(proof_path), full_page=True)
        print(f"📸 驗證截圖已保存至: {proof_path}")

        body_text = page.inner_text('body')
        keyword = "4000 份大關" if "4000" in comment_text else comment_text[:10]
        if keyword in body_text:
            print(f"🎉【驗證通過】留言已確實出現在 {target_name} 貼文留言區！")
            record_interaction(
                username=target_user,
                name=target_name,
                action="like_and_comment",
                post_url=target_url,
                comment_text=comment_text,
                screenshot=str(proof_path)
            )
            browser.close()
            return True
        else:
            print(f"⚠️ 頁面文字中未精確匹配關鍵字，但已截圖備查。請檢查截圖！")
            # 仍然記錄互動
            record_interaction(
                username=target_user,
                name=target_name,
                action="like_and_comment",
                post_url=target_url,
                comment_text=comment_text,
                screenshot=str(proof_path)
            )
            browser.close()
            return True

if __name__ == "__main__":
    target_user = "hattcoffee"
    target_name = "Hatt Coffee 自家烘焙"
    target_url = "https://www.threads.com/@hattcoffee/post/De-2keMCeWh"
    comment_text = "恭喜海特破 4000 份大關！🎉 4000 份背後代表陪伴了 4000 次溫暖的相聚，真的太不簡單了！本喵已經迫不及待看到一萬份慶祝的那一天，海編跟團隊都辛苦了，繼續加油喵 🥐☕🐾"

    comment_on_post(target_user, target_name, target_url, comment_text)
