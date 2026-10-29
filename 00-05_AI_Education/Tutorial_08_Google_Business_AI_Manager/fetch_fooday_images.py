import urllib.request
import re
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

dest_dir = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\01_Taitung_Shokunin_Diner\reference_photos"
os.makedirs(dest_dir, exist_ok=True)

url = "https://fooday.app/zh-TW/spots/3o8XC5tGBpWyaav7fRPJT9"
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    # Fooday image CDN is typically i.fooday.app or similar
    img_urls = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp)', html)
    fooday_imgs = re.findall(r'https?://i\.fooday\.app/[^\s"\'<>]+', html)
    
    all_imgs = list(set(img_urls + fooday_imgs))
    print(f"Total image links found: {len(all_imgs)}")
    for i in all_imgs:
        print("IMG:", i)
        
    # Download the first 5 images as references
    count = 0
    for img_url in all_imgs:
        if "avatar" in img_url.lower() or "icon" in img_url.lower() or "logo" in img_url.lower():
            continue
        try:
            ext = ".jpg"
            if ".png" in img_url: ext = ".png"
            if ".webp" in img_url: ext = ".webp"
            target_path = os.path.join(dest_dir, f"ref_{count+1:02d}{ext}")
            img_req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                with open(target_path, "wb") as f:
                    f.write(img_resp.read())
            print(f"Saved: {target_path} from {img_url}")
            count += 1
            if count >= 6:
                break
        except Exception as err:
            print("Download err:", err)

except Exception as e:
    print("Fetch error:", e)
