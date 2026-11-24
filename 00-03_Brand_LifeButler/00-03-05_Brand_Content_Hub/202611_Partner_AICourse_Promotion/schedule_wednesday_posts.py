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

# -------------------------------------------------------------
# Post 7: 2026-11-25 09:00 TW
# -------------------------------------------------------------
dt_7 = datetime.datetime(2026, 11, 25, 9, 0, 0, tzinfo=tz_tw)
ts_7 = int(dt_7.timestamp())
img7_path = os.path.abspath(r'02_Visual_Assets\postcard_05_final.jpg')
msg_7 = """【來到台東生活這幾年，你心裡的故事沈澱好了嗎？】

很多人選擇移居台東，都是人生中一段非常重要的轉折。告別城市的喧囂，在太平洋的海浪聲與都蘭的微風裡，每個人心裡都有一段值得被溫柔記錄的生命故事。

如果你一直想把這段追尋自我的過程寫下來：
在地作家江冠明老師帶你進入深度的生命敘事，哈爸老師教你用手機口述捕捉靈感。

在放鬆的山海氛圍裡，把內心的沉澱化為一部專屬書稿（亦可協助自費送印）。
雙實體教室：台東市正氣路（品碩駐場）／ 都蘭四季八里（阿鐘駐場）。

全期 6 堂 3,000 元，11/28 截止確認開班。
詳細課表在留言區第一樓，期待與你在文字中相遇。"""

print("🚀 正在排程【第 7 篇】(週三 09:00)...")
with open(img7_path, 'rb') as f:
    r7 = requests.post(
        f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos',
        files={'source': f},
        data={'access_token': TOKEN, 'published': 'false'}
    )
res7 = r7.json()
if 'id' in res7:
    payload7 = {
        'access_token': TOKEN,
        'message': msg_7,
        'published': False,
        'scheduled_publish_time': ts_7,
        'attached_media[0]': f'{{"media_fbid":"{res7["id"]}"}}'
    }
    r_feed7 = requests.post(f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed', data=payload7)
    res_feed7 = r_feed7.json()
    print("✅ 【第 7 篇】成功上架排程！Post ID:", res_feed7.get('id', res_feed7))
else:
    print("❌ 【第 7 篇】圖片上傳失敗:", res7)

# -------------------------------------------------------------
# Post 8: 2026-11-25 19:30 TW
# -------------------------------------------------------------
dt_8 = datetime.datetime(2026, 11, 25, 19, 30, 0, tzinfo=tz_tw)
ts_8 = int(dt_8.timestamp())
img8_path = os.path.abspath(r'02_Visual_Assets\postcard_06_final.jpg')
msg_8 = """【治好寫作拖延症：江冠明作家心法 ✕ AI 大綱架構】

你是不是也曾經雄心壯志想寫一本自己的書，但每次坐在電腦前，修修改改兩個小時，連第一章大綱都定不下來？

寫作最怕的不是沒有故事，而是「沒有系統和同伴」。

這堂 6 週慢活寫作營能幫你破關：
1. 哈爸教你用 AI 盤點記憶，10 分鐘搭出全書目錄骨架
2. 江冠明老師帶你進入真實敘事，學會捕捉細節與情感
3. 正氣路與都蘭現場助教每週陪跑，讓你想拖延都難！

6 週帶你產出專屬完整書稿（若想印出實體樣書可協助自費送印）。全期 3,000 元。
11/28 截止統計開班，報名表單在留言區第一樓！"""

print("🚀 正在排程【第 8 篇】(週三 19:30)...")
with open(img8_path, 'rb') as f:
    r8 = requests.post(
        f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos',
        files={'source': f},
        data={'access_token': TOKEN, 'published': 'false'}
    )
res8 = r8.json()
if 'id' in res8:
    payload8 = {
        'access_token': TOKEN,
        'message': msg_8,
        'published': False,
        'scheduled_publish_time': ts_8,
        'attached_media[0]': f'{{"media_fbid":"{res8["id"]}"}}'
    }
    r_feed8 = requests.post(f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed', data=payload8)
    res_feed8 = r_feed8.json()
    print("✅ 【第 8 篇】成功上架排程！Post ID:", res_feed8.get('id', res_feed8))
else:
    print("❌ 【第 8 篇】圖片上傳失敗:", res8)
