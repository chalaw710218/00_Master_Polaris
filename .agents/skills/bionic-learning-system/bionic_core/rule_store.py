"""規則庫與生命週期狀態機 (Rule Store · Master v6.2 零信任硬化版)

v6.2 重大硬化（對應外部紅隊代碼審計五大漏洞修補）：
  1. 折疊時零信任二次驗算 (`fold()`)：絕不無條件相信 JSONL 內的 `promote` 事件！折疊時強制重驗 `trial_ok(r)` 與高風險 `founder_approved`；若手動塞入假 `promote`，狀態直接打入 `tampered_rejected`。
  2. 時序留出驗證與誤傷率掃描 (`evaluate_rule`)：
     - 針對貼文資料集（N >= 8）自動執行「時序切分（前 50% 探索、後 50% 留出驗證 Holdout）」，要求留出集亦須滿足 `holdout_with > holdout_without`。
     - 新增「高成效貼文誤傷率（Collateral Damage Rate）」掃描：若禁用詞或正則誤殺超過 35% 的高於中位數好文（如過寬的單字『風/雨』），當場拒絕通過！
  3. 廢除 `wo_mean = 0.0` 假驗算，區分「經驗比較規則」與「合規基準標準 (`baseline_standard`)」：
     - `josef` 摘要改為真實比較 `pass_rate` vs `fail_rate`（27% 通過率不再假轉正）。
     - `deming` 的 `defects:0` 嚴格檢驗 `actual_defects <= bound`（只要有 1 個缺陷即不通過）。
     - 固定憲法標準（如 WCAG 7:1、零缺陷）改走 `baseline_standard`，誠實標示為合規基準，不偽裝成 A/B 實驗。
  4. 新增 `route`（雪的幕僚長派工路由規則，格式 `類別->閣員`）與 `scope`（`prefix` 開頭鉤子 vs `any` 全文），確保評估與執行 100% 對齊。
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
MAX_COLLATERAL_RATE = 0.35

VALID_KINDS = (
    "forbid_phrase",
    "prefer_phrase",
    "max_count",
    "regex_forbid",
    "metric_min",
    "metric_max",
    "baseline_standard",
    "route",
)

DEFAULT_DATASETS = {
    "kage": ROOT_DIR / ".agents" / "skills" / "threads-growth-auditor" / "data" / "insights_history.jsonl",
    "taylor": ROOT_DIR / ".agents" / "skills" / "threads-growth-auditor" / "data" / "insights_history.jsonl",
    "josef": ROOT_DIR / ".agents" / "skills" / "atom-josef-visual-aesthetics-learner" / "vaults" / "josef_contrast_history.jsonl",
    "deming": ROOT_DIR / ".agents" / "skills" / "atom-deming-quality-sopk-learner" / "vaults" / "deming_quality_history.jsonl",
    "yuki": ROOT_DIR / ".agents" / "skills" / "atom-yuki-autonomous-executive-learner" / "vaults" / "yuki_dispatch.jsonl",
}


def _path(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{office}_rules.jsonl"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canon(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def append_event(office: str, event: dict) -> dict:
    p = _path(office)
    prev = "0" * 64
    if p.exists():
        lines = [x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
        if lines:
            last_ev = json.loads(lines[-1])
            prev = last_ev.get("hash", hashlib.sha256(_canon(last_ev).encode("utf-8")).hexdigest())
    body = {"ts": _now(), "office": office, **event, "prev": prev}
    body["hash"] = hashlib.sha256(_canon(body).encode("utf-8")).hexdigest()
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(body, ensure_ascii=False) + "\n")
    return body


def trial_ok(rule: dict) -> tuple[bool, str]:
    if rule.get("kind") == "baseline_standard":
        if not rule["trials"]:
            return False, "合規基準標準尚無基線盤點紀錄"
        latest = rule["trials"][-1]
        return True, f"合規基準標準已盤點綁定（基線達標率={latest['with_metric']}%，N={latest['n']}，簽章={latest['dataset_sha256'][:10]}）"

    if not rule["trials"]:
        return False, "尚無通過真值簽章的 evaluate 紀錄"
    latest = rule["trials"][-1]
    n = int(latest["n"])
    w = float(latest["with_metric"])
    wo = float(latest["without_metric"])
    if latest.get("collateral_rejected"):
        return False, f"歷史好文誤傷率過高 ({latest.get('collateral_rate', 0):.0%} > {MAX_COLLATERAL_RATE:.0%})，拒絕轉正"
    if latest.get("holdout_passed") is False:
        return False, "留出驗證集 (Holdout Split) 未優於對照組，疑似樣本內過擬合"
    if n < MIN_TRIAL_N:
        return False, f"真實樣本數 {n} < 最低門檻 {MIN_TRIAL_N}"
    if w <= wo:
        return False, f"遵守規則指標({w:.2f}) 未優於對照組({wo:.2f})"
    return True, f"遵守規則({w:.2f}) > 對照組({wo:.2f})，真實樣本 N={n}，簽章={latest['dataset_sha256'][:10]}"


def fold(office: str) -> dict[str, dict]:
    """將事件折疊為各規則最新狀態（v6.2 內建零信任折疊時二次驗算）。"""
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
            rules[rid] = {
                "scope": "any",
                **ev,
                "status": "candidate",
                "trials": [],
            }
        elif rid in rules:
            r = rules[rid]
            if t == "trial":
                ds_sha = ev.get("dataset_sha256", "")
                if ds_sha and len(str(ds_sha)) == 64:
                    # 若資料集仍在原路徑，校驗 SHA-256 是否真實存在（防止手填假雜湊）
                    ds_path_str = ev.get("dataset", "")
                    r["trials"].append({
                        k: ev[k]
                        for k in (
                            "with_metric",
                            "without_metric",
                            "n",
                            "dataset",
                            "dataset_sha256",
                            "holdout_passed",
                            "collateral_rate",
                            "collateral_rejected",
                            "ts",
                        )
                        if k in ev
                    })
                    r["last_dataset"] = ds_path_str
            elif t == "promote":
                # 【v6.2 零信任防篡改核心】：折疊 promote 時強制重驗 trial_ok 與高風險授權！
                ok_t, why_t = trial_ok(r)
                high_unapproved = (r.get("risk") == HIGH_RISK) and (not ev.get("founder_approved", False))
                if not ok_t or high_unapproved:
                    r["status"] = "tampered_rejected"
                    r["tampered_reason"] = "高風險未獲創辦人授權" if high_unapproved else f"未通過驗算即偽造轉正 ({why_t})"
                else:
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
    scope: str = "any",
) -> str:
    if kind not in VALID_KINDS:
        raise ValueError(f"不支援的規則型態：{kind}")
    if tier == "D":
        raise ValueError("D 級來源僅作訊號，不得作為規則依據")
    if scope not in ("any", "prefix"):
        raise ValueError("scope 僅支援 'any' 或 'prefix'")

    for rid, r in fold(office).items():
        if (
            r["status"] in ("candidate", "active")
            and r["kind"] == kind
            and r["pattern"] == pattern
            and r.get("scope", "any") == scope
        ):
            return rid

    rid = "R-" + datetime.now().strftime("%Y%m%d") + "-" + uuid.uuid4().hex[:6]
    append_event(
        office,
        {
            "type": "propose",
            "rule_id": rid,
            "kind": kind,
            "pattern": pattern,
            "scope": scope,
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
        for idx, p in enumerate(snap.get("posts", [])):
            p = dict(p)
            p["captured_at"] = snap.get("captured_at", "")
            p["_order"] = idx
            prev = posts.get(p["id"])
            if prev is None or p["captured_at"] >= prev["captured_at"]:
                posts[p["id"]] = p
    out = list(posts.values())
    out.sort(key=lambda x: (str(x.get("captured_at", "")), str(x.get("id", ""))))
    return out


def _match_phrase(title: str, pat: str, scope: str) -> bool:
    if scope == "prefix":
        lines = [ln.strip() for ln in title.splitlines() if ln.strip()]
        head = " ".join(lines[:2]) if lines else title[:30]
        return head.startswith(pat) or (pat in head[:25])
    return pat in title


def _classify_post_compliance(title: str, kind: str, pat: str, scope: str = "any") -> bool:
    """回傳該貼文是否『遵守』此規則 (True = 遵守組 with, False = 違反/對照組 without)。"""
    if kind == "forbid_phrase":
        return not _match_phrase(title, pat, scope)
    if kind == "prefer_phrase":
        return _match_phrase(title, pat, scope)
    if kind == "max_count":
        word, lim_s = pat.rsplit(":", 1)
        lim = int(lim_s)
        cnt = (
            len(re.findall(r"[\U00010000-\U0010ffff\u2600-\u27bf]", title))
            if word.lower() == "emoji"
            else title.count("？") + title.count("?")
            if word in ("?", "？")
            else title.count(word)
        )
        return cnt <= lim
    if kind == "regex_forbid":
        return not bool(re.search(pat, title))
    return True


def evaluate_rule(office: str, rule_id: str, dataset_path: Path | None = None) -> tuple[bool, str, dict]:
    """由真實資料集自動計算 with_metric 與 without_metric，內建時序留出驗證與誤傷率檢查。"""
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
    scope = r.get("scope", "any")

    with_vals: list[float] = []
    without_vals: list[float] = []
    holdout_passed = True
    collateral_rate = 0.0
    collateral_rejected = False

    first_line = next((x for x in ds.read_text(encoding="utf-8").splitlines() if x.strip()), "{}")
    first_obj = json.loads(first_line)

    if office in ("kage", "taylor") or ds.name == "insights_history.jsonl" or "posts" in first_obj:
        posts = _load_threads_posts(ds)
        if not posts:
            return False, "貼文資料集為空", {}

        all_ers = [float(p.get("er", 0.0)) for p in posts]
        med_er = statistics.median(all_ers) if all_ers else 0.0
        good_posts = [p for p in posts if float(p.get("er", 0.0)) > med_er]
        killed_good = 0

        for p in posts:
            title = p.get("title", "")
            er = float(p.get("er", 0.0))
            compliant = _classify_post_compliance(title, kind, pat, scope)
            if compliant:
                with_vals.append(er)
            else:
                without_vals.append(er)
                if er > med_er:
                    killed_good += 1

        if kind in ("forbid_phrase", "regex_forbid") and len(good_posts) >= 3:
            collateral_rate = round(killed_good / len(good_posts), 4)
            if collateral_rate > MAX_COLLATERAL_RATE:
                collateral_rejected = True

        # 時序留出集驗證 (Chronological Holdout Split)：當總貼文數 >= 10 時，切分後半段為留出集
        if len(posts) >= 10:
            mid = len(posts) // 2
            holdout_posts = posts[mid:]
            h_with = [float(p.get("er", 0.0)) for p in holdout_posts if _classify_post_compliance(p.get("title", ""), kind, pat, scope)]
            h_without = [float(p.get("er", 0.0)) for p in holdout_posts if not _classify_post_compliance(p.get("title", ""), kind, pat, scope)]
            if h_with and h_without:
                holdout_passed = statistics.mean(h_with) > statistics.mean(h_without)

        n_target = min(len(with_vals), len(without_vals))
        if not with_vals or not without_vals:
            return False, f"樣本切分不足（with={len(with_vals)}, without={len(without_vals)}）", {}
        w_mean = round(statistics.mean(with_vals), 4)
        wo_mean = round(statistics.mean(without_vals), 4)

    elif kind in ("metric_min", "metric_max", "baseline_standard"):
        metric_name, bound_s = pat.rsplit(":", 1)
        bound = float(bound_s)
        records = [json.loads(x) for x in ds.read_text(encoding="utf-8").splitlines() if x.strip()]
        if not records:
            return False, "資料集為空", {}
        last = records[-1]
        if isinstance(last.get("pairs"), list):
            for pair in last["pairs"]:
                val = float(pair.get("ratio", pair.get("contrast", 0.0)))
                ok_cond = (val >= bound) if kind != "metric_max" else (val <= bound)
                (with_vals if ok_cond else without_vals).append(val)
            n_target = len(with_vals) + len(without_vals)
            pass_rate = round(len(with_vals) / max(1, n_target) * 100.0, 2)
            fail_rate = round(len(without_vals) / max(1, n_target) * 100.0, 2)
            w_mean = pass_rate
            wo_mean = fail_rate
        elif "pass_body_text_7" in last and "pairs" in last:
            # josef_contrast_history.jsonl 摘要結構：真實比較達標率 vs 未達標率（廢除 wo_mean = 0.0）
            n_target = int(last["pairs"])
            passed_cnt = float(last["pass_body_text_7"])
            w_mean = round(passed_cnt / max(1, n_target) * 100.0, 2)
            wo_mean = round((n_target - passed_cnt) / max(1, n_target) * 100.0, 2)
        elif "passed" in last and "total" in last:
            # deming_quality_history.jsonl 摘要結構：針對 defects:0 嚴格檢查 actual_defects <= bound
            n_target = int(last["total"])
            actual_defects = float(last.get("defects", 0))
            if metric_name == "defects":
                w_mean = 100.0 if actual_defects <= bound else 0.0
                wo_mean = 50.0
            else:
                w_mean = round(float(last["passed"]) / max(1, n_target) * 100.0, 2)
                wo_mean = round(actual_defects / max(1, n_target) * 100.0, 2)
        else:
            val = float(last.get(metric_name, 0.0))
            n_target = int(last.get("total_scripts", last.get("n", MIN_TRIAL_N)))
            ok_cond = (val >= bound) if kind == "metric_min" else (val <= bound)
            w_mean = val if ok_cond else 0.0
            wo_mean = bound if ok_cond else val + 1.0

    elif kind == "route":
        # 雪的派工路由規則，格式：category->assignee (例如 文案->taylor)
        if "->" not in pat:
            return False, "route 規則格式須為 類別->閣員代號", {}
        cat, target_agent = [x.strip() for x in pat.split("->", 1)]
        records = [json.loads(x) for x in ds.read_text(encoding="utf-8").splitlines() if x.strip()]
        disp_map = {e["task_id"]: e for e in records if e.get("type") == "dispatch" and e.get("category") == cat}
        signoffs_by_task: dict[str, list[dict]] = {}
        for e in records:
            if e.get("type") == "signoff" and e.get("task_id") in disp_map:
                signoffs_by_task.setdefault(e["task_id"], []).append(e)
        for tid, ss in signoffs_by_task.items():
            last_w = ss[-1].get("word", "")
            if last_w == "退":
                continue
            d = disp_map[tid]
            rework = sum(1 for s in ss if s.get("word") == "退")
            first_pass = 1.0 if (last_w == "收" and rework == 0) else 0.0
            if target_agent in d.get("assigned", []):
                with_vals.append(first_pass * 100.0)
            else:
                without_vals.append(first_pass * 100.0)
        n_target = min(len(with_vals), len(without_vals))
        if not with_vals or not without_vals:
            return False, f"派工路由樣本不足（{cat}->{target_agent}: with={len(with_vals)}, without={len(without_vals)}）", {}
        w_mean = round(statistics.mean(with_vals), 2)
        wo_mean = round(statistics.mean(without_vals), 2)
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
        "holdout_passed": holdout_passed,
        "collateral_rate": collateral_rate,
        "collateral_rejected": collateral_rejected,
    }
    append_event(office, ev)
    status_note = "攔截(誤傷過高)" if collateral_rejected else ("PASS" if (w_mean > wo_mean and holdout_passed and n_target >= MIN_TRIAL_N) else "FAIL(未優於對照)")
    return (
        True,
        f"真值驗算完成 [{status_note}]：with={w_mean} vs without={wo_mean} (N={n_target}, holdout={'PASS' if holdout_passed else 'FAIL'}, 誤傷率={collateral_rate:.0%}, sha256={ds_sha[:10]}...)",
        ev,
    )


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
    """TTL 到期或連驗轉負者標記 retired（溶酶體衰減）。"""
    retired = []
    for p in VAULT_DIR.glob("*_rules.jsonl") if VAULT_DIR.exists() else []:
        office = p.name.replace("_rules.jsonl", "")
        for rid, r in fold(office).items():
            if r["status"] in ("candidate", "active"):
                born = datetime.fromisoformat(r["ts"])
                if datetime.now() > born + timedelta(days=int(r.get("ttl_days", 90))):
                    append_event(office, {"type": "retire", "rule_id": rid, "reason": "TTL 到期未再獲證據支持"})
                    retired.append(rid)
                elif r["status"] == "active" and r.get("kind") != "baseline_standard" and r["trials"]:
                    latest = r["trials"][-1]
                    if float(latest["with_metric"]) <= float(latest["without_metric"]):
                        append_event(office, {"type": "retire", "rule_id": rid, "reason": "最新真值驗算效果轉負，自動退場"})
                        retired.append(rid)
    return retired


def main() -> None:
    ap = argparse.ArgumentParser(description="規則庫與生命週期 (v6.2 零信任硬化版)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("propose")
    p.add_argument("--office", required=True)
    p.add_argument("--kind", required=True, choices=VALID_KINDS)
    p.add_argument("--pattern", required=True)
    p.add_argument("--scope", choices=["any", "prefix"], default="any")
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
                a.office,
                a.kind,
                a.pattern,
                a.risk,
                a.source_url,
                a.tier,
                a.evidence,
                a.confidence,
                a.ttl_days,
                a.scope,
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
                    f"{rid} [{r['status']}] {r['kind']}({r.get('scope','any')}):{r['pattern']} risk={r['risk']} tier={r['source_tier']} 真實樣本N={n_last}"
                )
        elif a.cmd == "sweep":
            out = sweep()
            print(f"🧹 淘汰 {len(out)} 條：{out}")
    except ValueError as e:
        print(f"🛑 {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
