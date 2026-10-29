"""
Polaris AI Cabinet - Page Comment Order Listener
=================================================
監聽「生活的一部分，就醬點！」粉專指定貼文的最新留言，
自動解析 +1 / +2 / 自取 / 外送，並寫入 Order_Tracker.csv。
"""

import os
import sys
import re
import csv
import json
import requests
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
ENV_PATH = ROOT_DIR / ".secrets.env"
BASE_DIR = ROOT_DIR / "00-02_GroupBuy_Products" / "00-02-10_Vendor_洪一華_同步團購"
CSV_PATH = BASE_DIR / "00-02-10-03_Order_Tracker_Template.csv"

def load_env(env_path):
    env_vars = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                env_vars[key.strip()] = val.strip()
    return env_vars

ENV = load_env(ENV_PATH)
TOKEN = ENV.get("FB_PAGE_ACCESS_TOKEN")
TARGET_POST_ID = "110505444816362_1146589971383238" # 剛發布的測試貼文 ID

def parse_comment(text: str):
    cleaned = text.strip()
    
    # 模式: +1, +2, ＋1, ＋2
    plus_match = re.search(r'[+＋]\s*(\d+)', cleaned)
    if plus_match:
        qty = int(plus_match.group(1))
    else:
        unit_match = re.search(r'(?:要|買|加|來)?\s*(\d+)\s*(?:包|份|個|組|盒|罐|尾|條|斤|箱)', cleaned)
        qty = int(unit_match.group(1)) if unit_match else 0
        
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

def check_orders(post_id=TARGET_POST_ID):
    if not TOKEN:
        print("[-] 未設定 Token")
        return []
        
    url = f"https://graph.facebook.com/v20.0/{post_id}/comments?access_token={TOKEN}&limit=100"
    res = requests.get(url).json()
    
    data = res.get("data", [])
    orders = []
    
    for c in data:
        msg = c.get("message", "")
        # 排除官方自己的第一則留言
        if "【管家公告" in msg:
            continue
            
        author = c.get("from", {}).get("name", "Facebook 用戶")
        qty, fulfillment, delivery_fee = parse_comment(msg)
        
        if qty > 0:
            orders.append({
                "author": author,
                "qty": qty,
                "fulfillment": fulfillment,
                "delivery_fee": delivery_fee,
                "comment": msg,
                "created_time": c.get("created_time", "")
            })
            
    return orders

def main():
    print("=" * 60)
    print("📡 極星即時留言收單監聽器")
    print(f"🎯 目標貼文 ID: {TARGET_POST_ID}")
    print("=" * 60)
    
    orders = check_orders()
    if not orders:
        print("[*] 目前貼文底下尚無新的喊單留言（除管家公告第一則留言外）。")
        return
        
    total_qty = sum(o["qty"] for o in orders)
    print(f"🎉 成功統計到 {len(orders)} 筆訂單！累計總數量：{total_qty} 件\n")
    print(f"{'顧客姓名':<15} | {'數量':<5} | {'履約方式':<15} | {'原始留言'}")
    print("-" * 60)
    for o in orders:
        print(f"{o['author']:<15} | {o['qty']:<5} | {o['fulfillment']:<15} | {o['comment']}")
        
    print("-" * 60)
    print(f"📊 是否達到 +3 批發級距門檻: {'✅ 是' if total_qty >= 3 else '❌ 否 (待湊單)'}")

if __name__ == "__main__":
    main()
