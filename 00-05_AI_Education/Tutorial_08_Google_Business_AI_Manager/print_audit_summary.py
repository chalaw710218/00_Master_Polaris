import json
import os

mgr_dir = r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager"
with open(os.path.join(mgr_dir, "latest_live_audit.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== 1. Basic Info & Categories ===")
loc = data.get("location_info", {})
print("Title:", loc.get("title"))
print("Primary Category:", loc.get("categories", {}).get("primaryCategory", {}).get("displayName"))
print("Additional Categories:", [c.get("displayName") for c in loc.get("categories", {}).get("additionalCategories", [])])
print("Website URI:", loc.get("websiteUri"))
print("Description snippet:", loc.get("profile", {}).get("description", "")[:100], "...")

print("\n=== 2. Attributes Summary ===")
attrs = data.get("attributes", [])
for a in attrs:
    print(f"- {a.get('name')}: {a.get('values')}")

print("\n=== 3. Food Menus Summary ===")
menus = data.get("food_menus", {}).get("menus", [])
if menus:
    sections = menus[0].get("sections", [])
    print(f"Total Sections: {len(sections)}")
    for s in sections:
        sec_name = s.get("labels", [{}])[0].get("displayName")
        items = s.get("items", [])
        print(f"  * [{sec_name}]: {len(items)} items ({', '.join([it.get('labels', [{}])[0].get('displayName') for it in items[:3]])}...)")

print("\n=== 4. Media & Photos ===")
print("Total Media items in album:", data.get("media_count"))

print("\n=== 5. Local Posts ===")
print("Total Posts:", data.get("posts_count"))
lp = data.get("latest_post")
if lp:
    print("Latest Post State:", lp.get("state"))
    print("Latest Post CreateTime:", lp.get("createTime"))
    print("Latest Post Summary Snippet:", lp.get("summary", "")[:60], "...")

print("\n=== 6. Reviews Status ===")
print("Total Reviews:", data.get("total_reviews"))
print("Average Rating:", data.get("average_rating"))
print("Unreplied in latest batch:", data.get("unreplied_count_in_first_batch"))
