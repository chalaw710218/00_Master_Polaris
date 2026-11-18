import asyncio
import json
import os
import sqlite3
import urllib.request
import websockets
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

WORKSPACE_ROOT = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris"

GLOBAL_STATE = {
    "is_connected": True,
    "selected_ag_project": "00_Master_Polaris",
    "selected_claude_item": None,
    "last_sync_message": "已成功對齊 Antigravity 專案與 Claude 項目清單",
    "ag_projects": [],
    "claude_items": []
}

def scan_antigravity_projects():
    db_path = r"C:\Users\lenovo\.gemini\antigravity\conversation_summaries.db"
    if not os.path.exists(db_path):
        return [{"id": "current", "name": "💬 最高指揮 (當前主對話視窗)"}]

    chats = []
    seen = set()
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            SELECT conversation_id, title, preview, last_modified_time 
            FROM conversation_summaries 
            ORDER BY last_modified_time DESC
        """)
        for cid, title, prev, lmt in c.fetchall():
            name = (title or prev or "").strip()
            if not name or name in seen:
                continue
            if len(name) > 1 and not (len(name) == 36 and '-' in name):
                seen.add(name)
                is_cur = (cid == "44896662-b7c0-4aaa-9282-f12cda292979")
                prefix = "⭐ [當前] " if is_cur else "💬 "
                chats.append({
                    "id": cid,
                    "name": f"{prefix}{name}"
                })
        conn.close()
    except Exception:
        pass

    return chats if chats else [{"id": "current", "name": "💬 最高指揮 (當前主對話視窗)"}]

CLAUDE_ITEMS_CACHE = {}

async def fetch_claude_items_async():
    try:
        req = urllib.request.Request("http://127.0.0.1:9222/json")
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            tabs = json.loads(resp.read().decode())
    except Exception:
        return list(CLAUDE_ITEMS_CACHE.values())

    claude_pages = [t for t in tabs if t.get("type") == "page" and "claude.ai" in t.get("url", "")]
    if not claude_pages:
        return list(CLAUDE_ITEMS_CACHE.values())

    # 1. Register all active open tabs
    for tab in claude_pages:
        t_url = tab.get("url", "")
        t_title = tab.get("title", "").replace(" - Claude", "").strip() or "進行中對話"
        clean_href = "/" + t_url.split("claude.ai/")[-1] if "claude.ai/" in t_url else t_url
        if clean_href not in CLAUDE_ITEMS_CACHE:
            CLAUDE_ITEMS_CACHE[clean_href] = {
                "name": f"💬 [分頁] {t_title}",
                "href": clean_href,
                "type": "tab"
            }

    # 2. Iterate each open Claude tab to harvest sidebar Projects & Chats
    for tab in claude_pages:
        ws_url = tab.get("webSocketDebuggerUrl")
        if not ws_url:
            continue

        js = """
        (() => {
            const list = [];
            document.querySelectorAll('a[href*="/project/"], a[href*="/chat/"]').forEach(a => {
                const text = a.innerText.trim();
                const href = a.getAttribute('href');
                if (text && href && !href.includes('/new')) {
                    const isProj = href.includes('/project/');
                    list.push({
                        name: (isProj ? "📂 [專案] " : "💬 [項目] ") + text.replace(/\\n+/g, ' '),
                        href: href,
                        type: isProj ? "project" : "chat"
                    });
                }
            });
            return list;
        })()
        """
        try:
            async with websockets.connect(ws_url, ping_interval=None) as ws:
                msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
                await ws.send(json.dumps(msg))
                raw = await asyncio.wait_for(ws.recv(), timeout=1.5)
                items = json.loads(raw).get("result", {}).get("result", {}).get("value", [])
                for it in items:
                    CLAUDE_ITEMS_CACHE[it["href"]] = it
        except Exception:
            pass

    return list(CLAUDE_ITEMS_CACHE.values())

def background_scanner():
    while True:
        try:
            GLOBAL_STATE["ag_projects"] = scan_antigravity_projects()
            loop = asyncio.new_event_loop()
            items = loop.run_until_complete(fetch_claude_items_async())
            loop.close()
            if items:
                GLOBAL_STATE["claude_items"] = items
                if not GLOBAL_STATE["selected_claude_item"]:
                    GLOBAL_STATE["selected_claude_item"] = items[0]["href"]
        except Exception as e:
            pass
        time.sleep(3)

HTML_UI = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>極星 ✕ Claude 雙腦調度儀表板</title>
  <style>
    :root {
      --bg: #090d16;
      --card-bg: #131b2e;
      --border: #223254;
      --accent-blue: #38bdf8;
      --accent-orange: #f59e0b;
      --success: #10b981;
      --text: #f8fafc;
      --muted: #64748b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans TC", sans-serif; }
    body {
      background-color: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .panel {
      width: 100%;
      max-width: 880px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 32px;
      box-shadow: 0 16px 48px rgba(0,0,0,0.6);
      display: flex;
      flex-direction: column;
      gap: 24px;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255,255,255,0.06);
      padding-bottom: 16px;
    }
    .title {
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }
    .status-pill {
      font-size: 13px;
      padding: 6px 14px;
      border-radius: 999px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .status-on { background: rgba(16, 185, 129, 0.15); color: var(--success); border: 1px solid var(--success); }
    .status-off { background: rgba(100, 116, 139, 0.15); color: var(--muted); border: 1px solid var(--muted); }

    .router-row {
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      gap: 20px;
    }
    .node-box {
      background: #0d1527;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .node-label {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
    }
    .select-dropdown {
      width: 100%;
      background: #19233c;
      color: var(--text);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 14px;
      font-weight: 500;
      outline: none;
      cursor: pointer;
      transition: all 0.2s;
    }
    .select-dropdown:focus { border-color: var(--accent-blue); }
    .claude-box .select-dropdown:focus { border-color: var(--accent-orange); }

    .bridge-switch-col {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
    }
    .switch {
      position: relative;
      display: inline-block;
      width: 58px;
      height: 32px;
    }
    .switch input { opacity: 0; width: 0; height: 0; }
    .slider {
      position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
      background-color: #334155; transition: .3s; border-radius: 32px;
    }
    .slider:before {
      position: absolute; content: ""; height: 24px; width: 24px; left: 4px; bottom: 4px;
      background-color: white; transition: .3s; border-radius: 50%;
    }
    input:checked + .slider { background-color: var(--success); box-shadow: 0 0 16px rgba(16, 185, 129, 0.4); }
    input:checked + .slider:before { transform: translateX(26px); }

    .footer-note {
      text-align: center;
      font-size: 13px;
      color: #94a3b8;
      background: rgba(0,0,0,0.25);
      padding: 12px;
      border-radius: 10px;
      border: 1px solid rgba(255,255,255,0.04);
    }
  </style>
</head>
<body>

  <div class="panel">
    <div class="header">
      <div class="title">
        <span>⚡ 極星 ✕ Claude 雙腦調度儀表板</span>
      </div>
      <div id="statusBadge" class="status-pill status-on">🟢 直通對話已連線</div>
    </div>

    <div class="router-row">
      <!-- Left: Antigravity Project Dropdown -->
      <div class="node-box">
        <div class="node-label" style="color: var(--accent-blue);">1. ANTIGRAVITY 專案名稱 (PROJECTS)</div>
        <select class="select-dropdown" id="agSelect" onchange="updateAG()">
          <option>載入專案中...</option>
        </select>
      </div>

      <!-- Center: Switch -->
      <div class="bridge-switch-col">
        <div style="font-size: 11px; font-weight: 700; color: var(--muted); text-transform: uppercase;">串接開關</div>
        <label class="switch">
          <input type="checkbox" id="bridgeToggle" checked onchange="toggleBridge()">
          <span class="slider"></span>
        </label>
        <div style="font-size: 18px; color: var(--muted);">⇄</div>
      </div>

      <!-- Right: Claude Project/Chat Dropdown -->
      <div class="node-box claude-box">
        <div class="node-label" style="color: var(--accent-orange);">2. CLAUDE 項目名稱 (PROJECTS / CHATS)</div>
        <select class="select-dropdown" id="claudeSelect" onchange="updateClaude()">
          <option>深入掃描 Claude 項目中...</option>
        </select>
      </div>
    </div>

    <div class="footer-note" id="liveMsg">
      ✨ 雙向直通中：選定對接之專案與項目後，極星與 Claude 實體分頁直接進行對話，完全免手動發射。
    </div>
  </div>

  <script>
    async function loadData() {
      try {
        const res = await fetch('/api/state');
        const data = await res.json();

        // 1. Render Antigravity Projects
        const agSelect = document.getElementById('agSelect');
        const prevAG = agSelect.value;
        agSelect.innerHTML = '';
        data.ag_projects.forEach(p => {
          const el = document.createElement('option');
          el.value = p.id;
          el.innerText = p.name;
          if (p.id === data.selected_ag_project) el.selected = true;
          agSelect.appendChild(el);
        });

        // 2. Render Claude Full Items
        const claudeSelect = document.getElementById('claudeSelect');
        claudeSelect.innerHTML = '';
        if (!data.claude_items || data.claude_items.length === 0) {
          const el = document.createElement('option');
          el.innerText = '⚠️ 未偵測到 Claude 項目 (請確認已開啟 Claude 分頁)';
          claudeSelect.appendChild(el);
        } else {
          data.claude_items.forEach(item => {
            const el = document.createElement('option');
            el.value = item.href;
            el.innerText = item.name;
            if (item.href === data.selected_claude_item) el.selected = true;
            claudeSelect.appendChild(el);
          });
        }

        // 3. Render Switch
        const toggle = document.getElementById('bridgeToggle');
        toggle.checked = data.is_connected;
        const badge = document.getElementById('statusBadge');
        if (data.is_connected) {
          badge.className = 'status-pill status-on';
          badge.innerHTML = '🟢 直通對話已連線';
        } else {
          badge.className = 'status-pill status-off';
          badge.innerHTML = '⚪ 通道已斷開 (靜默)';
        }

        // 4. Render Message
        document.getElementById('liveMsg').innerText = data.last_sync_message;
      } catch (e) {
        console.error(e);
      }
    }

    async function toggleBridge() {
      const val = document.getElementById('bridgeToggle').checked;
      await fetch('/api/set_switch', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ is_connected: val })
      });
      loadData();
    }

    async function updateAG() {
      const val = document.getElementById('agSelect').value;
      await fetch('/api/set_ag', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ selected_antigravity_project: val })
      });
      loadData();
    }

    async function updateClaude() {
      const val = document.getElementById('claudeSelect').value;
      await fetch('/api/set_claude', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ selected_claude_item: val })
      });
      loadData();
    }

    setInterval(loadData, 3000);
    loadData();
  </script>
</body>
</html>
"""

class FastProjectBridgeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_UI.encode("utf-8"))
        elif self.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(GLOBAL_STATE, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        data = json.loads(body.decode('utf-8')) if body else {}

        if self.path == "/api/set_switch":
            GLOBAL_STATE["is_connected"] = data.get("is_connected", True)
            txt = "串接開啟" if GLOBAL_STATE["is_connected"] else "串接關閉"
            GLOBAL_STATE["last_sync_message"] = f"開關狀態：{txt}"
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        elif self.path == "/api/set_ag":
            GLOBAL_STATE["selected_ag_project"] = data.get("selected_antigravity_project")
            GLOBAL_STATE["last_sync_message"] = f"Antigravity 專案已對齊：{GLOBAL_STATE['selected_ag_project']}"
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        elif self.path == "/api/set_claude":
            GLOBAL_STATE["selected_claude_item"] = data.get("selected_claude_item")
            GLOBAL_STATE["last_sync_message"] = f"Claude 項目已對齊：{GLOBAL_STATE['selected_claude_item']}"
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=8765):
    # Start background scanner thread
    t = threading.Thread(target=background_scanner, daemon=True)
    t.start()
    server = HTTPServer(('127.0.0.1', port), FastProjectBridgeHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_server()
