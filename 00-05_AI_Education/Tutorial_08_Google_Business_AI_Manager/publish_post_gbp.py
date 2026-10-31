"""
publish_post_gbp.py
===================
台東 職人食堂 · Google 商家真實動態一鍵發布腳本
主理：情報長 雪柔 (Sheryl Sandberg / 獵鷹)

功能：
1. 讀取 token.json
2. 抓取職人食堂最新動態文案 (小籠湯包現蒸堅持)
3. 透過 Google Business Profile API (localPosts) 直接推送至 Google Maps！
"""

import os
import sys
import json
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(CURRENT_DIR, "token.json")
POST_TEXT_PATH = os.path.join(CURRENT_DIR, "clients", "01_Taitung_Shokunin_Diner", "03_Monthly_Google_Updates_Posts.md")

SCOPES = ["https://www.googleapis.com/auth/business.manage"]

def publish_week01_post(account_id: str, location_id: str):
    if not os.path.exists(TOKEN_FILE):
        print(f"❌ 找不到憑證檔案：{TOKEN_FILE}，請先執行【點我授權Google商家.bat】完成授權！")
        return

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    # 貼文內容
    summary = (
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
    )

    post_payload = {
        "languageCode": "zh-TW",
        "summary": summary,
        "callToAction": {
            "actionType": "CALL",
            "url": "tel:089342900"
        },
        "topicType": "STANDARD"
    }

    # Google Local Posts API 端點
    # 格式通常為：https://mybusiness.googleapis.com/v4/accounts/{accountId}/locations/{locationId}/localPosts
    url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/localPosts"
    
    print(f"📡 正在發布動態至 Google Maps (Location: {location_id})...")
    resp = requests.post(url, headers=headers, json=post_payload)
    print(f"狀態碼：{resp.status_code}")
    print("回應內容：", resp.text)

if __name__ == "__main__":
    print("請先執行 auth_google_business.py 取得 location_id 後填入呼叫！")
