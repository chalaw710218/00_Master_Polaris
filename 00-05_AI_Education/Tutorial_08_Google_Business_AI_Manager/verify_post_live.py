import json
import os
import time
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

post_name = "accounts/112884798662846885062/locations/1774177451467087781/localPosts/8567287819535635169"
get_url = f"https://mybusiness.googleapis.com/v4/{post_name}"

for i in range(3):
    time.sleep(3)
    res = requests.get(get_url, headers=headers)
    print(f"Check {i+1} status:", res.status_code)
    if res.status_code == 200:
        data = res.json()
        print("Current state:", data.get("state"))
        if data.get("state") == "LIVE":
            print("Post is LIVE!")
            print(json.dumps(data, ensure_ascii=False, indent=2))
            break
