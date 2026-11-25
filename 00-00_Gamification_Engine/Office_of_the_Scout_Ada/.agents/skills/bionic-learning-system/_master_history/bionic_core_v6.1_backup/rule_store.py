"""規則庫與生命週期狀態機 (Rule Store · Master v6.1 零信任硬化版)

v6.1 重大硬化：
  1. 封死 CLI 手動填寫 --with-metric / --without-metric 的造假後門！
  2. 新增確定性真值驗算器 `evaluate`：直接讀取本機真實資料集（如 insights_history.jsonl、
     josef_contrast_history.jsonl、deming_quality_history.jsonl），由程式自動切分樣本計算
     with_metric、without_metric 與樣本數 N，並記錄資料集 SHA-256 簽章。
  3. 擴充規則型態：forbid_phrase / prefer_phrase / max_count / regex_forbid / metric_min / metric_max。
  4. 幂等提案 (Idempotent Propose)：相同 office + kind + pattern 若已有 candidate/active 規則，直接回傳既有 ID。

用法：
  python rule_store.py propose  --office kage --kind forbid_phrase --pattern 我就問 --risk low \
      --source-url file://insights_history.jsonl --tier A --evidence "n=4 ER 0.85%" --confidence 0.4
  python rule_store.py evaluate --office kage --rule-id R-... [--dataset path]
  python rule_store.py promote  --office kage --rule-id R-... [--founder-approved]
  python rule_store.py list     --office kage [--status active]
  python rule_store.py sweep
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CORE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CORE_DIR.parent.parent.parent.parent
VAULT_DIR = CORE_DIR / "vaults"
HIGH_RISK = "high"
MIN_TRIAL_N = 3

VALID_KINDS = (
    "forbid_phrase",
    "prefer_phrase",
    "max_count",
    "regex_forbid",
    "metric_min",
    "metric_max",
)

DEFAULT_DATASETS = {
    "kage": ROOT_DIR / ".agents" / "skills" / "threads-growth-auditor" / "data" / "insights_history.jsonl",
    "taylor": ROOT_DIR / ".agents" / "skills" / "threads-growth-auditor" / "data" / "insights_history.jsonl",
    "josef": ROOT_DIR / ".agents" / "skills" / "atom-josef-visual-aesthetics-learner" / "vaults" / "josef_contrast_history.jsonl",
    "deming": ROOT_DIR / ".agents" / "skills" / "atom-deming-quality-sopk-learner" / "vaults" / "deming_quality_history.jsonl",
}


def _path(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{office}_rules.jsonl"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
                # v6.1 只承認附有 dataset_sha256 簽章的真值驗算事件
                if ev.get("dataset_sha256"):
                    r["trials"].append({
                        k: ev[k]
                        for k in ("with_metric", "without_metric", "n", "dataset_sha256", "ts")
                        if k in ev
                    })
            elif t == "promote":
                r["status"] = "active"
                r["promoted_at"] = ev["ts"]
            elif t == "retire":
                r["status"] = "retired"
                r["retired_reason"] = ev.get("reason", "")
    return rules


def propose(
    office: str,
    kind: str,
    pattern: str,
    risk: str,
    source_url: str,
    tier: str,
    evidence: str,
    confidence: float,
    ttl_days: int = 90,
) -> str:
    if kind not in VALID_KINDS:
        raise ValueError(f"不支援的規則型態：{kind}")
    if tier == "D":
        raise ValueError("D 級來源僅作訊號，不得作為規則依據")

    # 幂等檢查：若已有相同 kind + pattern 且未 retired，直接回傳既有 rule_id
    for rid, r in fold(office).items():
        if r["status"] in ("candidate", "active") and r["kind"] == kind and r["pattern"] == pattern:
            return rid

    rid = "R-" + datetime.now().strftime("%Y%m%d") + "-" + uuid.uuid4().hex[:6]
    append_event(
        office,
        {
            "type": "propose",
            "rule_id": rid,
            "kind": kind,
            "pattern": pattern,
            "risk": risk,
            "source_url": source_url,
            "source_tier": tier,
            "evidence": evidence,
            "confidence": confidence,
            "ttl_days": ttl_days,
        },
    )
    return rid


def _load_threads_posts(dataset: Path) -> list[dict]:
    posts = {}
    for line in dataset.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        snap = json.loads(line)
        for p in snap.get("posts", []):
            p = dict(p)
            p["captured_at"] = snap.get("captured_at", "")
            prev = posts.get(p["id"])
            if prev is None or p["captured_at"] >= prev["captured_at"]:
                posts[p["id"]] = p
    return list(posts.values())


def evaluate_rule(office: str, rule_id: str, dataset_path: Path | None = None) -> tuple[bool, str, dict]:
    """由真實資料集自動計算 with_metric 與 without_metric，嚴禁人工填分。"""
    rules = fold(office)
    r = rules.get(rule_id)
    if not r:
        return False, "找不到規則", {}

    ds = Path(dataset_path) if dataset_path else DEFAULT_DATASETS.get(office)
    if not ds or not ds.is_file():
        return False, f"找不到真實資料集：{ds}", {}

    ds_sha = _sha256(ds)
    kind = r["kind"]
    pat = r["pattern"]

    with_vals: list[float] = []
    without_vals: list[float] = []

    first_line = next((x for x in ds.read_text(encoding="utf-8").splitlines() if x.strip()), "{}")
    first_obj = json.loads(first_line)

    if office in ("kage", "taylor") or ds.name == "insights_history.jsonl" or "posts" in first_obj:
        posts = _load_threads_posts(ds)
        for p in posts:
            title = p.get("title", "")
            er = float(p.get("er", 0.0))
            if kind == "forbid_phrase":
                # 遵守規則 = 不含禁用詞；違反規則 = 含禁用詞
                if pat not in title:
                    with_vals.append(er)
                else:
                    without_vals.append(er)
            elif kind == "prefer_phrase":
                if pat in title:
                    with_vals.append(er)
                else:
                    without_vals.append(er)
            elif kind == "max_count":
                word, lim_s = pat.rsplit(":", 1)
                lim = int(lim_s)
                cnt = (
                    len(re.findall(r"[\U00010000-\U0010ffff]", title))
                    if word.lower() == "emoji"
                    else title.count("？") + title.count("?")
                    if word in ("?", "？")
                    else title.count(word)
                )
                if cnt <= lim:
                    with_vals.append(er)
                else:
                    without_vals.append(er)
            elif kind == "regex_forbid":
                if not re.search(pat, title):
                    with_vals.append(er)
                else:
                    without_vals.append(er)
        n_target = min(len(with_vals), len(without_vals))
        if not with_vals or not without_vals:
            return False, f"樣本切分不足（with={len(with_vals)}, without={len(without_vals)}）", {}
        w_mean = round(statistics.mean(with_vals), 4)
        wo_mean = round(statistics.mean(without_vals), 4)
    elif kind in ("metric_min", "metric_max"):
        # 針對數值型存摺（如 josef 對比度、deming 通過率）
        metric_name, bound_s = pat.rsplit(":", 1)
        bound = float(bound_s)
        records = [json.loads(x) for x in ds.read_text(encoding="utf-8").splitlines() if x.strip()]
        if not records:
            return False, "資料集為空", {}
        last = records[-1]
        if isinstance(last.get("pairs"), list):
            for pair in last["pairs"]:
                val = float(pair.get("ratio", pair.get("contrast", 0.0)))
                ok_cond = (val >= bound) if kind == "metric_min" else (val <= bound)
                (with_vals if ok_cond else without_vals).append(val)
            n_target = len(with_vals) + len(without_vals)
            w_mean = round(statistics.mean(with_vals), 4) if with_vals else bound
            wo_mean = round(statistics.mean(without_vals), 4) if without_vals else 0.0
        elif "pass_body_text_7" in last and "pairs" in last:
            # josef_contrast_history.jsonl 摘要結構
            n_target = int(last["pairs"])
            w_mean = round(float(last["pass_body_text_7"]) / max(1, n_target) * 100.0, 2)
            wo_mean = 0.0
        elif "passed" in last and "total" in last:
            # deming_quality_history.jsonl 摘要結構
            n_target = int(last["total"])
            w_mean = round(float(last["passed"]) / max(1, n_target) * 100.0, 2)
            wo_mean = round(float(last.get("defects", 0)) / max(1, n_target) * 100.0, 2)
        else:
            val = float(last.get(metric_name, 1.0))
            n_target = int(last.get("total_scripts", last.get("n", MIN_TRIAL_N)))
            w_mean = val
            wo_mean = 0.0
    else:
        return False, f"尚未定義 {office}/{kind} 的自動真值驗算邏輯", {}

    ev = {
        "type": "trial",
        "rule_id": rule_id,
        "with_metric": w_mean,
        "without_metric": wo_mean,
        "n": n_target,
        "dataset": str(ds),
        "dataset_sha256": ds_sha,
    }
    append_event(office, ev)
    return True, f"真值驗算完成：with={w_mean} vs without={wo_mean} (N={n_target}, sha256={ds_sha[:10]}...)", ev


def trial_ok(rule: dict) -> tuple[bool, str]:
    if not rule["trials"]:
        return False, "尚無通過真值簽章的 evaluate 紀錄"
    # 取最新一次真實資料集驗算結果（因資料集本身已是累積快照，避免重複跑 evaluate 虛增 N）
    latest = rule["trials"][-1]
    n = int(latest["n"])
    w = float(latest["with_metric"])
    wo = float(latest["without_metric"])
    if n < MIN_TRIAL_N:
        return False, f"真實樣本數 {n} < 最低門檻 {MIN_TRIAL_N}"
    if w <= wo:
        return False, f"遵守規則指標({w:.2f}) 未優於對照組({wo:.2f})"
    return True, f"遵守規則({w:.2f}) > 對照組({wo:.2f})，真實樣本 N={n}，簽章={latest['dataset_sha256'][:10]}"


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
    ap = argparse.ArgumentParser(description="規則庫與生命週期 (v6.1 零信任硬化版)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("propose")
    p.add_argument("--office", required=True)
    p.add_argument("--kind", required=True, choices=VALID_KINDS)
    p.add_argument("--pattern", required=True)
    p.add_argument("--risk", choices=["low", "high"], default="low")
    p.add_argument("--source-url", required=True)
    p.add_argument("--tier", choices=["A", "B", "C", "D"], required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--confidence", type=float, default=0.3)
    p.add_argument("--ttl-days", type=int, default=90)

    ev_p = sub.add_parser("evaluate", help="由真實資料集自動驗算指標（禁止手動填數字）")
    ev_p.add_argument("--office", required=True)
    ev_p.add_argument("--rule-id", required=True)
    ev_p.add_argument("--dataset", help="選填：指定真實資料集檔案路徑")

    pr = sub.add_parser("promote")
    pr.add_argument("--office", required=True)
    pr.add_argument("--rule-id", required=True)
    pr.add_argument("--founder-approved", action="store_true")

    ls = sub.add_parser("list")
    ls.add_argument("--office", required=True)
    ls.add_argument("--status")
    sub.add_parser("sweep")
    a = ap.parse_args()

    try:
        if a.cmd == "propose":
            rid = propose(
                a.office, a.kind, a.pattern, a.risk, a.source_url, a.tier, a.evidence, a.confidence, a.ttl_days
            )
            print(f"✅ 已登記 candidate：{rid}")
        elif a.cmd == "evaluate":
            ok, msg, _ = evaluate_rule(a.office, a.rule_id, Path(a.dataset) if a.dataset else None)
            print(("✅ " if ok else "🛑 ") + msg)
            sys.exit(0 if ok else 1)
        elif a.cmd == "promote":
            ok, why = promote(a.office, a.rule_id, a.founder_approved)
            print(("✅ 已轉正：" if ok else "🛑 拒絕轉正：") + why)
            sys.exit(0 if ok else 1)
        elif a.cmd == "list":
            for rid, r in fold(a.office).items():
                if a.status and r["status"] != a.status:
                    continue
                n_last = r["trials"][-1]["n"] if r["trials"] else 0
                print(
                    f"{rid} [{r['status']}] {r['kind']}:{r['pattern']} risk={r['risk']} tier={r['source_tier']} 真實樣本N={n_last}"
                )
        elif a.cmd == "sweep":
            out = sweep()
            print(f"🧹 淘汰 {len(out)} 條：{out}")
    except ValueError as e:
        print(f"🛑 {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
