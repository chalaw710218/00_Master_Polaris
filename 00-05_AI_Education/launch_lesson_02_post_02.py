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
    print("🚀 [Taylor] 啟動 Facebook 官方粉專發射程序 —— 第 2 講連載【篇號 02】...")
    print("=" * 60)
    
    img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\FB_L02_02_Official_API_Security.png"
    if not os.path.exists(img_path):
        img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\FB_L02_02_Official_API_Security.png"
        
    fb_message = """很多小老闆想做社群自動化，卻找了來路不明的黑心外掛或模擬器，結果往往是被官方封號、粉專降權，得不償失。

11/18 (週三) 下午第 2 講，我們不走旁門左道。
我手把手帶你串接 Meta 官方合法開放的通道：
Facebook Graph API 與 Threads 官方 API！

不用懂高深程式碼：
① 安全第一：Token 與金鑰環境隔離，100% 寫入防護規則，密碼永不洩漏。
② 3 秒發射：本地資料夾放好照片與文字，一鍵自動排程推播至 FB 粉專與 Threads。
③ 夜間守護：自動巡邏最新留言並高情商秒回，從此半夜安心睡覺。

現場依然是鐵血軍規：
打開自己的筆電，我坐在你身邊巡桌。沒親手發出第一篇自動貼文，當天不准下課！

老學員全免單，新朋友單堂 $500。
現場僅限 10 席，座位正在快速減少中。

💬 入席申請表請見【第一則留言】！"""

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
