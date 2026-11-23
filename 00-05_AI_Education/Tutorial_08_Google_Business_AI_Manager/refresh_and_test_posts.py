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
    print("Token expired, refreshing...")
    creds.refresh(Request())
    # Save back
    with open(token_path, "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    print("Token refreshed successfully!")

headers = {
    "Authorization": f"Bearer {creds.token}",
    "Content-Type": "application/json"
}

account_id = "112884798662846885062"
location_id = "1774177451467087781"

list_url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/localPosts"
res = requests.get(list_url, headers=headers)
print("List localPosts status:", res.status_code)
if res.status_code == 200:
    print("Existing posts count:", len(res.json().get("localPosts", [])))
else:
    print("List error:", res.text[:300])
