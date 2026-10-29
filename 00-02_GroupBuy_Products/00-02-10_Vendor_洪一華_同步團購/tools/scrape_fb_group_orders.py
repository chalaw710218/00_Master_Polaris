"""
Polaris AI Cabinet - Facebook Group Order Scraper & Sentinel
=============================================================
專為「生活管家，就醬點！」打造之社團留言自動抓單與自動巡邏引擎。
支援：
1. 指定貼文 URL 抓單
2. 全自動社團巡邏模式 (--patrol)：自動遍歷 watched_groups.json 搜尋「生活管家，就醬點！」貼文收單
"""

import os
import sys
import re
import csv
import json
import time
import argparse
import urllib.parse
from datetime import datetime
from playwright.sync_api import sync_playwright

DEFAULT_USER_DATA_DIR = os.path.expanduser(r"~\.gemini\polaris_fb_browser_data")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "00-02-10-03_Order_Tracker_Template.csv")
CONFIG_PATH = os.path.join(BASE_DIR, "watched_groups.json")

def parse_groupbuy_comment(text: str):
    """
    解析台灣社群團購口語化留言：
    - 辨識: +1, +2, ＋1, ＋2, 買2, 要2包, 2份, 2盒
    - 辨識配送意向: 外送, 送到府, 自取, 門市拿
    """
    cleaned = text.strip()
    
    plus_match = re.search(r'[+＋]\s*(\d+)', cleaned)
    if plus_match:
        qty = int(plus_match.group(1))
    else:
        unit_match = re.search(r'(?:要|買|加|來)?\s*(\d+)\s*(?:包|份|個|組|盒|罐|尾|條|公斤|斤|箱)', cleaned)
        if unit_match:
            qty = int(unit_match.group(1))
        else:
            qty = 0
            
    if re.search(r'(外送|到府|送到家|送正氣|送家)', cleaned):
        fulfillment = "外送(四五六19-21)"
        delivery_fee = 99
    elif re.search(r'(自取|店取|過去拿|門市)', cleaned):
        fulfillment = "門市自取"
        delivery_fee = 0
    else:
        fulfillment = "待確認"
        delivery_fee = 0

    return qty, fulfillment, delivery_fee

def extract_comments_from_page(page, post_url: str):
    print(f"[*] 正在分析貼文: {post_url}")
    page.goto(post_url, wait_until="networkidle", timeout=60000)
    time.sleep(3)
    
    # 循環展開留言
    print("[*] 正在展開留言與回覆...")
    for _ in range(12):
        try:
            expand_buttons = page.locator("div[role='button']:has-text('查看更多留言'), div[role='button']:has-text('查看其他留言'), div[role='button']:has-text('則回覆'), span:has-text('查看更多留言')")
            count = expand_buttons.count()
            if count > 0:
                for i in range(count):
                    try:
                        expand_buttons.nth(i).click(timeout=1000)
                        time.sleep(0.3)
                    except:
                        pass
        except:
            pass
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(0.8)

    orders = []
    comment_elements = page.locator("div[role='article']")
    total_comments = comment_elements.count()
    
    for i in range(total_comments):
        try:
            el = comment_elements.nth(i)
            text = el.inner_text()
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            if not lines:
                continue
            
            author = lines[0]
            if author in ["讚", "回覆", "分享", "傳送訊息", "Top fan", "頭號粉絲"]:
                continue
            
            comment_body = " ".join(lines[1:])
            qty, fulfillment, delivery_fee = parse_groupbuy_comment(comment_body)
            
            if qty > 0:
                orders.append({
                    "author": author,
                    "raw_comment": comment_body,
                    "qty": qty,
                    "fulfillment": fulfillment,
                    "delivery_fee": delivery_fee,
                    "post_url": post_url
                })
        except:
            continue
            
    return orders

def patrol_watched_groups(page, config):
    keywords = config.get("search_keywords", ["生活管家，就醬點！"])
    groups = config.get("target_groups", [])
    primary_kw = keywords[0]
    
    all_orders = []
    
    for g in groups:
        g_name = g.get("name", "未命名社團")
        g_url = g.get("url", "").rstrip("/")
        if not g_url or "SAMPLE_GROUP" in g_url:
            print(f"[-] 略過尚未配置真實網址的社團: {g_name}")
            continue
            
        print(f"\n[🔍 巡邏社團] {g_name} ({g_url})")
        # 構造社團搜尋 URL
        encoded_kw = urllib.parse.quote(primary_kw)
        search_url = f"{g_url}/search/?q={encoded_kw}"
        print(f"[*] 搜尋標的關鍵字: 「{primary_kw}」 -> {search_url}")
        
        try:
            page.goto(search_url, wait_until="networkidle", timeout=45000)
            time.sleep(3)
            
            # 尋找搜尋結果貼文連結
            post_links = set()
            links = page.locator("a[href*='/posts/'], a[href*='/permalink/']")
            for i in range(min(links.count(), 10)):
                href = links.nth(i).get_attribute("href")
                if href:
                    clean_href = href.split("?")[0]
                    post_links.add(clean_href)
                    
            print(f"[*] 找到 {len(post_links)} 篇「{primary_kw}」相關貼文")
            for p_url in post_links:
                post_orders = extract_comments_from_page(page, p_url)
                all_orders.extend(post_orders)
        except Exception as e:
            print(f"[!] 巡邏社團 {g_name} 失敗: {e}")
            
    return all_orders

