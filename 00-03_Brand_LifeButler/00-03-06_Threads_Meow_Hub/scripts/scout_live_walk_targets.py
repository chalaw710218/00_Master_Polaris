#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
即時嗅探台東友店與 Threads「台東」搜尋最新貼文內容，供影與喵編現場撰寫走心留言
"""
import sys
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"

# 優先熟客 + 在地友店共 9 家
SHOPS = [
    {"user": "hattcoffee", "name": "Hatt Coffee"},
    {"user": "slowfoodtaitung", "name": "臺東慢食節"},
    {"user": "956leissmoker", "name": "雨田燻"},
    {"user": "starrytaitung_", "name": "台東最美星空"},
    {"user": "love_love_cat_cake", "name": "小瑪莉貓的手作甜點"},
    {"user": "howhow_sweets", "name": "好好·食甜"},
    {"user": "sinapayan_youth", "name": "喜拿巴漾青年工作站"},
    {"user": "chaiyuan_bakery", "name": "柴源製菓"},
    {"user": "deepcoffee241", "name": "Deep coffee"}
]

def inspect_targets():
    results = {"shops": [], "search_taitung": []}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_PATH),
            viewport={"width": 1280, "height": 900},
            locale="zh-TW"
        )
        page = context.new_page()

        for s in SHOPS:
            u = s["user"]
            url = f"https://www.threads.net/@{u}"
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(2800)
                links = page.locator('a[href*="/post/"]').all()
                post_url = None
                for a in links:
                    href = a.get_attribute("href") or ""
                    if "/post/" in href:
                        post_url = f"https://www.threads.net{href}" if href.startswith("/") else href
                        break
                snippet = ""
                if post_url:
                    # 抓取第一篇貼文區塊文字
                    pressables = page.locator('div[data-pressable-container="true"]').all()
                    if pressables:
                        snippet = pressables[0].inner_text(timeout=1500)[:220].replace("\n", " ")
                results["shops"].append({
                    "user": u,
                    "name": s["name"],
                    "post_url": post_url,
                    "snippet": snippet
                })
                print(f"✅ @{u}: {post_url} | {snippet[:80]}", flush=True)
            except Exception as e:
                print(f"⚠️ @{u}: {e}", flush=True)

        # 搜尋「台東」最新貼文
        try:
            search_url = "https://www.threads.net/search?q=%E5%8F%B0%E6%9D%B1&serp_type=default&filter=recent"
            page.goto(search_url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(3500)
            containers = page.locator('div[data-pressable-container="true"]').all()
            for c in containers[:8]:
                try:
                    txt = c.inner_text(timeout=1000).replace("\n", " ")
                    link_el = c.locator('a[href*="/post/"]').first
                    href = link_el.get_attribute("href") if link_el.count() > 0 else ""
                    p_url = f"https://www.threads.net{href}" if href and href.startswith("/") else href
                    if p_url:
                        results["search_taitung"].append({
                            "post_url": p_url,
                            "snippet": txt[:220]
                        })
                        print(f"🔍 [台東搜尋] {p_url} | {txt[:80]}", flush=True)
                except Exception:
                    continue
        except Exception as e:
            print(f"⚠️ 搜尋台東失敗: {e}", flush=True)

        browser.close()

    out_path = SCRIPT_DIR / "latest_scout_targets.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    inspect_targets()
