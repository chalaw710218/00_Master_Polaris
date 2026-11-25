import urllib.request, json
with urllib.request.urlopen("http://127.0.0.1:9222/json") as r:
    tabs = json.loads(r.read().decode())
for t in tabs:
    if t.get("type") == "page":
        print(f"Title: {t.get('title')} | URL: {t.get('url')}")
