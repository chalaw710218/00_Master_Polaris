import json
import urllib.request
import urllib.error

def list_claude_tabs():
    url = "http://127.0.0.1:9222/json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'PolarisBridge'})
        with urllib.request.urlopen(req, timeout=2) as response:
            tabs = json.loads(response.read().decode())
    except urllib.error.URLError:
        return {"status": "error", "message": "Chrome 9222 端口尚未開啟。請確認已透過桌面捷徑啟動 Chrome。"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    claude_tabs = []
    other_tabs = []
    for tab in tabs:
        if tab.get("type") == "page":
            t_url = tab.get("url", "")
            t_title = tab.get("title", "")
            tab_info = {
                "id": tab.get("id"),
                "title": t_title,
                "url": t_url,
                "ws": tab.get("webSocketDebuggerUrl")
            }
            if "claude.ai" in t_url:
                claude_tabs.append(tab_info)
            else:
                other_tabs.append(tab_info)

    return {
        "status": "ok",
        "claude_tabs": claude_tabs,
        "total_pages": len(tabs),
        "other_sample": [t["title"] for t in other_tabs[:3]]
    }

if __name__ == "__main__":
    res = list_claude_tabs()
    print(json.dumps(res, ensure_ascii=False, indent=2))
