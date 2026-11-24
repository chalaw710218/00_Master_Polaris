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

tz_tw = datetime.timezone(datetime.timedelta(hours=8))

# ==============================================================================
# 🌙 【第 6 篇】排程於 2026-11-24 19:30:00 TW
# ==============================================================================
dt_6 = datetime.datetime(2026, 11, 24, 19, 30, 0, tzinfo=tz_tw)
ts_6 = int(dt_6.timestamp())

img6_path = os.path.abspath(r'02_Visual_Assets\postcard_04_final.jpg')
msg_6 = """【「我連複製貼上都不會，真的能學會 AI 寫書嗎？」】

很多人看到「AI」這兩個字，第一反應是：「這太高級了，我年紀大又不懂電腦，一定學不會。」

請完全放心！這堂課設計的初衷，就是給「完全不會打字、老花眼、甚至害怕電腦的人」上的！

・你只需要帶一張嘴：散步或坐著聊天說話，AI 自動幫你打字潤稿
・現場有人坐身邊：在台東市區正氣路教室，品碩助教全程坐在旁邊教你按手機，一步一步陪你完成專屬電子書稿（實體送印自費）

6 堂實戰只要 3,000 元。11/28（本週五）統計人數，差幾位就開班！
表單在留言區第一樓，放膽給自己一次嘗試的機會吧！"""

print("🚀 正在上傳 Postcard 04 並排程【第 6 篇】(今天 19:30)...")
with open(img6_path, 'rb') as f:
    r_photo = requests.post(
        f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos',
        files={'source': f},
        data={'access_token': TOKEN, 'published': 'false'}
    )
res_photo = r_photo.json()
print("Photo 6 Result:", res_photo)

if 'id' in res_photo:
    payload = {
        'access_token': TOKEN,
        'message': msg_6,
        'published': False,
        'scheduled_publish_time': ts_6,
        'attached_media[0]': f'{{"media_fbid":"{res_photo["id"]}"}}'
    }
    r_feed = requests.post(f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed', data=payload)
    res_feed = r_feed.json()
    print("✅ 【第 6 篇】成功上架排程！Post ID:", res_feed.get('id', res_feed))
else:
    print("❌ 【第 6 篇】圖片上傳失敗:", res_photo)
