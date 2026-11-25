#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_taiwan_trends.py — 即時熱點嗅探引擎 (v4.0 創辦人三道門禁硬化版)

落實創辦人（品碩）親定三道篩選門禁：
1. 題目黑名單：政治（政黨、選舉、罷免、公投、政治人物、政策爭議、官司對立）、災難、死亡、犯罪、社會對立事件，一律硬性跳過。
   發文前自問「這個題目會不會讓人吵起來？」，會就跳過。
2. 在地相關：只蹭台東人生活中真的會碰到的熱度（天氣、颱風、節日、連假、美食、運動賽事、演唱會、消費民生、台東在地新聞）。北部/西部純地方事件不蹭。
3. 寫法：從生活管家的日常角度切入（如颱風前提醒垃圾車停收怎麼辦），不准硬套。嚴禁虛構送餐送湯等未提供之服務！熱詞跟台東無關，不准加 hashtag。
4. 熱搜貼文另外標記 "hot_trend": true，供後續比較成效。
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET
import requests
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
    except Exception:
        pass

# ── 第一道門禁：題目硬性黑名單（政治、對立、災難、司法、犯罪） ──
POLITICAL_AND_DISPUTE_BLACKLIST = [
    # 政治與政黨
    "政黨", "選舉", "罷免", "公投", "政治", "民調", "立法院", "國會", "內閣", "行政院",
    "黨部", "黨團", "民進黨", "國民黨", "民眾黨", "藍綠", "柯文哲", "賴清德", "韓國瑜",
    "盧秀燕", "侯友宜", "朱立倫", "議員", "立委", "市長", "縣長", "水庫", "抗爭",
    # 災難與死亡
    "命案", "墜樓", "命危", "凶殺", "虐童", "槍擊", "輕生", "死亡", "車禍", 
    "身亡", "離世", "遺體", "喪命", "重傷", "火警", "猝死", "分屍", "自戕", "罹難",
    # 司法刑事與弊案
    "通緝", "收押", "保釋", "起訴", "羈押", "判刑", "受審", "貪污", "弊案", "搜索",
    # 社會衝突與敏感對立
    "性侵", "偷拍", "性騷", "出軌", "外遇", "黑道", "詐騙集團", "吸毒", "槍毒"
]

# ── 第二道門禁：非在地外縣市排除名單（純北部/西部地方事務不蹭） ──
NON_TAITUNG_LOCAL_EXCLUDE = [
    "基隆", "台北", "新北", "桃園", "新竹", "苗栗", "台中", "彰化", "南投", 
    "雲林", "嘉義", "台南", "高雄", "屏東市", "宜蘭", "北捷", "中捷", "高捷", 
    "翡翠水庫", "石門水庫", "德基水庫", "曾文水庫"
]

# ── 允許蹭的常民在地生活熱點領域（白名單類別） ──
ALLOWED_CATEGORIES = [
    "天氣與風雨", "節日與連假", "美食與常民餐飲", "運動賽事", "搶票與休閒娛樂", "民生消費與物價"
]

KNOWN_STOCK_CODES = {
    "2330": "台積電",
    "2317": "鴻海",
    "2454": "聯發科",
    "0050": "元大台灣50",
    "0056": "元大高股息",
    "00878": "國泰永續高股息",
    "00919": "群益台灣精選高息",
    "NVDA": "輝達",
    "TSLA": "特斯拉",
    "AAPL": "蘋果"
}

def is_fatal_dispute(text: str) -> tuple[bool, str]:
    """檢驗是否觸犯政治、爭議、災難黑名單"""
    for bad in POLITICAL_AND_DISPUTE_BLACKLIST:
        if bad in text:
            return True, f"命中政治/爭議/災難黑名單: 『{bad}』"
    return False, ""

def is_non_taitung_regional(keyword: str, text: str) -> tuple[bool, str]:
    """檢驗是否為非台東之純外縣市地方事務"""
    # 若關鍵字直接提及外縣市地名且無關全台/台東
    for regional in NON_TAITUNG_LOCAL_EXCLUDE:
        if regional in keyword:
            return True, f"命中非台東外縣市地方熱點: 『{regional}』"
    return False, ""

def fetch_google_trends_tw():
    """從 Google Trends 台灣官方 RSS 抓取即時趨勢"""
    url = "https://trends.google.com.tw/trending/rss?geo=TW"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    items = []
    try:
        res = requests.get(url, headers=headers, timeout=12)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            for item in root.findall(".//item"):
                title_elem = item.find("title")
                title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                
                traffic = ""
                for child in item:
                    if "approx_traffic" in child.tag and child.text:
                        traffic = child.text.strip()
                        break
                        
                news_items = []
                for child in item:
                    if "news_item" in child.tag:
                        news_title = ""
                        for sub in child:
                            if "news_item_title" in sub.tag and sub.text:
                                news_title = sub.text.strip()
                        if news_title:
                            news_items.append(news_title)
                                
                desc_elem = item.find("description")
                desc = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""
                
                if title:
                    items.append({
                        "keyword": title,
                        "traffic": traffic,
                        "description": desc,
                        "news_titles": news_items
                    })
    except Exception as e:
        print(f"⚠️ Google Trends RSS 解析異常: {e}")
        
    return items

