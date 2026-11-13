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

# 一級戴明安燈硬性黑名單（絕對不可蹭的血腥、性騷與惡意抹黑）
FATAL_BLACKLIST = [
    # 傷亡與血腥凶案
    "命案", "墜樓", "命危", "凶殺", "虐童", "槍擊", "輕生", "死亡", "車禍", 
    "身亡", "離世", "遺體", "喪命", "重傷", "火警", "猝死", "分屍",
    # 刑事司法深水區（指名道姓案件）
    "通緝", "收押", "保釋", "起訴", "羈押", "判刑", "受審", "貪污", "弊案",
    # 爭議與對立
    "性侵", "偷拍", "性騷", "出軌", "外遇"
]

# 台灣常見熱門股票代碼對照表（常民熱議）
KNOWN_STOCK_CODES = {
    "2330": "台積電",
    "2317": "鴻海",
    "2454": "聯發科",
    "0050": "元大台灣50",
    "0056": "元大高股息",
    "00878": "國泰永續高股息",
    "00919": "群益台灣精選高息",
    "00757": "統一FANG+",
    "2603": "長榮",
    "2609": "陽明",
    "2615": "萬海",
    "NVDA": "輝達",
    "TSLA": "特斯拉",
    "AAPL": "蘋果"
}

def fetch_google_trends_tw():
    """從 Google Trends 台灣官方 RSS 抓取即時趨勢，並深度提取新聞上下文"""
    url = "https://trends.google.com.tw/trending/rss?geo=TW"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    items = []
    try:
        res = requests.get(url, headers=headers, timeout=12)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            for item in root.findall(".//item"):
                title_elem = item.find("title")
                title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                
                # traffic
                traffic = ""
                for child in item:
                    if "approx_traffic" in child.tag and child.text:
                        traffic = child.text.strip()
                        break
                        
                # 深度提取新聞標題與新聞來源
                news_items = []
                for child in item:
                    if "news_item" in child.tag:
                        news_title = ""
                        news_snippet = ""
                        for sub in child:
                            if "news_item_title" in sub.tag and sub.text:
                                news_title = sub.text.strip()
                            elif "news_item_snippet" in sub.tag and sub.text:
                                news_snippet = sub.text.strip()
                        if news_title:
                            news_items.append(news_title + (f" ({news_snippet})" if news_snippet else ""))
                                
                desc_elem = item.find("description")
                desc = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""
                
                if title:
                    items.append({
                        "keyword": title,
                        "traffic": traffic,
                        "description": desc,
                        "news_titles": news_items
                    })
            if items:
                return items
    except Exception as e:
        print(f"⚠️ Google Trends RSS 解析異常: {e}")
        
    return items

def filter_and_translate_trends(raw_trends):
    """戴明安燈過濾與創辦人親授『三不三轉』高階降維轉譯"""
    approved_trends = []
    
    for t in raw_trends:
        keyword = t["keyword"]
        news_titles = t.get("news_titles", [])
        context_str = keyword + " " + " ".join(news_titles) + " " + t.get("description", "")
        
        # 1. 致命一級物理攔截（血腥、性騷、司法案件）
        is_fatal = False
        for bad_word in FATAL_BLACKLIST:
            if bad_word in context_str:
                is_fatal = True
                break
        if is_fatal:
            continue
            
        # 2. 深度事件情節轉譯（含股市代碼、大選喧囂、極端氣候、社會焦慮之降維轉譯）
        event_analysis = generate_event_storyline(keyword, news_titles)
        
        approved_trends.append({
            "keyword": keyword,
            "category": event_analysis["category"],
            "traffic": t.get("traffic", ""),
            "news_sample": news_titles[0] if news_titles else "",
            "event_context": event_analysis["event_context"],
            "life_pain_point": event_analysis["life_pain_point"],
            "meow_hook": event_analysis["meow_hook"],
            "shadow_hook": event_analysis["shadow_hook"],
            "visual_concept": event_analysis["visual_concept"]
        })
        
        if len(approved_trends) >= 5:
            break
            
    return approved_trends

