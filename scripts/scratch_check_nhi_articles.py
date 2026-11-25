import urllib.request, re

url = "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=L0060009"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")
        matches = re.findall(r'href="LawSingle\.aspx\?pcode=L0060009&flno=(\d+)"[^>]*>第\s*(\d+)\s*條</a>.*?<div class="law-article">(.*?)</div>', html, re.DOTALL)
        for flno, num, text in matches:
            clean = re.sub(r'<[^>]+>', ' ', text)
            if any(k in clean for k in ['慢性病', '處方箋', '調劑', '代領']):
                print(f"flno={flno} (第{num}條): {clean.strip()[:120]}")
except Exception as e:
    print("Error:", e)
