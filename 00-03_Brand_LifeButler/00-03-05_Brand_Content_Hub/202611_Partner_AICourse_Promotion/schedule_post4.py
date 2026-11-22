# -*- coding: utf-8 -*-
import requests
import datetime
import os
import sys

secrets_path = r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.secrets.env'
PAGE_ID = '110505444816362'
TOKEN = ''

with open(secrets_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('FB_PAGE_ACCESS_TOKEN='):
            TOKEN = line.split('=', 1)[1].strip()
        elif line.startswith('FB_PAGE_ID='):
            PAGE_ID = line.split('=', 1)[1].strip()

if not TOKEN:
    print("❌ 找不到有效 TOKEN！")
    sys.exit(1)

tz_tw = datetime.timezone(datetime.timedelta(hours=8))

# ==============================================================================
# 🌙 【第 4 篇】排程於 2026-11-23 19:30:00 TW
# ==============================================================================
dt_4 = datetime.datetime(2026, 11, 23, 19, 30, 0, tzinfo=tz_tw)
ts_4 = int(dt_4.timestamp())

img4_path = os.path.abspath(r'02_Visual_Assets\postcard_02_final.jpg')
msg_4 = """【學了半年 AI，你做出過任何一件真正的作品嗎？】

很多人買了線上課、看了幾十支教學影片，結果還是只停在跟 AI 問問天氣、改改幾句公文。

真正的 AI 學習，不是記一堆 Prompt 指令，而是直接完成一件具體落地的成果！

都蘭共學堂 6 週寫作營：
不講空泛理論，直接帶你從「語音口述 ➔ AI 潤稿 ➔ 篇章結構 ➔ 專屬排版」完成一本真正屬於你的個人電子書稿（現場亦可協助自費送印成實體書）。

全期 6 堂 3,000 元（平均一堂才 500 元，市區正氣路教室有實體助教現場陪跑）。
11/28 截止開班統計，詳細課表與報名連結在留言區第一樓！"""

print("🚀 正在上傳 Postcard 02 並排程【第 4 篇】(明天 19:30)...")
with open(img4_path, 'rb') as f:
    r_photo = requests.post(
        f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos',
        files={'source': f},
        data={'access_token': TOKEN, 'published': 'false'}
    )
res_photo = r_photo.json()
print("Photo 4 Result:", res_photo)

if 'id' in res_photo:
    payload = {
        'access_token': TOKEN,
        'message': msg_4,
        'published': False,
        'scheduled_publish_time': ts_4,
        'attached_media[0]': f'{{"media_fbid":"{res_photo["id"]}"}}'
    }
    r_feed = requests.post(f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed', data=payload)
    res_feed = r_feed.json()
    print("✅ 【第 4 篇】成功上架排程！Post ID:", res_feed.get('id', res_feed))
else:
    print("❌ 【第 4 篇】圖片上傳失敗:", res_photo)
