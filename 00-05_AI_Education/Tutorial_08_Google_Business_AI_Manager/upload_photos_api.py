import json
import os
import requests
from google.oauth2.credentials import Credentials

mgr_dir = r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager"
token_path = os.path.join(mgr_dir, "token.json")

with open(token_path, "r", encoding="utf-8") as f:
    token_data = json.load(f)

creds = Credentials.from_authorized_user_info(token_data)
headers = {
    "Authorization": f"Bearer {creds.token}",
    "Content-Type": "application/json"
}

account_id = "112884798662846885062"
location_id = "1774177451467087781"
media_create_url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/media"

photos = [
    {
        "name": "手工爆汁小籠湯包",
        "url": "https://raw.githubusercontent.com/chalaw710218/shokunin-taitung/main/images/soup_dumplings_macro.jpg",
        "category": "FOOD_AND_DRINK",
        "description": "現點現蒸爆汁手工小籠湯包，皮薄餡豐湯汁鮮甜"
    },
    {
        "name": "柴魚昆布讚岐烏龍麵",
        "url": "https://raw.githubusercontent.com/chalaw710218/shokunin-taitung/main/images/udon_macro.jpg",
        "category": "FOOD_AND_DRINK",
        "description": "北海道昆布與柴魚熬煮清冽甘甜高湯，搭配彈牙讚岐烏龍麵"
    },
    {
        "name": "炙燒牛五花燒肉丼飯",
        "url": "https://raw.githubusercontent.com/chalaw710218/shokunin-taitung/main/images/oyakodon_macro.jpg",
        "category": "FOOD_AND_DRINK",
        "description": "高溫炙燒焦香牛五花，搭配溫泉蛋、胡麻綠花椰與特製泡菜"
    }
]

for p in photos:
    payload = {
        "mediaFormat": "PHOTO",
        "locationAssociation": {
            "category": p["category"]
        },
        "sourceUrl": p["url"],
        "description": p["description"]
    }
    res = requests.post(media_create_url, headers=headers, json=payload)
    print(f"Uploading {p['name']}: Status {res.status_code}")
    if res.status_code in [200, 201]:
        print("Success:", res.json().get("name"), res.json().get("googleUrl"))
    else:
        print("Error details:", res.text)
