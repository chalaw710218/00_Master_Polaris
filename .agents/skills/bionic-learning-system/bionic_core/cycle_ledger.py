"""輪次帳本與十輪強制停機 (Cycle Ledger · Master v6.2 零信任硬化版)

v6.2 重大硬化（修補漏洞 4 與漏洞 5）：
  1. 去時間戳規範化雜湊 (`_canonical_evidence_sha256`)：
     對 JSON 憑證檔遞迴剝離 `executed_at`、`ts`、`discovered_at`、`fetched_at`、`updated_at`、`learned_at` 等時間戳欄位後再算 SHA-256。
     若資料與規則實質內容未變，重跑幾次雜湊皆相同，當場阻斷空轉刷輪次！
  2. 程式化十輪衝突與互斥掃描器 (`audit_scan`)：
     廢除純文字樣板空殼審計！`audit_done` 解鎖時強制執行 `audit_scan(office)`，實質掃描規則庫是否存在：
       - 同詞同時被 `forbid_phrase` 與 `prefer_phrase`（直接矛盾）
       - `prefer_phrase` 被 `regex_forbid` 命中，或同指標 `metric_min > metric_max`（互斥死鎖）
       - 竄改攔截 (`tampered_rejected`) 或驗算失敗待淘汰規則
     若規則庫仍存在未排除之矛盾或互斥，`audit_done` 拒絕解鎖！
  3. 統一 `MIN_AUDIT_CHARS = 100`（與規格文件完全一致）。

用法：
  python cycle_ledger.py tick --office kage --summary "本輪做了什麼" --evidence path\\to\\real_file.json
  python cycle_ledger.py status --office kage
  python cycle_ledger.py audit-scan --office kage [--out path\\to\\audit_report.md]
  python cycle_ledger.py audit-done --office kage --report path\\to\\audit_report.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rule_store  # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

VAULT_DIR = Path(__file__).resolve().parent / "vaults"
AUDIT_EVERY = 10
REQUIRED_AUDIT_SECTIONS = ("矛盾比對", "互斥掃描", "淘汰清單")
MIN_AUDIT_CHARS = 100
VOLATILE_TIME_KEYS = {"executed_at", "ts", "discovered_at", "fetched_at", "updated_at", "learned_at", "promoted_at"}


def _ledger(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{office}_cycles.jsonl"


def _lock(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{office}.AUDIT_REQUIRED.lock"


def _strip_volatile(obj):
    if isinstance(obj, dict):
        return {k: _strip_volatile(v) for k, v in sorted(obj.items()) if k not in VOLATILE_TIME_KEYS}
    if isinstance(obj, list):
        return [_strip_volatile(x) for x in obj]
    return obj


def _canonical_evidence_sha256(ev_path: Path) -> str:
    """計算排除微秒/時間戳後的實質內容 SHA-256，防止靠時間戳刷輪次。"""
    raw = ev_path.read_bytes()
    try:
        text = raw.decode("utf-8")
        if ev_path.suffix.lower() == ".json":
            obj = json.loads(text)
            clean = _strip_volatile(obj)
            canon = json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            return hashlib.sha256(canon.encode("utf-8")).hexdigest()
        if ev_path.suffix.lower() == ".jsonl":
            lines = [ _strip_volatile(json.loads(line)) for line in text.splitlines() if line.strip() ]
            canon = json.dumps(lines, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            return hashlib.sha256(canon.encode("utf-8")).hexdigest()
    except Exception:
        pass
    return hashlib.sha256(raw).hexdigest()


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

    sha = _canonical_evidence_sha256(ev_path)
    history = read(office)
    used_shas = {e.get("evidence_sha256") for e in history if e.get("type") == "tick"}
    if sha in used_shas:
        raise ValueError(f"防刷輪次阻斷：去時間戳實質內容 SHA-256 ({sha[:12]}...) 與歷史輪次重複，無實質新變更！")

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


def audit_scan(office: str) -> dict:
    """程式化掃描指定辦公室規則庫之直接矛盾、正則/數值互斥與待淘汰項目。"""
    old_vault = rule_store.VAULT_DIR
    rule_store.VAULT_DIR = VAULT_DIR
    try:
        rules = rule_store.fold(office)
    finally:
        rule_store.VAULT_DIR = old_vault

    live = [r for r in rules.values() if r.get("status") in ("active", "candidate")]
    forbids = {r["pattern"]: r["rule_id"] for r in live if r.get("kind") == "forbid_phrase"}
    prefers = {r["pattern"]: r["rule_id"] for r in live if r.get("kind") == "prefer_phrase"}
    regexes = [(r["pattern"], r["rule_id"]) for r in live if r.get("kind") == "regex_forbid"]

    contradictions: list[str] = []
    for pat, fid in forbids.items():
        if pat in prefers:
            contradictions.append(f"直接矛盾：詞彙『{pat}』同時存在於 forbid_phrase ({fid}) 與 prefer_phrase ({prefers[pat]})")

    mutual_exclusions: list[str] = []
    for pat, pid in prefers.items():
        for rx, rid in regexes:
            try:
                if re.search(rx, pat):
                    mutual_exclusions.append(f"正則互斥：prefer_phrase『{pat}』({pid}) 會被 regex_forbid `{rx}` ({rid}) 攔截")
            except re.error:
                pass

    metric_mins: dict[str, tuple[float, str]] = {}
    metric_maxs: dict[str, tuple[float, str]] = {}
    for r in live:
        if r.get("kind") in ("metric_min", "metric_max") and ":" in r.get("pattern", ""):
            k, v_s = r["pattern"].rsplit(":", 1)
            try:
                val = float(v_s)
                if r["kind"] == "metric_min":
                    metric_mins[k] = (val, r["rule_id"])
                else:
                    metric_maxs[k] = (val, r["rule_id"])
            except ValueError:
                pass
    for k, (mn, mn_id) in metric_mins.items():
        if k in metric_maxs:
            mx, mx_id = metric_maxs[k]
            if mn > mx:
                mutual_exclusions.append(f"數值互斥：指標 `{k}` 下限 {mn} ({mn_id}) > 上限 {mx} ({mx_id})")

    retire_list: list[str] = []
    for rid, r in rules.items():
        if r.get("status") == "tampered_rejected":
            retire_list.append(f"{rid} [竄改攔截]: {r.get('tampered_reason', '')}")
        elif r.get("status") == "retired":
            retire_list.append(f"{rid} [已淘汰]: {r.get('retired_reason', '')}")
        elif r.get("status") == "candidate" and r.get("trials"):
            last_t = r["trials"][-1]
            if float(last_t.get("with_metric", 0)) <= float(last_t.get("without_metric", 0)):
                retire_list.append(f"{rid} [候選未達標]: with={last_t.get('with_metric')} <= without={last_t.get('without_metric')}")

    scan_payload = {
        "office": office,
        "total_rules": len(rules),
        "live_rules": len(live),
        "contradictions": contradictions,
        "mutual_exclusions": mutual_exclusions,
        "retire_list": retire_list,
        "clean": (not contradictions) and (not mutual_exclusions),
    }
    digest = hashlib.sha256(
        json.dumps(scan_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    scan_payload["scan_digest"] = digest
    return scan_payload


def render_audit_markdown(scan: dict) -> str:
    c_lines = "\n".join(f"- {x}" for x in scan["contradictions"]) if scan["contradictions"] else "- 經程式掃描全量規則庫，0 項直接語義矛盾（forbid vs prefer 零交集）。"
    m_lines = "\n".join(f"- {x}" for x in scan["mutual_exclusions"]) if scan["mutual_exclusions"] else "- 經程式掃描所有正則與數值上下限，0 項互斥死鎖現象。"
    r_lines = "\n".join(f"- {x}" for x in scan["retire_list"]) if scan["retire_list"] else "- 本周期無過期或劣化待退場規則，全數通過真值檢驗。"
    return (
        f"# 第十輪程式化衝突大審計報告 ({scan['office']})\n\n"
        f"- **掃描簽章 (SCAN-DIGEST)**：`{scan['scan_digest']}`\n"
        f"- **總規則數**：{scan['total_rules']}（現役/候選：{scan['live_rules']}）\n\n"
        f"## 1. 矛盾比對\n{c_lines}\n\n"
        f"## 2. 互斥掃描\n{m_lines}\n\n"
        f"## 3. 淘汰清單\n{r_lines}\n"
    )


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

    # 【v6.2 強制執行真實程式化矛盾與互斥掃描】
    scan = audit_scan(office)
    if not scan["clean"]:
        issues = scan["contradictions"] + scan["mutual_exclusions"]
        raise ValueError(f"程式化衝突掃描未通過，拒絕解鎖！請先解決以下規則衝突：{issues}")

    sha = hashlib.sha256(rp.read_bytes()).hexdigest()
    ev = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "type": "audit_done",
        "report": str(rp),
        "report_sha256": sha,
        "scan_digest": scan["scan_digest"],
    }
    with open(_ledger(office), "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    if _lock(office).exists():
        _lock(office).unlink()


def main() -> None:
    ap = argparse.ArgumentParser(description="輪次帳本 (v6.2 零信任硬化版)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tick")
    t.add_argument("--office", required=True)
    t.add_argument("--summary", required=True)
    t.add_argument("--evidence", required=True)
    s = sub.add_parser("status")
    s.add_argument("--office", required=True)
    sc = sub.add_parser("audit-scan")
    sc.add_argument("--office", required=True)
    sc.add_argument("--out", help="選填：輸出 Markdown 審計報告路徑")
    d = sub.add_parser("audit-done")
    d.add_argument("--office", required=True)
    d.add_argument("--report", required=True)
    a = ap.parse_args()
    try:
        if a.cmd == "tick":
            n = tick(a.office, a.summary, a.evidence)
            print(
                f"✅ {a.office} 第 {n} 輪已入帳（去時間戳實質 SHA-256 已簽章）"
                + ("｜🛑 已達十輪，強制停機，須提交衝突審計報告" if n % AUDIT_EVERY == 0 else "")
            )
        elif a.cmd == "status":
            print(f"{a.office}: 已完成 {cycle_count(a.office)} 輪｜停機鎖={'是' if is_locked(a.office) else '否'}")
        elif a.cmd == "audit-scan":
            scan = audit_scan(a.office)
            md = render_audit_markdown(scan)
            if a.out:
                Path(a.out).write_text(md, encoding="utf-8")
            print(md)
            if not scan["clean"]:
                sys.exit(1)
        elif a.cmd == "audit-done":
            audit_done(a.office, a.report)
            print("✅ 審計報告與程式化衝突掃描通過，停機鎖已解除")
    except (RuntimeError, ValueError, FileNotFoundError) as e:
        print(f"🛑 {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
