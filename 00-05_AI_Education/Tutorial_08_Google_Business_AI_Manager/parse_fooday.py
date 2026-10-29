import urllib.request
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}

url = "https://fooday.app/zh-TW/spots/3o8XC5tGBpWyaav7fRPJT9"
req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        
    # Extract NEXT_DATA JSON
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">({.*?})</script>', content, re.DOTALL)
    if m:
        data = json.loads(m.group(1))
        print("Found __NEXT_DATA__!")
        # Find all image URLs in the json
        json_str = json.dumps(data)
        imgs = re.findall(r'https://i\.fooday\.app/[a-zA-Z0-9_-]+', json_str)
        print("Images in JSON:", list(set(imgs)))
    else:
        imgs = re.findall(r'https://i\.fooday\.app/[a-zA-Z0-9_-]+', content)
        print("Images in HTML:", list(set(imgs)))

except Exception as e:
    print("Error:", e)
