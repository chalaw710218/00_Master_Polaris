import asyncio
import sys
import json
from pathlib import Path

HERE = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\scripts")
sys.path.insert(0, str(HERE))

import claude_relay
import websockets

async def check():
    pair_key = "c06c2e4f-8afc-4b48-8bd9-11ddbcdeb1e5"
    i, p = claude_relay.find_pair(pair_key)
    tab = claude_relay.find_tab(p["claude_href"])
    ws_url = tab["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        js = """(() => {
            const divs = document.querySelectorAll('[data-test-render-count], .standard-markdown, [class*="font-claude"], [data-message-author-role="assistant"]');
            const res = [];
            divs.forEach(d => res.push(d.innerText.slice(0, 100)));
            return {
                url: window.location.href,
                count: divs.length,
                last: divs.length > 0 ? divs[divs.length - 1].innerText : document.body.innerText.slice(-1500)
            };
        })()"""
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        data = json.loads(res)
        val = data.get("result", {}).get("result", {}).get("value", {})
        print("URL:", val.get("url"))
        print("Count:", val.get("count"))
        print("LAST TEXT:")
        print(val.get("last"))

if __name__ == "__main__":
    asyncio.run(check())
