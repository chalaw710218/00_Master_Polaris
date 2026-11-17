import requests
import json
import sys
import os

PAGE_ID = '110505444816362'
TOKEN = 'EAATKJBLZArMgBTNM3QQIHc1digSFLIZBgv3CbrO7ZB8EsFPqlioqMk1dRl1kNvwsml3fZBk2Ww2SOaZCcZACByKTYZC5DtbwlHl2QlaLsZA9iykZBBbOqiQKxhzAf98OKgLMAmqRKOYc2cWm0NcaTcHGiz2N2neXK66ZAS8iQvECLNlsJnnnrdf77D8eOXAAsZBRzhk89x39Q0mdYjOOMVaFn5uq0IZD'

photo_path = r"00-03_Brand_LifeButler\00-03-01_Marketing_Assets\20261117_免費送_生活良品器皿.jpg"

message = """【下午快閃・免費送】讓美好的生活器皿，在台東找到珍惜它的新主人 ☕✨

今天整理生活物資時，紙箱蓋上靜靜寫著：「免費送，讓價值延續」。

看著箱子裡這些乾淨如新的生活良品——手提保溫壺、隨行冷熱杯、手沖花茶壺、一整套復古印花玻璃杯，還有典雅的陶瓷小碟與瓷碗……每一件都還散發著家的溫度，好好的東西放在櫃子裡太寂寞，最好的方式就是走進另一座溫暖的廚房。

惜物、愛物，讓日常美好的器皿繼續陪伴日常。
生活管家今天下午限時開放，免費與有緣的朋友結緣！

---

📦【快閃免費結緣明細】
・隨身手提保溫壺／運動隨行杯
・泡茶咖啡壺／雙層保溫杯
・經典印花透明玻璃杯套組
・典雅日式小花陶瓷小碟／白瓷碗

⏰【自取時間】
今天（11/17 週二）下午 14:00 ～ 17:00（限時快閃，送完為止）

📍【自取地點】
生活管家 正氣北路家宅據點（台東市正氣北路巷內）

📍【領取方式】
為避免大家撲空，請在底下留言「+1」或直接私訊【生活管家】，小幫手會即刻為您登記保留並提供詳細家宅門牌與導航資訊。
（一人限選 1～2 樣，讓更多家庭都能分享這份惜物的心意～）

#生活的一部分就醬點 #生活管家 #台東惜物日常 #免費送 #生活良品 #價值延續 #台東快閃"""

def publish():
    print("1. 上傳照片至 Facebook...")
    url_photo = f'https://graph.facebook.com/v20.0/{PAGE_ID}/photos'
    with open(photo_path, 'rb') as f:
        r = requests.post(url_photo, files={'source': f}, data={'access_token': TOKEN, 'published': 'false'})
        res = r.json()
        if 'id' not in res:
            print("圖片上傳失敗:", res)
            return
        photo_id = res['id']
        print(f"圖片上傳成功, ID: {photo_id}")

    print("2. 發布公開貼文...")
    url_feed = f'https://graph.facebook.com/v20.0/{PAGE_ID}/feed'
    payload = {
        'access_token': TOKEN,
        'message': message,
        'attached_media[0]': f'{{"media_fbid":"{photo_id}"}}',
        'published': True
    }
    r2 = requests.post(url_feed, data=payload)
    post_res = r2.json()
    print("貼文發布結果:", post_res)

    if 'id' in post_res:
        post_id = post_res['id']
        print("3. 自動發表第一則留言（防降權導流）...")
        url_comment = f'https://graph.facebook.com/v20.0/{post_id}/comments'
        comment_payload = {
            'access_token': TOKEN,
            'message': '👉 提醒大家：器皿均保存良好但數量有限，一人以 1~2 樣為原則～需要的朋友請私訊粉專索取自取地址，管家會依照訊息順序為您保留喔！'
        }
        r3 = requests.post(url_comment, data=comment_payload)
        print("留言發布結果:", r3.json())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--publish":
        publish()
    else:
        print("Dry run mode. Pass --publish to really send.")
