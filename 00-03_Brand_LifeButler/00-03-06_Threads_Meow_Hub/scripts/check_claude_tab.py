import asyncio
import json
import urllib.request
import websockets

async def check():
    url = 'http://127.0.0.1:9222/json'
    try:
        with urllib.request.urlopen(url) as resp:
            tabs = json.loads(resp.read())
    except Exception as e:
        print('Error connecting to port 9222:', e)
        return

    target = next((t for t in tabs if 'a213ac7e' in t.get('url', '')), None)
    if not target:
        print('Tab not found among open tabs:')
        for t in tabs:
            print('-', t.get('title'), t.get('url'))
        return
        
    print('Found tab:', target.get('title'))
    ws_url = target.get('webSocketDebuggerUrl')
    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        expr = '''(() => {
            const msgs = Array.from(document.querySelectorAll("[data-message-author-role]"));
            return msgs.map(m => ({role: m.getAttribute("data-message-author-role"), text: m.innerText.slice(-200)}));
        })()'''
        msg = {'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}
        await ws.send(json.dumps(msg))
        res = json.loads(await ws.recv())
        val = res.get('result', {}).get('result', {}).get('value', [])
        print(f'Total messages: {len(val)}')
        for m in val[-4:]:
            print(f"[{m['role']}]: {m['text'].replace(chr(10), ' ')}")

if __name__ == '__main__':
    asyncio.run(check())
