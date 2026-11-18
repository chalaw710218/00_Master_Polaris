import asyncio
import json
import urllib.request
import websockets

async def check():
    req = urllib.request.Request("http://127.0.0.1:9222/json")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
    claude_tab = next((t for t in tabs if t.get("type") == "page" and "claude.ai" in t.get("url", "")), None)
    if not claude_tab:
        return

    async with websockets.connect(claude_tab["ws"]) as ws:
        js = """
        (() => {
            // Check if there is a sidebar toggle button
            const btn = document.querySelector('button[aria-label*="側邊欄"]') || 
                        document.querySelector('button[aria-label*="sidebar"]') ||
                        document.querySelector('button[aria-label*="Menu"]') ||
                        document.querySelector('button[aria-label*="導覽"]') ||
                        document.querySelector('button svg path[d*="M3 18h18"]')?.closest('button');
            
            return {
                hasSidebarToggle: !!btn,
                btnLabel: btn ? btn.getAttribute('aria-label') : null,
                allButtons: Array.from(document.querySelectorAll('button')).map(b => b.getAttribute('aria-label') || b.innerText.trim()).filter(Boolean).slice(0, 15)
            };
        })()
        """
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        print(json.dumps(json.loads(res), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(check())
