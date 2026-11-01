"""
autopilot_google_business.py
============================
極星 Google 商家 24H 全自動巡航大腦 (Autopilot Core)
主理：情報長 雪柔 (Sheryl Sandberg / 獵鷹) ✕ 執行長 雪 (Yuki)

功能亮點：
1. 一鍵全自動推播最新在地 SEO 動態貼文（支援輪播：湯包/烏龍麵/親子丼/預約默契）
2. 零人工干預：Python 觸發 ➔ Make Active 管道秒級直發 Google Maps
3. 嚴格遵守創辦人品碩親定之商業規格與 Local SEO 關鍵字矩陣
"""

import os
import sys
import json
import requests
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/qgaec1o5a2fee1cjohfb67gwobfgrp7n"

POST_TEMPLATES = [
    {
        "id": "week01_soup_dumplings",
        "title": "爆汁小籠湯包 · 現蒸堅持 8 分鐘",
        "summary": (
            "【輕輕咬一小口，鮮甜肉汁直接爆開！為什麼我們堅持每一籠現點現蒸？🥟】\n\n"
            "在安慶街的日常裡，最療癒的聲音，就是蒸籠蓋掀開那一瞬間的「嘶——」聲，伴隨著熱氣與肉香撲鼻而來！✨\n\n"
            "常有熟客問我們：「老闆，你們湯包皮這麼薄、肉汁這麼多，怎麼不多蒸幾籠放著等客人？」\n"
            "我們的回答永遠只有一句：「熱度會騙人，但肉汁跟麵皮的彈性騙不了人。」\n"
            "只要提前蒸好保溫，皮就會被蒸氣浸軟，湯汁也會被麵皮吸乾。所以每一籠【爆汁小籠湯包】，我們堅持客訂後才送入蒸籠，精準鎖住 8~10 分鐘的黃金鮮美！\n\n"
            "🥢 老饕吃法三步驟：\n"
            "1. 輕輕夾起，先在湯匙裡咬開一小孔\n"
            "2. 吸一口溫潤鮮甜的純肉高湯\n"
            "3. 沾點薑絲黑醋，整顆入口享受飽滿扎實！\n\n"
            "📍 趕時間的朋友小秘訣：出門前 10 分鐘先打通電話給我們，人剛好到，湯包剛好出爐熱騰騰上桌！\n\n"
            "🏠 地址：台東市安慶街 60 號（職人食堂）\n"
            "📞 預約專線：089-342900 / 0920-081-326\n"
            "歡迎來安慶街坐坐，品嚐最踏實的職人手作溫度！✨"
        ),
        "phone": "089342900"
    },
    {
        "id": "week02_udon_noodles",
        "title": "入秋微涼 · 喝一碗清甜回甘的職人烏龍麵",
        "summary": (
            "【台東的秋風漸起，最需要這碗暖胃又暖心的清甜回甘！🍲】\n\n"
            "看似最家常的一碗麵，往往藏著最深的手藝功夫。\n"
            "在【職人食堂】，很多朋友第一次來是為了湯包，但第二次回訪，一定會指名點這碗「職人烏龍麵」！\n\n"
            "我們的湯頭沒有複雜的人工添加，而是用時間耐著性子慢熬，喝完清爽甘醇、完全不會口渴。\n"
            "吸飽高湯精華的烏龍麵條，滑順又帶著剛好的 Q 彈咬勁，吸溜一口滑進嘴裡，整個人都溫暖了起來～✨\n\n"
            "中午想要吃得飽足又無負擔？或是放假帶著家人想找個舒服乾淨的空間好好吃頓便飯？\n"
            "安慶街 60 號的蒸氣正熱，隨時等著您走進來吃碗熱麵！\n\n"
            "📍 台東 職人食堂｜台東市安慶街 60 號\n"
            "📞 門市專線：089-342900"
        ),
        "phone": "089342900"
    }
]

def auto_publish(post_index: int = 0):
    post = POST_TEMPLATES[post_index]
    payload = {
        "store_name": "台東 職人食堂",
        "title": post["title"],
        "summary": post["summary"],
        "phone": post["phone"],
        "action_type": "CALL"
    }

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 極星全自動巡航啟動：推送「{post['title']}」至 Google Maps...")
    resp = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=15)
    print(f"📡 狀態碼：{resp.status_code} ({resp.text})")
    if resp.status_code == 200:
        print("✅ 成功！Google 商家全自動無人接管發布完成！")

if __name__ == "__main__":
    auto_publish(0)
