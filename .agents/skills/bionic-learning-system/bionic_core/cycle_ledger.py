"""輪次帳本與十輪強制停機 (Cycle Ledger · Master v6.0 第四章/第十一章 ⑦)

輪次只能由本程式遞增，模型不得自行宣稱「第 N 輪」。
滿 10 輪 ➔ 程式建立停機鎖；在提交衝突審計報告（檔案須存在）前，enforce.gate 一律 Exit Code 1。

用法：
  python cycle_ledger.py tick --office kage --summary "本輪做了什麼" --evidence path_or_url
  python cycle_ledger.py status --office kage
  python cycle_ledger.py audit-done --office kage --report path\\to\\audit_report.md
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

VAULT_DIR = Path(__file__).resolve().parent / "vaults"
AUDIT_EVERY = 10


def _ledger(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{office}_cycles.jsonl"


def _lock(office: str) -> Path:
    return VAULT_DIR / f"{office}.AUDIT_REQUIRED.lock"


def read(office: str) -> list[dict]:
    p = _ledger(office)
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def cycle_count(office: str) -> int:
    return sum(1 for e in read(office) if e.get("type") == "tick")


def is_locked(office: str) -> bool:
    return _lock(office).exists()


def tick(office: str, summary: str, evidence: str) -> int:
    if is_locked(office):
        raise RuntimeError("已停機：滿 10 輪須先提交衝突審計報告（audit-done）")
    if not evidence.strip():
        raise ValueError("每一輪必須附物理憑證（檔案路徑或 URL），不得只靠宣稱")
    n = cycle_count(office) + 1
    ev = {"ts": datetime.now().isoformat(timespec="seconds"), "type": "tick", "cycle": n,
          "summary": summary, "evidence": evidence}
    with open(_ledger(office), "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    if n % AUDIT_EVERY == 0:
        _lock(office).write_text(f"cycle {n} reached at {ev['ts']}\n", encoding="utf-8")
    return n


def audit_done(office: str, report: str) -> None:
    if not Path(report).exists():
        raise FileNotFoundError(f"審計報告不存在：{report}")
    ev = {"ts": datetime.now().isoformat(timespec="seconds"), "type": "audit_done", "report": report}
    with open(_ledger(office), "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    if _lock(office).exists():
        _lock(office).unlink()


def main() -> None:
    ap = argparse.ArgumentParser(description="輪次帳本")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tick")
    t.add_argument("--office", required=True)
    t.add_argument("--summary", required=True)
    t.add_argument("--evidence", required=True)
    s = sub.add_parser("status")
    s.add_argument("--office", required=True)
    d = sub.add_parser("audit-done")
    d.add_argument("--office", required=True)
    d.add_argument("--report", required=True)
    a = ap.parse_args()
    try:
        if a.cmd == "tick":
            n = tick(a.office, a.summary, a.evidence)
            print(f"✅ {a.office} 第 {n} 輪已入帳" + ("｜🛑 已達十輪，強制停機，須提交衝突審計報告" if n % AUDIT_EVERY == 0 else ""))
        elif a.cmd == "status":
            print(f"{a.office}: 已完成 {cycle_count(a.office)} 輪｜停機鎖={'是' if is_locked(a.office) else '否'}")
        elif a.cmd == "audit-done":
            audit_done(a.office, a.report)
            print("✅ 審計報告已登記，停機解除")
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f"🛑 {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
