import requests
from bs4 import BeautifulSoup
import re

url = "https://www.facebook.com/p/%E8%81%B7%E4%BA%BA%E9%A3%9F%E5%A0%82-61561543646858/?locale=zh_TW"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

try:
    res = requests.get(url, headers=headers, timeout=10)
    print("Status:", res.status_code)
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.find("title")
    print("Page Title:", title.text if title else "None")
    
    meta_desc = soup.find("meta", {"name": "description"})
    if meta_desc:
        print("Meta Desc:", meta_desc.get("content"))
        
    og_title = soup.find("meta", {"property": "og:title"})
    og_desc = soup.find("meta", {"property": "og:description"})
    print("OG Title:", og_title.get("content") if og_title else "None")
    print("OG Desc:", og_desc.get("content") if og_desc else "None")
    
    # 搜尋文字中是否有 安慶街、台東、089、342900 等特徵
    text = res.text
    keywords = ["安慶", "台東", "臺東", "342900", "512505", "加依軒", "湯包"]
    matches = {k: k in text for k in keywords}
    print("Keyword matches:", matches)
except Exception as e:
    print("Error:", e)
