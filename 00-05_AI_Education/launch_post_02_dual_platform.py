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
# 1. FACEBOOK LAUNCH (Post 02)
# ==========================================
def launch_facebook():
    print("=" * 50)
    print("🚀 [Taylor] 啟動 Facebook 官方粉專發射程序 (Post 02)...")
    print("=" * 50)
    
    img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\FB_Posts\FB_02_Funnel_Prompting_Minimal.png"
    
    fb_message = """很多開店或做生意的朋友常跟我抱怨：「我也試過用 ChatGPT 寫行銷文或問營運建議啊，但它吐出來的東西，永遠都是『1.加強社群宣傳 2.推出促銷方案 3.提升顧客體驗』這種幾千字的教科書官腔廢話，看兩眼就想把視窗關掉！」

其實，這真的不能怪 AI 不聰明。
問題出在——你一開局就急著「向它求答案」。

AI 就像一個剛從頂尖名校畢業、滿腦子理論的高材生。你如果只跟他說：「我是台東開小吃店的，想增加營業額，該怎麼做？」他當然只能把管理學教科書搬出來背給你聽。

要讓 AI 講人話、吐出刀刀見血的實戰對策，關鍵在於「漏斗式三層深挖提問法（Funnel Prompting）」：

🔹 第 1 層：先鋪全景（Context）
不要一開始就問它怎麼做！先把店裡的真實情境一次餵飽——包括你的菜單品項、進貨單、客單價、平日/假日營業額、最頭痛的痛點，甚至台東在地的客群特性。在脈絡未鋪滿前，嚴禁它給任何建議。

🔹 第 2 層：再逼細節（Constraints）
主動給出殘酷的邊界條件！例如：「我們只有老闆跟老闆娘兩個人，完全沒預算投廣告，每天只能撥 20 分鐘操作，請直接排除任何需要花錢買流量的做法。」鎖死限制，逼退教科書空話。

🔹 第 3 層：飽和求解（Decision）
當脈絡與限制條件 100% 飽和，最後一步才是向它要解法！這時候 AI 給你的，就不會是假大空的理論，而是明天早上就能執行的精準行動清單。

這套心法與實戰操作，我們會在 11/11 (週三) 下午的台東實體家教班現場，一步一步帶大家演練排錯。

我們會用你店裡的真實資料，現場打磨出你專屬的「AI 提問框架」，直到 AI 吐出讓你拍案叫絕的答案為止。

每班嚴格限額 10 席，自備筆電，做完專屬成果才准下課。

💬 老學員 0 元免單 ＆ 線上申請，請見【第一則留言】。"""

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
# 2. THREADS LAUNCH (Post 02)
# ==========================================
def launch_threads():
    print("=" * 50)
    print("🚀 [Kage] 啟動 Threads (脆) 官方發射程序 (Post 02)...")
    print("=" * 50)
    
    sys.path.append(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\scripts")
    from threads_publisher import upload_local_image_to_meta_cdn, create_media_container, publish_container
    
    img_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-05_Brand_Content_Hub\20261111_AI_Tutoring_6_Posts_Matrix\Threads_Posts\TH_02_ChatGPT_Fluff_Red_Cross.jpg"
    if not os.path.exists(img_path):
        img_path = r"C:\Users\lenovo\.gemini\antigravity\brain\fab99572-f34f-40f2-ab07-c039187414cc\TH_02_ChatGPT_Fluff_Red_Cross.jpg"
        
    th_message = """「問 AI 怎麼改善小店生意，它永遠回我三千字教科書廢話。」

很多台東在地老闆跟我吐過苦水：
問 AI 怎麼做行銷，它叫你「加強社群宣傳、推出促銷優惠、精準鎖定受眾」。
幹！誰不知道？！預算就兩萬、店裡就兩個人，到底要怎麼做？！

其實不能怪 AI 笨。
是你一開局就急著向它求答案，脈絡根本沒熱身！

AI 就像個頂尖高材生，你不給它真實背景，它只能背教科書給你看。
想讓它吐出刀刀見血的解法，只需要換個問法：
1. 先鋪全景：把菜單、真實客群與平日營業額一次塞給它，嚴禁它給建議。
2. 再逼細節：鎖死預算、人力與時間，把教科書空話全部堵死。
3. 飽和求解：脈絡餵飽了才要清單，吐出來的答案立刻就能用。

下週三下午在台東家宅，我現場帶大家實戰演練一次。
純實體巡桌排錯，限額 10 席。

留言區放申請表，老學員 0 元免單。"""

    th_first_comment = """🐾 11/11 (週三) 14:00《AI 家教實戰系列班 · 第 1 講》
• 實體限額 10 席，現場巡桌排錯，沒做完專屬成果不准下課
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
    print("🏁 雙平台 Post 02 發射執行總結：")
    print(f"📘 Facebook: {'✅ 成功' if fb_ok else '❌ 失敗'} -> {fb_url}")
    print(f"📱 Threads:  {'✅ 成功' if th_ok else '❌ 失敗'} -> {th_url}")
    print("=" * 50)
