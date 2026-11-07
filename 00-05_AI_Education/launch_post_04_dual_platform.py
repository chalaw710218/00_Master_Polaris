import os
import sys
import time
import json
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

# ==========================================
# 1. FACEBOOK LAUNCH (Post 04)
# ==========================================
def launch_facebook():
    print("=" * 50)
    print("🚀 [Taylor] 啟動 Facebook 官方粉專發射程序 (Post 04)...")
    print("=" * 50)
    
    img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\FB_Posts\FB_04_Iron_Discipline_Black_Gold.png"
    if not os.path.exists(img_path):
        img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\FB_04_Iron_Discipline_Black_Gold.png"
        
    fb_message = """說真的，大家時間都很寶貴。

如果你上過那種：講師在台上投影片按得飛快、台下聽得頻頻點頭，結果一回到家連軟體怎麼開都卡住的課……你一定懂那種深深的挫折感。

所以這次的實戰家教班，我訂了最硬的軍規：
⚠️【堅持 100% 純實體教學，絕無線上同步，多一張椅子都不加！】
⚠️【前半段講心法，後半段全員打開筆電，巡桌一個一個盯著操作！】
⚠️【遇到報錯當場排查，沒做出店裡的專屬成果，當天不准下課！】

我不搞大班演講，也不吹噓假大空的 AI 噱頭。
很多朋友問：「三週課到底會帶走什麼？」
這是一套完整的小老闆落地三部曲，每週三下午 14:00 - 16:00 在正氣北路家宅開練：

📅【秋季三週完整實戰課表】
🔹 第 1 講 ｜ 11/11 (週三)：【打造店內專屬數位大腦 ✕ 漏斗式深挖提問法】
把進貨單、菜單、長篇公文餵飽 Google NotebookLM，1 分鐘生出雙人 Podcast，學會精準三層提問，逼 AI 吐出刀刀見血的生意解法。
🔥【緊急公告：第 1 講 10 席實體座位目前已過半，僅剩最後 5 席！】

🔹 第 2 講 ｜ 11/18 (週三)：【Antigravity 操作 ✕ Meta 官方自動發文串接】
手把手帶你串接 Facebook 粉專與 Threads 官方 API！教你用 Python 自動排程發布圖文，並實現 24 小時留言自動巡邏秒回，再也不用半夜手忙腳亂回私訊。

🔹 第 3 講 ｜ 11/25 (週三)：【資料架構管理 ✕ Antigravity 擬人化工程】
解鎖「心智逆向工程」！把你的說話口氣、經商原則與店鋪 SOP 封裝進 AI，親手打造一個 24 小時不睡覺、永遠懂你的「數位店長」與「生活特務」。

這不是推銷，這是一份對在地教學品質的死磕承諾。

💬 第 1 講最後 5 席即將鎖定，線上申請表請見【第一則留言】！"""

    fb_first_comment = """🐾 2026 秋季《AI 家教實戰系列班 · 三週課表與報名須知》
⚠️ 堅持【100% 純實體現場教學】，絕無線上同步！導師手把手巡桌排錯！
現場極限 10 席，多一張椅子都不加（第 1 講目前僅剩 5 席！）。

📅 三堂課表（每週三 14:00 - 16:00 ｜ 台東市正氣北路166巷90號家宅）：
• 11/11 第 1 講：NotebookLM 數位大腦 ✕ 漏斗提問法（🔥 剩 5 席）
• 11/18 第 2 講：Antigravity 操作 ✕ Meta 官方自動發文串接
• 11/25 第 3 講：資料架構管理 ✕ Antigravity 擬人化店長分身

💰 費用與繳費流程：
• 👑 老學員回娘家：表單內勾選「老學員」經審查即享學費 0 元免單！
• 🌟 新朋友實戰價：單堂 $500 元（可單選或三堂完整聯報）
• 📩 收費方式：填表後由導師親自審查設備與需求，審查通過後將統一寄發【Email 正取通知信】提供專屬繳費方式，完成繳費即正式鎖定席次（未排入本梯次者優先保留至加開場）。

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
📍 上課地點：台東市正氣北路166巷90號（家宅）
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6 （加入後可直接私訊管家）"""

    # 上傳圖片
    print(f"📤 正在上傳 FB 專屬配圖: {img_path}")
    url_photo = f"https://graph.facebook.com/v20.0/{FB_PAGE_ID}/photos"
    with open(img_path, "rb") as f:
        r_photo = requests.post(url_photo, files={"source": f}, data={
            "access_token": FB_PAGE_TOKEN,
            "published": "false"
        }, timeout=30).json()
    
    media_id = r_photo.get("id")
    if not media_id:
        print(f"❌ 上傳 FB 圖片失敗: {r_photo}")
        return False, None
    print(f"✅ FB 圖片暫存成功，Photo ID: {media_id}")
    
    # 發布貼文
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
        print(f"❌ FB 貼文發布失敗: {r_feed}")
        return False, None
    
    print(f"🎉 FB 貼文發布成功！Post ID: {post_id}")
    fb_url = f"https://www.facebook.com/{post_id}"
    print(f"🔗 FB 貼文網址: {fb_url}")
    
    # 發表第一則留言
    print("💬 正在置頂第一則留言...")
    time.sleep(2)
    url_comment = f"https://graph.facebook.com/v20.0/{post_id}/comments"
    r_comment = requests.post(url_comment, data={
        "access_token": FB_PAGE_TOKEN,
        "message": fb_first_comment
    }, timeout=30).json()
    
    comment_id = r_comment.get("id")
    if comment_id:
        print(f"✅ FB 第一則留言發布成功！Comment ID: {comment_id}")
    else:
        print(f"⚠️ FB 第一則留言未成功: {r_comment}")
        
    return True, fb_url

