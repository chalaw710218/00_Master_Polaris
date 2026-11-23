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
url = f"https://mybusinessbusinessinformation.googleapis.com/v1/locations/{location_id}/attributes"

# 查看當前完整的 attribute 物件結構
res = requests.get(url, headers=headers)
print("Current attributes JSON:")
data = res.json()
print(json.dumps(data, ensure_ascii=False, indent=2))
