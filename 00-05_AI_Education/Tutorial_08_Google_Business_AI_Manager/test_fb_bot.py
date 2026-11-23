import urllib.request
import re

url = "https://www.facebook.com/p/%E8%81%B7%E4%BA%BA%E9%A3%9F%E5%A0%82-61561543646858/"
req = urllib.request.Request(
    url, 
    headers={
        'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'
    }
)

try:
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8')
        print("Length:", len(html))
        # 尋找 og:title, og:description
        og_title = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        og_desc = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        if og_title:
            print("OG Title:", og_title.group(1))
        if og_desc:
            print("OG Desc:", og_desc.group(1))
            
        # 尋找頁面中的關鍵文字
        for m in re.finditer(r'"text":"([^"]+)"', html):
            t = m.group(1)
            if any(k in t for k in ["台東", "臺東", "安慶", "湯包", "麵", "丼"]):
                print("Matched text:", t)
except Exception as e:
    print("Error:", e)
