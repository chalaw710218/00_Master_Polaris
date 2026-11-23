# -*- coding: utf-8 -*-
"""
生活管家 · 2026 秋季實戰家教班 · 第 3 講 倒數 48 小時發射腳本
嚴格遵循創辦人指示：
1. 主文案 100% 零外部連結（保護演算法自然觸及率）
2. 報名表單與 LINE 導流連結 100% 置入於【第一則留言 (First Comment)】
3. 搭配高清生動海報 POST_01_倒數48小時海報.png
4. Facebook 官方粉專 ＆ Threads 雙平台同步發射
"""

import os
import requests
import json
import time

# 1. 讀取密鑰
secrets_path = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.secrets.env"
env = {}
with open(secrets_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()

FB_PAGE_ID = env.get("FB_PAGE_ID", "110505444816362")
FB_PAGE_TOKEN = env.get("FB_PAGE_ACCESS_TOKEN", "")
TH_UID = env.get("THREADS_USER_ID", "29191709603824305")
TH_TOK = env.get("THREADS_ACCESS_TOKEN", "")

# 2. 海報檔案
image_path = r"C:\Users\lenovo\Desktop\POST_01_倒數48小時海報.png"

# 3. 文案定義 (主文嚴禁任何 http 外部連結)
FB_CAPTION = """還有最後 48 小時。

上週帶著幾位在地頭家把自動發射台跑通了，
一張照片丟給 AI，文案、排版、發文 3 秒搞定。
大家看著手機貼文秒級冒出來，很興奮，但接著問了一句最扎心的話：

「發文變快了沒錯，但 AI 寫出來的東西，怎麼看都像機器人，根本不像我在店裡跟客人說話的口氣啊？」

這就是為什麼後天週三下午【第 3 講 · 終極壓軸】，我們要帶大家突破最關鍵的死穴：
《商業資料與價格架構 ✕ AI 擬人化工程：打造專屬 AI 數位店長》！

有手有腳沒有靈魂，只是個發公文的機器人；
有大腦有靈魂，才叫為你親自顧店的數位分身。

在這堂課，我們要徹底幫你的 AI 換上一顆在地心臟：
1. 建立單一真相價格庫（SSOT）：拒絕檔案混亂，價格規格分毫不差，告別 AI 亂報價。
2. 五層同心圓捏臉工程：把你的口頭禪、顧店習慣與人情溫度，1:1 刻印進去。
3. 現場實機對話驗收：開口不再是「親愛的顧客、竭誠為您服務」，而是像你親自倒茶寒暄一樣溫暖親切！

⚠️ 這堂課堅持【100% 純實體現場教學】，絕無線上同步。
導師現場個別巡桌調校，沒捏出合格的 AI 分身不准下課！
為求最高教學品質，【嚴格限額 6 席】，最後名額額滿即刻關門。

👉 實體席位申請表單與老學員特權，我直接放在【第一則留言】！

#生活管家 #生活就醬點 #AI實戰家教班 #AI擬人化工程 #打造專屬數位店長 #告別罐頭公文 #純實體教學 #限額6席"""

FB_FIRST_COMMENT = """🐾 11/25 (週三) 14:00 - 17:00《商業資料架構 ✕ AI 擬人化工程》
⚠️ 本課程堅持【純實體現場教學】，絕無線上課！導師逐桌調校，保證做出成果！
實體座位【嚴格限額 6 席】，額滿即關門（超過者將為您保留至加開場）：

📝 實體入席申請表：https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
👑 老學員回娘家：表單內勾選「老學員」即享學費 0 元免單特權！
🌟 新朋友實戰價：單堂 $500 元（審查通過後個別發送正取報到通知）

📍 上課地點：生活管家總部（台東市正氣北路166巷90號）
💬 官方 LINE 諮詢：https://lin.ee/z83YSq6 （加入後可直接私訊管家）"""

TH_CAPTION = """倒數 48 小時。

上週帶老闆們把發文發射台跑通了，
3 秒自動發文很爽，但老闆們問了下一句扎心話：
「AI 寫出來的文案，滿滿公文塑膠味，根本不像我在店裡跟客人說話啊？」

後天週三下午，第 3 講大壓軸：
《AI 擬人化工程：把老闆的靈魂捏進去》

告別冷冰冰的公文腔。
開口就像老闆親自倒熱茶、笑咪咪跟客人寒暄一樣有溫度。

純實體【嚴格限額 6 席】，沒捏出合格分身不准下課。
台東市正氣北路 166 巷 90 號。
報名表單我放在第一則留言，想捏出自己專屬 AI 分身的頭家，留言「分身」傳表單給你 ☕✨"""

TH_FIRST_COMMENT = """📝 11/25 (週三) 14:00 純實體席位申請表（限額 6 席）：
https://docs.google.com/forms/d/e/1FAIpQLSe9MXndx8AA2hqxS9tgAlreSdFtR3HapZJMWBU1k1UDTPvm-w/viewform
老學員回娘家 0 元免單，新朋友實戰價 500 元。
正氣北路家宅總部現場見！"""

def publish():
    print("🚀 [生活管家發射台] 開始執行發布流程...")
    
    # --- Facebook 發布 ---
    print("\n📘 [Facebook] 上傳圖片與發布主貼文...")
    url_fb_photo = f"https://graph.facebook.com/v21.0/{FB_PAGE_ID}/photos"
    with open(image_path, "rb") as img_file:
        files = {"source": img_file}
        data = {
            "caption": FB_CAPTION,
            "access_token": FB_PAGE_TOKEN
        }
        res_fb = requests.post(url_fb_photo, files=files, data=data).json()
    
    fb_post_id = res_fb.get("post_id") or res_fb.get("id")
    if not fb_post_id:
        print("❌ [Facebook] 發布失敗:", res_fb)
        return
    print(f"🎉 [Facebook] 主貼文發布成功！Post ID: {fb_post_id}")
    
    # 獲取高畫質 CDN 圖片網址供 Threads 調用
    photo_id = res_fb.get("id")
    url_pinfo = f"https://graph.facebook.com/v21.0/{photo_id}?fields=images&access_token={FB_PAGE_TOKEN}"
    r_pinfo = requests.get(url_pinfo).json()
    cdn_image_url = r_pinfo.get("images", [{}])[0].get("source", "")
    print(f"📸 [CDN] 提取高畫質圖片網址: {cdn_image_url[:60]}...")
    
    # Facebook 第一則留言
    time.sleep(2)
    url_fb_comment = f"https://graph.facebook.com/v21.0/{fb_post_id}/comments"
    res_fb_c = requests.post(url_fb_comment, data={
        "message": FB_FIRST_COMMENT,
        "access_token": FB_PAGE_TOKEN
    }).json()
    print(f"💬 [Facebook] 第一則留言發布成功！Comment ID: {res_fb_c.get('id')}")

    # --- Threads 發布 ---
    print("\n🧵 [Threads] 建立單圖容器並推播...")
    url_th_container = f"https://graph.threads.net/v1.0/{TH_UID}/threads"
    res_th_c = requests.post(url_th_container, data={
        "media_type": "IMAGE",
        "image_url": cdn_image_url,
        "text": TH_CAPTION,
        "access_token": TH_TOK
    }).json()
    
    th_creation_id = res_th_c.get("id")
    if not th_creation_id:
        print("❌ [Threads] 容器建立失敗:", res_th_c)
        return
    
    print("⏳ [Threads] 等待 5 秒完成伺服器轉碼...")
    time.sleep(5)
    
    url_th_publish = f"https://graph.threads.net/v1.0/{TH_UID}/threads_publish"
    res_th_pub = requests.post(url_th_publish, data={
        "creation_id": th_creation_id,
        "access_token": TH_TOK
    }).json()
    
    th_post_id = res_th_pub.get("id")
    if not th_post_id:
        print("❌ [Threads] 發布失敗:", res_th_pub)
        return
    print(f"🎉 [Threads] 單圖主貼文推播成功！Post ID: {th_post_id}")
    
    # Threads 第一則留言
    time.sleep(2)
    res_th_rep_c = requests.post(url_th_container, data={
        "media_type": "TEXT",
        "text": TH_FIRST_COMMENT,
        "reply_to_id": th_post_id,
        "access_token": TH_TOK
    }).json()
    
    th_rep_cid = res_th_rep_c.get("id")
    if th_rep_cid:
        time.sleep(2)
        res_th_rep_pub = requests.post(url_th_publish, data={
            "creation_id": th_rep_cid,
            "access_token": TH_TOK
        }).json()
        print(f"💬 [Threads] 第一則留言發布成功！Comment ID: {res_th_rep_pub.get('id')}")

    print("\n==========================================")
    print("🎯 雙平台發布大圓滿！零外部連結 ✕ 留言導流成功！")
    print(f"Facebook: https://www.facebook.com/{fb_post_id}")
    print("==========================================")

if __name__ == "__main__":
    publish()
