import asyncio
import json
import urllib.request
import websockets

async def check():
    url = 'http://127.0.0.1:9222/json'
    with urllib.request.urlopen(url) as resp:
        tabs = json.loads(resp.read())

    for idx, t in enumerate(tabs):
        if t.get('type') != 'page' or 'claude.ai/chat' not in t.get('url', ''):
            continue
        print(f"=== Tab {idx}: {t.get('title')} ({t.get('url')}) ===")
        ws_url = t.get('webSocketDebuggerUrl')
        try:
            async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
                expr = '(() => { const b = document.body ? document.body.innerText : ""; return b.slice(-300); })()'
                msg = {'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}
                await ws.send(json.dumps(msg))
                res = json.loads(await ws.recv())
                print(res.get('result', {}).get('result', {}).get('value', '').replace('\n', ' '))
        except Exception as e:
            print("Error reading tab:", e)

if __name__ == '__main__':
    asyncio.run(check())
