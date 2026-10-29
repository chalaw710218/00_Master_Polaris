import urllib.request
import urllib.parse
import re
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

dest_dir = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\01_Taitung_Shokunin_Diner\reference_photos"

# Try DuckDuckGo Image Search API directly
query = "職人食堂 安慶街60號 台東"
url = f"https://duckduckgo.com/i.js?l=wt-wt&o=json&q={urllib.parse.quote(query)}"
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        results = data.get('results', [])
        print("DDG Results count:", len(results))
        for idx, item in enumerate(results[:5]):
            img_url = item.get('image')
            title = item.get('title')
            print(f"[{idx+1}] {title} -> {img_url}")
            try:
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=8) as img_resp:
                    img_data = img_resp.read()
                    if len(img_data) > 15000:
                        path = os.path.join(dest_dir, f"ddg_real_{idx+1:02d}.jpg")
                        with open(path, "wb") as f:
                            f.write(img_data)
                        print(f"Saved: {path}")
            except Exception as e:
                print("Failed to download image:", e)
except Exception as e:
    print("DDG search failed:", e)
