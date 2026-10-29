import urllib.request
import re
import json
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1. Search for Fooday image URLs directly
query = "site:fooday.app 職人食堂 台東"
search_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"

dest_dir = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\Tutorial_08_Google_Business_AI_Manager\clients\01_Taitung_Shokunin_Diner\reference_photos"
os.makedirs(dest_dir, exist_ok=True)

try:
    req = urllib.request.Request(search_url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        # Find fooday restaurant links
        fooday_links = re.findall(r'href="([^"]*fooday\.app[^"]*)"', html)
        print("Found Fooday links:", fooday_links[:5])
except Exception as e:
    print("Search error:", e)
