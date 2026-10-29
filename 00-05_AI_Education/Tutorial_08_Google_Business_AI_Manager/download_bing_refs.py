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

# Search Bing images or Duckduckgo
query = "台東 職人食堂 安慶街"
url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}&form=HDRSC2&first=1"
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    # Bing images has murl="https://..."
    murls = re.findall(r'murl&quot;:&quot;(https?://[^&]+)&quot;', html)
    print("Found bing image murls:", len(murls))
    
    saved = 0
    for idx, murl in enumerate(murls[:10]):
        try:
            print("Downloading:", murl)
            img_req = urllib.request.Request(murl, headers=headers)
            with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                data = img_resp.read()
                if len(data) > 30000: # larger than 30kb
                    target = os.path.join(dest_dir, f"bing_ref_{saved+1:02d}.jpg")
                    with open(target, "wb") as f:
                        f.write(data)
                    print(f"Saved: {target} ({len(data)} bytes)")
                    saved += 1
                    if saved >= 4:
                        break
        except Exception as e:
            print("Failed murl:", e)

except Exception as e:
    print("Bing search err:", e)
