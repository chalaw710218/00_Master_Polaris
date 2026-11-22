# -*- coding: utf-8 -*-
import requests
import datetime
import os
import sys

# 1. 自動從 .secrets.env 讀取正式 Token
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

def upload_photo(img_path):
    url_photo = f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos'
    abs_path = os.path.abspath(img_path)
    with open(abs_path, 'rb') as f:
        files = {'source': f}
        data = {'access_token': TOKEN, 'published': 'false'}
        r = requests.post(url_photo, files=files, data=data)
        return r.json()

def schedule_feed_post(message, photo_id, dt_tw):
    ts = int(dt_tw.timestamp())
    url_feed = f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed'
    payload = {
        'access_token': TOKEN,
        'message': message,
        'published': False,
        'scheduled_publish_time': ts,
        'attached_media[0]': f'{{"media_fbid":"{photo_id}"}}'
    }
    r = requests.post(url_feed, data=payload)
    return r.json()

# ==============================================================================
# ☀️ 【第 1 篇】排程於 2026-11-22 09:00:00 TW
# ==============================================================================
dt_1 = datetime.datetime(2026, 11, 22, 9, 0, 0, tzinfo=tz_tw)
msg_1 = """【不用打字，用講話就能把一生的故事留給孩子】

很多台東長輩心裡都有很精彩的人生經歷，很想把走過的大半輩子留給孩子看，但每次一想到要打字、要用電腦，就覺得太難而作罷。

其實現在 AI 最棒的作用，就是當你的「隨身代筆秘書」。

你只要像平常跟朋友泡茶一樣「開口說話」，手機自動幫你把口語整理成順暢的文字，完全不需要碰鍵盤！

12 月初的【慢活口述寫作營】，兩邊都有實體教室，不用擔心自己摸索：
・台東市區：正氣路教室（品碩在現場一步一步陪寫）
・都蘭現場：四季八里莊園（阿鐘哥現場指導）
（住外地的朋友也可以線上同步參與）

6 週課程 3,000 元，帶你完成專屬的電子書稿（若想印成實體書留念，現場也能協助自費送印）。
11/28 截止確認開班人數。想留給子孫最溫暖禮物的朋友，詳細介紹與報名表放在留言區第一樓！"""

print("🚀 正在排程【第 1 篇】(今天 09:00)...")
res_photo_1 = upload_photo(r'02_Visual_Assets\poster_01_cinematic_final.jpg')
if 'id' in res_photo_1:
    res_post_1 = schedule_feed_post(msg_1, res_photo_1['id'], dt_1)
    print("✅ 【第 1 篇】成功上架排程！Post ID:", res_post_1.get('id', res_post_1))
else:
    print("❌ 【第 1 篇】海報上傳失敗:", res_photo_1)

# ==============================================================================
# 🌙 【第 2 篇】排程於 2026-11-22 19:30:00 TW
# ==============================================================================
dt_2 = datetime.datetime(2026, 11, 22, 19, 30, 0, tzinfo=tz_tw)
msg_2 = """【別花幾萬塊找行銷寫手，用嘴巴把你的品牌故事說出來】

在台東做農業、開特色小店，你對土地的堅持就是最好的品牌行銷。但每次要寫簡介或創業故事，坐在電腦前就是擠不出字？

其實你最感人的創業心血，用嘴巴講的最動聽！

這堂 6 週共創營，教你用 AI 當你的專屬文案助理：
・你只管開口講述創業的酸甜苦辣
・AI 自動幫你提煉成吸引人的品牌故事與章節
・在地文化作家江冠明老師親授心法，幫你的文字注入土地靈魂

台東市區正氣路教室有實體現場手把手陪產出。全期 6 堂 3,000 元（實體樣書送印自費），11/28 截止確認開班。
報名表單在留言區第一樓，給自己的品牌一次說故事的機會！"""

print("\n🚀 正在排程【第 2 篇】(今天 19:30)...")
res_photo_2 = upload_photo(r'02_Visual_Assets\poster_02_cinematic_final.jpg')
if 'id' in res_photo_2:
    res_post_2 = schedule_feed_post(msg_2, res_photo_2['id'], dt_2)
    print("✅ 【第 2 篇】成功上架排程！Post ID:", res_post_2.get('id', res_post_2))
else:
    print("❌ 【第 2 篇】海報上傳失敗:", res_photo_2)
