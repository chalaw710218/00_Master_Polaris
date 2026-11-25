import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://law.moj.gov.tw/LawClass/LawSingle.aspx?pcode=L0060009&flno=25"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
    html = r.read().decode("utf-8", errors="ignore")
    idx = html.find("第 25 條")
    if idx != -1:
        print(html[idx:idx+1500])
