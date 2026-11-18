"""極星 ✕ Claude 雙腦調度儀表板 v2
- 最多 3 組通道：每組 = 1 個 Antigravity 對話 ⇄ 1 個 Claude 對話分頁
- 每組獨立開關，預設關閉；伺服器每次啟動都會把所有通道重設為關閉
- 通道設定寫入 bridge_pairs.json，供 claude_relay.py 讀取
啟動：python dual_brain_server_v2.py  → 開 http://127.0.0.1:8765
"""
import asyncio
import json
import os
import sqlite3
import threading
import time
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

import websockets

HERE = Path(__file__).resolve().parent
STATE_FILE = HERE / "bridge_pairs.json"
AG_DB = r"C:\Users\lenovo\.gemini\antigravity\conversation_summaries.db"
MAX_PAIRS = 3
LOCK = threading.Lock()


def empty_pair():
    return {"ag_id": "", "ag_name": "", "claude_href": "", "claude_name": "", "enabled": False}


def load_pairs():
    try:
        pairs = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        pairs = []
    pairs = (pairs + [empty_pair() for _ in range(MAX_PAIRS)])[:MAX_PAIRS]
    for p in pairs:
        p["enabled"] = False  # 安全預設：啟動時全部關閉
    return pairs


def save_pairs():
    STATE_FILE.write_text(json.dumps(STATE["pairs"], ensure_ascii=False, indent=2), encoding="utf-8")


STATE = {"pairs": load_pairs(), "ag_projects": [], "claude_items": [], "msg": "所有通道預設關閉"}
save_pairs()


def scan_antigravity():
    if not os.path.exists(AG_DB):
        return []
    out, seen = [], set()
    try:
        conn = sqlite3.connect(AG_DB)
        rows = conn.execute(
            "SELECT conversation_id, title, preview FROM conversation_summaries "
            "ORDER BY last_modified_time DESC"
        ).fetchall()
        conn.close()
        for cid, title, prev in rows:
            name = (title or prev or "").strip()
            if name and cid not in seen:
                seen.add(cid)
                out.append({"id": cid, "name": name[:60]})
    except Exception:
        pass
    return out


async def scan_claude():
    """只回傳 /chat/ 對話（專案頁送出會變成開新對話，不適合配對）。"""
    items = {}
    try:
        with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=1.0) as r:
            tabs = json.loads(r.read().decode())
    except Exception:
        return list(STATE["claude_items"])
    for t in tabs:
        url = t.get("url", "")
        if t.get("type") != "page" or "claude.ai/chat/" not in url:
            continue
        href = "/chat/" + url.split("claude.ai/chat/")[-1].split("?")[0]
        title = t.get("title", "").replace(" - Claude", "").strip() or "進行中對話"
        items[href] = {"href": href, "name": f"[已開分頁] {title}", "open": True}
        ws_url = t.get("webSocketDebuggerUrl")
        if not ws_url:
            continue
        js = """(() => Array.from(document.querySelectorAll('a[href*="/chat/"]'))
            .map(a => ({href: a.getAttribute('href'), name: a.innerText.trim().replace(/\\n+/g,' ')}))
            .filter(x => x.name && !x.href.includes('/new')))()"""
        try:
            async with websockets.connect(ws_url, ping_interval=None, max_size=None) as ws:
                await ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                                          "params": {"expression": js, "returnByValue": True}}))
                raw = await asyncio.wait_for(ws.recv(), timeout=1.5)
                for it in json.loads(raw).get("result", {}).get("result", {}).get("value", []) or []:
                    items.setdefault(it["href"], {"href": it["href"], "name": it["name"], "open": False})
        except Exception:
            pass
    return list(items.values())


def background_scanner():
    while True:
        try:
            ag = scan_antigravity()
            loop = asyncio.new_event_loop()
            cl = loop.run_until_complete(scan_claude())
            loop.close()
            with LOCK:
                STATE["ag_projects"] = ag
                STATE["claude_items"] = cl
        except Exception:
            pass
        time.sleep(3)


