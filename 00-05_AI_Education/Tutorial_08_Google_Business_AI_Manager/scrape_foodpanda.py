import urllib.request
import urllib.parse
import re
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

dest_dir = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\01_Taitung_Shokunin_Diner\reference_photos"
os.makedirs(dest_dir, exist_ok=True)

# Search Foodpanda via google or duckduckgo
query = "site:foodpanda.com.tw 職人食堂 台東"
search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"

try:
    req = urllib.request.Request(search_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    
    links = re.findall(r'href="([^"]*foodpanda\.com\.tw/restaurant/[^"]*)"', html)
    print("Found Foodpanda restaurant links:", len(links), links[:3])
    
    if links:
        target_link = links[0]
        # unquote uddg
        if 'uddg=' in target_link:
            target_link = urllib.parse.unquote(target_link.split('uddg=')[1].split('&')[0])
        print("Scraping Foodpanda page:", target_link)
        
        fp_req = urllib.request.Request(target_link, headers=headers)
        with urllib.request.urlopen(fp_req, timeout=10) as fp_resp:
            fp_html = fp_resp.read().decode('utf-8', errors='ignore')
            
        # Foodpanda images are on images.deliveryhero.io
        dh_imgs = re.findall(r'https://images\.deliveryhero\.io/[^\s"\'<>]+', fp_html)
        print("Found DeliveryHero image URLs:", len(dh_imgs))
        
        saved = 0
        for idx, img_url in enumerate(list(set(dh_imgs))[:15]):
            if "logo" in img_url.lower() or "hero" in img_url.lower() and saved > 0:
                continue
            try:
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                    img_data = img_resp.read()
                    if len(img_data) > 10000:
                        path = os.path.join(dest_dir, f"foodpanda_dish_{saved+1:02d}.jpg")
                        with open(path, "wb") as f:
                            f.write(img_data)
                        print(f"Saved real Foodpanda dish: {path} ({len(img_data)} bytes)")
                        saved += 1
                        if saved >= 5:
                            break
            except Exception as e:
                print("Failed to save img:", e)

except Exception as e:
    print("Error:", e)