def save_orders_to_csv(orders, csv_path, product_code="HYH-001", product_name="生活管家選品"):
    if not orders:
        return
        
    date_str = datetime.now().strftime("%Y%m%d")
    file_exists = os.path.exists(csv_path)
    
    with open(csv_path, mode="a", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        if not file_exists or os.path.getsize(csv_path) == 0:
            writer.writerow([
                "OrderId", "CustomerName", "Phone", "ProductCode", "ProductName",
                "Quantity", "FulfillmentType", "DeliveryFee", "Subtotal",
                "PaymentStatus", "FulfillmentStatus", "VendorSource", "Notes"
            ])
            
        for idx, o in enumerate(orders, 1):
            order_id = f"HYH-{date_str}-{idx:03d}"
            writer.writerow([
                order_id,
                o["author"],
                "",
                product_code,
                product_name,
                o["qty"],
                o["fulfillment"],
                o["delivery_fee"],
                "",
                "未付款",
                "待提貨",
                "社團巡邏",
                f"來源: {o.get('post_url', '')} | 留言: {o['raw_comment']}"
            ])
            
    print(f"\n[+] 數據已成功自動同步寫入清冊：\n    {csv_path}")

def main():
    parser = argparse.ArgumentParser(description="Facebook 社團 +1 留言自動抓單與定點巡邏工具")
    parser.add_argument("--url", help="指定單篇 Facebook 貼文網址（若有提供則直接抓該篇）")
    parser.add_argument("--patrol", action="store_true", help="啟動社團定點巡邏模式（自動搜尋「生活管家，就醬點！」）")
    parser.add_argument("--headed", action="store_true", help="以可見視窗開啟（首次登入或調試）")
    parser.add_argument("--product_code", default="HYH-001", help="商品代碼")
    parser.add_argument("--product_name", default="生活管家選品", help="商品名稱")
    parser.add_argument("--csv", default=DEFAULT_CSV_PATH, help="輸出 CSV 路徑")
    args = parser.parse_args()

    os.makedirs(DEFAULT_USER_DATA_DIR, exist_ok=True)
    
    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=DEFAULT_USER_DATA_DIR,
            headless=not args.headed,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"],
            viewport=None
        )
        
        page = browser_context.pages[0] if browser_context.pages else browser_context.new_page()
        
        # 首次登入檢查
        if args.url and ("facebook.com" in args.url) and args.headed and not args.patrol:
            print("[*] 正在開啟 Facebook 首頁進行登入/連線驗證...")
            page.goto(args.url)
            print("[*] 請在彈出的瀏覽器視窗中完成登入，完成後關閉視窗或按 Enter 結束。")
            if sys.stdin.isatty():
                input("登入完成後請按 Enter 鍵...")
            else:
                time.sleep(10)
            browser_context.close()
            return

        orders = []
        if args.patrol:
            print("[*] 啟動【社團定點巡邏模式】...")
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    config = json.load(f)
            else:
                config = {"search_keywords": ["生活管家，就醬點！"], "target_groups": []}
            orders = patrol_watched_groups(page, config)
        elif args.url:
            orders = extract_comments_from_page(page, args.url)
        else:
            print("[!] 請提供 --url 或指定 --patrol 巡邏模式！")
            browser_context.close()
            return
            
        browser_context.close()

    if not orders:
        print("\n[-] 巡邏結束，未發現符合條件的新喊單留言。")
        return

    print("\n" + "="*60)
    print(f"🎉 成功解析訂單！累計共 {len(orders)} 筆顧客喊單")
    print("="*60)
    
    total_qty = sum(o["qty"] for o in orders)
    print(f"{'顧客姓名':<15} | {'數量':<5} | {'履約方式':<15} | {'原始留言'}")
    print("-" * 60)
    for o in orders:
        print(f"{o['author']:<15} | {o['qty']:<5} | {o['fulfillment']:<15} | {o['raw_comment'][:30]}")

    print("-" * 60)
    print(f"📊 總訂購件數：{total_qty} 件 (是否達 +3 門檻: {'✅ 是' if total_qty >= 3 else '❌ 否'})")
    
    save_orders_to_csv(orders, args.csv, args.product_code, args.product_name)

if __name__ == "__main__":
    main()
