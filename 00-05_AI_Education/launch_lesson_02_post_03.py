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
    print("🚀 [Taylor] 啟動 Facebook 官方粉專發射程序 —— 第 2 講連載【篇號 03】...")
    print("=" * 60)
    
    img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_L02_03_Final_Call_Tomorrow.png"
    if not os.path.exists(img_path):
        img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\FB_L02_03_Final_Call_Tomorrow.png"
        
    fb_message = """最後通報！明天下午 14:00，正氣北路家宅準時開練！

第 2 講【Antigravity 操作 ✕ Meta 官方自動發文串接】。
我們要帶大家把折磨小老闆一整年的「手動排程發文」與「半夜回留言」，一口氣徹底自動化。

說到做到，現場堅持 100% 純實體：
現場就 10 張椅子，多一張都沒有，絕無線上同步。
帶著你的筆電來，現場把專屬發射台串通才放人下課！

• 老學員（含第 1 講學員）：0 元全額免單
• 全新夥伴：單堂 $500

正選名額即將全數鎖定，額滿系統將立即關閉表單，超額填表自動轉入候補。
想把時間買回來的在地夥伴，把握最後席次！

💬 申請表在【第一則留言】，明天下午 14:00 家宅見！"""

    fb_first_comment = """🐾 2026 秋季《AI 家教實戰系列班 · 第 2 講報名須知》
⚠️ 堅持【100% 純實體現場教學】，絕無線上同步！導師手把手巡桌排錯到底！
現場極限 10 席，多一張椅子都不加，API 沒跑通不准走！

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
