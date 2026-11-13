import os
import sys
import time
import json
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris")
ENV_PATH = ROOT_DIR / ".secrets.env"

def load_env(path):
    env = {}
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

ENV = load_env(ENV_PATH)
FB_PAGE_TOKEN = ENV.get("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = "110505444816362"

TZ_TW = timezone(timedelta(hours=8))

# ==========================================
# 貼文資料設定
# ==========================================
POSTS_TO_SCHEDULE = [
    {
        "name": "第 2 講連載 · 篇號 02【技術硬核 ✕ 官方合法直連】",
        "schedule_dt": datetime(2026, 11, 15, 20, 30, 0, tzinfo=TZ_TW),
        "img_path": r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_L02_02_Official_API_Security.png",
        "message": """很多小老闆想做社群自動化，卻找了來路不明的黑心外掛或模擬器，結果往往是被官方封號、粉專降權，得不償失。

11/18 (週三) 下午第 2 講，我們不走旁門左道。
我手把手帶你串接 Meta 官方合法開放的通道：
Facebook Graph API 與 Threads 官方 API！

不用懂高深程式碼：
① 安全第一：Token 與金鑰環境隔離，100% 寫入防護規則，密碼永不洩漏。
② 3 秒發射：本地資料夾放好照片與文字，一鍵自動排程推播至 FB 粉專與 Threads。
③ 夜間守護：自動巡邏最新留言並高情商秒回，從此半夜安心睡覺。

現場依然是鐵血軍規：
打開自己的筆電，我坐在你身邊巡桌。沒親手發出第一篇自動貼文，當天不准下課！

• 老學員（含第 1 講夥伴）：0 元全免單回娘家
• 新朋友實戰價：單堂 $500
現場僅限 6 席純實體，座位正在快速減少中。

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
📍 上課地點：台東市正氣北路166巷90號（家宅）
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6"""
    },
    {
        "name": "第 2 講連載 · 篇號 03【最後召集 ✕ 明天下午開練】",
        "schedule_dt": datetime(2026, 11, 17, 20, 30, 0, tzinfo=TZ_TW),
        "img_path": r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_L02_03_Final_Call_Tomorrow.png",
        "message": """最後通報！明天下午 14:00，正氣北路家宅準時開練！

第 2 講【Antigravity 操作 ✕ Meta 官方自動發文串接】。
我們要帶大家把折磨小老闆一整年的「手動排程發文」與「半夜回留言」，一口氣徹底自動化。

說到做到，現場堅持 100% 純實體：
現場就 6 張椅子，多一張都沒有，絕無線上同步。
帶著你的筆電來，現場把專屬發射台串通才放人下課！

• 老學員（含第 1 講夥伴）：0 元全額免單
• 全新夥伴：單堂 $500

正選名額即將全數鎖定，額滿系統將立即關閉表單，超額填表自動轉入候補。
想把時間買回來的在地夥伴，把握最後席次！

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
📍 上課地點：台東市正氣北路166巷90號（家宅）
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6"""
    }
]

def schedule_post(item):
    name = item["name"]
    dt = item["schedule_dt"]
    ts = int(dt.timestamp())
    img_path = item["img_path"]
    message = item["message"]
    
    print("\n" + "=" * 60)
    print(f"🚀 正在上傳並排程：{name}")
    print(f"📅 預約發布時間：{dt.strftime('%Y-%m-%d %H:%M:%S (台灣時間)')} (Timestamp: {ts})")
    print("=" * 60)
    
    if not os.path.exists(img_path):
        print(f"❌ 找不到圖片檔案: {img_path}")
        return False, None
        
    # 步驟 1: 上傳圖片作為未發布照片
    print(f"📤 正在上傳配圖至 Facebook 照片庫: {os.path.basename(img_path)}")
    url_photo = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
    with open(img_path, "rb") as f:
        r_photo = requests.post(url_photo, files={"source": f}, data={
            "access_token": FB_PAGE_TOKEN,
            "published": "false"
        }, timeout=30).json()
        
    photo_id = r_photo.get("id")
    if not photo_id:
        print(f"❌ 上傳圖片失敗: {r_photo}")
        return False, None
    print(f"✅ 圖片暫存成功，Photo ID: {photo_id}")
    
    # 步驟 2: 建立排程貼文
    print("⏳ 正在建立 Facebook 預約排程貼文...")
    url_feed = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/feed"
    payload = {
        "access_token": FB_PAGE_TOKEN,
        "message": message,
        "attached_media[0]": f'{{"media_fbid":"{photo_id}"}}',
        "published": "false",
        "scheduled_publish_time": ts
    }
    r_feed = requests.post(url_feed, data=payload, timeout=30).json()
    post_id = r_feed.get("id")
    if not post_id:
        print(f"❌ 建立排程貼文失敗: {r_feed}")
        return False, None
        
    print(f"🎉 排程成功！Scheduled Post ID: {post_id}")
    return True, post_id

def main():
    print("🌟 [Taylor] 開始執行 Facebook 官方粉專 02、03 篇預約排程作業...")
    results = []
    for item in POSTS_TO_SCHEDULE:
        ok, pid = schedule_post(item)
        results.append((item["name"], item["schedule_dt"], ok, pid))
        time.sleep(2)
        
    print("\n" + "=" * 60)
    print("🏁 全部排程執行成果總報：")
    for name, dt, ok, pid in results:
        status_str = f"✅ 排程成功 (ID: {pid})" if ok else "❌ 排程失敗"
        print(f"• {name} ➔ {dt.strftime('%m/%d %H:%M')} ｜ {status_str}")
    print("=" * 60)

if __name__ == "__main__":
    main()
