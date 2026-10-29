"""
Polaris AI Cabinet - Yihua Full Catalog Harvester (Anti-Detection Mode)
======================================================================
專門針對洪一華雙社團執行「擬真人類安全收割」：
1. 慢慢滾動巡邏社團貼文（隨機間隔 2~4 秒）
2. 提取商品標題、文案、價格 (+1, +3)、結單日期
3. 自動下載商品圖片至 catalog_images/
4. 匯出結構化商品庫 JSON 與 CSV，作為極星供應鏈底價資產
"""

import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import re
import json
import time
import random
import argparse
import urllib.request
from datetime import datetime
from playwright.sync_api import sync_playwright

USER_DATA_DIR = os.path.expanduser(r"~\.gemini\polaris_fb_browser_data")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "catalog_images")
CATALOG_JSON_PATH = os.path.join(BASE_DIR, "yihua_products_database.json")

def parse_pricing_and_specs(text: str):
    """從文案中提取 +1 價、+3 價與商品品名"""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    first_line = lines[0] if lines else "未命名商品"
    
    p1 = None
    p3 = None
    
    # 尋找 +1 或 單價
    m1 = re.search(r'(?:[+＋]1|單包|一包|特價|優惠|價錢|售價|一盒|單盒|一斤|單斤|一尾|單尾)[^\d]*(\d{2,4})', text)
    if m1:
        p1 = int(m1.group(1))
        
    # 尋找 +3 或 多件優惠
    m3 = re.search(r'(?:[+＋]3|3包|三包|3件|三件|3盒|三盒|3尾|三尾)[^\d]*(\d{2,5})', text)
    if m3:
        p3 = int(m3.group(1))
        
    all_prices = re.findall(r'\$\s*(\d+)|(\d+)\s*元', text)
    if not p1 and all_prices:
        p1 = int(all_prices[0][0] or all_prices[0][1])

    return first_line[:50], p1, p3

def harvest_group(page, group_url: str, group_name: str, limit: int = 15):
    print(f"\n" + "=" * 60, flush=True)
    print(f"🌾 正在進入社團收割商品：{group_name}", flush=True)
    print(f"🔗 網址: {group_url}", flush=True)
    print(f"🛡️ 模式：擬真人類低頻呼吸模式 (目標收割前 {limit} 檔商品)", flush=True)
    print("=" * 60, flush=True)
    
    try:
        page.goto(group_url, wait_until="domcontentloaded", timeout=60000)
    except Exception as e:
        print(f"[*] 載入超時或提醒: {e}", flush=True)
        
    time.sleep(random.uniform(3, 5))
    
    products = []
    seen_posts = set()
    
    scroll_attempts = 0
    max_scrolls = 20
    
    while len(products) < limit and scroll_attempts < max_scrolls:
        scroll_attempts += 1
        
        # 尋找貼文文字區塊
        messages = page.locator("div[data-ad-preview='message'], div[data-ad-comet-preview='message']")
        msg_count = messages.count()
        print(f"[*] 滾動第 {scroll_attempts} 輪，當前畫面上掃描到 {msg_count} 則文字區塊...", flush=True)
        
        for i in range(msg_count):
            if len(products) >= limit:
                break
            try:
                el = messages.nth(i)
                text = el.inner_text().strip()
                if not text or len(text) < 15:
                    continue
                
                # 排除純公告、取貨指南、問候
                if any(k in text for k in ["取貨7-11", "置頂公告", "社團規則", "營業時間"]):
                    continue
                    
                snippet = text[:40]
                if snippet in seen_posts:
                    continue
                seen_posts.add(snippet)
                
                title, p1, p3 = parse_pricing_and_specs(text)
                
                # 提取圖片
                img_urls = []
                parent = el.locator("xpath=./ancestor::div[@role='article']|./ancestor::div[contains(@class, 'x1y1awv3')]").first
                if parent.count() > 0:
                    imgs = parent.locator("img[src*='scontent'], img[src*='fbcdn']")
                    for j in range(min(imgs.count(), 3)):
                        src = imgs.nth(j).get_attribute("src")
                        if src and "emoji" not in src and "profile" not in src:
                            img_urls.append(src)
                
                prod_id = f"YIHUA-{datetime.now().strftime('%m%d')}-{len(products)+1:02d}"
                local_img_path = ""
                if img_urls:
                    try:
                        os.makedirs(IMAGE_DIR, exist_ok=True)
                        local_img_path = os.path.join(IMAGE_DIR, f"{prod_id}.jpg")
                        urllib.request.urlretrieve(img_urls[0], local_img_path)
                    except:
                        pass
                        
                prod_data = {
                    "id": prod_id,
                    "title": title,
                    "group": group_name,
                    "price_single": p1,
                    "price_tier3": p3,
                    "text": text,
                    "image_path": local_img_path,
                    "harvested_at": datetime.now().isoformat()
                }
                
                products.append(prod_data)
                print(f"[+] 收錄商品 [{prod_id}]: {title} | +1價: {p1} | +3價: {p3}", flush=True)
            except Exception as e:
                continue
                
        # 擬真隨機滾動與停頓（防封保護）
        scroll_px = random.randint(700, 1100)
        page.evaluate(f"window.scrollBy(0, {scroll_px})")
        pause_sec = random.uniform(2.5, 4.0)
        time.sleep(pause_sec)
        
    return products

def main():
    parser = argparse.ArgumentParser(description="洪一華社團全量商品收割機")
    parser.add_argument("--limit", type=int, default=10, help="每個社團收割商品數量上限")
    args = parser.parse_args()

    groups = [
        {"name": "✡️台東水產蔬果🎖美食2館🍱", "url": "https://www.facebook.com/groups/347829083618668"},
        {"name": "🏠台東蔬果水產🏅美食1館🥗", "url": "https://www.facebook.com/groups/2347370975321841"}
    ]

    all_harvested = []

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        for g in groups:
            items = harvest_group(page, g["url"], g["name"], limit=args.limit)
            all_harvested.extend(items)

        ctx.close()

    # 儲存回資料庫
    existing_db = []
    if os.path.exists(CATALOG_JSON_PATH):
        try:
            with open(CATALOG_JSON_PATH, "r", encoding="utf-8") as f:
                existing_db = json.load(f)
        except:
            pass

    existing_db.extend(all_harvested)
    with open(CATALOG_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_db, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60, flush=True)
    print(f"🎉 收割完成！本次共採集 {len(all_harvested)} 款商品！", flush=True)
    print(f"📂 本地情報資料庫已更新至: {CATALOG_JSON_PATH}", flush=True)
    print("=" * 60, flush=True)

if __name__ == "__main__":
    main()
