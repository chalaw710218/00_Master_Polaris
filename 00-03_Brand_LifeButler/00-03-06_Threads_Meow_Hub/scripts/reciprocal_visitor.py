"""
Polaris Reciprocal Visitor Protocol (登門回訪與友店走心留言標準作業程序 v2.0)
由影 (Kage · 首席特務兼生活管家) 執掌
已修復 Playwright 動態相對座標定位黑色圓形向上箭頭 (↑) 發佈按鈕
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


def submit_inline_reply(page, comment_text: str) -> bool:
    """
    在 Threads 貼文詳情頁定位內嵌回覆框、輸入文字，
    並透過相對 reply_box 的動態幾何座標精準點擊右側 36x36 黑色圓形向上箭頭 (↑) 送出按鈕。
    """
    reply_box = page.locator('div[role="textbox"], div[contenteditable="true"]').first
    if not reply_box.is_visible(timeout=2000):
        bubble = page.locator(
            'div[role="button"]:has(svg[title="回覆"]), '
            'div[role="button"]:has(svg[aria-label="回覆"]), '
            'div[role="button"]:has(svg[aria-label="Reply"])'
        ).first
        if bubble.is_visible(timeout=2000):
            bubble.click(force=True)
            page.wait_for_timeout(1500)

    reply_box = page.locator('div[role="textbox"], div[contenteditable="true"]').first
    if not reply_box.is_visible(timeout=2500):
        print("   ⚠️ 未能定位到回覆輸入框", flush=True)
        return False

    reply_box.click(force=True)
    page.wait_for_timeout(500)
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.wait_for_timeout(300)

    print(f"   ✍️ 正在鍵入走心留言 ({len(comment_text)} 字): {comment_text[:30]}...", flush=True)
    page.keyboard.type(comment_text, delay=25)
    page.wait_for_timeout(1500)

    rbox = reply_box.bounding_box()
    buttons = page.locator('div[role="button"]').all()
    candidates = []
    for idx, b in enumerate(buttons):
        if b.is_visible():
            bb = b.bounding_box()
            if bb and rbox:
                if (
                    rbox["y"] - 30 <= bb["y"] <= rbox["y"] + rbox["height"] + 30
                    and 20 <= bb["width"] <= 60
                    and bb["x"] > rbox["x"] + 100
                ):
                    candidates.append((bb["x"], idx, bb))

    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_btn = buttons[candidates[0][1]]
        print(f"   🚀 點擊最右側圓形向上箭頭送出按鈕: box={candidates[0][2]}", flush=True)
        best_btn.click(force=True)
    else:
        post_btn = page.locator('div[role="button"]:has-text("發佈"), div[role="button"]:has-text("Post")').last
        if post_btn.is_visible():
            post_btn.click(force=True)
        else:
            print("   ⚠️ 未找到送出按鈕", flush=True)
            return False

    print("   ⏳ 等待伺服器響應與『已發佈』Toast 渲染 (6秒)...", flush=True)
    page.wait_for_timeout(6000)
    return True


def visit_and_reply_page(page, target_handle: str, custom_comment: str = None, post_url: str = None) -> bool:
    """
    使用現有的 Playwright page 登門拜訪指定 Threads 帳號的最新貼文並實際送出走心留言
    """
    handle = target_handle.lstrip("@").strip()
    history = load_reciprocal_history()

    # 安全門禁與每日上限檢查 (15則上限 / 120秒間隔)
    from interaction_safety_gate import can_comment, wait_comment_cooldown, record_comment
    allowed, reason = can_comment()
    if not allowed:
        print(f"   🛑 [安全門禁阻斷] {reason}", flush=True)
        return False
    wait_comment_cooldown()

    if not post_url:
        profile_url = f"https://www.threads.net/@{handle}"
        print(f"   🕵️‍♂️ 登門探訪首頁: {profile_url}", flush=True)
        try:
            page.goto(profile_url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(3500)

            post_links = page.locator('a[href*="/post/"]').all()
            for a in post_links:
                href = a.get_attribute("href") or ""
                if "/post/" in href:
                    post_url = f"https://www.threads.net{href}" if href.startswith("/") else href
                    break

            if not post_url:
                print(f"   ℹ️ 未在 @{handle} 主頁找到公開貼文連結", flush=True)
                return False

            print(f"   🎯 鎖定最新貼文網址: {post_url}", flush=True)
        except Exception as pe:
            print(f"   ⚠️ 探訪主頁提示: {pe}", flush=True)
            return False

    print(f"   📖 前往貼文詳情: {post_url}", flush=True)
    try:
        page.goto(post_url, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(3500)

        comment_text = custom_comment or "在台東看到這麼用心的日常分享特別有共鳴喵！今天出攤與生活都順順利利喵🐾"
        ok = submit_inline_reply(page, comment_text)
        if not ok:
            return False

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shot_path = SCREENSHOT_DIR / f"reciprocal_{handle}_{timestamp}.png"
        page.screenshot(path=str(shot_path))
        print(f"   🎉 走心留言發佈成功！驗收截圖: {shot_path.name}", flush=True)

        history[handle] = {
            "last_visited": datetime.now().isoformat(),
            "post_url": post_url,
            "comment": comment_text,
            "proof_screenshot": str(shot_path.relative_to(BASE_DIR))
        }
        save_reciprocal_history(history)

        # 登記至每日安全計數器與好友帳本
        try:
            from interaction_safety_gate import record_comment
            record_comment(target_user=handle, post_url=post_url, comment_text=comment_text)
        except Exception:
            pass

        try:
            from friend_ledger import record_interaction
            record_interaction(
                username=handle,
                name=handle,
                action="comment",
                post_url=post_url,
                comment_text=comment_text,
                screenshot=str(shot_path.relative_to(BASE_DIR))
            )
        except Exception:
            pass

        return True
    except Exception as e:
        print(f"   ⚠️ 留言執行異常: {e}", flush=True)
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
