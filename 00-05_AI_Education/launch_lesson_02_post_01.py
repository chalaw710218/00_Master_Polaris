import os
import sys
import time
import requests
from pathlib import Path

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

def launch():
    print("=" * 60)
    print("🚀 [Taylor] 啟動 Facebook 官方粉專發射程序 —— 第 2 講連載【篇號 01】...")
    print("=" * 60)
    
    img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_L02_01_No_Photo_Automation.png"
    if not os.path.exists(img_path):
        img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\FB_L02_01_No_Photo_Automation.png"
        
    fb_message = """說一件有點不好意思、但很真實的事：

週三下午第 1 講在家宅開練，兩個小時我巡桌巡到滿頭大汗，一個一個幫大家排錯，盯著每位小老闆做出專屬成果。直到大家笑著下課，我才發現：我忙到連一張照片都忘了拍！

但比起擺拍大合照，更踏實的是每個人筆電螢幕都亮著，帶走的成果是實打實的。

下週三（11/18）第 2 講，我們要解決做生意最煩的雜事：
每天忙完進貨顧店，累得半死還要想文案，發完臉書還要手動貼 Threads，半夜客人留言還要盯著手機深怕漏回……

下週三下午，手把手帶你把這套流程徹底自動化：
串接 Meta 官方合法 API，文案照片丟進資料夾，Python 3 秒自動排程發布雙平台，24 小時留言自動秒回！

⚠️【堅持 100% 純實體 6 席，自備筆電，API 沒跑通不准走！】
• 老學員（含第 1 講夥伴）0 元免單回娘家
• 新朋友實戰價單堂 $500

💬 線上申請表請見【第一則留言】，下週三下午家宅見！"""

    fb_first_comment = """🐾 2026 秋季《AI 家教實戰系列班 · 第 2 講報名須知》
⚠️ 堅持【100% 純實體現場教學】，絕無線上同步！導師手把手巡桌排錯到底！
現場極限 6 席，多一張椅子都不加，API 沒跑通不准走！

📅 上課時間：2026-11-18 (週三) 14:00 - 16:00
📍 上課地點：台東市正氣北路166巷90號（家宅）
🎯 核心主題：Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads API)

💰 費用與繳費流程：
• 👑 老學員回娘家：表單第 4.1 題勾選「第 2 講」，身份勾選「老學員」經審查即享學費 0 元免單！
• 🌟 新朋友實戰價：單堂 $500 元（審查通過後寄發 Email 正取通知與繳費方式）

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6 （加入後可直接私訊管家）"""

    print(f"📤 正在上傳 FB 配圖: {img_path}")
    url_photo = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
    with open(img_path, "rb") as f:
        r_photo = requests.post(url_photo, files={"source": f}, data={
            "access_token": FB_PAGE_TOKEN,
            "published": "false"
        }, timeout=30).json()
    
    media_id = r_photo.get("id")
    if not media_id:
        print(f"❌ 上傳圖片失敗: {r_photo}")
        return False, None
    print(f"✅ 圖片暫存成功，Photo ID: {media_id}")
    
    print("📤 正在發布 FB 貼文...")
    url_feed = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/feed"
    payload = {
        "access_token": FB_PAGE_TOKEN,
        "message": fb_message,
        "attached_media[0]": f'{{"media_fbid":"{media_id}"}}',
        "published": True
    }
    r_feed = requests.post(url_feed, data=payload, timeout=30).json()
    post_id = r_feed.get("id")
    if not post_id:
        print(f"❌ 貼文發布失敗: {r_feed}")
        return False, None
    
    print(f"🎉 貼文發布成功！Post ID: {post_id}")
    fb_url = f"https://www.facebook.com/{post_id}"
    print(f"🔗 貼文網址: {fb_url}")
    
    print("💬 正在置頂第一則留言...")
    time.sleep(2)
    url_comment = f"https://graph.facebook.com/v20.0/{post_id}/comments"
    r_comment = requests.post(url_comment, data={
        "access_token": FB_PAGE_TOKEN,
        "message": fb_first_comment
    }, timeout=30).json()
    
    comment_id = r_comment.get("id")
    if comment_id:
        print(f"✅ 第一則留言發布成功！Comment ID: {comment_id}")
    else:
        print(f"⚠️ 第一則留言未成功: {r_comment}")
        
    return True, fb_url

if __name__ == "__main__":
    ok, url = launch()
