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
# 查詢當前 location 的詳細資料（readMask=*）
get_url = f"https://mybusinessbusinessinformation.googleapis.com/v1/locations/{location_id}?readMask=name,title,storeCode,categories,storefrontAddress,websiteUri,regularHours,specialHours,serviceArea,labels,adWordsLocationExtensions,latlng,openInfo,metadata,profile,relationshipData,moreHours"
res = requests.get(get_url, headers=headers)
print("Location details status:", res.status_code)
if res.status_code == 200:
    data = res.json()
    print("Categories:", json.dumps(data.get("categories"), ensure_ascii=False, indent=2))
    print("Profile:", json.dumps(data.get("profile"), ensure_ascii=False, indent=2))
    print("Metadata:", json.dumps(data.get("metadata"), ensure_ascii=False, indent=2))
