import json
import os

profile_path = r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\01_Taitung_Shokunin_Diner\data\store_profile.json"

profile_data = {
    "merchant_id": "01_Taitung_Shokunin_Diner",
    "name": "職人食堂",
    "gcp_account_id": "112884798662846885062",
    "gcp_location_id": "1774177451467087781",
    "address": "台東縣台東市安慶街60號",
    "phone": "089-342900",
    "phone_mobile": "0933-512-505",
    "website_url": "https://chalaw710218.github.io/shokunin-taitung/",
    "google_maps_url": "https://maps.google.com/maps?cid=2490326888156108049",
    "place_id": "ChIJpXV-WBu5bzQRERUmRxxrjyI",
    "status": "OPERATIONAL",
    "categories": {
        "primary": "categories/gcid:mandarin_restaurant (中式餐廳)",
        "additional": [
            "categories/gcid:noodle_shop (麵店)",
            "categories/gcid:dim_sum_restaurant (茶餐廳/點心)"
        ]
    },
    "metrics_baseline_20261123": {
        "total_reviews": 208,
        "replied_reviews": 208,
        "reply_rate": "100%",
        "rating_average": 4.5
    },
    "uploaded_macro_photos": [
        {
            "name": "手工爆汁小籠湯包",
            "media_id": "CIABIhCqAb61_abLY3_aKg7KhDR4",
            "category": "FOOD_AND_DRINK"
        },
        {
            "name": "柴魚昆布讚岐烏龍麵",
            "media_id": "CIABIhC0OjClpheKeooSw1Z6OShY",
            "category": "FOOD_AND_DRINK"
        },
        {
            "name": "炙燒牛五花燒肉丼飯",
            "media_id": "CIABIhDINmjaApqeb6Rl_VwvU0ja",
            "category": "FOOD_AND_DRINK"
        }
    ],
    "structured_menu_status": "PUBLISHED_VIA_API_20261123",
    "automation_cron": {
        "scheduled_task_name": "Polaris_GBP_Midnight_Autopilot",
        "schedule": "Daily at 00:00",
        "action": "Fetch new reviews, auto reply, sync metrics"
    }
}

with open(profile_path, "w", encoding="utf-8") as f:
    json.dump(profile_data, f, ensure_ascii=False, indent=2)

print("Updated store_profile.json successfully!")
