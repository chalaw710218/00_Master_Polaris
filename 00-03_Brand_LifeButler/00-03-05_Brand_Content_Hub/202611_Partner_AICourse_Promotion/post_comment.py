# -*- coding: utf-8 -*-
import requests
import sys

secrets_path = r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.secrets.env'
TOKEN = ''

with open(secrets_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('FB_PAGE_ACCESS_TOKEN='):
            TOKEN = line.split('=', 1)[1].strip()

FIRST_COMMENT_TEXT = """📋【慢活寫作共創營】詳細介紹與線上報名表單：
👉 https://docs.google.com/forms/d/e/1FAIpQLScaDQISH90wSn0ZX013VRshzlH-ISCDMvZqxChLm05UkYUEaQ/viewform

・開課時間：12/4 起每週五晚間 19:00～21:00（共 6 堂）
・實體教室：台東市正氣路教室 ／ 都蘭四季八里自然莊園（亦有線上視訊）
・費用：全期 3,000 元（含專屬出書排版模板；實體樣書送印需自費）
・重要期程：11/28 截止確認開班人數
・課程諮詢電話：品碩 0972-928-864 ／ 阿鐘哥 0908-853-322"""

def post_comment(post_id):
    url = f'https://graph.facebook.com/v20.0/{post_id}/comments'
    payload = {
        'access_token': TOKEN,
        'message': FIRST_COMMENT_TEXT
    }
    r = requests.post(url, data=payload)
    res = r.json()
    if 'id' in res:
        print(f"✅ 第一則留言發布成功！Comment ID: {res['id']}")
    else:
        print(f"❌ 第一則留言發布失敗: {res}")
    return res

if __name__ == '__main__':
    # 支援傳入 post_id，預設第 1 篇
    pid = sys.argv[1] if len(sys.argv) > 1 else '110505444816362_1170497268992508'
    print(f"💬 正在為貼文 {pid} 發布第一則留言...")
    post_comment(pid)
