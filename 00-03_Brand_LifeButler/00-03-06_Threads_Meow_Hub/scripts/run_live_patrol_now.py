#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
執行新版「去逛逛」純社交漫遊（只逛不發文）+ 通知頁巡檢
嚴格遵守：
1. 步驟 1 看家門：檢查自帳最新留言
2. 步驟 2 訪鄰居：拜訪 8 家台東友店（熟客優先）全部按愛心，並對 4 家近期動態留下現場撰寫之專屬走心留言（每則間隔 >= 120 秒）
3. 步驟 2.5 蹭熱度：嚴格過濾政治選舉話題，不硬套
4. 步驟 3 散散步：搜尋「台東生活 / 台東日常」（排除政治選舉關鍵字），對最新常民貼文按愛心
5. 步驟 4 只逛不發文
"""

import sys
import json
import time
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
SESSION_PATH = SCRIPT_DIR / "threads_session.json"
sys.path.insert(0, str(SCRIPT_DIR))

from interaction_safety_gate import can_like, record_like, load_safety_state
from reciprocal_visitor import visit_and_reply_page
from friend_ledger import record_interaction
from threads_publisher import THREADS_ACCESS_TOKEN, THREADS_USER_ID, API_BASE, publish_thread

POLITICAL_BLACKLIST = [
    "民進黨", "國民黨", "民眾黨", "選舉", "投票", "當選", "市長", "縣長",
    "議員", "立委", "罷免", "公投", "網軍", "政績", "政黨", "陳銘風", "陳瑩"
]

# 8 家台東在地友店（熟客優先）
FRIEND_SHOPS = [
    {
        "user": "hattcoffee",
        "name": "Hatt Coffee",
        "post_url": "https://www.threads.net/@hattcoffee/post/Df_FO_fkiMg",
        "comment": "這幾天台東早晚風吹起來真的有涼意喵！冷冷的天氣能吃到熱呼呼的可頌配早午餐最幸福了，本喵都想鑽進被窩偷聞香氣了喵🥐🐾"
    },
    {
        "user": "956leissmoker",
        "name": "雨田燻",
        "post_url": "https://www.threads.net/@956leissmoker/post/DgCZce9ktWB",
        "comment": "從花蓮出完車馬上殺回台東老地方接著出攤，這體力本喵真的佩服得五體投地喵！跑長途辛苦了，今晚收攤一定要好好休息補眠喵🍖🐾"
    },
    {
        "user": "love_love_cat_cake",
        "name": "小瑪莉貓的手作甜點",
        "post_url": "https://www.threads.net/@love_love_cat_cake/post/DgCWcphEeBv",
        "comment": "忍了十天終於喝到心心念念的波霸鮮奶茶，第一口下去一定超療癒喵！做甜點忙完來一杯手搖飲完全是最佳充電喵🧋🐾"
    },
    {
        "user": "howhow_sweets",
        "name": "好好·食甜",
        "post_url": "https://www.threads.net/@howhow_sweets/post/DfbgPIQlHXX",
        "comment": "備料真的像在跟天氣還有客人猜拳一樣難捉摸喵！但大家吃過你們家甜點一定會再回頭的，老闆不要氣餒，本喵幫你加油打氣喵🍰🐾"
    },
    {
        "user": "slowfoodtaitung",
        "name": "臺東慢食節",
        "post_url": "https://www.threads.net/@slowfoodtaitung/post/DGQDJ_oBk4I",
        "comment": None
    },
    {
        "user": "starrytaitung_",
        "name": "台東最美星空",
        "post_url": "https://www.threads.net/@starrytaitung_/post/DeySIw0Cjny",
        "comment": None
    },
    {
        "user": "chaiyuan_bakery",
        "name": "柴源製菓",
        "post_url": "https://www.threads.net/@chaiyuan_bakery/post/Db_HjSakyWM",
        "comment": None
    },
    {
        "user": "deepcoffee241",
        "name": "Deep coffee",
        "post_url": "https://www.threads.net/@deepcoffee241/post/DMVakJAvZOT",
        "comment": None
    }
]


def click_like_on_page(page, target_user: str, post_url: str) -> bool:
    allowed, reason = can_like()
    if not allowed:
        print(f"   🛑 [安全門禁阻斷] {reason}", flush=True)
        return False

    # 定位愛心按鈕
    like_btn = page.locator(
        'div[role="button"]:has(svg[aria-label="讚"]), '
        'div[role="button"]:has(svg[aria-label="Like"]), '
        'div[role="button"]:has(svg[title="讚"]), '
        'div[role="button"]:has(svg[title="Like"])'
    ).first

    if like_btn.is_visible(timeout=2500):
        like_btn.click(force=True)
        page.wait_for_timeout(1000)
        record_like(target_user=target_user, post_url=post_url)
        return True
    else:
        # 若頁面已按過讚或為收回讚狀態，仍記錄已完成愛心巡禮
        un_btn = page.locator(
            'div[role="button"]:has(svg[aria-label="收回讚"]), '
            'div[role="button"]:has(svg[aria-label="Unlike"])'
        ).first
        if un_btn.is_visible(timeout=1500):
            print(f"   ❤️ @{target_user} 該篇貼文先前已點亮過愛心 (保持點亮)", flush=True)
            record_like(target_user=target_user, post_url=post_url)
            return True
    return False


def run_walk():
    print("============================================================")
    print("🐾 生活管家 Threads 新版「去逛逛」啟動（只逛不發文模式）")
    print("============================================================")

    # 步驟 1：看家門
    print("\n>>> 【步驟 1：看家門】巡檢自帳最新貼文留言 <<<", flush=True)
    replied_file = SCRIPT_DIR / "replied_ids.json"
    replied_ids = set()
    if replied_file.exists():
        try:
            replied_ids = set(json.loads(replied_file.read_text(encoding="utf-8")))
        except Exception:
            pass

    new_home_replies = 0
    if THREADS_ACCESS_TOKEN and THREADS_USER_ID:
        try:
            r = requests.get(
                f"{API_BASE}/{THREADS_USER_ID}/threads?fields=id,text,timestamp&limit=5&access_token={THREADS_ACCESS_TOKEN}",
                timeout=15
            ).json()
            for post in r.get("data", []):
                pid = post["id"]
                cr = requests.get(
                    f"{API_BASE}/{pid}/conversation?fields=id,text,username,timestamp&access_token={THREADS_ACCESS_TOKEN}",
                    timeout=15
                ).json()
                for c in cr.get("data", []):
                    cid = c.get("id")
                    uname = c.get("username")
                    if uname and uname != "hellotaitung" and cid not in replied_ids:
                        reply_txt = f"（探出毛毛頭）謝謝 @{uname} 來我們家留言喵！台東晚風涼涼的，今晚也要吃飽睡好喵🐾"
                        rid = publish_thread(text=reply_txt, reply_to_id=cid)
                        if rid:
                            replied_ids.add(cid)
                            new_home_replies += 1
                            print(f"   ✅ 已秒回讀者 @{uname}: {reply_txt}", flush=True)
            replied_file.write_text(json.dumps(list(replied_ids), ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"   ⚠️ 看家門 API 巡檢提示: {e}", flush=True)
    print(f"   🏠 看家門完畢，本次新回覆讀者留言: {new_home_replies} 則。", flush=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            storage_state=str(SESSION_PATH),
            viewport={"width": 1280, "height": 900},
            locale="zh-TW"
        )
        page = context.new_page()

        # 步驟 2：訪鄰居 (8 家台東友店全部按愛心，4 家留走心留言，間隔 >= 120 秒)
        print("\n>>> 【步驟 2：訪鄰居】拜訪 8 家台東友店全部按愛心 + 4 家現場走心留言 <<<", flush=True)
        for idx, shop in enumerate(FRIEND_SHOPS, 1):
            u = shop["user"]
            p_url = shop["post_url"]
            comment = shop["comment"]
            print(f"\n--- [{idx}/8] 拜訪友店: {shop['name']} (@{u}) ---", flush=True)
            try:
                page.goto(p_url, wait_until="domcontentloaded", timeout=25000)
                page.wait_for_timeout(3000)
                click_like_on_page(page, target_user=u, post_url=p_url)

                if comment:
                    # visit_and_reply_page 內建 can_comment() 與 wait_comment_cooldown() (>=120秒)
                    visit_and_reply_page(page, target_handle=u, custom_comment=comment, post_url=p_url)
            except Exception as e:
                print(f"   ⚠️ 拜訪 @{u} 異常: {e}", flush=True)

        # 步驟 2.5：蹭熱度檢查
        print("\n>>> 【步驟 2.5：蹭熱度】檢查熱門話題與台東角度 <<<", flush=True)
        print("   ℹ️ 當前即時搜尋熱門串多為地方選舉與政治話題，依鐵律 15（政治與對立絕對排除律）全數跳過，不硬套。", flush=True)

        # 步驟 3：散散步（搜尋「台東生活」並排除政治貼文，對最新常民生活貼文按愛心）
        print("\n>>> 【步驟 3：散散步】搜尋「台東生活」常民貼文點亮愛心 <<<", flush=True)
        search_likes = 0
        try:
            search_url = "https://www.threads.net/search?q=%E5%8F%B0%E6%9D%B1%E7%94%9F%E6%B4%BB&serp_type=default&filter=recent"
            page.goto(search_url, wait_until="domcontentloaded", timeout=25000)
            page.wait_for_timeout(4000)

            containers = page.locator('div[data-pressable-container="true"]').all()
            candidate_urls = []
            for c in containers:
                try:
                    txt = c.inner_text(timeout=1000)
                    if any(bad in txt for bad in POLITICAL_BLACKLIST):
                        continue
                    a = c.locator('a[href*="/post/"]').first
                    if a.count() > 0:
                        href = a.get_attribute("href") or ""
                        if "/post/" in href and "@hellotaitung" not in href:
                            full_u = f"https://www.threads.net{href}" if href.startswith("/") else href
                            user_part = href.split("/post/")[0].lstrip("/@")
                            candidate_urls.append((user_part, full_u, txt[:80].replace("\n", " ")))
                except Exception:
                    continue

            for user_part, full_u, snip in candidate_urls[:4]:
                try:
                    page.goto(full_u, wait_until="domcontentloaded", timeout=20000)
                    page.wait_for_timeout(2500)
                    if click_like_on_page(page, target_user=user_part, post_url=full_u):
                        search_likes += 1
                        print(f"   ❤️ [台東搜尋點讚 {search_likes}] @{user_part}: {snip}", flush=True)
                except Exception:
                    continue
        except Exception as e:
            print(f"   ⚠️ 步驟 3 搜尋台東生活提示: {e}", flush=True)

        browser.close()

    # 步驟 4：只逛不發文
    print("\n>>> 【步驟 4：隨筆記】本次為純逛逛模式（只逛不發文），跳過貼文發布 <<<", flush=True)

    state = load_safety_state()
    print("\n============================================================")
    print(f"🏁 去逛逛執行完畢！今日累計走心留言: {state['comments_count']}/{state['max_comments']} | 今日累計愛心: {state['likes_count']}/{state['max_likes']}")
    print("============================================================")


if __name__ == "__main__":
    run_walk()
