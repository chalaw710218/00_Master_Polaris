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
# 貼文文案設定
# ==========================================
MSG_TODAY_FB = """很多人問我：「現在到處都在教 AI，市面上動輒一、兩萬塊的課，到底跟你們有什麼不一樣？」

我的回答很簡單：
如果上完課回到店裡，你依然要每天手動複製文字、手動挑照片、手動按排程、半夜盯著手機深怕漏回客人訊息……那你不叫學會 AI，你只是成了 AI 文案的廉價搬運工。

外面請行銷公司代操，一個月兩萬塊起跳，合約一停你什麼都沒留下；
找來路不明的黑心外掛排程，隨時面臨粉專被官方封號降權的風險。

本週三（11/18）下午第 2 講，我們要帶大家把最煩人的雜事「物理消滅」：
直接在你的筆電架設一套終身受用的「自動化社群發射台」！

三大核心模組現場打通：
❶ 本地資料夾規格化：文案與圖片丟進去，腳本自動檢測格式，告別開瀏覽器剪貼的狼狽。
❷ 直連 Meta 官方合法 API：不碰黑心外掛，走 Facebook 與 Threads 官方通道，3 秒程式直發，金鑰安全隔離永不外洩。
❸ 24 小時守護與自動秒回：夜間自動巡邏最新留言、高情商自動秒回，晚上安心睡覺，雜事交給系統在後台安靜運轉。

一樣是我的鐵血承諾：
⚠️【100% 純實體現場教學，絕無線上同步！】
⚠️【全員自備筆電，導師坐在你旁邊巡桌，沒親手跑通、沒發出第一篇，當天不准下課！】

💰 席次與特權：
• 👑 老學員（含第 1 講夥伴）：0 元免單回娘家！
• 🌟 全新夥伴實戰價：單堂 $500 元
• 現場極限 6 席純實體手把手，多一張椅子都不加。

想把時間買回來的小老闆，線上申請表請見【第一則留言】，週三下午 14:00 家宅見！"""

MSG_TOMORROW_FB = """最後通報！明天下午 14:00，正氣北路家宅準時開練！

第 2 講【Antigravity 操作 ✕ Meta 官方自動發文串接】。
我們要帶大家把折磨小老闆一整年的「手動排程發文」與「半夜回留言」，一口氣徹底自動化。

說到做到，現場堅持 100% 純實體：
現場就 6 張椅子，多一張都沒有，絕無線上同步。
帶著你的筆電來，現場把專屬發射台串通才放人下課！

• 老學員（含第 1 講夥伴）：0 元全額免單
• 全新夥伴：單堂 $500

正選名額即將全數鎖定，額滿系統將立即關閉表單，超額填表自動轉入候補。
想把時間買回來的在地夥伴，把握最後席次！

💬 申請表在【第一則留言】，明天下午 14:00 家宅見！"""

COMMENT_PINNED = """🐾 2026 秋季《AI 家教實戰系列班 · 第 2 講極致小班須知》
⚠️ 堅持【100% 純實體現場教學】，絕無線上同步！導師手把手巡桌排錯到底！
全班極限 6 席深度陪伴，API 沒跑通不准走。

📅 時間：11/18 (週三) 14:00 - 16:00 ｜ 台東市正氣北路166巷90號（家宅）
🎯 主題：Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads API)
💰 費用：老學員（含第 1 講夥伴）0 元免單 ｜ 新朋友單堂 $500

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6"""

def delete_old_scheduled_post(post_id):
    print(f"🗑️ 正在檢查並刪除舊排程貼文: {post_id}...")
    url = f"https://graph.facebook.com/v20.0/{post_id}?access_token={FB_PAGE_TOKEN}"
    try:
        r = requests.delete(url, timeout=15).json()
        print(f"  回應: {r}")
        return r.get("success", False)
    except Exception as e:
        print(f"  刪除時發生例外: {e}")
        return False

def schedule_fb_post(name, dt, img_path, message):
    ts = int(dt.timestamp())
    print("\n" + "=" * 60)
    print(f"🚀 [FB 排程發射] 正在上傳並排程：{name}")
    print(f"📅 預約發布時間：{dt.strftime('%Y-%m-%d %H:%M:%S (台灣時間)')} (Timestamp: {ts})")
    print("=" * 60)
    
    if not os.path.exists(img_path):
        print(f"❌ 找不到圖片檔案: {img_path}")
        return None
        
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
        return None
    print(f"✅ 圖片暫存成功，Photo ID: {photo_id}")
    
    print("⏳ 正在向 Meta 官方申請雲端排程貼文...")
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
        return None
        
    print(f"🎉 Facebook 官方雲端排程成功！Scheduled Post ID: {post_id}")
    return post_id

def main():
    print("🌟 正在啟動極星全自動發射台重組程序...")
    
    # 1. 刪除原定明天 20:30 的舊排程
    old_post_id = "110505444816362_1161855476523354"
    delete_old_scheduled_post(old_post_id)
    
    # 2. 排程今天 11:30 的全新藍圖文案
    dt_today = datetime(2026, 11, 16, 11, 30, 0, tzinfo=TZ_TW)
    img_today = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_Lesson_02_Automation_Blueprint.png"
    pid_today = schedule_fb_post("第 2 講連載 · 今天中午 11:30【全新自動化藍圖篇】", dt_today, img_today, MSG_TODAY_FB)
    
    # 3. 排程明天 11:30 的最後 24H 登機倒數
    dt_tomorrow = datetime(2026, 11, 17, 11, 30, 0, tzinfo=TZ_TW)
    img_tomorrow = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_L02_03_Final_Call_Tomorrow.png"
    pid_tomorrow = schedule_fb_post("第 2 講連載 · 明天中午 11:30【最後 24H 登機倒數篇】", dt_tomorrow, img_tomorrow, MSG_TOMORROW_FB)
    
    print("\n" + "=" * 60)
    print("📊 Facebook 官方雲端排程最新戰報：")
    print(f"• 今天 11/16 11:30 ➔ Scheduled Post ID: {pid_today}")
    print(f"• 明天 11/17 11:30 ➔ Scheduled Post ID: {pid_tomorrow}")
    print("=" * 60)

if __name__ == "__main__":
    main()