def filter_and_translate_trends(raw_trends):
    """落實品碩親定三道篩選：政治硬擋、在地關聯、管家切角"""
    approved_trends = []
    
    for t in raw_trends:
        keyword = t["keyword"]
        news_titles = t.get("news_titles", [])
        context_str = keyword + " " + " ".join(news_titles) + " " + t.get("description", "")
        
        # 門禁 1：題目黑名單（政治、災難、對立、吵架話題一律跳過）
        is_bad, reason = is_fatal_dispute(context_str)
        if is_bad:
            continue
            
        # 門禁 2：外縣市地方事務排除（北部/西部純地方事件跳過）
        is_reg, reg_reason = is_non_taitung_regional(keyword, context_str)
        if is_reg:
            continue
            
        # 門禁 3：切角審計（必須能自然轉化為生活管家常民情境，絕不虛構未提供之服務）
        event_analysis = generate_safe_lifestyle_storyline(keyword, news_titles)
        if not event_analysis:
            continue
            
        approved_trends.append({
            "keyword": keyword,
            "category": event_analysis["category"],
            "traffic": t.get("traffic", ""),
            "news_sample": news_titles[0] if news_titles else "",
            "event_context": event_analysis["event_context"],
            "life_pain_point": event_analysis["life_pain_point"],
            "meow_hook": event_analysis["meow_hook"],
            "shadow_hook": event_analysis["shadow_hook"],
            "hashtag_allowed": event_analysis["hashtag_allowed"],
            "hot_trend": True
        })
        
        if len(approved_trends) >= 3:
            break
            
    return approved_trends

def generate_safe_lifestyle_storyline(keyword, news_titles):
    """
    將合規熱點以「生活管家真實視角」切入：
    1. 只能提到目前真實服務（如代倒垃圾，或純粹生活陪伴、提醒天氣/作息）
    2. 絕不承諾熱湯熱飯送到家等虛構服務！
    3. 若與台東無直接地緣關係，hashtag_allowed = False，禁止加 hashtag！
    """
    full_news = " ".join(news_titles)
    
    # 1. 氣候與極端天氣（颱風、強風、降溫、東北季風）
    if any(k in full_news or k in keyword for k in ["颱風", "暴雨", "豪雨", "強風", "寒流", "冷氣團", "低溫", "東北季風"]):
        is_typhoon = "颱風" in keyword or "颱風" in full_news
        return {
            "category": "天氣與風雨",
            "event_context": f"天氣系統影響東部，迎來強風降溫或風雨。",
            "life_pain_point": "風大天涼外出追垃圾車不便，需要注意保暖與居安防風",
            "meow_hook": f"外面這陣海風吹得呼呼叫喵！天氣變涼了，大家出門記得套上厚外套。如果下雨天不想狼狽追垃圾車，記得生活管家代倒垃圾隨時都在喔！🐾",
            "shadow_hook": f"這兩天台東的風明顯變涼了，吹過屋簷呼呼作響。提醒大家晚上出門多加件防風外套，門窗檢查關好。若是遇到風雨天垃圾車停收或不便出門，生活管家的代倒垃圾服務都在後排隨時支援大家。🍵",
            "hashtag_allowed": True if "台東" in keyword or "東北季風" in keyword else False
        }
        
    # 2. 體育與國際賽事（棒球、賽事熱血）
    elif any(k in full_news or k in keyword for k in ["棒球", "12強", "賽事", "中華隊", "球賽", "經典賽"]):
        return {
            "category": "運動賽事",
            "event_context": "熱門棒球或國際賽事引發全網關注熱議。",
            "life_pain_point": "專心看球賽容易忘記時間，需要準時打理生活瑣事",
            "meow_hook": f"大家今天是不是也盯著球賽激動吶喊喵！看球固然過癮，但別忘了準時吃晚餐、垃圾也要記得打包好喵！⚾",
            "shadow_hook": f"今晚全網都在為賽事沸騰喝采。生活就是這樣，在緊湊的日常裡為熱愛的事情專注一回。別忘了把晚餐好好吃完，眼前的生活依然要踏實過好。🍵",
            "hashtag_allowed": False
        }
        
    # 3. 節日、連假、交通疏運
    elif any(k in full_news or k in keyword for k in ["連假", "中秋", "跨年", "春節", "端午", "火車票", "高鐵", "返鄉"]):
        return {
            "category": "節日與連假",
            "event_context": "返鄉與假期即將到來，交通與出遊話題熱絡。",
            "life_pain_point": "返鄉團聚或出遠門時，家中的日常垃圾與門戶打理需要安心支援",
            "meow_hook": f"準備放假的心情是不是已經飛到太平洋了喵！放假出遠門前，記得把家裡的垃圾清乾淨，才不會回來聞到驚喜的味道喔喵～🐾",
            "shadow_hook": f"假期將近，街上的腳步好像都輕快了起來。出門遠行前，把家裡的瑣事打理整齊，門窗關妥，才能放心地享受屬於自己的時光。生活管家一直都在。🍵",
            "hashtag_allowed": False
        }

    # 4. 常民民生消費與股市起伏（僅作生活放鬆切入）
    elif any(k in full_news or k in keyword for k in ["0050", "00878", "0056", "台積電", "2330", "物價", "電費"]):
        return {
            "category": "民生消費與物價",
            "event_context": f"圍繞 {keyword} 的民生財經討論度高。",
            "life_pain_point": "看著數字起伏容易焦慮，不如回歸生活安頓好身心",
            "meow_hook": f"螢幕上的數字跳來跳去讓人眼花喵！與其盯著數字心煩，不如先喝口溫水。肚子照顧好了，日子自然就踏實了喵！🐾",
            "shadow_hook": f"外界的數字起伏再劇烈，終究是遠方的資訊流。回到台東的老木桌前，水剛煮開、茶香淡淡。把當下的日子過好，就是最大的踏實。🍵",
            "hashtag_allowed": False
        }

    return None
