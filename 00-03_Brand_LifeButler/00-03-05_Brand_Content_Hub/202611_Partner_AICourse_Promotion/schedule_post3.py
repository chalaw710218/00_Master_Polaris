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
# ☀️ 【第 3 篇】排程於 2026-11-23 09:00:00 TW
# ==============================================================================
dt_3 = datetime.datetime(2026, 11, 23, 9, 0, 0, tzinfo=tz_tw)
ts_3 = int(dt_3.timestamp())

img3_path = os.path.abspath(r'02_Visual_Assets\postcard_01_final.jpg')
msg_3 = """【今年送給爸媽最珍貴的禮物：幫他們把人生經歷寫成一本書】

我們常聽爸媽講以前年輕時的打拼故事，每次聽都覺得好精彩，很想幫他們留下來，但自己平日上班顧家，根本抽不出時間整理。

都蘭共學堂 ✕ 江冠明老師的 6 週口述寫作營，就是專門為長輩設計的：
爸媽不用會電腦，只要坐在教室裡「開口聊天」，AI 就會幫忙把話梳理成章節，最後甚至套用模板排版成專屬書稿！

如果爸媽住在台東市區，直接來正氣路教室，品碩助教會在現場一步一步陪著爸媽操作，完全不用擔心長輩學不會。

全期 6 堂 3,000 元（若想印成實體書留念可協助自費送印），11/28 截止統計開班。
幫爸媽報名卡位，詳細表單已放在留言區第一樓！"""

print("🚀 正在上傳 Postcard 01 並排程【第 3 篇】(明天 09:00)...")
with open(img3_path, 'rb') as f:
    r_photo = requests.post(
        f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos',
        files={'source': f},
        data={'access_token': TOKEN, 'published': 'false'}
    )
res_photo = r_photo.json()
print("Photo 3 Result:", res_photo)

if 'id' in res_photo:
    payload = {
        'access_token': TOKEN,
        'message': msg_3,
        'published': False,
        'scheduled_publish_time': ts_3,
        'attached_media[0]': f'{{"media_fbid":"{res_photo["id"]}"}}'
    }
    r_feed = requests.post(f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed', data=payload)
    res_feed = r_feed.json()
    print("✅ 【第 3 篇】成功上架排程！Post ID:", res_feed.get('id', res_feed))
else:
    print("❌ 【第 3 篇】圖片上傳失敗:", res_photo)
