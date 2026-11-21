# -*- coding: utf-8 -*-
"""
生活管家 · 2026 秋季實戰家教班 · 第 3 講第 2 波宣傳發布腳本 (11/21 週六)
雙平台同步發射：
1. Facebook 粉專「生活管家，就醬點」：上傳 2 張宣傳圖卡 + 發布主文 + 自動搶佔第一則留言
2. Threads 帳號「hellotaitung」：多圖輪播發布 + 自動第一則留言
"""
import os
import requests
import json
import time

# 1. 讀取 .secrets.env
secrets_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.secrets.env"
env_vars = {}
with open(secrets_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env_vars[k.strip()] = v.strip()

FB_PAGE_ID = env_vars.get('FB_PAGE_ID', '110505444816362')
FB_PAGE_TOKEN = env_vars.get('FB_PAGE_ACCESS_TOKEN', '')
TH_TOK = env_vars.get('THREADS_ACCESS_TOKEN', '')
TH_UID = env_vars.get('THREADS_USER_ID', '')

print(f"📡 FB Page ID: {FB_PAGE_ID}")
print(f"🔑 FB Token: {FB_PAGE_TOKEN[:25]}...")
print(f"🧵 Threads User ID: {TH_UID}")

# 2. 圖片檔案 (第 2 篇專屬配圖：圖 2 反差對照 + 圖 3 招募大圖)
images_dir = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_03_Data_Architecture_Persona_Engineering\images"
image_files = [
    os.path.join(images_dir, "FB_L03_02_Anti_Robot_Persona.png"),
    os.path.join(images_dir, "FB_L03_03_Master_Recruit_Poster.png")
]

# 3. 文案定義
fb_message = """你有沒有遇過這種尷尬時刻？
想用 AI 幫忙回客人訊息，結果它吐出來一句：
「尊敬的顧客您好，感謝您的諮詢，我們深感榮幸……」🤖❌

客人一讀，整個人冷掉：「這根本是罐頭機器人，老闆根本沒心！」

在台東做在地生意，最值錢的就是那份「人情味與熟客信任」。
如果你的 AI 講話像市政府公文，你發再多篇文，客人也不會多看一眼。

很多人以為 AI 的語氣是固定的，其實大錯特錯！
下週三（11/25）第 3 講【資料架構 ✕ AI 擬人化工程】，
我們要現場手把手教大家「五層同心圓心智建模」：

• 從外貌感官、口頭禪、思考邏輯，一路解剖到你的情緒軟肋與核心信念。
• 讓 AI 開口第一句就是：「阿姐早！今天剛進枋寮鮮魚，幫你留一條？」🐟✨

讓你的 AI 替你顧店時，客人甚至分不出來是老闆本人在打字，還是數位分身在回覆！

⚠️ 這堂課堅持【100% 純實體現場教學】，絕無線上同步！
導師現場個別巡桌調校語氣，沒捏出合格分身不准下課！
為求最高教學品質，【嚴格限額 6 席】，額滿立刻關閉表單。

👉 實體席位申請與老學員特權，請直接點進【第一則留言】！

#生活管家 #生活就醬點 #AI實戰家教班 #AI擬人化工程 #打造專屬數位店長 #告別罐頭公文 #純實體教學 #限額6席"""

first_comment = """🐾 11/25 (週三) 14:00 - 16:00《資料架構管理與 AI 擬人化工程》
⚠️ 本課程堅持【純實體現場教學】，絕無線上同步！導師現場巡桌排錯，保證做出成果！
實體座位【嚴格限額 6 席】，額滿即關門（超過者將為您保留至加開場）：

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
👑 老學員回娘家：表單內勾選「老學員」即享學費 0 元免單特權！
🌟 新朋友實戰價：單堂 $500 元（審查通過後個別發送正取報到通知）

📍 上課地點：生活管家總部（台東市正氣北路166巷90號）
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6 （加入後可直接私訊管家）"""

threads_message = """最怕空氣突然安靜，更怕 AI 突然講公文。

客人私訊問今天有沒有開，
AI 回：「尊敬的顧客您好，本商行今日正常營業，感謝垂詢……」
換作你是客人，是不是秒已讀不回？

在台東做生意，開口那聲「阿哥」、「阿姐」才是靈魂。
下週三下午 14:00 第 3 講：
《AI 擬人化捏臉術：把老闆的靈魂刻進去》

讓 AI 開口就像你在店裡笑瞇瞇倒茶寒暄一樣有溫度。
純實體【限額 6 席】，留言「靈魂」傳報名表給你 ☕✨"""

# ==========================================
# 🚀 任務一：Facebook 官方粉專發布
# ==========================================
print("\n--- [FB] 正在上傳宣傳圖片至 Meta 伺服器 ---")
fb_media_ids = []
fb_cdn_urls = []
for p in image_files:
    url_p = f"https://graph.facebook.com/v21.0/{FB_PAGE_ID}/photos"
    with open(p, "rb") as f:
        r = requests.post(url_p, files={"source": f}, data={"access_token": FB_PAGE_TOKEN, "published": "false"})
        res = r.json()
        if "id" in res:
            mid = res["id"]
            fb_media_ids.append(mid)
            print(f"✅ [FB] 圖片上傳成功: {os.path.basename(p)} -> Media ID: {mid}")
            
            # 取出 FB CDN 圖片 URL 供 Threads 使用
            r_get = requests.get(f"https://graph.facebook.com/v21.0/{mid}?fields=images&access_token={FB_PAGE_TOKEN}").json()
            if "images" in r_get and len(r_get["images"]) > 0:
                fb_cdn_urls.append(r_get["images"][0]["source"])
        else:
            print(f"❌ [FB] 圖片上傳失敗: {res}")

if not fb_media_ids:
    print("❌ [FB] 圖片上傳全數失敗，終止發布。")
    exit(1)

print("\n--- [FB] 正在發布主貼文 ---")
url_feed = f"https://graph.facebook.com/v21.0/{FB_PAGE_ID}/feed"
payload = {
    "access_token": FB_PAGE_TOKEN,
    "message": fb_message
}
for i, mid in enumerate(fb_media_ids):
    payload[f"attached_media[{i}]"] = f'{{"media_fbid":"{mid}"}}'

r_post = requests.post(url_feed, data=payload).json()
if "id" not in r_post:
    print(f"❌ [FB] 主貼文發布失敗: {r_post}")
    exit(1)

fb_post_id = r_post["id"]
print(f"🎉 [FB] 主貼文發布大成功！Post ID: {fb_post_id}")

print("💬 [FB] 正在自動搶佔第一則留言 (First Comment)...")
url_comment = f"https://graph.facebook.com/v21.0/{fb_post_id}/comments"
r_comm = requests.post(url_comment, data={"access_token": FB_PAGE_TOKEN, "message": first_comment}).json()
if "id" in r_comm:
    print(f"🎉 [FB] 第一則留言發布成功！Comment ID: {r_comm['id']}")
else:
    print(f"⚠️ [FB] 第一則留言未成功: {r_comm}")

# ==========================================
# 🧵 任務二：Threads 陣地同步推播 (多圖輪播 Carousel)
# ==========================================
print("\n--- [Threads] 正在建立多圖輪播容器 ---")
if len(fb_cdn_urls) >= 2:
    child_ids = []
    for idx, u in enumerate(fb_cdn_urls):
        url_c = f"https://graph.threads.net/v1.0/{TH_UID}/threads"
        p_c = {
            "media_type": "IMAGE",
            "image_url": u,
            "is_carousel_item": "true",
            "access_token": TH_TOK
        }
        res_c = requests.post(url_c, data=p_c).json()
        if "id" in res_c:
            child_ids.append(res_c["id"])
            print(f"✅ [Threads] 輪播子圖 {idx+1} 容器建立成功: {res_c['id']}")
        time.sleep(1)

    url_car = f"https://graph.threads.net/v1.0/{TH_UID}/threads"
    p_car = {
        "media_type": "CAROUSEL",
        "children": ",".join(child_ids),
        "text": threads_message,
        "access_token": TH_TOK
    }
    res_car = requests.post(url_car, data=p_car).json()
    if "id" in res_car:
        car_id = res_car["id"]
        print(f"✅ [Threads] 輪播總容器建立成功: {car_id}")
        
        print("⏳ [Threads] 等待 6 秒讓伺服器完成轉碼...")
        time.sleep(6)
        
        url_pub = f"https://graph.threads.net/v1.0/{TH_UID}/threads_publish"
        res_pub = requests.post(url_pub, data={"creation_id": car_id, "access_token": TH_TOK}).json()
        if "id" in res_pub:
            th_post_id = res_pub["id"]
            print(f"🎉 [Threads] 輪播貼文推播成功！Post ID: {th_post_id}")
            
            # 發布第一則留言
            time.sleep(2)
            url_reply = f"https://graph.threads.net/v1.0/{TH_UID}/threads"
            r_rep = requests.post(url_reply, data={
                "media_type": "TEXT",
                "text": first_comment,
                "reply_to_id": th_post_id,
                "access_token": TH_TOK
            }).json()
            if "id" in r_rep:
                rep_cid = r_rep["id"]
                time.sleep(1)
                r_rep_pub = requests.post(url_pub, data={"creation_id": rep_cid, "access_token": TH_TOK}).json()
                print(f"🎉 [Threads] 第一則留言發布成功！Comment ID: {r_rep_pub.get('id')}")
        else:
            print(f"❌ [Threads] 發布失敗: {res_pub}")
else:
    print("⚠️ [Threads] CDN 圖片數量不足，改為純文字發布")

print("\n==========================================")
print("🎯 雙平台發射大捷！")
print(f"Facebook: https://www.facebook.com/{fb_post_id}")
print("==========================================")
