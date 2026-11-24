import asyncio
import json
import urllib.request
import websockets

async def check():
    url = 'http://127.0.0.1:9222/json'
    with urllib.request.urlopen(url) as resp:
        tabs = json.loads(resp.read())

    target = next((t for t in tabs if 'a213ac7e' in t.get('url', '')), None)
    if not target:
        print('Tab not found')
        return

    ws_url = target.get('webSocketDebuggerUrl')
    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        expr = '''(() => {
            const msgs = document.querySelectorAll('[data-is-streaming]');
            if (!msgs.length) return "NO_STREAM_MSGS";
            return msgs[msgs.length - 1].innerText;
        })()'''
        msg = {'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}
        await ws.send(json.dumps(msg))
        res = json.loads(await ws.recv())
        val = res.get('result', {}).get('result', {}).get('value', '')
        print('=== Claude Latest Full Response ===')
        print(val)

if __name__ == '__main__':
    asyncio.run(check())
