import json
import os
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

mgr_dir = r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager"
token_path = os.path.join(mgr_dir, "token.json")

with open(token_path, "r", encoding="utf-8") as f:
    token_data = json.load(f)

creds = Credentials.from_authorized_user_info(token_data)
if not creds.valid or creds.expired:
    creds.refresh(Request())
    with open(token_path, "w", encoding="utf-8") as f:
        f.write(creds.to_json())

headers = {
    "Authorization": f"Bearer {creds.token}",
    "Content-Type": "application/json"
}

account_id = "112884798662846885062"
location_id = "1774177451467087781"
post_url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/localPosts"

post_payload = {
    "languageCode": "zh-Hant",
    "summary": "【堅持手工現點現蒸・鎖住鮮甜爆汁美味！】\n\n微涼的季節，最需要一籠熱氣蒸騰的溫暖滋味！\n職人食堂堅持每日新鮮備餡，手工捏製透光薄皮，現點現蒸不微波，咬開滿滿鮮甜肉汁！搭配現切薑絲與特調烏醋，一口入魂。\n\n🥢 招牌人氣推薦：\n・手工爆汁小籠湯包（NT$ 80）\n・打拋豬小籠湯包（NT$ 90）\n・柴魚昆布讚岐烏龍麵（NT$ 90）\n・炙燒牛五花燒肉丼飯（NT$ 170）\n\n現蒸約需 8~10 分鐘，趕時間的鄉親朋友歡迎提早來電預訂，為您提早出蒸籠熱騰騰帶著走！\n\n📍 門市地址：台東市安慶街60號\n📞 外帶專線：089-342900 / 0933-512-505",
    "callToAction": {
        "actionType": "CALL"
    },
    "media": [
        {
            "mediaFormat": "PHOTO",
            "sourceUrl": "https://raw.githubusercontent.com/chalaw710218/shokunin-taitung/main/images/soup_dumplings_macro.jpg"
        }
    ],
    "topicType": "STANDARD"
}

res = requests.post(post_url, headers=headers, json=post_payload)
print("Create LocalPost status:", res.status_code)
if res.status_code in [200, 201]:
    data = res.json()
    print("Post created successfully!")
    print("Post Name:", data.get("name"))
    print("Search URL:", data.get("searchUrl"))
    print("State:", data.get("state"))
else:
    print("Error:", res.text)
    # 如果 CALL 需要 url 或不支援，嘗試 LEARN_MORE
    if "callToAction" in res.text:
        print("Retrying with LEARN_MORE...")
        post_payload["callToAction"] = {
            "actionType": "LEARN_MORE",
            "url": "https://chalaw710218.github.io/shokunin-taitung/"
        }
        res2 = requests.post(post_url, headers=headers, json=post_payload)
        print("Retry status:", res2.status_code, res2.text[:300])
