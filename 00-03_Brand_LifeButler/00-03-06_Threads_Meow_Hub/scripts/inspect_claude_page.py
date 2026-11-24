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
        print('Tab not found')
        return
        
    print('Found tab:', target.get('title'), target.get('url'))
    ws_url = target.get('webSocketDebuggerUrl')
    async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
        expr = '''(() => {
            const body = document.body ? document.body.innerText : 'NO_BODY';
            const count = document.querySelectorAll('[data-is-streaming]').length;
            const input = !!document.querySelector('div[contenteditable="true"]');
            return { length: body.length, count: count, hasInput: input, tail: body.slice(-800) };
        })()'''
        msg = {'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}
        await ws.send(json.dumps(msg))
        res = json.loads(await ws.recv())
        val = res.get('result', {}).get('result', {}).get('value', {})
        print('Page info:')
        print(f"Total length: {val.get('length')}, stream blocks: {val.get('count')}, hasInput: {val.get('hasInput')}")
        print("--- TAIL ---")
        print(val.get('tail'))

if __name__ == '__main__':
    asyncio.run(check())
