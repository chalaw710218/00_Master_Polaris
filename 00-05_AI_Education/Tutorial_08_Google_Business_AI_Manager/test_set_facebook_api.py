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

location_id = "1774177451467087781"
url = f"https://mybusinessbusinessinformation.googleapis.com/v1/locations/{location_id}/attributes?attributeMask=attributes/url_facebook"

# 測試用不同的 values 格式傳入 Facebook URL
fb_url = "https://www.facebook.com/profile.php?id=61561543646858"

payload = {
    "attributes": [
        {
            "name": "attributes/url_facebook",
            "values": [fb_url]
        }
    ]
}

res = requests.patch(url, headers=headers, json=payload)
print("Update url_facebook status:", res.status_code)
print("Response:", res.text[:400])
