#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Threads RSS Sentinel (脆友動態巡邏與自動化走心互動哨兵)
北極星專屬技能: threads-rss-sentinel
作者: 影 (Shadow / 小編)
"""

import sys
import os
import json
import re
import html
import ssl
import argparse
from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Default priority targets in Taitung
DEFAULT_TARGETS = [
    {"username": "hungryyyummy", "name": "台東餓人 ✶ 台東美食", "tag": "美食/宵夜/日常"},
    {"username": "slowfoodtaitung", "name": "臺東慢食節", "tag": "在地產地/文化旬味"},
    {"username": "travel_zztaitung", "name": "台東製造", "tag": "在地人文/生活自媒體"},
    {"username": "tsao_min", "name": "草民 Tsao Min", "tag": "老屋早午餐/慢活"},
    {"username": "hattcoffee", "name": "草月咖啡館", "tag": "獨立咖啡/日常"},
    {"username": "taitung_man", "name": "台東男子", "tag": "在地生活/氣候/閒聊"}
]

def clean_html(raw_html):
    """Clean HTML tags and unescape entities."""
    if not raw_html:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    clean = html.unescape(clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def fetch_threads_feed(username, timeout=12):
    """Fetch RSS feed for a Threads user via OpenRSS."""
    url = f"https://openrss.org/feed/www.threads.com/@{username}"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            data = resp.read()
            root = ET.fromstring(data)
            items = []
            for item in root.findall('.//item'):
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                desc = item.find('description').text if item.find('description') is not None else ''
                pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                guid = item.find('guid').text if item.find('guid') is not None else link
                
                clean_desc = clean_html(desc)
                # Extract post ID from link
                m = re.search(r'/post/([A-Za-z0-9_-]+)', link)
                post_id = m.group(1) if m else guid
                
                items.append({
                    "username": username,
                    "post_id": post_id,
                    "title": clean_html(title),
                    "link": link,
                    "content": clean_desc,
                    "pub_date": pub_date
                })
            return {"status": "ok", "items": items, "error": None}
    except Exception as e:
        return {"status": "error", "items": [], "error": str(e)}

def generate_draft_replies(post):
    """Generate high-EQ tactical reply suggestions based on post content."""
    content = post.get("content", "") or post.get("title", "")
    username = post.get("username", "")
    
    # Analyze topic heuristics
    is_food = any(k in content for k in ["吃", "美味", "咖啡", "肉", "店", "午餐", "晚餐", "宵夜", "甜點", "菜單", "麵"])
    is_weather = any(k in content for k in ["雨", "颱風", "風", "熱", "冷", "天氣", "太陽", "陰天"])
    is_tired_or_busy = any(k in content for k in ["累", "忙", "休息", "下班", "放假", "週末", "休假", "想睡"])
    
    drafts = []
    
    # Option 1: 小編（影）· 溫暖日常共鳴
    if is_weather:
        drafts.append({
            "persona": "小編（影）· 溫暖守候",
            "text": "台東這幾天的風真的有感～出門巡店真的要小心！你們今天店裡一切都安好嗎？☕"
        })
    elif is_food:
        drafts.append({
            "persona": "小編（影）· 走心同溫層",
            "text": "看著看著螢幕直接飄出香味是正常的嗎...默默收進小編私房口袋名單，這週放假一定要去朝聖！✨"
        })
    elif is_tired_or_busy:
        drafts.append({
            "persona": "小編（影）· 體貼陪伴",
            "text": "辛苦了！台東的節奏就是要提醒大家累了先停下來喘口氣～今晚給自己點一杯好喝的好好犒賞一下吧 🌿"
        })
    else:
        drafts.append({
            "persona": "小編（影）· 真誠互動",
            "text": "完全懂這種感覺！在台東生活最迷人的就是這些小細節，看完心裡一陣舒坦～🍃"
        })

    # Option 2: 小編（影）· 機智幽默 / 熟人吐槽
    if is_food:
        drafts.append({
            "persona": "小編（影）· 深夜幽默",
            "text": "這個時間點發這個太犯規了吧！闆仔在旁邊看著螢幕已經開始翻冰箱了啦 🤣"
        })
    else:
        drafts.append({
            "persona": "小編（影）· 台東鄰里感",
            "text": "這篇不能只有我看到！台東在地人的默契真的都在這篇貼文裡了 💯"
        })

    # Option 3: 喵編 · 傲嬌吃貨貓
    if is_food:
        drafts.append({
            "persona": "喵編 · 吃貨本色",
            "text": "喵！本喵隔著手機螢幕爪子都在蠢蠢欲動了...那個肉肉可以分一塊給打工貓嗎 🐾🐟"
        })
    else:
        drafts.append({
            "persona": "喵編 · 傲嬌打氣",
            "text": "喵嗚～不管今天發生什麼事，先摸摸貓貓吸一口，台東的陽光明天還是會照常出來的喵 🐾"
        })
        
    return drafts

def run_sentinel(targets, cache_file, limit_per_user=5, dry_run=False):
    """Run sentinel monitoring loop across all specified targets."""
    # Load cache
    seen_ids = set()
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                seen_ids = set(data.get("seen_ids", []))
        except Exception:
            pass
            
    print(f"📡 [Threads Sentinel] 開始海巡... 目前已記錄快照: {len(seen_ids)} 筆貼文")
    
    new_findings = []
    
    for t in targets:
        uname = t["username"]
        name = t.get("name", uname)
        print(f"🔍 掃描目標: @{uname} ({name})...", end=" ", flush=True)
        
        feed = fetch_threads_feed(uname)
        if feed["status"] != "ok":
            print(f"❌ 抓取失敗: {feed['error']}")
            continue
            
        items = feed["items"][:limit_per_user]
        user_new_count = 0
        
        for item in items:
            pid = item["post_id"]
            if pid not in seen_ids:
                user_new_count += 1
                drafts = generate_draft_replies(item)
                item["draft_replies"] = drafts
                item["detected_at"] = datetime.now().isoformat()
                item["author_name"] = name
                new_findings.append(item)
                if not dry_run:
                    seen_ids.add(pid)
                    
        if user_new_count > 0:
            print(f"✨ 發現 {user_new_count} 則新動態！")
        else:
            print(f"已是最新 ({len(items)} 則已讀)")
            
    # Save cache
    if not dry_run:
        try:
            os.makedirs(os.path.dirname(os.path.abspath(cache_file)), exist_ok=True)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({
                    "last_updated": datetime.now().isoformat(),
                    "total_seen": len(seen_ids),
                    "seen_ids": list(seen_ids)
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 快照寫入失敗: {e}")
            
    return new_findings

def main():
    parser = argparse.ArgumentParser(description="Threads 友店動態巡邏與自動化走心互動哨兵")
    parser.add_argument("--targets", type=str, default="default", help="逗號分隔的使用者名稱或 'default'")
    parser.add_argument("--cache", type=str, default="", help="快照快取檔案路徑")
    parser.add_argument("--output", type=str, default="", help="新發現與草稿輸出檔案路徑")
    parser.add_argument("--dry-run", action="store_true", help="演練模式，不寫入已讀快取")
    parser.add_argument("--reset-cache", action="store_true", help="清空已讀快取重來")
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    cache_path = args.cache or os.path.join(skill_root, "data", "sentinel_cache.json")
    
    if args.reset_cache and os.path.exists(cache_path):
        os.remove(cache_path)
        print("🧹 已清除歷史快照快取！")

    targets = DEFAULT_TARGETS
    if args.targets != "default":
        u_list = [u.strip().lstrip("@") for u in args.targets.split(",") if u.strip()]
        targets = [{"username": u, "name": f"@{u}"} for u in u_list]
        
    findings = run_sentinel(targets, cache_path, dry_run=args.dry_run)
    
    print("\n" + "="*60)
    print(f"🎯 海巡完成！共捕獲 {len(findings)} 則需要關注的友店新動態")
    print("="*60)
    
    for i, post in enumerate(findings, 1):
        print(f"\n【動態 #{i}】 @{post['username']} ({post.get('author_name', '')})")
        print(f"🔗 連結: {post['link']}")
        print(f"📝 內容摘錄: {post['content'][:120]}...")
        print("💡 推薦互動留言草稿:")
        for idx, draft in enumerate(post.get("draft_replies", []), 1):
            print(f"   [{idx}] [{draft['persona']}]:")
            print(f"       \"{draft['text']}\"")
            
    if args.output:
        out_path = args.output
    else:
        out_path = os.path.join(skill_root, "data", "latest_findings.json")
        
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(findings, f, ensure_ascii=False, indent=2)
    print(f"\n📁 最新動態與回覆草稿已歸檔至: {out_path}")

if __name__ == "__main__":
    main()
