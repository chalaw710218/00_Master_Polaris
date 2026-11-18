import asyncio
import json
import urllib.request
import websockets

async def inspect_claude():
    req = urllib.request.Request("http://127.0.0.1:9222/json")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
    claude_tab = next((t for t in tabs if "claude.ai" in t.get("url", "")), None)
    if not claude_tab or not claude_tab.get("ws"):
        print("No Claude tab")
        return

    async with websockets.connect(claude_tab["ws"]) as ws:
        # JS to inspect sidebar, projects, and recent chats
        js = """
        (() => {
            // Find projects
            const projects = [];
            // Look for links with /project/
            document.querySelectorAll('a[href*="/project/"]').forEach(a => {
                const title = a.innerText.trim();
                const href = a.getAttribute('href');
                if (title && !projects.some(p => p.href === href)) {
                    projects.push({ name: title.replace(/\\n+/g, ' '), href: href, type: 'project' });
                }
            });

            // Look for chats / recents
            const chats = [];
            document.querySelectorAll('a[href*="/chat/"]').forEach(a => {
                const title = a.innerText.trim();
                const href = a.getAttribute('href');
                if (title && !chats.some(c => c.href === href)) {
                    chats.push({ name: title.replace(/\\n+/g, ' '), href: href, type: 'chat' });
                }
            });

            // Look for any sidebar group headers or buttons
            const navItems = [];
            document.querySelectorAll('nav a, aside a, [data-testid*="project"] a').forEach(a => {
                const text = a.innerText.trim();
                if (text) navItems.push({ text: text.replace(/\\n+/g, ' '), href: a.getAttribute('href') });
            });

            return {
                current_title: document.title,
                current_url: window.location.href,
                projects: projects,
                chats_count: chats.length,
                chats_sample: chats.slice(0, 10),
                nav_sample: navItems.slice(0, 10)
            };
        })()
        """
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": js, "returnByValue": True}
        }
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        data = json.loads(res)
        val = data.get("result", {}).get("result", {}).get("value", {})
        print(json.dumps(val, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(inspect_claude())
