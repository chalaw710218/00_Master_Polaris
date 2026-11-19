"""Antigravity → Claude 傳話器
閣員在 Antigravity 裡執行：
    python claude_relay.py --ag <自己的對話ID或標題關鍵字> --name 雪 "要問 Claude 的話"
流程：查 bridge_pairs.json 找到對應通道 → 通道必須是開啟 → 把訊息打進對應的 Claude 分頁並送出
     → 等 Claude 回完 → 把回覆印到 stdout（閣員直接讀指令輸出）
結束碼：0 成功｜2 通道關閉或沒配對｜3 找不到分頁／輸入框｜4 等回覆逾時｜5 該分頁正被其他閣員使用
需求：Chrome 以 --remote-debugging-port=9222 啟動（用你的桌面捷徑），pip install websockets
"""
import argparse
import asyncio
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

import websockets

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
STATE_FILE = HERE / "bridge_pairs.json"

JS_FOCUS = """(() => { const el = document.querySelector('div[contenteditable="true"]');
  if (!el) return false; el.focus(); return true; })()"""
JS_COUNT = "document.querySelectorAll('[data-is-streaming]').length"
JS_CLICK_SEND = """(() => { const b = document.querySelector(
  'button[aria-label*="Send"],button[aria-label*="傳送"],button[aria-label*="送出"]');
  if (!b || b.disabled) return false; b.click(); return true; })()"""
JS_STATUS = """(() => { const a = document.querySelectorAll('[data-is-streaming]');
  const stop = !!document.querySelector('button[aria-label*="Stop"],button[aria-label*="停止"]');
  if (!a.length) return {n:0, streaming:true, stop, text:''};
  const l = a[a.length-1];
  return {n:a.length, streaming:l.getAttribute('data-is-streaming')==='true', stop, text:l.innerText}; })()"""


def fail(code, msg):
    print(f"[relay] {msg}", file=sys.stderr)
    sys.exit(code)


def find_pair(key):
    try:
        pairs = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        fail(2, "找不到 bridge_pairs.json，請先啟動 dual_brain_server_v2.py")
    for i, p in enumerate(pairs):
        if p.get("ag_id") and (p["ag_id"] == key or key in p.get("ag_name", "")):
            return i, p
    fail(2, f"沒有任何通道配對到「{key}」")


def find_tab(href):
    try:
        with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=2) as r:
            tabs = json.loads(r.read().decode())
    except Exception:
        fail(3, "Chrome 9222 埠沒開，請用桌面捷徑啟動 Chrome")
    for t in tabs:
        if t.get("type") == "page" and href in t.get("url", ""):
            return t
    fail(3, f"Claude 對話 {href} 沒有開著的分頁，請先在 Chrome 打開它")


class TabLock:
    """同一個分頁一次只讓一個閣員用。超過 20 分鐘的舊鎖視為殘留自動清掉。"""

    def __init__(self, tab_id):
        self.path = HERE / f".relay_lock_{tab_id}"

    def __enter__(self):
        if self.path.exists() and time.time() - self.path.stat().st_mtime > 1200:
            self.path.unlink(missing_ok=True)
        try:
            os.close(os.open(self.path, os.O_CREAT | os.O_EXCL))
        except FileExistsError:
            fail(5, "這個 Claude 分頁正在被其他閣員使用，稍後再試")
        return self

    def __exit__(self, *a):
        self.path.unlink(missing_ok=True)


class CDP:
    def __init__(self, ws):
        self.ws, self.i = ws, 0

    async def call(self, method, params=None):
        self.i += 1
        mid = self.i
        await self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(await self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})

    async def js(self, expr):
        r = await self.call("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return r.get("result", {}).get("value")


async def relay(ws_url, text, timeout):
    async with websockets.connect(ws_url, ping_interval=None, max_size=None) as ws:
        cdp = CDP(ws)
        # 讓背景分頁也以為自己在前景，避免被節流
        try:
            await cdp.call("Emulation.setFocusEmulationEnabled", {"enabled": True})
        except Exception:
            pass
        before_text = await cdp.js("""(() => {
            const a = document.querySelectorAll('[data-is-streaming]');
            return a.length ? a[a.length-1].innerText : '';
        })()""") or ""
        if not await cdp.js(JS_FOCUS):
            fail(3, "找不到 Claude 輸入框（頁面可能還沒載入）")
        await cdp.call("Input.insertText", {"text": text})
        await asyncio.sleep(0.8)
        if not await cdp.js(JS_CLICK_SEND):
            for t in ("keyDown", "keyUp"):
                await cdp.call("Input.dispatchKeyEvent", {"type": t, "key": "Enter", "code": "Enter",
                                                          "windowsVirtualKeyCode": 13})
        deadline = time.time() + timeout
        last_text, stable_since = None, None
        while time.time() < deadline:
            await asyncio.sleep(1.5)
            s = await cdp.js(JS_STATUS) or {}
            curr_text = s.get("text", "")
            if curr_text == before_text or s.get("streaming") or s.get("stop"):
                last_text, stable_since = None, None
                continue
            if curr_text == last_text:
                if time.time() - stable_since >= 5:  # 內容 5 秒沒變才算回完
                    return curr_text
            else:
                last_text, stable_since = curr_text, time.time()
        fail(4, f"等了 {timeout} 秒 Claude 還沒回完")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ag", required=True, help="自己的 Antigravity 對話 ID 或標題關鍵字")
    ap.add_argument("--name", default="閣員", help="署名，例如 雪")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("message")
    a = ap.parse_args()

    i, p = find_pair(a.ag)
    if not p.get("enabled"):
        fail(2, f"通道 {i+1} 目前關閉，品碩開啟前不能傳話")
    tab = find_tab(p["claude_href"])
    with TabLock(tab["id"]):
        reply = asyncio.run(relay(tab["webSocketDebuggerUrl"], f"【{a.name}】{a.message}", a.timeout))
    print(reply)


if __name__ == "__main__":
    main()
