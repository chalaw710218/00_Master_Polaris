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
location_id = "1774177451467087781"

audit_report = {}

# 1. 基本資訊與類別
loc_url = f"https://mybusinessbusinessinformation.googleapis.com/v1/locations/{location_id}?readMask=name,title,categories,storefrontAddress,websiteUri,profile,metadata"
res_loc = requests.get(loc_url, headers=headers)
if res_loc.status_code == 200:
    audit_report["location_info"] = res_loc.json()

# 2. 屬性標籤 (Attributes)
attr_url = f"https://mybusinessbusinessinformation.googleapis.com/v1/locations/{location_id}/attributes"
res_attr = requests.get(attr_url, headers=headers)
if res_attr.status_code == 200:
    audit_report["attributes"] = res_attr.json().get("attributes", [])

# 3. 結構化菜單 (Food Menus)
menu_url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/foodMenus"
res_menu = requests.get(menu_url, headers=headers)
if res_menu.status_code == 200:
    audit_report["food_menus"] = res_menu.json()

# 4. 相簿照片 (Media Items)
media_url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/media"
res_media = requests.get(media_url, headers=headers)
if res_media.status_code == 200:
    items = res_media.json().get("mediaItems", [])
    audit_report["media_count"] = len(items)
    audit_report["latest_media"] = items[-3:] if len(items) >= 3 else items

# 5. 最新動態 (Local Posts)
posts_url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/localPosts"
res_posts = requests.get(posts_url, headers=headers)
if res_posts.status_code == 200:
    posts = res_posts.json().get("localPosts", [])
    audit_report["posts_count"] = len(posts)
    audit_report["latest_post"] = posts[0] if posts else None

# 6. 評論現況 (Reviews)
rev_url = f"https://mybusiness.googleapis.com/v4/accounts/{account_id}/locations/{location_id}/reviews"
res_rev = requests.get(rev_url, headers=headers)
if res_rev.status_code == 200:
    rev_data = res_rev.json()
    audit_report["total_reviews"] = rev_data.get("totalReviewCount", 0)
    audit_report["average_rating"] = rev_data.get("averageRating", 0)
    # 檢查是否有未回覆的
    unreplied = [r for r in rev_data.get("reviews", []) if "reviewReply" not in r]
    audit_report["unreplied_count_in_first_batch"] = len(unreplied)

with open(os.path.join(mgr_dir, "latest_live_audit.json"), "w", encoding="utf-8") as f:
    json.dump(audit_report, f, ensure_ascii=False, indent=2)

print("Live audit completed successfully!")
