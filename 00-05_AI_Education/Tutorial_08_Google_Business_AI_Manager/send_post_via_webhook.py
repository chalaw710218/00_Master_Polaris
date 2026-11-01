"""
send_post_via_webhook.py
========================
極星 Google 商家敏捷發文引擎 (Make.com 官方白名單跳板)
主理：情報長 雪柔 (Sheryl Sandberg / 獵鷹)
"""

import sys
import json
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

MAKE_WEBHOOK_URL = "https://hook.eu1.make.com/qgaec1o5a2fee1cjohfb67gwobfgrp7n"

def publish():
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

    payload = {
        "store_name": "台東 職人食堂",
        "summary": summary,
        "phone": "089342900",
        "action_type": "CALL"
    }

    print("🚀 正在透過 Make 敏捷通道發布動態至 Google Maps...")
    resp = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=15)
    print(f"📡 Webhook 回應狀態碼：{resp.status_code}")
    print(f"📡 Webhook 回應內容：{resp.text}")
    if resp.status_code == 200:
        print("🎉 訊號已成功送達 Make！請檢查 Make 節點是否觸發發布！")

if __name__ == "__main__":
    publish()
