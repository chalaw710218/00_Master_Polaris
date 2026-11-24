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
url = f"https://mybusinessbusinessinformation.googleapis.com/v1/accounts/{account_id}/locations?readMask=name,title,storefrontAddress"

res = requests.get(url, headers=headers)
print("Status:", res.status_code)
if res.status_code == 200:
    locations = res.json().get("locations", [])
    print(f"Total verified locations under your account: {len(locations)}")
    for i, loc in enumerate(locations, 1):
        addr = loc.get("storefrontAddress", {})
        addr_line = "".join(addr.get("addressLines", []))
        print(f"{i}. 【{loc.get('title')}】 ID: {loc.get('name')} | 地址: {addr.get('locality', '')}{addr_line}")
