import asyncio
import json
import urllib.request
import websockets

async def test_cdp():
    # 1. Get Claude tab WS URL
    req = urllib.request.Request("http://127.0.0.1:9222/json")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())

    claude_tab = None
    for t in tabs:
        if "claude.ai" in t.get("url", ""):
            claude_tab = t
            break

    if not claude_tab:
        print("No Claude tab found")
        return

    print("Target Tab Title:", claude_tab["title"])
    print("Target Tab URL:", claude_tab["url"])
    ws_url = claude_tab.get("webSocketDebuggerUrl")
    if not ws_url:
        print("No webSocketDebuggerUrl")
        return

    async with websockets.connect(ws_url) as ws:
        # Check if textbox exists in DOM
        check_js = """
        (() => {
            const el = document.querySelector('div[contenteditable="true"]') || document.querySelector('fieldset div[contenteditable="true"]');
            return {
                found: !!el,
                tagName: el ? el.tagName : null,
                classes: el ? el.className : null,
                placeholder: el ? el.getAttribute('data-placeholder') : null,
                url: window.location.href,
                title: document.title
            };
        })()
        """
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": check_js,
                "returnByValue": True
            }
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        data = json.loads(res)
        print("DOM Check Result:", json.dumps(data.get("result", {}).get("result", {}).get("value", {}), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(test_cdp())
