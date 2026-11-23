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

# 1. 查詢現有相片列表
media_url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/media"
res = requests.get(media_url, headers=headers)
print("Media GET status:", res.status_code)
if res.status_code == 200:
    data = res.json()
    items = data.get("mediaItems", [])
    print(f"Total media items: {len(items)}")
    for item in items[:5]:
        print("Item:", item.get("mediaFormat"), item.get("locationAssociation"), item.get("googleUrl", "")[:60])
else:
    print("Media GET error:", res.text)
