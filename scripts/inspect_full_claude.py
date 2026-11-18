import asyncio
import json
import urllib.request
import websockets

async def inspect_tab(ws_url):
    async with websockets.connect(ws_url) as ws:
        # Get project name, breadcrumbs, sidebar items
        js = """
        (() => {
            // 1. Check breadcrumbs or top header
            const headerTexts = [];
            document.querySelectorAll('header *').forEach(el => {
                if (el.children.length === 0 && el.innerText.trim()) {
                    headerTexts.push(el.innerText.trim());
                }
            });

            // 2. Check project indicators
            let projectName = null;
            const projectLink = document.querySelector('a[href*="/project/"]');
            if (projectLink) {
                projectName = projectLink.innerText.trim();
            }

            // 3. Check conversation title in DOM
            let chatTitle = null;
            const titleEl = document.querySelector('[data-testid="chat-title"]') || document.querySelector('h1') || document.querySelector('header button');
            if (titleEl) {
                chatTitle = titleEl.innerText.trim();
            }

            // 4. Find all projects in sidebar
            const allProjects = [];
            document.querySelectorAll('nav a[href*="/project/"], aside a[href*="/project/"]').forEach(a => {
                const name = a.innerText.trim();
                const href = a.getAttribute('href');
                if (name && !allProjects.some(p => p.href === href)) {
                    allProjects.push({ name: name.replace(/\\n+/g, ' '), href: href });
                }
            });

            // 5. Recent chats in sidebar
            const recentChats = [];
            document.querySelectorAll('nav a[href*="/chat/"], aside a[href*="/chat/"]').forEach(a => {
                const name = a.innerText.trim();
                const href = a.getAttribute('href');
                if (name && !recentChats.some(c => c.href === href)) {
                    recentChats.push({ name: name.replace(/\\n+/g, ' '), href: href });
                }
            });

            return {
                url: window.location.href,
                title: document.title,
                projectName: projectName,
                chatTitle: chatTitle,
                headerTexts: headerTexts.slice(0, 5),
                allProjects: allProjects,
                recentChatsCount: recentChats.length,
                recentChats: recentChats.slice(0, 10)
            };
        })()
        """
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        res = await ws.recv()
        data = json.loads(res)
        return data.get("result", {}).get("result", {}).get("value", {})

async def main():
    req = urllib.request.Request("http://127.0.0.1:9222/json")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())

    for t in tabs:
        if t.get("type") == "page" and "claude.ai" in t.get("url", ""):
            print("====================================")
            print("Tab:", t.get("title"), "|", t.get("url"))
            ws_url = t.get("webSocketDebuggerUrl")
            if ws_url:
                info = await inspect_tab(ws_url)
                print(json.dumps(info, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
