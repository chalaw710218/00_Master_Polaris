# -*- coding: utf-8 -*-
import requests
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

img_path = os.path.abspath(r'02_Visual_Assets\postcard_03_final.jpg')
msg_5 = """【家裡長輩的拿手菜味道，你有多久沒記錄下來了？】

每個家庭都有一道只有媽媽、阿嬤才做得出來的招牌菜，還有那些老一輩人才知道的家族老故事。如果沒有記下來，幾十年後可能就漸漸被淡忘了。

這次的慢活口述營，很適合陪長輩一起來：
・長輩坐在椅子上一邊回憶、一邊講述料理撇步
・手機 AI 自動把口述步驟、回憶細節整理成精美的圖文手冊
・6 週後，完成一本專屬於你們家的「家族傳承記憶冊」（可協助自費送印）

市區正氣路教室現場有品碩助教手把手協助。全期 3,000 元，11/28 截止開班統計。
報名表單在留言區第一樓，一起把最珍貴的家族味道留下來！"""

first_comment_text = """📋【慢活寫作共創營】詳細介紹與線上報名表單：
👉 https://docs.google.com/forms/d/e/1FAIpQLScaDQISH90wSn0ZX013VRshzlH-ISCDMvZqxChLm05UkYUEaQ/viewform

・開課時間：12/4 起每週五晚間 19:00～21:00（共 6 堂）
・實體教室：台東市正氣路教室 ／ 都蘭四季八里自然莊園（亦有線上視訊）
・費用：全期 3,000 元（含專屬出書排版模板；實體樣書送印需自費）
・重要期程：11/28 截止確認開班人數
・課程諮詢電話：品碩 0972-928-864 ／ 阿鐘哥 0908-853-322"""

print("📸 正在上傳 Postcard 03...")
with open(img_path, 'rb') as f:
    r_photo = requests.post(
        f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos',
        files={'source': f},
        data={'access_token': TOKEN, 'published': 'false'}
    )
res_photo = r_photo.json()
print("Photo result:", res_photo)

if 'id' in res_photo:
    mid = res_photo['id']
    payload = {
        'access_token': TOKEN,
        'message': msg_5,
        'published': True,
        'attached_media[0]': f'{{"media_fbid":"{mid}"}}'
    }
    r_feed = requests.post(f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed', data=payload)
    res_feed = r_feed.json()
    print("Feed post result:", res_feed)
    
    if 'id' in res_feed:
        post_id = res_feed['id']
        print(f"🎉 貼文即時發布成功！Post ID: {post_id}")
        
        # 立即發布第一則留言
        r_comment = requests.post(
            f'https://graph.facebook.com/v20.0/{post_id}/comments',
            data={'access_token': TOKEN, 'message': first_comment_text}
        )
        res_comment = r_comment.json()
        print(f"✅ 第一則留言發布結果: {res_comment}")
    else:
        print("❌ 貼文發布失敗:", res_feed)
else:
    print("❌ 圖片上傳失敗:", res_photo)
