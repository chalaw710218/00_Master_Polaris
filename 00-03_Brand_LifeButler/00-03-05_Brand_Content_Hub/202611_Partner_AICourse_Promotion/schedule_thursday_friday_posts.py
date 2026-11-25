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

schedule_queue = [
    {
        'num': 9,
        'title': '市區免奔波篇',
        'dt': datetime.datetime(2026, 11, 26, 9, 0, 0, tzinfo=tz_tw),
        'img': os.path.abspath(r'02_Visual_Assets\postcard_07_final.jpg'),
        'msg': """【住在台東市區的朋友，不用大老遠跑都蘭！正氣路教室現場陪寫】

之前有幾位市區朋友說：「這堂課聽說很棒，但我住在台東市區，每週五晚上開車跑都蘭山路有點遠，怎麼辦？」

其實我們在台東市區「正氣路教室」有實體同步班！

・市區朋友直接在正氣路教室上課，市區免奔波
・我（品碩）會在現場，一對一陪大家操作手機語音、大綱梳理到電子書排版（想印實體書現場亦協助自費送印）
・都蘭海線的朋友則就近去四季八里莊園找阿鐘哥

全期 6 堂共 3,000 元（平均一堂 500 元）。本週五 11/28 截止確認開班人數！
想就近在市區學會口述出書的朋友，報名表單已放在留言區第一樓！"""
    },
    {
        'num': 10,
        'title': '一堂500元CP值篇',
        'dt': datetime.datetime(2026, 11, 26, 19, 30, 0, tzinfo=tz_tw),
        'img': os.path.abspath(r'02_Visual_Assets\postcard_08_final.jpg'),
        'msg': """【一堂 500 元的寫作課：雙師資 ✕ 實體助教 ✕ 電子書模板全包】

市面上一般的 AI 課程，動輒要價數千甚至上萬元，而且大部分只是給你看預錄影片。

都蘭共學堂這次辦的 6 週口述寫作營，全期 3,000 元，平均一堂才 500 元：
・兩位資深老師雙師聯手（江冠明作家心法 ＋ 哈爸實戰工具）
・台東市正氣路與都蘭四季八里兩大實體教室，助教在身邊手把手指導
・附贈專屬電子書出書排版模板，幫你省去幾千元的排版費（實體送印自費）

這不是昂貴的商業課，而是在地共生共學的溫暖平台。
11/28 截止開班人數統計，詳細課表與報名連結在留言區第一樓！"""
    },
    {
        'num': 11,
        'title': '倒數36小時告急篇',
        'dt': datetime.datetime(2026, 11, 27, 9, 0, 0, tzinfo=tz_tw),
        'img': os.path.abspath(r'02_Visual_Assets\postcard_09_final.jpg'),
        'msg': """【只差最後幾位就開班！明天 11/28 截止人數統計】

很感謝這幾天許多朋友詢問慢活口述寫作營的細節。

為了維持實體班每個人都能被照顧到的小班品質，我們滿 12 人就開班。明天（11/28）晚上 11 點是最後的人數盤點，如果人數不足額，這期課程就會直接順延。

如果你心裡一直想把自己的故事留下來、想學會用手機口述完成一本專屬電子書稿：
請不要再猶豫了，正氣路教室與都蘭教室的助教都已經準備好陪你一起寫！

全期 6 堂 3,000 元。把握最後席次，報名表單在留言區第一樓！"""
    },
    {
        'num': 12,
        'title': '今晚最後壓線篇',
        'dt': datetime.datetime(2026, 11, 27, 19, 30, 0, tzinfo=tz_tw),
        'img': os.path.abspath(r'02_Visual_Assets\postcard_10_final.jpg'),
        'msg': """【今晚最後倒數：給自己這個冬天，留下一本專屬的書】

今晚是【第二期慢活寫作共創營】確認開班人數的最後死線。

歲月走得很快，很多記憶如果不去捕捉，慢慢就會模糊。給自己一個週五晚上的時間，給自己泡杯茶，坐在教室裡，跟著老師和同伴，把那些走過的路、愛過的人、流過的汗，用自己的聲音說出來。

6 週後，你會收穫一本排版完整的專屬電子書稿，甚至能自費印成一本捧在手心的實體書送給自己。

台東市正氣路教室（品碩駐場）✕ 都蘭四季八里（阿鐘駐場）。
今晚最後報名機會，表單在留言區第一樓，期待下週五與你見面！"""
    }
]

def schedule_all():
    for item in schedule_queue:
        num = item['num']
        ts = int(item['dt'].timestamp())
        img_path = item['img']
        print(f"🚀 正在排程【第 {num} 篇】({item['title']}) 至 {item['dt'].strftime('%Y-%m-%d %H:%M:%S')}...")

        with open(img_path, 'rb') as f:
            r_photo = requests.post(
                f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos',
                files={'source': f},
                data={'access_token': TOKEN, 'published': 'false'}
            )
        res_photo = r_photo.json()
        if 'id' not in res_photo:
            print(f"❌ 【第 {num} 篇】圖片上傳失敗:", res_photo)
            continue

        payload = {
            'access_token': TOKEN,
            'message': item['msg'],
            'published': False,
            'scheduled_publish_time': ts,
            'attached_media[0]': f'{{"media_fbid":"{res_photo["id"]}"}}'
        }
        r_feed = requests.post(f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed', data=payload)
        res_feed = r_feed.json()
        print(f"✅ 【第 {num} 篇】成功上架排程！Post ID:", res_feed.get('id', res_feed))

if __name__ == '__main__':
    schedule_all()
