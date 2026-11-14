"""規則庫與生命週期狀態機 (Rule Store · Master v6.0 第十一章 ④⑥⑦ 段)

規則以 Append-Only 事件溯源儲存（RFC #001 無鎖協議）：
  propose ➔ candidate；trial 累積 A/B 證據；promote ➔ active；sweep/retire ➔ retired。
高風險規則（定價/法務/對外發布/金錢/憲法）必須 --founder-approved 才可轉正。

用法：
  python rule_store.py propose --office kage --kind forbid_phrase --pattern 我就問 --risk low \
      --source-url file://insights_history.jsonl --tier A --evidence "n=4 ER 0.85%" --confidence 0.4
  python rule_store.py trial   --rule-id R-... --with-metric 3.1 --without-metric 2.0 --n 3
  python rule_store.py promote --rule-id R-... [--founder-approved]
  python rule_store.py list --office kage [--status active]
  python rule_store.py sweep   # TTL 到期者標記 retired
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

VAULT_DIR = Path(__file__).resolve().parent / "vaults"
HIGH_RISK = "high"
MIN_TRIAL_N = 3


def _path(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{office}_rules.jsonl"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def append_event(office: str, event: dict) -> None:
    event = {"ts": _now(), "office": office, **event}
    with open(_path(office), "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def fold(office: str) -> dict[str, dict]:
    """將事件折疊為各規則最新狀態。"""
    rules: dict[str, dict] = {}
    p = _path(office)
    if not p.exists():
        return rules
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        ev = json.loads(line)
        rid = ev.get("rule_id")
        t = ev.get("type")
        if t == "propose":
            rules[rid] = {**ev, "status": "candidate", "trials": []}
        elif rid in rules:
            r = rules[rid]
            if t == "trial":
                r["trials"].append({k: ev[k] for k in ("with_metric", "without_metric", "n", "ts")})
            elif t == "promote":
                r["status"] = "active"
                r["promoted_at"] = ev["ts"]
            elif t == "retire":
                r["status"] = "retired"
                r["retired_reason"] = ev.get("reason", "")
    return rules


def propose(office, kind, pattern, risk, source_url, tier, evidence, confidence, ttl_days=90) -> str:
    rid = "R-" + datetime.now().strftime("%Y%m%d") + "-" + uuid.uuid4().hex[:6]
    append_event(office, {
        "type": "propose", "rule_id": rid, "kind": kind, "pattern": pattern,
        "risk": risk, "source_url": source_url, "source_tier": tier,
        "evidence": evidence, "confidence": confidence, "ttl_days": ttl_days,
    })
    return rid


def trial_ok(rule: dict) -> tuple[bool, str]:
    n = sum(t["n"] for t in rule["trials"])
    if n < MIN_TRIAL_N:
        return False, f"試用樣本 {n} < {MIN_TRIAL_N}"
    w = sum(t["with_metric"] * t["n"] for t in rule["trials"]) / n
    wo = sum(t["without_metric"] * t["n"] for t in rule["trials"]) / n
    if w <= wo:
        return False, f"用規則({w:.2f}) 未優於對照({wo:.2f})"
    return True, f"用規則({w:.2f}) > 對照({wo:.2f})，N={n}"


def promote(office: str, rule_id: str, founder_approved: bool = False) -> tuple[bool, str]:
    rules = fold(office)
    r = rules.get(rule_id)
    if not r:
        return False, "找不到規則"
    if r["status"] != "candidate":
        return False, f"狀態為 {r['status']}，只有 candidate 可轉正"
    ok, why = trial_ok(r)
    if not ok:
        return False, why
    if r["risk"] == HIGH_RISK and not founder_approved:
        return False, "高風險規則必須創辦人點頭（--founder-approved）"
    append_event(office, {"type": "promote", "rule_id": rule_id, "founder_approved": founder_approved})
    return True, why


def sweep() -> list[str]:
    """TTL 到期且仍為 candidate/active 者標記 retired（溶酶體衰減）。"""
    retired = []
    for p in VAULT_DIR.glob("*_rules.jsonl") if VAULT_DIR.exists() else []:
        office = p.name.replace("_rules.jsonl", "")
        for rid, r in fold(office).items():
            if r["status"] in ("candidate", "active"):
                born = datetime.fromisoformat(r["ts"])
                if datetime.now() > born + timedelta(days=int(r.get("ttl_days", 90))):
                    append_event(office, {"type": "retire", "rule_id": rid, "reason": "TTL 到期未再獲證據支持"})
                    retired.append(rid)
    return retired


def main() -> None:
    ap = argparse.ArgumentParser(description="規則庫與生命週期")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("propose")
    p.add_argument("--office", required=True)
    p.add_argument("--kind", required=True, choices=["forbid_phrase", "prefer_phrase", "max_count"])
    p.add_argument("--pattern", required=True)
    p.add_argument("--risk", choices=["low", "high"], default="low")
    p.add_argument("--source-url", required=True)
    p.add_argument("--tier", choices=["A", "B", "C", "D"], required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--confidence", type=float, default=0.3)
    p.add_argument("--ttl-days", type=int, default=90)
    t = sub.add_parser("trial")
    t.add_argument("--office", required=True)
    t.add_argument("--rule-id", required=True)
    t.add_argument("--with-metric", type=float, required=True)
    t.add_argument("--without-metric", type=float, required=True)
    t.add_argument("--n", type=int, required=True)
    pr = sub.add_parser("promote")
    pr.add_argument("--office", required=True)
    pr.add_argument("--rule-id", required=True)
    pr.add_argument("--founder-approved", action="store_true")
    ls = sub.add_parser("list")
    ls.add_argument("--office", required=True)
    ls.add_argument("--status")
    sub.add_parser("sweep")
    a = ap.parse_args()

    if a.cmd == "propose":
        if a.tier == "D":
            print("🛑 D 級來源僅作訊號，不得作為規則依據。")
            sys.exit(1)
        rid = propose(a.office, a.kind, a.pattern, a.risk, a.source_url, a.tier, a.evidence, a.confidence, a.ttl_days)
        print(f"✅ 已建立 candidate：{rid}")
    elif a.cmd == "trial":
        if a.rule_id not in fold(a.office):
            print("🛑 找不到規則")
            sys.exit(1)
        append_event(a.office, {"type": "trial", "rule_id": a.rule_id, "with_metric": a.with_metric,
                                "without_metric": a.without_metric, "n": a.n})
        print("✅ 已記錄試用結果（真值須來自外部指標，不得自評）")
    elif a.cmd == "promote":
        ok, why = promote(a.office, a.rule_id, a.founder_approved)
        print(("✅ 已轉正：" if ok else "🛑 拒絕轉正：") + why)
        sys.exit(0 if ok else 1)
    elif a.cmd == "list":
        for rid, r in fold(a.office).items():
            if a.status and r["status"] != a.status:
                continue
            print(f"{rid} [{r['status']}] {r['kind']}:{r['pattern']} risk={r['risk']} tier={r['source_tier']} 試用N={sum(x['n'] for x in r['trials'])}")
    elif a.cmd == "sweep":
        out = sweep()
        print(f"🧹 淘汰 {len(out)} 條：{out}")


if __name__ == "__main__":
    main()
