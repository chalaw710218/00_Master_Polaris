"""
Polaris Reciprocal Visitor Protocol (登門回訪標準作業程序)
由影 (Kage · 首席特務兼生活管家) 執掌
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_PATH = BASE_DIR / "scripts" / "threads_session.json"
SCREENSHOT_DIR = BASE_DIR / "scripts" / "screenshots"
LOG_PATH = BASE_DIR / "data" / "reciprocal_log.json"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_reciprocal_history() -> dict:
    if LOG_PATH.exists():
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_reciprocal_history(data: dict):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def visit_and_reply_page(page, target_handle: str, custom_comment: str = None, post_url: str = None) -> bool:
    """
    使用現有的 Playwright page 登門回訪指定 Threads 帳號的最新貼文並留言
    """
    handle = target_handle.lstrip("@").strip()
    history = load_reciprocal_history()
    
    # 若無指定 post_url，則從個人頁面探尋最新貼文
    if not post_url:
        profile_url = f"https://www.threads.net/@{handle}"
        print(f"   🕵️‍♂️ 登門探訪首頁: {profile_url}", flush=True)
        try:
            page.goto(profile_url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(3000)
            
            # 抓取第一篇貼文連結
            post_links = page.locator(f'a[href*="/@{handle}/post/"]').all()
            if not post_links:
                print(f"   ℹ️ 未在 @{handle} 主頁找到公開貼文，改為在首頁點讚留下足跡", flush=True)
                like_btn = page.locator('div[role="button"]:has(svg[title="Like"]), div[role="button"]:has(svg[title="讚"])').first
                if like_btn.is_visible(timeout=2000):
                    like_btn.click(force=True)
                return True
                
            href = post_links[0].get_attribute("href")
            if href.startswith("/"):
                post_url = f"https://www.threads.net{href}"
            else:
                post_url = href
            print(f"   🎯 鎖定最新貼文網址: {post_url}", flush=True)
        except Exception as pe:
            print(f"   ⚠️ 探訪主頁提示: {pe}", flush=True)
            return False
        
    print(f"   📖 前往貼文詳情: {post_url}", flush=True)
    try:
        page.goto(post_url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(3500)
        
        # 激活輸入框
        bubble = page.locator('div[role="button"]:has(svg[title="回覆"]), svg[title="回覆"]').first
        if bubble.is_visible():
            bubble.click(force=True)
            page.wait_for_timeout(1500)
            
        reply_box = page.locator('div[role="textbox"], div[contenteditable="true"]').first
        if not reply_box.is_visible():
            print("   ⚠️ 未能定位到輸入框", flush=True)
            return False
            
        reply_box.click(force=True)
        page.wait_for_timeout(500)
        
        # 文案
        comment_text = custom_comment or f"好深刻的分享！在台東做生活管家看著很有共鳴，默默端上一杯鹿野紅烏龍致敬！🍵✨"
        print(f"   ✍️ 正在鍵入回訪留言: {comment_text[:25]}...", flush=True)
        page.keyboard.type(comment_text, delay=25)
        page.wait_for_timeout(1500)
        
        # 精準鎖定 36x36 黑色圓形向上箭頭發布按鈕
        buttons = page.locator('div[role="button"]').all()
        submit_btn = None
        for b in buttons:
            if b.is_visible():
                box = b.bounding_box()
                if box and 30 <= box['width'] <= 42 and 30 <= box['height'] <= 42 and 550 <= box['y'] <= 650:
                    submit_btn = b
                    break
                    
        if submit_btn:
            submit_btn.click(force=True)
        else:
            page.mouse.click(792, 597)
            
        print("   ⏳ 等待伺服器響應與 Toast 渲染...", flush=True)
        page.wait_for_timeout(6000)
        
        # 截圖存證
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shot_path = SCREENSHOT_DIR / f"reciprocal_{handle}_{timestamp}.png"
        page.screenshot(path=str(shot_path))
        print(f"   🎉 登門回訪成功！驗收截圖: {shot_path.name}", flush=True)
        
        # 記錄歷史
        history[handle] = {
            "last_visited": datetime.now().isoformat(),
            "post_url": post_url,
            "comment": comment_text,
            "proof_screenshot": str(shot_path.relative_to(BASE_DIR))
        }
        save_reciprocal_history(history)
        return True
    except Exception as e:
        print(f"   ⚠️ 登門回訪執行異常: {e}", flush=True)
        return False


def visit_and_reply(target_handle: str, custom_comment: str = None, post_url: str = None) -> bool:
    """獨立調用版本"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_PATH),
            viewport={"width": 1280, "height": 900},
            locale="zh-TW"
        )
        page = context.new_page()
        res = visit_and_reply_page(page, target_handle, custom_comment, post_url)
        browser.close()
        return res


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        comment = sys.argv[2] if len(sys.argv) > 2 else None
        visit_and_reply(target, comment)
    else:
        print("使用方式: python scripts/reciprocal_visitor.py <handle> [comment]")