# ==========================================
# 2. THREADS LAUNCH (Post 04)
# ==========================================
def launch_threads():
    print("=" * 50)
    print("🚀 [Kage] 啟動 Threads (脆) 官方發射程序 (Post 04)...")
    print("=" * 50)
    
    sys.path.append(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts")
    from threads_publisher import upload_local_image_to_meta_cdn, create_media_container, publish_container
    
    img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\Threads_Posts\TH_04_Classroom_Chairs_Countdown.jpg"
    if not os.path.exists(img_path):
        img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\TH_04_Classroom_Chairs_Countdown.jpg"
        
    th_message = """醜話說在前面：
這堂課沒有線上同步，所有人都在正氣北路家宅現場。
而且我會非常嚴厲。

我極度討厭那種「講師在台上投影片按得飛快，學員回家連軟體怎麼開都卡住」的課。
所以現場就 10 張椅子，多一張都沒有。

【緊急戰報】：目前 10 席已審查過半，僅剩最後 5 席！

前半段講心法，後半段全員筆電打開，一個一個螢幕盯著看。
遇到報錯當場排查，沒做出專屬成果，當天真的不放人下課。

秋季完整三週實戰：
• 11/11 第 1 講：NotebookLM 數位大腦 ✕ 漏斗深挖提問法（剩 5 席）
• 11/18 第 2 講：Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads API)
• 11/25 第 3 講：資料架構管理 ✕ 擬人化店長分身

想混學分的千萬別來。
想做出成果的，留言區申請。"""

    th_first_comment = """🐾 2026 秋季《AI 家教實戰系列班 · 三週課表與報名須知》
⚠️ 堅持【100% 純實體現場教學】，絕無線上同步！導師手把手巡桌排錯！
現場極限 10 席，多一張椅子都不加（第 1 講目前僅剩 5 席！）。

📅 三堂課表（每週三 14:00 - 16:00 ｜ 台東市正氣北路166巷90號家宅）：
• 11/11 第 1 講：NotebookLM 數位大腦 ✕ 漏斗提問法（🔥 剩 5 席）
• 11/18 第 2 講：Antigravity 操作 ✕ Meta 官方自動發文串接
• 11/25 第 3 講：資料架構管理 ✕ Antigravity 擬人化店長分身

👉 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
（老朋友回娘家記得勾免單 0 元，全新夥伴單堂 $500 審查通過後通知）
📍 地址：台東市正氣北路166巷90號（家宅）
💬 官方 LINE：https://lin.ee/z83YSq6"""

    # 上傳圖片至 Meta CDN
    print(f"📤 正在託管 Threads 配圖至 Meta CDN: {img_path}")
    cdn_url = upload_local_image_to_meta_cdn(img_path)
    if not cdn_url:
        print("⚠️ 無法取得 CDN 網址，將以純文字發布！")
        
    # 建立主貼文容器
    creation_id = create_media_container(
        text=th_message,
        image_url=cdn_url,
        topic_tag="生活服務"
    )
    if not creation_id:
        print("❌ Threads 建立貼文容器失敗！")
        return False, None
        
    time.sleep(3)
    post_id = publish_container(creation_id)
    if not post_id:
        print("❌ Threads 主貼文發布失敗！")
        return False, None
        
    th_url = f"https://www.threads.net/@hellotaitung/post/{post_id}"
    print(f"🎉 Threads 主貼文發布成功！Post ID: {post_id}")
    print(f"🔗 Threads 貼文網址: {th_url}")
    
    # 發表 Threads 首留言橋接
    print("💬 正在發布 Threads 首則留言（表單連結）...")
    time.sleep(3)
    reply_creation_id = create_media_container(
        text=th_first_comment,
        reply_to_id=post_id
    )
    if reply_creation_id:
        time.sleep(2)
        reply_id = publish_container(reply_creation_id)
        if reply_id:
            print(f"✅ Threads 首則留言發布成功！Reply ID: {reply_id}")
        else:
            print("⚠️ Threads 首留言發布失敗")
    else:
        print("⚠️ Threads 建立留言容器失敗")
        
    return True, th_url

if __name__ == "__main__":
    fb_ok, fb_url = launch_facebook()
    time.sleep(3)
    th_ok, th_url = launch_threads()
    
    print("\n" + "=" * 50)
    print("🏁 雙平台 Post 04 發射執行總結：")
    print(f"📘 Facebook: {'✅ 成功' if fb_ok else '❌ 失敗'} -> {fb_url}")
    print(f"📱 Threads:  {'✅ 成功' if th_ok else '❌ 失敗'} -> {th_url}")
    print("=" * 50)
