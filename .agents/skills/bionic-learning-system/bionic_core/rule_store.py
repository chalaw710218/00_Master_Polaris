"""萬用規則庫與生命週期狀態機 (Universal Rule Store · Master v6.5 嚴格快照與反盲簽版)

v6.5 核心升級（外部紅隊審計全面硬化）：
  1. 快照存證與 Trial 強制重算（消除偽造繞過）：
     - `evaluate_rule()` 驗算時，強制將標準資料集複製至不可篡改之快照目錄 `vaults/snapshots/{dataset_sha256}.jsonl`。
     - `fold()` 處理 `trial` 時，**強制要求對應之快照檔存在且 SHA-256 完全吻合**；快照缺失或雜湊不符一律打入 `tampered_rejected`，並逐筆現場重算核驗指標，徹底杜絕手寫假 `trial` 繞過！
  2. 規則狀態機防重放 (Anti-Replay)：
     - `fold()` 處理 `promote` 事件時，**嚴格檢查 `r["status"] == "candidate"`**！若規則已被 `retire` 或 `tampered_rejected`，複製貼上舊已簽事件直接打入 `tampered_rejected`。
  3. 反盲簽與公鑰指紋校驗 (Anti-Blind-Signing)：
     - 高風險規則轉正時，於真實終端機完整展示該規則之全量數值、證據與留出驗證結果，並於簽章 payload 強綁定 `(office, rule_id, kind, pattern, trial_sha256)`。
  4. 留出驗證 (Holdout Split) 雙組門檻提升：
     - 文字規則與路由規則之後半段留出集，**強制要求遵守組與對照組每組皆須 `>= 3` 筆**（`len(h_with) >= 3 and len(h_without) >= 3`），否則 `holdout_passed` 維持 `False` 拒絕轉正！
  5. 預覽與寫入解耦 (`preview_evaluation`)：
     - 提供無副作用之指標試算，供調度器在確認輪次無重複後才正式寫入帳本與快照。
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import founder_auth  # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CORE_DIR = Path(__file__).resolve().parent
ROOT_DIR = CORE_DIR.parent.parent.parent.parent
VAULT_DIR = CORE_DIR / "vaults"
SNAPSHOTS_DIR = VAULT_DIR / "snapshots"
REGISTRY_FILE = CORE_DIR / "verifier_registry.json"
META_PATH: Path | None = None  # None 時使用 founder_auth.DEFAULT_META_PATH
HIGH_RISK = "high"
MIN_TRIAL_N = 3
MIN_HOLDOUT_GROUP_N = 3
MAX_COLLATERAL_RATE = 0.35
ZERO_HASH = "0" * 64

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


def resolve_default_dataset(office: str) -> Path | None:
    if not REGISTRY_FILE.exists():
        return None
    try:
        reg = json.loads(REGISTRY_FILE.read_text(encoding="utf-8")).get("registry", {})
        rel = reg.get(office, {}).get("dataset_path")
        if rel:
            return ROOT_DIR / rel
    except Exception:
        pass
    return None


def _path(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{office}_rules.jsonl"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canon(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _hash_body(body: dict) -> str:
    return hashlib.sha256(_canon(body).encode("utf-8")).hexdigest()


def parse_metric_pattern(pat: str, kind: str) -> tuple[str, str, float]:
    if ">=" in pat:
        k, v = pat.split(">=", 1)
        return k.strip(), ">=", float(v)
    if "<=" in pat:
        k, v = pat.split("<=", 1)
        return k.strip(), "<=", float(v)
    if ":" in pat:
        k, v = pat.rsplit(":", 1)
        op = "<=" if kind == "metric_max" else ">="
        return k.strip(), op, float(v)
    raise ValueError(f"數值規則格式錯誤（須為 key>=val, key<=val 或 key:val）：{pat}")


def append_event(office: str, event: dict) -> dict:
    p = _path(office)
    prev = ZERO_HASH
    if p.exists():
        lines = [x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
        if lines:
            last_ev = json.loads(lines[-1])
            prev = last_ev.get("hash", _hash_body({k: v for k, v in last_ev.items() if k != "hash"}))
    body = {"ts": _now(), "office": office, **event, "prev": prev}
    body["hash"] = _hash_body(body)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(body, ensure_ascii=False) + "\n")
    return body


def _load_standard_text_samples(dataset: Path) -> list[dict]:
    records: dict[str, dict] = {}
    for idx, line in enumerate(dataset.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        obj = json.loads(line)
        items = obj.get("samples") if isinstance(obj.get("samples"), list) else [obj]
        batch_ts = str(obj.get("ts", ""))
        for sub_i, row in enumerate(items):
            if not isinstance(row, dict) or "text" not in row or "metric" not in row:
                continue
            rid = str(row.get("id", f"{idx}-{sub_i}"))
            rts = str(row.get("ts", batch_ts or f"{idx:06d}"))
            prev = records.get(rid)
            if prev is None or rts >= prev["ts"]:
                records[rid] = {
                    "id": rid,
                    "text": str(row["text"]),
                    "metric": float(row["metric"]),
                    "ts": rts,
                }
    out = list(records.values())
    out.sort(key=lambda x: (x["ts"], x["id"]))
    return out


def _match_phrase(title: str, pat: str, scope: str) -> bool:
    if scope == "prefix":
        lines = [ln.strip() for ln in title.splitlines() if ln.strip()]
        head = " ".join(lines[:2]) if lines else title[:30]
        return head.startswith(pat) or (pat in head[:25])
    return pat in title


def _classify_post_compliance(title: str, kind: str, pat: str, scope: str = "any") -> bool:
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


def _compute_metrics_from_dataset(r: dict, ds: Path) -> tuple[bool, str, dict]:
    if not ds or not ds.is_file():
        return False, f"找不到真實資料集檔案：{ds}", {}

    ds_sha = _sha256(ds)
    kind = r["kind"]
    pat = r["pattern"]
    scope = r.get("scope", "any")

    with_vals: list[float] = []
    without_vals: list[float] = []
    holdout_passed = False
    collateral_rate = 0.0
    collateral_rejected = False

    if kind in ("forbid_phrase", "prefer_phrase", "max_count", "regex_forbid"):
        samples = _load_standard_text_samples(ds)
        if not samples:
            return False, "標準文字成效樣本集為空", {}

        all_metrics = [float(p["metric"]) for p in samples]
        med_val = statistics.median(all_metrics) if all_metrics else 0.0
        good_samples = [p for p in samples if float(p["metric"]) > med_val]
        killed_good = 0

        for p in samples:
            text_val = p["text"]
            val = float(p["metric"])
            compliant = _classify_post_compliance(text_val, kind, pat, scope)
            if compliant:
                with_vals.append(val)
            else:
                without_vals.append(val)
                if val > med_val:
                    killed_good += 1

        if kind in ("forbid_phrase", "regex_forbid") and len(good_samples) >= 3:
            collateral_rate = round(killed_good / len(good_samples), 4)
            if collateral_rate > MAX_COLLATERAL_RATE:
                collateral_rejected = True

        # 時序留出集驗證 (Holdout Split)：前半段 Discovery，後半段 Holdout
        # 【v6.5 鐵律】：後半段留出集雙組皆須 >= 3 筆，不再 1 筆就算數
        if len(samples) >= 8:
            mid = len(samples) // 2
            holdout_samples = samples[mid:]
            h_with = [float(p["metric"]) for p in holdout_samples if _classify_post_compliance(p["text"], kind, pat, scope)]
            h_without = [float(p["metric"]) for p in holdout_samples if not _classify_post_compliance(p["text"], kind, pat, scope)]
            if len(h_with) >= MIN_HOLDOUT_GROUP_N and len(h_without) >= MIN_HOLDOUT_GROUP_N:
                holdout_passed = statistics.mean(h_with) > statistics.mean(h_without)

        n_target = min(len(with_vals), len(without_vals))
        if not with_vals or not without_vals:
            return False, f"樣本切分不足（with={len(with_vals)}, without={len(without_vals)}）", {}
        w_mean = round(statistics.mean(with_vals), 4)
        wo_mean = round(statistics.mean(without_vals), 4)

    elif kind in ("metric_min", "metric_max", "baseline_standard"):
        metric_name, op, bound = parse_metric_pattern(pat, kind)
        records = [json.loads(x) for x in ds.read_text(encoding="utf-8").splitlines() if x.strip()]
        if not records:
            return False, "數值樣本集為空", {}
        last = records[-1]

        if isinstance(last.get("samples"), list) and last["samples"]:
            for s in last["samples"]:
                if metric_name not in s:
                    continue
                val = float(s[metric_name])
                is_ok = (val >= bound) if op == ">=" else (val <= bound)
                (with_vals if is_ok else without_vals).append(val)
            n_target = len(with_vals) + len(without_vals)
            if n_target == 0:
                return False, f"樣本陣列中找不到指標 `{metric_name}`", {}
            w_mean = round(len(with_vals) / n_target * 100.0, 2)
            wo_mean = round(len(without_vals) / n_target * 100.0, 2)
            holdout_passed = True
        elif "n" in last and "compliant" in last:
            n_target = int(last["n"])
            comp_cnt = float(last["compliant"])
            metrics_map = last.get("metrics", last)
            if metric_name in metrics_map:
                val = float(metrics_map[metric_name])
                is_ok = (val >= bound) if op == ">=" else (val <= bound)
                if not is_ok and kind != "baseline_standard":
                    w_mean = 0.0
                    wo_mean = 100.0
                else:
                    w_mean = round(comp_cnt / max(1, n_target) * 100.0, 2)
                    wo_mean = round((n_target - comp_cnt) / max(1, n_target) * 100.0, 2)
            else:
                w_mean = round(comp_cnt / max(1, n_target) * 100.0, 2)
                wo_mean = round((n_target - comp_cnt) / max(1, n_target) * 100.0, 2)
            holdout_passed = True
        else:
            metrics_map = last.get("metrics", last)
            if metric_name not in metrics_map:
                return False, f"標準數值列缺少指標 `{metric_name}`", {}
            val = float(metrics_map[metric_name])
            n_target = int(last.get("n", len(records) if len(records) >= MIN_TRIAL_N else MIN_TRIAL_N))
            is_ok = (val >= bound) if op == ">=" else (val <= bound)
            w_mean = 100.0 if is_ok else 0.0
            wo_mean = 0.0 if is_ok else 100.0
            holdout_passed = True

    elif kind == "route":
        if "->" not in pat:
            return False, "route 規則格式須為 類別->閣員代號", {}
        cat, target_agent = [x.strip() for x in pat.split("->", 1)]
        raw_lines = [json.loads(x) for x in ds.read_text(encoding="utf-8").splitlines() if x.strip()]
        if not raw_lines:
            return False, "路由樣本檔為空", {}
        envelope = raw_lines[-1]
        if envelope.get("kind") != "verified_route_samples":
            return False, "route 驗算拒絕讀取未驗簽之原始帳本！須由創辦人執行 dispatch.py export-verified 匯出", {}

        samples = envelope.get("samples", [])
        expected_sha = hashlib.sha256(_canon(samples).encode("utf-8")).hexdigest()
        if expected_sha != envelope.get("samples_sha256"):
            return False, "路由樣本列雜湊與簽章宣告不符（遭竄改）", {}
        ok_sig, msg_sig = founder_auth.verify_founder_action(
            {"action": "route_samples", "samples_sha256": expected_sha, "count": len(samples)},
            envelope.get("founder_sig"),
            meta_path=META_PATH,
        )
        if not ok_sig:
            return False, f"路由樣本列創辦人簽章驗證失敗：{msg_sig}", {}

        cat_samples = [s for s in samples if s.get("category") == cat]
        for s in cat_samples:
            val = float(s.get("metric", 0.0))
            if target_agent in s.get("assigned", []):
                with_vals.append(val)
            else:
                without_vals.append(val)
        n_target = min(len(with_vals), len(without_vals))
        if not with_vals or not without_vals:
            return False, f"已驗簽派工路由樣本不足（{cat}->{target_agent}: 主組={len(with_vals)}, 對照組={len(without_vals)}）", {}
        w_mean = round(statistics.mean(with_vals), 2)
        wo_mean = round(statistics.mean(without_vals), 2)
        if len(cat_samples) >= 8:
            mid = len(cat_samples) // 2
            h_samples = cat_samples[mid:]
            hw = [float(s["metric"]) for s in h_samples if target_agent in s.get("assigned", [])]
            hwo = [float(s["metric"]) for s in h_samples if target_agent not in s.get("assigned", [])]
            holdout_passed = bool(len(hw) >= MIN_HOLDOUT_GROUP_N and len(hwo) >= MIN_HOLDOUT_GROUP_N and statistics.mean(hw) > statistics.mean(hwo))
        else:
            holdout_passed = False
    else:
        return False, f"不支援的規則型態：{kind}", {}

    ev = {
        "type": "trial",
        "rule_id": r["rule_id"],
        "with_metric": w_mean,
        "without_metric": wo_mean,
        "n": n_target,
        "dataset_sha256": ds_sha,
        "holdout_passed": holdout_passed,
        "collateral_rate": collateral_rate,
        "collateral_rejected": collateral_rejected,
    }
    return True, "OK", ev


def _ensure_snapshot(ds_path: Path, ds_sha: str) -> Path:
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    snap_file = SNAPSHOTS_DIR / f"{ds_sha}.jsonl"
    if not snap_file.exists():
        snap_file.write_bytes(ds_path.read_bytes())
    return snap_file


def preview_evaluation(office: str, rule_id: str, dataset_path: Path | None = None) -> tuple[bool, str, dict]:
    """無副作用純指標試算（不寫入規則帳本、不存快照）。"""
    rules = fold(office)
    r = rules.get(rule_id)
    if not r:
        return False, "找不到規則", {}
    ds = Path(dataset_path) if dataset_path else resolve_default_dataset(office)
    return _compute_metrics_from_dataset(r, ds)  # type: ignore[arg-type]


def evaluate_rule(office: str, rule_id: str, dataset_path: Path | None = None) -> tuple[bool, str, dict]:
    """萬用真值驗算器：計算指標、複製不可篡改快照、寫入雜湊鏈帳本。"""
    rules = fold(office)
    r = rules.get(rule_id)
    if not r:
        return False, "找不到規則", {}

    ds = Path(dataset_path) if dataset_path else resolve_default_dataset(office)
    ok_calc, why_calc, ev = _compute_metrics_from_dataset(r, ds)  # type: ignore[arg-type]
    if not ok_calc:
        return False, why_calc, {}

    # 【v6.5 核心】：將真實資料集寫入快照存證目錄，供 fold() 重算鎖定
    _ensure_snapshot(ds, ev["dataset_sha256"])  # type: ignore[arg-type]

    append_event(office, ev)
    w_mean = ev["with_metric"]
    wo_mean = ev["without_metric"]
    n_target = ev["n"]
    holdout_passed = ev["holdout_passed"]
    collateral_rejected = ev["collateral_rejected"]
    collateral_rate = ev["collateral_rate"]
    ds_sha = ev["dataset_sha256"]

    status_note = (
        "攔截(誤傷過高)"
        if collateral_rejected
        else ("PASS" if (w_mean > wo_mean and holdout_passed and n_target >= MIN_TRIAL_N) else "FAIL(未達轉正門檻)")
    )
    return (
        True,
        f"真值驗算完成 [{status_note}]：with={w_mean} vs without={wo_mean} (N={n_target}, holdout={'PASS' if holdout_passed else 'FAIL'}, 誤傷率={collateral_rate:.0%}, sha256={ds_sha[:10]}...)",
        ev,
    )


def trial_ok(rule: dict) -> tuple[bool, str]:
    if rule.get("kind") == "baseline_standard":
        if not rule["trials"]:
            return False, "合規基準標準尚無基線盤點紀錄"
        latest = rule["trials"][-1]
        return True, f"合規基準標準已盤點綁定（基線達標率={latest['with_metric']}%，N={latest['n']}，簽章={latest['dataset_sha256'][:10]}）"

    if not rule["trials"]:
        return False, "尚無通過真值簽章與快照重算核驗的 evaluate 紀錄"
    latest = rule["trials"][-1]
    n = int(latest["n"])
    w = float(latest["with_metric"])
    wo = float(latest["without_metric"])
    if latest.get("collateral_rejected"):
        return False, f"高成效樣本誤傷率過高 ({latest.get('collateral_rate', 0):.0%} > {MAX_COLLATERAL_RATE:.0%})，拒絕轉正"
    if not latest.get("holdout_passed", False):
        return False, f"留出驗證集 (Holdout Split) 雙組未達各 {MIN_HOLDOUT_GROUP_N} 筆或未優於對照組，拒絕轉正"
    if n < MIN_TRIAL_N:
        return False, f"真實樣本數 {n} < 最低門檻 {MIN_TRIAL_N}"
    if w <= wo:
        return False, f"遵守規則指標({w:.2f}) 未優於對照組({wo:.2f})"
    return True, f"遵守規則({w:.2f}) > 對照組({wo:.2f})，真實樣本 N={n}，簽章={latest['dataset_sha256'][:10]}"


def build_promote_payload(office: str, r: dict) -> dict:
    """構造高風險轉正簽章與反盲簽審批畫面共用之完整 Payload（防盲簽、防欄位缺失為 None）。"""
    latest_t = r["trials"][-1] if r.get("trials") else {}
    return {
        "action": "promote",
        "office": office,
        "rule_id": r.get("rule_id", ""),
        "kind": r.get("kind", ""),
        "pattern": r.get("pattern", ""),
        "scope": r.get("scope", "any"),
        "with_metric": float(latest_t.get("with_metric", 0.0)),
        "without_metric": float(latest_t.get("without_metric", 0.0)),
        "n": int(latest_t.get("n", 0)),
        "holdout_passed": bool(latest_t.get("holdout_passed", False)),
        "trial_sha256": str(latest_t.get("dataset_sha256", "")),
        "evidence": str(r.get("evidence", "")),
    }


def fold(office: str) -> dict[str, dict]:
    """將事件折疊為各規則最新狀態（雜湊鏈驗證 + 快照強制重算 + 狀態機防舊簽重放 + 公鑰驗簽）。"""
    rules: dict[str, dict] = {}
    p = _path(office)
    if not p.exists():
        return rules

    prev_hash = ZERO_HASH
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        ev = json.loads(line)
        rid = ev.get("rule_id")
        t = ev.get("type")

        # 1. 驗證 JSONL 雜湊鏈完整性
        body = {k: v for k, v in ev.items() if k != "hash"}
        expected_hash = _hash_body(body)
        chain_valid = (body.get("prev") == prev_hash) and (ev.get("hash") == expected_hash)
        if chain_valid:
            prev_hash = ev["hash"]
        else:
            if rid and rid in rules:
                rules[rid]["status"] = "tampered_rejected"
                rules[rid]["tampered_reason"] = "規則帳本雜湊鏈斷裂或事件未經合法雜湊簽章"
            continue

        if t == "propose":
            rules[rid] = {
                "scope": "any",
                **ev,
                "status": "candidate",
                "trials": [],
            }
        elif rid in rules:
            r = rules[rid]
            if r["status"] == "tampered_rejected":
                continue
            if t == "trial":
                ds_sha = ev.get("dataset_sha256", "")
                if not ds_sha or len(str(ds_sha)) != 64:
                    r["status"] = "tampered_rejected"
                    r["tampered_reason"] = "Trial 缺少合法 64 碼 dataset_sha256"
                    continue

                # 【v6.5 核心】：強制重算！必須從 snapshots/ 讀取對應快照，若快照不存在或雜湊不符直接判 tampered
                snap_file = SNAPSHOTS_DIR / f"{ds_sha}.jsonl"
                if not snap_file.is_file():
                    r["status"] = "tampered_rejected"
                    r["tampered_reason"] = f"找不到不可篡改之資料集快照 (snapshots/{ds_sha[:16]}.jsonl)，疑似偽造 trial"
                    continue
                if _sha256(snap_file) != ds_sha:
                    r["status"] = "tampered_rejected"
                    r["tampered_reason"] = f"資料集快照檔案雜湊遭篡改 (預期 {ds_sha})"
                    continue

                # 現場重新執行純數學驗算
                ok_re, why_re, calc_ev = _compute_metrics_from_dataset(r, snap_file)
                if not ok_re:
                    r["status"] = "tampered_rejected"
                    r["tampered_reason"] = f"Trial 重算未通過：{why_re}"
                    continue
                if (
                    float(calc_ev["with_metric"]) != float(ev.get("with_metric", -999))
                    or float(calc_ev["without_metric"]) != float(ev.get("without_metric", -999))
                    or int(calc_ev["n"]) != int(ev.get("n", -1))
                    or bool(calc_ev["holdout_passed"]) != bool(ev.get("holdout_passed", False))
                    or bool(calc_ev["collateral_rejected"]) != bool(ev.get("collateral_rejected", True))
                ):
                    r["status"] = "tampered_rejected"
                    r["tampered_reason"] = "Trial 指標數值與真實資料集重算結果不符（手填偽造被抓）"
                    continue

                r["trials"].append({
                    k: ev[k]
                    for k in (
                        "with_metric",
                        "without_metric",
                        "n",
                        "dataset_sha256",
                        "holdout_passed",
                        "collateral_rate",
                        "collateral_rejected",
                        "ts",
                    )
                    if k in ev
                })

            elif t == "promote":
                # 【v6.5 核心】：狀態機防重放！只有當前狀態為 candidate 時才准 promote；已淘汰規則遭重貼舊簽章維持 retired
                if r["status"] != "candidate":
                    if r["status"] == "retired":
                        r["tampered_attempt"] = "已淘汰規則遭重貼 promote 簽章攻擊，維持 retired"
                        continue
                    r["status"] = "tampered_rejected"
                    r["tampered_reason"] = f"規則當前狀態為 {r['status']}（非 candidate），禁止重放轉正事件"
                    continue

                ok_t, why_t = trial_ok(r)
                if not ok_t:
                    r["status"] = "tampered_rejected"
                    r["tampered_reason"] = f"未通過驗算即偽造轉正 ({why_t})"
                    continue

                if r.get("risk") == HIGH_RISK:
                    sig_payload = build_promote_payload(office, r)
                    ok_sig, why_sig = founder_auth.verify_founder_action(
                        sig_payload,
                        ev.get("founder_sig"),
                        meta_path=META_PATH,
                    )
                    if not ok_sig:
                        r["status"] = "tampered_rejected"
                        r["tampered_reason"] = f"高風險規則未通過創辦人密碼學驗簽：{why_sig}"
                        continue

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


def promote(
    office: str,
    rule_id: str,
    _test_passphrase: str | None = None,
) -> tuple[bool, str]:
    rules = fold(office)
    r = rules.get(rule_id)
    if not r:
        return False, "找不到規則"
    if r["status"] != "candidate":
        return False, f"狀態為 {r['status']}，只有 candidate 可轉正"
    ok, why = trial_ok(r)
    if not ok:
        return False, why

    ev_body: dict = {"type": "promote", "rule_id": rule_id}
    if r["risk"] == HIGH_RISK:
        sig_payload = build_promote_payload(office, r)
        try:
            sig_bundle = founder_auth.sign_founder_action(
                sig_payload,
                meta_path=META_PATH,
                _test_passphrase=_test_passphrase,
                prompt_label=f"創辦人授權口令（核准高風險規則 {office}/{rule_id} 轉正）：",
            )
        except (PermissionError, ValueError) as e:
            return False, f"高風險規則轉正遭拒：{e}"
        ev_body["founder_sig"] = sig_bundle

    append_event(office, ev_body)
    return True, why


def sweep() -> list[str]:
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
    ap = argparse.ArgumentParser(description="萬用規則庫與生命週期 (v6.5 嚴格快照與反盲簽版)")
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

    ev_p = sub.add_parser("evaluate", help="由標準資料集自動驗算指標並建立快照（禁止手動填數字）")
    ev_p.add_argument("--office", required=True)
    ev_p.add_argument("--rule-id", required=True)
    ev_p.add_argument("--dataset", help="選填：指定標準資料集檔案路徑")

    pr = sub.add_parser("promote", help="將候選規則轉正（高風險規則將展示反盲簽明細並要求創辦人口令簽章）")
    pr.add_argument("--office", required=True)
    pr.add_argument("--rule-id", required=True)

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
            ok, why = promote(a.office, a.rule_id)
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
    except (ValueError, PermissionError) as e:
        print(f"🛑 {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