HTML_UI = """<!DOCTYPE html><html lang="zh-TW"><head><meta charset="UTF-8">
<title>極星 ✕ Claude 雙腦調度儀表板</title>
<style>
body{background:#090d16;color:#f8fafc;font-family:-apple-system,"Segoe UI","Noto Sans TC",sans-serif;padding:24px;display:flex;justify-content:center}
.panel{width:100%;max-width:960px;background:#131b2e;border:1px solid #223254;border-radius:16px;padding:24px}
h1{font-size:19px;margin:0 0 6px}.note{color:#94a3b8;font-size:13px;margin-bottom:18px}
.row{display:grid;grid-template-columns:28px 1fr 1fr 90px;gap:12px;align-items:center;background:#0d1527;border:1px solid #223254;border-radius:12px;padding:12px;margin-bottom:10px}
.row.on{border-color:#10b981;box-shadow:0 0 12px rgba(16,185,129,.25)}
select{width:100%;background:#19233c;color:#f8fafc;border:1px solid #223254;border-radius:8px;padding:9px}
.lbl{font-size:11px;color:#64748b;margin-bottom:4px}
button{border:0;border-radius:999px;padding:8px 0;font-weight:700;cursor:pointer;width:90px}
.off{background:#334155;color:#cbd5e1}.onb{background:#10b981;color:#fff}
#msg{margin-top:12px;font-size:13px;color:#94a3b8}
</style></head><body><div class="panel">
<h1>⚡ 極星 ✕ Claude 雙腦調度儀表板</h1>
<div class="note">每組通道獨立開關，預設關閉。只能配對 Claude 的「對話」（/chat/），且該對話必須在 Chrome 開著分頁。</div>
<div id="rows"></div><div id="msg"></div></div>
<script>
let S=null;
function opts(list,sel,key,label){return '<option value="">— 未選 —</option>'+list.map(x=>
 `<option value="${x[key]}" ${x[key]===sel?'selected':''}>${(x[label]||'').replace(/</g,'&lt;')}</option>`).join('');}
function render(){
 if(document.activeElement && document.activeElement.tagName==='SELECT') return;
 document.getElementById('rows').innerHTML=S.pairs.map((p,i)=>`
 <div class="row ${p.enabled?'on':''}"><b>${i+1}</b>
  <div><div class="lbl">ANTIGRAVITY 對話</div><select onchange="setPair(${i},{ag_id:this.value})">${opts(S.ag_projects,p.ag_id,'id','name')}</select></div>
  <div><div class="lbl">CLAUDE 對話</div><select onchange="setPair(${i},{claude_href:this.value})">${opts(S.claude_items,p.claude_href,'href','name')}</select></div>
  <button class="${p.enabled?'onb':'off'}" onclick="setPair(${i},{enabled:${!p.enabled}})">${p.enabled?'🟢 開啟':'⚪ 關閉'}</button>
 </div>`).join('');
 document.getElementById('msg').innerText=S.msg;}
async function load(){S=await (await fetch('/api/state')).json();render();}
async function setPair(i,patch){
 const r=await fetch('/api/pair',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({index:i,...patch})});
 S=await r.json(); document.activeElement.blur(); render();}
setInterval(load,3000);load();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _json(self, obj, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_UI.encode("utf-8"))
        elif self.path == "/api/state":
            with LOCK:
                self._json(STATE)
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path != "/api/pair":
            return self._json({"error": "not found"}, 404)
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)) or 0)
        data = json.loads(body.decode("utf-8")) if body else {}
        with LOCK:
            i = int(data.get("index", -1))
            if not 0 <= i < MAX_PAIRS:
                return self._json({"error": "bad index"}, 400)
            p = STATE["pairs"][i]
            if "ag_id" in data:
                p["ag_id"] = data["ag_id"]
                p["ag_name"] = next((x["name"] for x in STATE["ag_projects"] if x["id"] == data["ag_id"]), "")
                p["enabled"] = False  # 換配對就先斷開
            if "claude_href" in data:
                p["claude_href"] = data["claude_href"]
                p["claude_name"] = next((x["name"] for x in STATE["claude_items"] if x["href"] == data["claude_href"]), "")
                p["enabled"] = False
            if "enabled" in data:
                want = bool(data["enabled"])
                if want and not (p["ag_id"] and p["claude_href"]):
                    STATE["msg"] = f"通道 {i+1}：兩邊都選好才能開啟"
                elif want and any(j != i and q["enabled"] and q["claude_href"] == p["claude_href"]
                                  for j, q in enumerate(STATE["pairs"])):
                    STATE["msg"] = f"通道 {i+1}：這個 Claude 對話已被其他通道使用"
                else:
                    p["enabled"] = want
                    STATE["msg"] = f"通道 {i+1} {'已開啟' if want else '已關閉'}"
            save_pairs()
            return self._json(STATE)


if __name__ == "__main__":
    threading.Thread(target=background_scanner, daemon=True).start()
    print("儀表板：http://127.0.0.1:8765  （所有通道預設關閉）")
    HTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