def generate_event_storyline(keyword, news_titles):
    """根據新聞副標題與描述，提煉出明確的事件脈絡、文案與視覺彩蛋（落實三不三轉）"""
    full_news = " ".join(news_titles)
    
    # ── 類別 A：純數字股市代碼或盤面起伏（降維轉譯：打工人心電圖 ✕ 今日犒賞指數） ──
    is_stock_code = (keyword.isdigit() and len(keyword) in [4, 5]) or (keyword.upper() in KNOWN_STOCK_CODES)
    is_stock_market = any(k in full_news or k in keyword for k in ["台股", "股市", "大盤", "跌破", "創新高", "台積電", "美股", "標普", "納斯達克", "ETF", "配息", "漲停", "跌停", "綠油油", "紅通通"])
    
    if is_stock_code or is_stock_market:
        stock_name = KNOWN_STOCK_CODES.get(keyword.upper(), keyword)
        is_drop = any(k in full_news for k in ["跌", "挫", "崩", "綠", "重挫", "翻黑", "賣壓"])
        
        if is_drop:
            event_context = f"股市波動加劇，{stock_name} 或大盤盤面一片綠油油，引發打工人與散戶對資產縮水的心慌焦慮。"
            return {
                "category": "股市降維轉譯（心電圖與犒賞）",
                "event_context": event_context,
                "life_pain_point": "看盤看得心驚肉跳，但指數是別人的，肚子才是自己的；需要一盒永遠不會破底的香脆雞腿便當撫慰心靈",
                "meow_hook": f"今天看大家的手機螢幕全都綠成一片……別盯著 {stock_name} 嘆氣了喵！指數是別人的，肚子是自己的。關掉看盤軟體，剛出爐的金黃現炸大雞腿便當已經送到了，大口咬下去肉汁噴出來，這才是永遠不會破底的漲停板啦！🍗✨",
                "shadow_hook": f"今天很多人的手機螢幕都是綠色的，數字起起伏伏，看得心驚肉跳。但股市是別人的漲跌，你今天認真跑完會議、搬完重物的疲憊，卻是真實的。關掉 App 吧，無論指數跌到哪裡，巷口那碗熱騰騰的現切滷肉飯，永遠是不會破底的防線。🍵",
                "visual_concept": f"【反差犒賞】老木桌上擺著熱騰騰剛出爐的超大金黃炸雞腿便當與香濃熱湯，喵編兩隻前爪緊緊護住便當，眼神傲嬌又堅定；木桌旁貼著手寫牛皮紙便簽：『{stock_name} 可以跌，但今天的炸雞腿便當必須香！放過自己，好好吃肉。——生活管家』"
            }
        else:
            event_context = f"股市氣勢如虹，{stock_name} 或大盤創新高，社群群組全在狂歡慶祝獲利。"
            return {
                "category": "股市降維轉譯（落地餐桌）",
                "event_context": event_context,
                "life_pain_point": "帳面數字若沒換成好飯好菜，就只是伺服器裡的電子跳動；賺到了要懂得落地犒賞自己與家人",
                "meow_hook": f"今天全網都在歡呼大漲喵！但螢幕上的數字要是沒換成肥美的大罐罐或香噴噴炸排骨，那就只是看得到吃不到的空氣！今天收盤，值得本喵跟小編多點一盤鹽酥雞慶祝啦！🍗🎉",
                "shadow_hook": f"今天很多群組都在歡呼慶祝。但螢幕上的數字如果沒有換成餐桌上的一壺好茶、給爸媽買的當季水果、或是今晚給自己多點的一份熱湯，那它就只是伺服器裡的跳動。收盤了，回歸生活，今晚值得吃頓不看價格的家常好飯。🍵",
                "visual_concept": "【慶祝犒賞】老木桌擺著豐盛的四菜一湯加雙份大排骨，喵編好奇地嗅著剛端上桌的熱湯；手寫牛皮紙便簽寫著：『收盤了，數字要落地成好飯好菜才有意義。——生活管家 影』"
            }

    # ── 類別 B：政治大選與政策喧囂（降維轉譯：柴米油鹽超越政治） ──
    elif any(k in full_news or k in keyword for k in ["選戰", "候選人", "立法院", "政見", "民調", "造勢", "大選", "黨團", "國會"]):
        event_context = f"政治選戰與政策攻防持續升溫，各大政論與社群口水戰激烈，讓人感到疲憊窒息。"
        return {
            "category": "政治喧囂降維轉譯（踏實過日子）",
            "event_context": event_context,
            "life_pain_point": "外面的政治口水吵翻天，但升斗小民明天依然得準時起床賺錢，眼前的柴米油鹽才最踏實",
            "meow_hook": f"滑開手機到處都在吵架拍桌子，本喵耳朵都快被吵聾了喵～人類每天為了誰當選爭得面紅耳赤，明天太陽升起還不是一樣得餵本喵吃飯！肚子餓了就別跟著激動，吃飽睡個午覺比什麼都重要！🐟",
            "shadow_hook": f"這兩天街上的宣傳車喇叭聲很大，手機裡的爭論也沒停過。但說真的，政治喧囂再熱鬧，明天清晨五點太陽升起時，中央市場的菜販阿姨依然要彎腰挑地瓜葉，我們依然要牽著孩子出門上學。大局留給大人物去忙，生活管家只負責幫大家把眼前的柴米油鹽打理好、把今晚的家門關緊，睡個安穩覺。🍵",
            "visual_concept": "【老宅幽靜反差】窗外隱約可見遠處熱鬧的街景，室內暖黃老木桌前卻是一人獨享的一壺清茶與剛出爐的菜脯蛋熱便當；手寫便簽寫著：『世界再吵，也記得把眼前的飯好好吃完。——生活管家 影』"
        }

    # ── 類別 C：極端天候與風雨守護（降維轉譯：報平安 ✕ 居安防線） ──
    elif any(k in full_news or k in keyword for k in ["颱風", "暴雨", "豪雨", "強風", "寒流", "冷氣團", "起風", "低溫", "東北季風"]):
        event_context = f"強烈天氣系統逼近，全台或東部迎來劇烈風雨／低溫驟降，通勤受阻且外出危險。"
        return {
            "category": "氣候守護降維轉譯（報平安與到府防線）",
            "event_context": event_context,
            "life_pain_point": "風大雨大出門危險、不想冒險穿拖鞋排隊買飯或追垃圾車，需要溫暖熱食與居安守護",
            "meow_hook": f"外面這風吹得像颱風一樣，看到大家都裹成一顆粽子喵！下班如果不想出門吹風受凍，個人檔案有生活管家任意門，熱湯送到門口、垃圾順手清走，躲在被窩等熱飯才是生存之道喵！🍲",
            "shadow_hook": f"風雨聲開始撞鐵捲門了。請大家今晚千萬別冒險出門看浪，也別催外送員。家裡有什麼就煮碗雜菜麵，沒乾糧的也別慌，生活管家把緊急照明跟熱水壺備在玄關最順手的位置。在風雨面前，全家人圍在一起平平安安，就是今晚最大的勝利。🍵",
            "visual_concept": "【溫暖避風港】窗外狂風夜色，室內暖黃老木桌前擺著冒熱氣的粗陶大骨湯與保溫袋；喵編整隻貓裹在厚羊毛毯裡只露鼻頭；手寫便簽寫著：『外頭風大，把熱湯喝透再睡。——生活管家 影』"
        }

    # ── 類別 D：影視文化 / 演員話題（常民生活破圈） ──
    elif any(k in full_news or k in keyword for k in ["影后", "曾莞婷", "劇", "金馬", "影集", "演員", "角色", "潘茵茵"]):
        event_context = "Netflix 爆款台劇《影后》熱播，曾莞婷飾演的潘茵茵為維持美貌身材連一粒澱粉都不吃，引發全網對打工人身不由己與極限容貌焦慮的熱議。"
        return {
            "category": "影視文化共鳴",
            "event_context": event_context,
            "life_pain_point": "普通人不用走紅毯，週五不需要對自己太苛刻，把想吃的熱食大口吃完才是真實生活",
            "meow_hook": f"看網路上大家都在討論曾莞婷在《影后》裡演的大明星……為了美連一粒米都不能吃，看得本喵下巴肉都在發抖。還好我們只是凡人，不用去坎城走紅毯。今天都星期五了，肚子餓了就放過自己吧！剛出爐的現炸大雞腿便當，大口咬下去肉汁流出來，這才是真正的影后人生啦！🍗✨",
            "shadow_hook": f"最近全網都在討論《影后》裡曾莞婷演的那種極致緊繃與身不由己。在大城市裡，我們好像每天都在扮演一個不能出錯、隨時要光鮮亮麗的大人。但推開家門回到台東，你不需要演給任何人看。換上最鬆垮的舊睡衣，熱騰騰的飯菜生活管家幫你送到門口，今晚好好做回那個可以放心大口吃飯的自己。🍵",
            "visual_concept": "【微戲劇反差】喵編兩隻前爪緊緊護住桌上剛出爐的超大金黃炸雞腿便當，眼神警惕又傲嬌瞪著鏡頭；便當旁貼著一張手寫牛皮紙便簽：『《影后》潘茵茵不能吃澱粉，但你可以。放過自己，大口吃肉！——生活管家 影』"
        }

    # ── 類別 E：棒球 / 國際賽事 ──
    elif any(k in full_news or k in keyword for k in ["棒球", "12強", "賽事", "馬傑森", "中華隊", "球賽", "經典賽", "大巨蛋"]):
        event_context = f"世界棒球12強賽事熱血開打，全網緊盯賽況激動吶喊，球迷紛紛尋找邊看球邊吃的罪惡炸物宵夜。"
        return {
            "category": "體育賽事熱血",
            "event_context": event_context,
            "life_pain_point": "看球賽最怕肚子餓，熱血為中華隊吶喊時需要熱騰騰的便當小吃與冷飲隨傳隨到",
            "meow_hook": f"看全網都在為球賽熱血激動，本喵也跟著在沙發上瘋狂甩尾巴！看球最痛苦的就是肚子叫但不敢離開螢幕，小編已經把剛炸好的熱便當送到門口了喵，一邊大口咬肉一邊看球才是神仙享受！⚾🍗",
            "shadow_hook": f"今晚全網都在為賽事沸騰。不管戰況多緊張，生活管家把熱騰騰的在地晚餐與熱湯平安送到門口，讓你舒舒服服窩在沙發上為熱愛的事情喝采。🍵",
            "visual_concept": "【微戲劇反差】老木桌前擺著大碗現炸排骨便當與冰紅茶，喵編頭戴著迷你球迷頭巾坐在便當旁眼神專注；木桌便利貼寫著：『球賽要贏，晚餐也要吃飽！——生活管家』"
        }

    # ── 類別 F：演唱會 / 搶票 ──
    elif any(k in full_news or k in keyword for k in ["搶票", "演唱會", "售票", "當機", "拓元", "黃牛", "搶光"]):
        event_context = f"熱門演唱會門票開賣秒殺，購票系統轉圈圈塞爆當機，引發全網搶不到票的集體心碎與無力感。"
        return {
            "category": "休閒搶票痛點",
            "event_context": event_context,
            "life_pain_point": "搶票心力交瘁、螢幕戳破還是落空，需要一頓真真切切的熱美食來撫平挫折",
            "meow_hook": f"聽說大家今天又為了搶票把螢幕戳冒煙了喵～搶不到票真的不要難過，本喵試著搶罐罐也常常被小編沒收。今天中午不如搶一盒剛出爐的現炸大雞腿便當，這個保證不當機、三分鐘送到門口！🍗",
            "shadow_hook": f"今天全網都在搶票的失落與焦慮裡旋轉。搶不到票的遺憾，今晚讓生活管家送上的熱熱家常飯菜替你補回來，真實吃到肚子裡的熱湯，永遠不會讓你失望。🍵",
            "visual_concept": "【生無可戀反差】喵編整隻貓液態癱軟趴在筆電鍵盤上，眼神呆滯放空；旁邊放著生活管家的保溫提袋與熱壓吐司；手寫便簽寫著：『搶票辛苦了，至少便當永遠不會轉圈圈！——生活管家』"
        }

    # ── 類別 G：通識常民生活熱點 ──
    else:
        sample = news_titles[0] if news_titles else keyword
        event_context = f"全網熱搜話題：{sample}，引發大量網友在社群上熱烈圍觀與討論。"
        return {
            "category": "常民日常關注",
            "event_context": event_context,
            "life_pain_point": "社群資訊轟炸讓人疲憊，但在柴米油鹽的真實生活裡，吃飽睡好才是最大的踏實",
            "meow_hook": f"滑開手機大家都在熱烈聊『{keyword}』，討論得不可開交喵～本喵雖然看不太懂人類的世界，但知道肚子餓了一定要吃熱便當！不管世界怎麼變，中午這盒香脆雞腿是絕對不會背叛你的！🍗",
            "shadow_hook": f"今天整個網路世界因為『{keyword}』熱鬧非凡。但在台東的老木桌前，水剛煮滾、飯菜正香，推開門，生活管家替你守護最平凡踏實的溫飽日常。🍵",
            "visual_concept": "【老宅生活定心丸】老木桌前擺著熱騰騰的在地家常便當與熱茶，光影靜謐溫柔；手寫便簽寫著：『世界再吵，也記得把眼前的飯好好吃完。——生活管家 影』"
        }

