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

THREADS_USER_ID = ENV.get("THREADS_USER_ID")
THREADS_TOKEN = ENV.get("THREADS_ACCESS_TOKEN")

# ==========================================
# 1. FACEBOOK LAUNCH
# ==========================================
def launch_facebook():
    print("=" * 50)
    print("🚀 [Taylor] 啟動 Facebook 官方粉專發射程序...")
    print("=" * 50)
    
    img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\FB_Posts\FB_01_Time_And_Family_Minimal.png"
    
    fb_message = """在台東做生意、跑物流這幾年，我最深的體會就是：我們這種小老闆和自營店家，時間真的永遠不夠用。

每天一睜開眼，備料、進貨、算帳、回客人訊息，常常一個人當三個人用。等忙完坐下來，夜深了，孩子也睡了。我們那麼努力，本是為了給家人更好的生活，最後卻連好好陪他們吃頓飯的時間，都被雜事吃得乾乾淨淨。

這幾個月，我在電腦裡打造了一套專屬的 AI 虛擬辦公室。我沒有花大錢請團隊，但我身邊多了一群安靜踏實的數位助理，幫我把雜亂的資料理得井井有條。

把雜事交給 AI，不是為了追求高科技潮流，只是想幫自己買回一點時間，拿回生活的主導權，多陪陪家人，活得從容一點。

11/11 (週三) 下午，秋季 AI 家教實戰班第 1 講正式開跑。
這堂課我不講艱澀難懂的程式碼，只手把手帶大家做兩件最落地的實戰：
① 打造店裡的「專屬數位大腦」：把你最頭痛的進貨單、補助案公文或手寫筆記丟給 Google NotebookLM，1 分鐘抓出關鍵重點，甚至能自動生成雙人對話廣播（Podcast），開車通勤用聽的就搞定。
② 漏斗式深挖提問法：徹底告別「問一句 AI 回三千字官腔廢話」的吐血窘境，學會精準餵脈絡，逼 AI 吐出刀刀見血的生意解法。

每班嚴格限額 10 位，自己帶筆電來，我會坐在你身邊巡桌排錯，現場做出你店裡的專屬成果才准下課。

💬 詳細課表與線上申請表，請見【第一則留言】，歡迎來家宅喝杯咖啡，把時間找回來！"""

    fb_first_comment = """🐾 11/11 (週三) 14:00 - 16:00《AI 家教實戰系列班 · 第 1 講》
⚠️ 堅持【100% 純實體現場教學】，絕無線上同步！導師手把手巡桌排錯！
實體座位嚴格限額 10 席，多一張椅子都不加。

💰 費用與繳費流程：
• 👑 老學員回娘家：表單內勾選「老學員」經審查即享學費 0 元免單！
• 🌟 新朋友實戰價：單堂 $500 元
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
# 2. THREADS LAUNCH
# ==========================================
def launch_threads():
    print("=" * 50)
    print("🚀 [Kage] 啟動 Threads (脆) 官方發射程序...")
    print("=" * 50)
    
    # 導入 threads_publisher 中的模組
    sys.path.append(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts")
    from threads_publisher import upload_local_image_to_meta_cdn, create_thread_container, publish_container
    
    img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\Threads_Posts\TH_Desk_Scene_AI_Delivery.jpg"
    if not os.path.exists(img_path):
        img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\TH_Desk_Scene_AI_Delivery.jpg"
        
    th_message = """做物流、管店鋪這些年，最深的體會只有一個：
我們的時間真的永遠不夠用。

每天忙完店裡的雜事坐下來，夜深了，小孩也睡了。
那麼努力打拼是為了家人，結果連陪他們好好吃頓飯的時間都被吃光。

這幾個月我用 AI 打造了一套辦公室，幫我把資料整理好。
不是為了追什麼科技潮流，只是想把屬於自己的時間和主導權買回來，活得從容一點。

下週三下午在台東家宅，我開一間小教室，手把手帶大家做一次。
限 10 個人，多一張椅子都沒有。

留言區放表單，想把時間找回來的來喝杯茶吧。"""

    th_first_comment = """🐾 11/11 (週三) 14:00《AI 家教實戰系列班 · 第 1 講》
• 實體限額 10 席，沒做完專屬成果不准下課
• 學費：新朋友 $500 / 老學員 0 元免單回娘家
• 流程：填表後由導師審查，審查通過會寄 Email 通知繳費與報到，確認完成才鎖定席次
• 申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
• 地點：台東市正氣北路166巷90號（家宅）"""

    # 上傳圖片至 Meta CDN
    print(f"📤 正在託管 Threads 配圖至 Meta CDN: {img_path}")
    cdn_url = upload_local_image_to_meta_cdn(img_path)
    if not cdn_url:
        print("⚠️ 無法取得 CDN 網址，將以純文字發布！")
        
    # 建立主貼文容器
    creation_id = create_thread_container(
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
    reply_creation_id = create_thread_container(
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
    print("🏁 雙平台發射執行總結：")
    print(f"📘 Facebook: {'✅ 成功' if fb_ok else '❌ 失敗'} -> {fb_url}")
    print(f"📱 Threads:  {'✅ 成功' if th_ok else '❌ 失敗'} -> {th_url}")
    print("=" * 50)
