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

# 依據 Google 規範，attributeMask 為需要更新的屬性名稱，逗號分隔
attr_names = [
    "attributes/has_takeout",
    "attributes/serves_dine_in",
    "attributes/has_seating",
    "attributes/serves_lunch",
    "attributes/serves_dinner",
    "attributes/requires_cash_only"
]
mask_str = ",".join(attr_names)
url = f"https://mybusinessbusinessinformation.googleapis.com/v1/locations/{location_id}/attributes?attributeMask={mask_str}"

payload = {
  "attributes": [
    {
      "name": "attributes/has_takeout",
      "valueType": "BOOL",
      "values": [True]
    },
    {
      "name": "attributes/serves_dine_in",
      "valueType": "BOOL",
      "values": [True]
    },
    {
      "name": "attributes/has_seating",
      "valueType": "BOOL",
      "values": [True]
    },
    {
      "name": "attributes/serves_lunch",
      "valueType": "BOOL",
      "values": [True]
    },
    {
      "name": "attributes/serves_dinner",
      "valueType": "BOOL",
      "values": [True]
    },
    {
      "name": "attributes/requires_cash_only",
      "valueType": "BOOL",
      "values": [True]
    }
  ]
}

res = requests.patch(url, headers=headers, json=payload)
print("Update attributes status:", res.status_code)
if res.status_code == 200:
    print("Successfully updated attributes!")
    print(res.text[:300])
else:
    print("Error:", res.text[:400])
