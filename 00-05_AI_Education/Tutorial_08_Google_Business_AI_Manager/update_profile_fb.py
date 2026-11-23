import json
import os

profile_path = r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\01_Taitung_Shokunin_Diner\data\store_profile.json"

with open(profile_path, "r", encoding="utf-8") as f:
    data = json.load(f)

data["social_profiles"] = {
    "facebook": "https://www.facebook.com/p/職人食堂-61561543646858/",
    "facebook_page_id": "61561543646858",
    "status": "LINKED_TO_GOOGLE_BUSINESS_PROFILE"
}

with open(profile_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated social_profiles in store_profile.json!")
