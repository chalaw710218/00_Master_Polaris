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

location_id = "1774177451467087781"

# 1. 查詢可用的 attributes 或當前 attributes
url = f"https://mybusinessbusinessinformation.googleapis.com/v1/locations/{location_id}/attributes"
res = requests.get(url, headers=headers)
print("Attributes GET status:", res.status_code)
if res.status_code == 200:
    data = res.json()
    print("Current attributes count:", len(data.get("attributes", [])))
    for a in data.get("attributes", []):
        print(a.get("name"), a.get("values"), a.get("valueType"))
else:
    print("Error:", res.text[:400])

# 也測試 categories.batchGet 或 attributes 列表
