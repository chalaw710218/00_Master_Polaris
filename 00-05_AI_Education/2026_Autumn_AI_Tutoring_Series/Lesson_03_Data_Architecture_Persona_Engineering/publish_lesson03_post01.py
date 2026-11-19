# -*- coding: utf-8 -*-
"""
生活管家 · 2026 秋季實戰家教班 · 第 3 講首波宣傳發布腳本
功能：
1. 上傳 3 張高清宣傳圖至 Meta 草稿區 (published=false)
2. 發布主貼文 (第 1 篇：實況承啟篇)
3. 自動於下方發表第一則留言 (First Comment 模組，附帶報名表單與 LINE 連結)
4. 寫入歷史日誌歸檔
"""
import os
import requests
import json
from pathlib import Path

# 1. 讀取 .secrets.env
secrets_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.secrets.env"
env_vars = {}
with open(secrets_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            env_vars[k.strip()] = v.strip()

PAGE_ID = env_vars.get('FB_PAGE_ID', '110505444816362')
PAGE_TOKEN = env_vars.get('FB_PAGE_ACCESS_TOKEN', '')

print(f"📡 目標粉專 ID: {PAGE_ID}")
print(f"🔑 Page Token 前綴: {PAGE_TOKEN[:25]}... (長度: {len(PAGE_TOKEN)})")

# 2. 圖片路徑
images_dir = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_03_Data_Architecture_Persona_Engineering\images"
image_files = [
    os.path.join(images_dir, "FB_L03_01_Evolution_Trilogy.png"),
    os.path.join(images_dir, "FB_L03_02_Anti_Robot_Persona.png"),
    os.path.join(images_dir, "FB_L03_03_Master_Recruit_Poster.png")
]

# 3. 文案內容
message = """昨天下午在正氣北路總部，我們帶著幾位在地老闆與夥伴，
一步一步打開電腦，親手把 AI 與臉書官方發射台串接起來。

過去大家做社群最痛苦的，不是沒想法，
而是開店已經忙著備料、招呼客人，哪有美國時間每天搬運、手動發文？
昨天跑通之後，大家親眼見證：
「以後只要把一張照片丟給 AI，後續的文案排版、貼文發布、甚至第一則留言導流，全部交給 AI 幫你搞定！」☕⚡

但，這只是第二步。
手腳接上了，接下來最關鍵的痛點來了：
「AI 寫出來的東西雖然快，但為什麼總有一股冷冰冰的塑膠感、機器人公文味，根本不像我在店裡跟客人說話的口氣？」

這就是下週三（11/25）秋季系列班【第 3 講 · 終極大壓軸】要帶大家突破的：
《商業資料架構管理 ✕ AI 擬人化工程：打造專屬語氣的數位店長》！

我們要替你的自動發射台「注入靈魂」：
1. 告別檔案垃圾場（SSOT 哲學）：建立一套讓 AI 永遠報對價錢、講對故事的乾淨商業資料庫！
2. 五層同心圓捏臉術：把你的說話習慣、在地常民用語、甚至面對奧客的情緒防線，精準刻印進 AI 大腦。
3. 現場捏出專屬 AI 分身：開口不再是「尊敬的顧客您好」，而是像你親自倒茶寒暄一樣親切接地氣！

⚠️ 這堂課堅持【100% 純實體現場教學】，絕無冷冰冰的線上課！
導師現場個別巡桌調校，沒捏出合格的 AI 分身不准下課！
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

# 4. 上傳圖片至 Meta 草稿區
media_ids = []
print("📸 正在上傳 3 張宣傳圖卡至 Meta 伺服器...")
for img_path in image_files:
    if not os.path.exists(img_path):
        print(f"❌ 找不到圖片: {img_path}")
        continue
    url_photo = f"https://graph.facebook.com/v21.0/{PAGE_ID}/photos"
    with open(img_path, "rb") as f:
        files = {"source": f}
        data = {"access_token": PAGE_TOKEN, "published": "false"}
        r = requests.post(url_photo, files=files, data=data)
        res = r.json()
        if "id" in res:
            media_ids.append(res["id"])
            print(f"✅ 上傳成功: {os.path.basename(img_path)} -> Media ID: {res['id']}")
        else:
            print(f"❌ 上傳失敗: {res}")

if not media_ids:
    print("❌ 沒有任何圖片上傳成功，終止發布。")
    exit(1)

# 5. 發布主貼文
print("🚀 正在發布主貼文...")
url_feed = f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed"
payload = {
    "access_token": PAGE_TOKEN,
    "message": message
}
for i, mid in enumerate(media_ids):
    payload[f"attached_media[{i}]"] = f'{{"media_fbid":"{mid}"}}'

r_post = requests.post(url_feed, data=payload)
post_res = r_post.json()

if "id" not in post_res:
    print(f"❌ 主貼文發布失敗: {post_res}")
    exit(1)

post_id = post_res["id"]
print(f"🎉 主貼文發布成功！Post ID: {post_id}")

# 6. 自動搶佔第一則留言
print("💬 正在自動搶佔第一則留言 (First Comment)...")
url_comment = f"https://graph.facebook.com/v21.0/{post_id}/comments"
comment_payload = {
    "access_token": PAGE_TOKEN,
    "message": first_comment
}
r_comment = requests.post(url_comment, data=comment_payload)
comment_res = r_comment.json()

if "id" in comment_res:
    comment_id = comment_res["id"]
    print(f"🎉 第一則留言發布成功！Comment ID: {comment_id}")
else:
    print(f"⚠️ 第一則留言未成功: {comment_res}")

print("\n=== 發布閉環大功告成 ===")
print(f"貼文網址: https://www.facebook.com/{post_id}")
