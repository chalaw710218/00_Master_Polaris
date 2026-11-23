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
menu_url = f"https://mybusiness.googleapis.com/v4/accounts/112884798662846885062/locations/{location_id}/foodMenus"

res = requests.get(menu_url, headers=headers)
print("GET foodMenus:", res.status_code)
if res.status_code == 200:
    data = res.json()
    with open(os.path.join(mgr_dir, "current_food_menus.json"), "w", encoding="utf-8") as out_f:
        json.dump(data, out_f, ensure_ascii=False, indent=2)
    print("Saved current_food_menus.json! Summary:")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
