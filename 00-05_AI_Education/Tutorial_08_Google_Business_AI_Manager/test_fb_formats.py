import urllib.request
import re

test_urls = [
    "https://www.facebook.com/profile.php?id=61561543646858",
    "https://www.facebook.com/p/職人食堂-61561543646858/",
    "https://www.facebook.com/p/%E8%81%B7%E4%BA%BA%E9%A3%9F%E5%A0%82-61561543646858"
]

for u in test_urls:
    try:
        req = urllib.request.Request(
            u, 
            headers={'User-Agent': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            og_title = re.search(r'<meta property="og:title" content="([^"]+)"', html)
            print(f"URL: {u[:45]}... Status: {response.status} Title: {og_title.group(1) if og_title else 'None'}")
    except Exception as e:
        print(f"URL: {u[:45]}... Error: {e}")
