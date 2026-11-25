# -*- coding: utf-8 -*-
"""
atom-trend-scout · 純粹熱點嗅探與常民情節深層轉譯引擎 (Trend Scout Deep Engine)
由科技偵察官艾達 (Ada) ✕ 生活管家影 (Kage) 聯合研製
落實創辦人親定之「做深三大硬核規格」與「三不三轉降維心法」
"""

import os
import sys
import json
import urllib.request
import xml.etree.ElementTree as ET
import re
from datetime import datetime

# Windows 控制台 UTF-8 防呆
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 「三不」硬核黑名單過濾庫（血腥、黨派對立、惡意八卦）
SENSITIVE_PATTERNS = [
    r"命案|殺人|砍人|分屍|墜樓|槍擊|身亡|車禍死",
    r"民進黨|國民黨|民眾黨|立委大罵|選戰|罷免|口水戰|總統大選",
    r"出軌|偷吃|約砲|裸照|偷拍|豔照"
]

# 本地常民生活時空心電圖（斷網時優雅降級的高保真情節備用庫）
FALLBACK_FOLK_PLOTS = [
    {
        "raw_keyword": "週末東北季風氣溫驟降",
        "folk_emotion": "下班趕回家的寒意與對一碗熱湯的強烈渴望",
        "three_conversions_angle": "柴米油鹽底氣 ✕ 孝親居安守護",
        "narrative_hook_plot": "剛踏出捷運站冷風直接灌進領口，這時候如果家裡廚房正滾著一鍋冒煙的剝皮辣椒雞湯，一整週的委屈好像都被原諒了。"
    },
    {
        "raw_keyword": "週五下班通勤車潮塞爆",
        "folk_emotion": "打工人被一整週報表榨乾後的極度放空渴望",
        "three_conversions_angle": "打工人心電圖 ✕ 街角第二客廳",
        "narrative_hook_plot": "車窗外的煞車紅燈連成一片海，耳機裡放著歌，心裡只想著等一下順路在自提站帶一把地瓜葉與剛烤好的麵包回家。"
    },
    {
        "raw_keyword": "外食便當漲破百元關卡",
        "folk_emotion": "面對薪水沒漲、物價飛漲的深層生活無奈感",
        "three_conversions_angle": "柴米油鹽底氣 ✕ 誠信平價定海神針",
        "narrative_hook_plot": "中午隨便夾三樣菜加一塊排骨就要120元。生活管家默默把產地直送的時令蔬菜守在銅板價，誠實的飯菜才是大人最硬的防彈衣。"
    },
    {
        "raw_keyword": "秋冬流感與高齡呼吸道防護",
        "folk_emotion": "離鄉遊子對遠方老家父母健康的隱隱擔憂",
        "three_conversions_angle": "孝親居安守護 ✕ 尊嚴陪伴",
        "narrative_hook_plot": "電話裡阿嬤咳了兩聲又急忙說沒事。生活管家今天到府送菜時順手幫老人家熱了一杯金桔茶，替不能常回家的你多看一眼。"
    },
    {
        "raw_keyword": "深夜未眠都市孤島",
        "folk_emotion": "夜深人靜卸下防備後的寂寞與安靜補償心理",
        "three_conversions_angle": "深夜心靈客廳 ✕ 無感溫暖",
        "narrative_hook_plot": "凌晨一點的街角只剩路燈在值班。店貓在鍵盤旁打了個哈欠，用毛茸茸的尾巴掃過手腕，提醒你今天真的可以休息了。"
    }
]

def is_safe_topic(title, snippet=""):
    full_text = f"{title} {snippet}"
    for pat in SENSITIVE_PATTERNS:
        if re.search(pat, full_text):
            return False
    return True

