import json
import os

profile_path = r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\01_Taitung_Shokunin_Diner\data\store_profile.json"

with open(profile_path, "r", encoding="utf-8") as f:
    data = json.load(f)

data["latest_post_20261123"] = {
    "post_id": "8567287819535635169",
    "state": "LIVE",
    "createTime": "2026-11-23T15:06:56Z",
    "title_topic": "堅持手工現點現蒸・鎖住鮮甜爆汁美味！",
    "searchUrl": "https://local.google.com/place?id=2490326888156108049&use=posts&lpsid=CAIQACoeChxtc3BfaDpPTkdxMUJCRjhCZ3UzWGVEczYwZVdB",
    "media_google_url": "https://lh3.googleusercontent.com/p/AF1QipNYl0U9wHLELE2XypDblcLyhawrMR7DYptnN0NG",
    "call_to_action": "CALL (撥打電話預約外帶)"
}

with open(profile_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated store_profile.json with latest post!")