def scan_hot_trends():
    """主函數：執行掃描並輸出結構化結果"""
    print("📡 [時事熱點雷達 v3.0] 正在探測台灣最新即時熱搜（啟動三不三轉降維轉譯機制）...")
    raw = fetch_google_trends_tw()
    if not raw:
        print("⚠️ 無法獲取即時網路熱點，啟動生活常規熱點備份方案...")
        raw = [
            {"keyword": "2330", "news_titles": ["台積電股價波動劇烈散戶看盤心驚膽戰"]},
            {"keyword": "影后台劇熱播", "news_titles": ["Netflix 爆款台劇影后引發全網對身材焦慮與演藝圈心酸大討論"]},
            {"keyword": "東北季風降溫", "news_titles": ["北部東部氣溫驟降早晚溫差大下班回家冷風刺骨"]}
        ]
    
    approved = filter_and_translate_trends(raw)
    print(f"✅ 成功通過戴明安燈門禁與三不三轉審計，產出 {len(approved)} 組【具備深度生活轉譯】之安全高共鳴生活梗：\n")
    for i, t in enumerate(approved, 1):
        print(f"📌 {i}. 【{t['keyword']}】 | 類別: {t['category']} (熱度: {t['traffic']})")
        print(f"   📖 事件脈絡: {t['event_context']}")
        print(f"   💡 常民痛點: {t['life_pain_point']}")
        print(f"   🐱 喵編嘴替: {t['meow_hook'][:55]}...")
        print(f"   🍵 影之撫慰: {t['shadow_hook'][:55]}...")
        print(f"   🎨 視覺彩蛋: {t['visual_concept']}")
        print("-" * 65)
    
    out_dir = Path(__file__).resolve().parent.parent / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "latest_hot_trends.json"
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "scanned_at": "2026-11-13 (v3.0 旗艦三不三轉版)",
            "count": len(approved),
            "trends": approved
        }, f, ensure_ascii=False, indent=2)
        
    print(f"\n📁 熱點結構化卷宗已存檔: {out_file}")
    return approved

if __name__ == "__main__":
    scan_hot_trends()
