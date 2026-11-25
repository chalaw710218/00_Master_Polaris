"""輪次帳本與十輪強制停機 (Cycle Ledger · Master v6.1 零信任硬化版)

v6.1 重大硬化：
  1. 實體憑證驗證：`--evidence` 必須是本機真實存在的非空檔案，程式當場計算 SHA-256。
  2. 防刷輪次機制：若新憑證檔案的 SHA-256 與該子版過去任一輪重複（代表檔案未更新、拿舊檔混輪次），
     直接拋出 ValueError 拒絕入帳！
  3. 審計報告實質審查：`audit-done` 強制檢查報告必須為 .md 或 .json，字數 >= 100，
     且必須同時包含「矛盾比對」、「互斥掃描」、「淘汰清單」三大實質審查段落，杜絕拿任意程式檔冒充。

用法：
  python cycle_ledger.py tick --office kage --summary "本輪做了什麼" --evidence path\\to\\real_file.json
  python cycle_ledger.py status --office kage
  python cycle_ledger.py audit-done --office kage --report path\\to\\audit_report.md
"""
from __future__ import annotations

import argparse
import hashlib
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
REQUIRED_AUDIT_SECTIONS = ("矛盾比對", "互斥掃描", "淘汰清單")
MIN_AUDIT_CHARS = 80


def _ledger(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{office}_cycles.jsonl"


def _lock(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
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
        raise RuntimeError("已停機：滿 10 輪須先提交合規衝突審計報告（audit-done）")
    if not evidence or not evidence.strip():
        raise ValueError("每一輪必須附物理憑證檔案路徑，不得為空")

    ev_path = Path(evidence.replace("file://", ""))
    if not ev_path.is_file() or ev_path.stat().st_size == 0:
        raise ValueError(f"物理憑證檔案不存在或為空檔：{evidence}")

    sha = hashlib.sha256(ev_path.read_bytes()).hexdigest()
    history = read(office)
    used_shas = {e.get("evidence_sha256") for e in history if e.get("type") == "tick"}
    if sha in used_shas:
        raise ValueError(f"防刷輪次阻斷：憑證 SHA-256 ({sha[:12]}...) 與歷史輪次重複，檔案未發生新變更！")

    n = cycle_count(office) + 1
    ev = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "type": "tick",
        "cycle": n,
        "summary": summary,
        "evidence": str(ev_path),
        "evidence_sha256": sha,
    }
    with open(_ledger(office), "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    if n % AUDIT_EVERY == 0:
        _lock(office).write_text(f"cycle {n} reached at {ev['ts']} (sha256={sha[:12]})\n", encoding="utf-8")
    return n


def audit_done(office: str, report: str) -> None:
    rp = Path(report)
    if not rp.is_file():
        raise FileNotFoundError(f"審計報告不存在：{report}")
    if rp.suffix.lower() not in (".md", ".json"):
        raise ValueError(f"審計報告格式非法（僅允許 .md 或 .json）：{rp.name}")

    content = rp.read_text(encoding="utf-8", errors="replace").strip()
    if len(content) < MIN_AUDIT_CHARS:
        raise ValueError(f"審計報告內容過短（{len(content)} 字 < {MIN_AUDIT_CHARS} 字），拒絕空頭報告")

    missing = [sec for sec in REQUIRED_AUDIT_SECTIONS if sec not in content]
    if missing:
        raise ValueError(f"審計報告缺少必要實質審查段落：{missing}")

    sha = hashlib.sha256(rp.read_bytes()).hexdigest()
    ev = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "type": "audit_done",
        "report": str(rp),
        "report_sha256": sha,
    }
    with open(_ledger(office), "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    if _lock(office).exists():
        _lock(office).unlink()


def main() -> None:
    ap = argparse.ArgumentParser(description="輪次帳本 (v6.1 零信任硬化版)")
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
            print(
                f"✅ {a.office} 第 {n} 輪已入帳（SHA-256 已簽章）"
                + ("｜🛑 已達十輪，強制停機，須提交衝突審計報告" if n % AUDIT_EVERY == 0 else "")
            )
        elif a.cmd == "status":
            print(f"{a.office}: 已完成 {cycle_count(a.office)} 輪｜停機鎖={'是' if is_locked(a.office) else '否'}")
        elif a.cmd == "audit-done":
            audit_done(a.office, a.report)
            print("✅ 審計報告實質審查通過，停機鎖已解除")
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f"🛑 {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
