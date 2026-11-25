import urllib.request
import re

url = "https://www.mol.gov.tw/1607/28162/28296/28340/28342/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html)
        print("Total links:", len(links))
        for l in links:
            if any(k in l.lower() for k in ["pdf", "media", "12431", "1080128698", "attach", "file"]):
                print("Candidate:", l)
except Exception as e:
    print("Error:", e)