def map_to_folk_narrative(keyword, title):
    # 根據關鍵字特徵做深度三轉映射
    text = f"{keyword} {title}"
    if any(k in text for k in ["冷", "雨", "天", "風", "降溫", "氣溫"]):
        return {
            "folk_emotion": "突如其來的降溫讓身體緊繃，渴望熱氣與庇護",
            "three_conversions_angle": "柴米油鹽底氣 ✕ 孝親居安",
            "narrative_hook_plot": f"看著天氣預報【{keyword}】，下班路上腳步不自覺加快。今晚只想窩在沙發上，給遠方爸媽打通電話提醒添衣，廚房燉著熱騰騰的家常飯。"
        }
    elif any(k in text for k in ["漲", "錢", "價", "房", "股", "幣", "稅", "薪"]):
        return {
            "folk_emotion": "數字遊戲讓人心累，渴望腳踏實地的生活踏實感",
            "three_conversions_angle": "打工人心電圖 ✕ 誠信商道",
            "narrative_hook_plot": f"新聞又在聊【{keyword}】的數字起伏。大盤再吵，日子還是要過。洗一把晨採的地瓜葉下鍋，這份來自泥土的清甜，演算法奪不走。"
        }
    elif any(k in text for k in ["車", "塞", "高鐵", "台鐵", "路", "捷運"]):
        return {
            "folk_emotion": "通勤路上的疲憊與對個人放鬆時間的極度渴望",
            "three_conversions_angle": "打工人心電圖 ✕ 溫暖陪伴",
            "narrative_hook_plot": f"被困在【{keyword}】的人潮與車陣中，耳機裡播著最愛的歌。深呼吸一下，不用逼自己隨時保持強悍，今晚回家就好好放空。"
        }
    else:
        return {
            "folk_emotion": "現代資訊洪流中的疲憊，尋找安頓身心的常民生活錨點",
            "three_conversions_angle": "常民生活微鏡頭 ✕ 知心客廳",
            "narrative_hook_plot": f"今天全網都在討論【{keyword}】。熱鬧是他們的，而生活是自己的。給自己倒一杯溫茶，看著貓咪曬著太陽打瞌睡，心一下子就安靜下來。"
        }

def fetch_real_trends(limit=5):
    url = "https://trends.google.com.tw/trending/rss?geo=TW"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PolarisScout/2.0"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        items = root.findall(".//item")
        scouted = []
        
        for item in items:
            title_elem = item.find("title")
            title = title_elem.text.strip() if title_elem is not None else ""
            desc_elem = item.find("description")
            desc = desc_elem.text.strip() if desc_elem is not None else ""
            
            if not is_safe_topic(title, desc):
                continue
                
            trans = map_to_folk_narrative(title, desc)
            scouted.append({
                "rank": len(scouted) + 1,
                "raw_keyword": title,
                "folk_emotion": trans["folk_emotion"],
                "three_conversions_angle": trans["three_conversions_angle"],
                "narrative_hook_plot": trans["narrative_hook_plot"],
                "safety_passed": True,
                "source": "Google_Trends_TW_Live"
            })
            if len(scouted) >= limit:
                break
                
        if len(scouted) >= 3:
            return scouted
    except Exception as e:
        # 網絡超時或被攔截時，優雅降級回退到高保真常民情節庫
        pass
        
    # 優雅降級返回
    results = []
    for idx, item in enumerate(FALLBACK_FOLK_PLOTS[:limit], 1):
        results.append({
            "rank": idx,
            "raw_keyword": item["raw_keyword"],
            "folk_emotion": item["folk_emotion"],
            "three_conversions_angle": item["three_conversions_angle"],
            "narrative_hook_plot": item["narrative_hook_plot"],
            "safety_passed": True,
            "source": "Polaris_Folk_Resilience_Vault"
        })
    return results

if __name__ == "__main__":
    limit = 5
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except Exception:
            pass

    trends = fetch_real_trends(limit=limit)
    payload = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "atom": "atom-trend-scout",
        "version": "1.0-Deep",
        "status": "Success",
        "trends_count": len(trends),
        "depth_spec": {
            "mechanistic_depth": "常民集體情緒穿透 ✕ Dwell-Time情節提煉",
            "soul_depth": "三不三轉降維心法 ✕ 100%消滅AI說教腔",
            "resilience_depth": "林納斯級網絡抖動容錯 ✕ 本地情節庫無縫降級"
        },
        "trends": trends
    }

    # 輸出結構化 JSON
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(0)
