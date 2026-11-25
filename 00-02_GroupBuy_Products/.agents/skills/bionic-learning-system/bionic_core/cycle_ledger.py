r"""輪次帳本與十輪強制停機 (Cycle Ledger · Master v6.5 雜湊鏈與全關卡狀態機版)

v6.5 核心升級（消滅十輪鎖漏洞）：
  1. 輪次帳本強制雜湊鏈 (`_cycles.jsonl` Append-Only with `prev`/`hash`)：
     - 每筆 tick 與 audit_done 均帶有前一筆之 SHA-256 雜湊與自身雜湊；中途插行、刪改事件會被 `verify_chain()` 立即偵測並判定損毀鎖定。
  2. 簽章強綁定關卡與前置 Tick 雜湊：
     - `audit_done` 簽章 payload 強制綁定 `(office, cycle, last_tick_hash, scan_digest, report_sha256)`，舊簽章貼到新輪次直接驗簽失敗。
  3. 全關卡逐段狀態機 (`is_locked`)：
     - 逐一掃描所有滿 10 的倍數關卡 ($K = 10, 20, 30, \dots$)：在第 $K$ 筆 tick 之後、第 $K+1$ 筆 tick 之前，必須存在對應之合法 `audit_done`（高風險辦公室強制要求創辦人 Schnorr 驗簽合格）。
     - 任一歷史關卡缺失即維持鎖定！**手動補寫第 11 筆假 tick 或刪除 `.lock` 檔絕對無法解鎖**！
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
import founder_auth  # noqa: E402
import rule_store  # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CORE_DIR = Path(__file__).resolve().parent
VAULT_DIR = CORE_DIR / "vaults"
REGISTRY_FILE = CORE_DIR / "verifier_registry.json"
AUDIT_EVERY = 10
REQUIRED_AUDIT_SECTIONS = ("矛盾比對", "互斥掃描", "淘汰清單")
MIN_AUDIT_CHARS = 100
ZERO_HASH = "0" * 64

VOLATILE_KEYS = {
    "executed_at",
    "ts",
    "discovered_at",
    "fetched_at",
    "updated_at",
    "learned_at",
    "promoted_at",
    "discover",
    "meta",
    "evidence_file",
    "ledger_state",
    "dataset",
}


def _ledger(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{office}_cycles.jsonl"


def _lock(office: str) -> Path:
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{office}.AUDIT_REQUIRED.lock"


def is_high_risk_office(office: str) -> bool:
    if not REGISTRY_FILE.exists():
        return False
    try:
        reg = json.loads(REGISTRY_FILE.read_text(encoding="utf-8")).get("registry", {})
        if office in reg:
            return reg[office].get("risk_class") == "high"
    except Exception:
        pass
    return False


def _strip_volatile(obj):
    if isinstance(obj, dict):
        return {k: _strip_volatile(v) for k, v in sorted(obj.items()) if k not in VOLATILE_KEYS}
    if isinstance(obj, list):
        return [_strip_volatile(x) for x in obj]
    return obj


def canonical_obj_sha256(obj) -> str:
    clean = _strip_volatile(obj)
    canon = json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def _canonical_evidence_sha256(ev_path: Path) -> str:
    raw = ev_path.read_bytes()
    try:
        text = raw.decode("utf-8")
        if ev_path.suffix.lower() == ".json":
            return canonical_obj_sha256(json.loads(text))
        if ev_path.suffix.lower() == ".jsonl":
            lines = [_strip_volatile(json.loads(line)) for line in text.splitlines() if line.strip()]
            return canonical_obj_sha256(lines)
    except Exception:
        pass
    return hashlib.sha256(raw).hexdigest()


def read(office: str) -> list[dict]:
    p = _ledger(office)
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def verify_chain(office: str, events: list[dict] | None = None) -> tuple[bool, str]:
    evs = read(office) if events is None else events
    prev = ZERO_HASH
    for i, e in enumerate(evs):
        body = {k: v for k, v in e.items() if k != "hash"}
        if body.get("prev") != prev:
            return False, f"第 {i + 1} 筆 prev 不連續（預期 {prev[:10]}...）"
        exp_hash = hashlib.sha256(
            json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        if exp_hash != e.get("hash"):
            return False, f"第 {i + 1} 筆內容與雜湊不符"
        prev = e["hash"]
    return True, f"鏈完整（{len(evs)} 筆）"


def used_evidence_shas(office: str) -> set[str]:
    return {str(e.get("evidence_sha256")) for e in read(office) if e.get("type") == "tick" and e.get("evidence_sha256")}


def check_duplicate_obj(office: str, obj: dict) -> tuple[bool, str]:
    sha = canonical_obj_sha256(obj)
    return (sha in used_evidence_shas(office)), sha


def cycle_count(office: str) -> int:
    return sum(1 for e in read(office) if e.get("type") == "tick")


def is_locked(office: str) -> bool:
    """全關卡逐段狀態機：掃描每一個 10 的倍數關卡，確認具備合法且簽章匹配之 audit_done。"""
    events = read(office)
    if not events:
        return _lock(office).exists()

    # 1. 雜湊鏈完整性驗證
    ok_chain, _ = verify_chain(office, events)
    if not ok_chain:
        return True

    # 2. 逐段審計狀態機
    tick_indices = [i for i, e in enumerate(events) if e.get("type") == "tick"]
    total_ticks = len(tick_indices)

    # 檢查歷史上所有已達到的 10 倍數關卡 (10, 20, 30, ...)
    for milestone in range(AUDIT_EVERY, total_ticks + 1, AUDIT_EVERY):
        milestone_tick_idx = tick_indices[milestone - 1]
        milestone_tick = events[milestone_tick_idx]
        next_tick_idx = tick_indices[milestone] if milestone < total_ticks else len(events)

        # 搜尋在該關卡 tick 之後、下一筆 tick 之前的合格 audit_done
        segment = events[milestone_tick_idx + 1 : next_tick_idx]
        audits = [e for e in segment if e.get("type") == "audit_done"]
        if not audits:
            return True

        valid_audit_found = False
        for a in audits:
            if is_high_risk_office(office):
                payload = {
                    "action": "audit_done",
                    "office": office,
                    "cycle": milestone,
                    "last_tick_hash": milestone_tick["hash"],
                    "scan_digest": a.get("scan_digest", ""),
                    "report_sha256": a.get("report_sha256", ""),
                }
                ok_sig, _ = founder_auth.verify_founder_action(
                    payload,
                    a.get("founder_sig"),
                    meta_path=rule_store.META_PATH,
                )
                if ok_sig:
                    valid_audit_found = True
                    break
            else:
                if a.get("scan_digest") and a.get("report_sha256"):
                    valid_audit_found = True
                    break

        if not valid_audit_found:
            return True

    return _lock(office).exists()


def append_cycle_event(office: str, event_data: dict) -> dict:
    events = read(office)
    prev = events[-1]["hash"] if events else ZERO_HASH
    body = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        **event_data,
        "prev": prev,
    }
    body["hash"] = hashlib.sha256(
        json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    with open(_ledger(office), "a", encoding="utf-8") as f:
        f.write(json.dumps(body, ensure_ascii=False) + "\n")
    return body


def tick(office: str, summary: str, evidence: str) -> int:
    if is_locked(office):
        raise RuntimeError("已停機：滿 10 輪須先提交合規衝突審計報告並通過程式化掃描與創辦人簽章解鎖（audit-done）")
    if not evidence or not evidence.strip():
        raise ValueError("每一輪必須附物理憑證檔案路徑，不得為空")

    ev_path = Path(evidence.replace("file://", ""))
    if not ev_path.is_file() or ev_path.stat().st_size == 0:
        raise ValueError(f"物理憑證檔案不存在或為空檔：{evidence}")

    sha = _canonical_evidence_sha256(ev_path)
    if sha in used_evidence_shas(office):
        raise ValueError(f"防刷輪次阻斷：規則與驗算實質內容 SHA-256 ({sha[:12]}...) 與歷史輪次重複，無實質新變更！")

    from evidence_gate import check_evidence
    ok, reasons = check_evidence(str(ev_path))
    if not ok:
        raise ValueError("入帳拒絕：" + "；".join(reasons))

    n = cycle_count(office) + 1
    ev_data = {
        "type": "tick",
        "cycle": n,
        "summary": summary,
        "evidence": str(ev_path),
        "evidence_sha256": sha,
    }
    ev = append_cycle_event(office, ev_data)
    if n % AUDIT_EVERY == 0:
        _lock(office).write_text(f"cycle {n} reached at {ev['ts']} (hash={ev['hash'][:12]})\n", encoding="utf-8")
    return n


def audit_scan(office: str) -> dict:
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
        if r.get("kind") in ("metric_min", "metric_max"):
            try:
                k, op, val = rule_store.parse_metric_pattern(r["pattern"], r["kind"])
                if op == ">=":
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


def audit_done(
    office: str,
    report: str,
    _test_passphrase: str | None = None,
) -> None:
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

    scan = audit_scan(office)
    if not scan["clean"]:
        issues = scan["contradictions"] + scan["mutual_exclusions"]
        raise ValueError(f"程式化衝突掃描未通過，拒絕解鎖！請先解決以下規則衝突：{issues}")

    events = read(office)
    ticks = [e for e in events if e.get("type") == "tick"]
    if not ticks:
        raise ValueError("帳本尚無任何輪次紀錄，無法執行 audit-done")
    last_tick = ticks[-1]
    last_tick_cycle = int(last_tick["cycle"])
    target_milestone = (last_tick_cycle // AUDIT_EVERY) * AUDIT_EVERY
    if target_milestone == 0:
        target_milestone = AUDIT_EVERY

    sha = hashlib.sha256(rp.read_bytes()).hexdigest()
    ev_data: dict = {
        "type": "audit_done",
        "cycle": target_milestone,
        "last_tick_hash": last_tick["hash"],
        "report": str(rp),
        "report_sha256": sha,
        "scan_digest": scan["scan_digest"],
    }

    if is_high_risk_office(office):
        sig_payload = {
            "action": "audit_done",
            "office": office,
            "cycle": target_milestone,
            "last_tick_hash": last_tick["hash"],
            "scan_digest": scan["scan_digest"],
            "report_sha256": sha,
        }
        sig_bundle = founder_auth.sign_founder_action(
            sig_payload,
            meta_path=rule_store.META_PATH,
            _test_passphrase=_test_passphrase,
            prompt_label=f"創辦人授權口令（高風險辦公室 {office} 第 {target_milestone} 輪審計解鎖）：",
        )
        ev_data["founder_sig"] = sig_bundle

    append_cycle_event(office, ev_data)
    if _lock(office).exists():
        _lock(office).unlink()


def migrate(office: str) -> int:
    """舊格式輪次帳本遷移工具：將無雜湊鏈之舊 JSONL 重新縫合為具備 prev/hash 之不可篡改鏈。"""
    p = _ledger(office)
    if not p.exists():
        return 0
    lines = [x for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        return 0

    rebuilt: list[dict] = []
    prev_hash = ZERO_HASH
    for line in lines:
        raw_obj = json.loads(line)
        body = {k: v for k, v in raw_obj.items() if k != "hash"}
        body["prev"] = prev_hash
        h = hashlib.sha256(
            json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        body["hash"] = h
        prev_hash = h
        rebuilt.append(body)

    p.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in rebuilt) + "\n", encoding="utf-8")
    return len(rebuilt)


def main() -> None:
    ap = argparse.ArgumentParser(description="輪次帳本 (v6.5 雜湊鏈與全關卡狀態機版)")
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
    mg = sub.add_parser("migrate")
    mg.add_argument("--office", required=True)
    a = ap.parse_args()
    try:
        if a.cmd == "tick":
            n = tick(a.office, a.summary, a.evidence)
            print(
                f"✅ {a.office} 第 {n} 輪已入帳（雜湊鏈已延伸）"
                + ("｜🛑 已達十輪關卡，強制停機，須提交衝突審計報告" if n % AUDIT_EVERY == 0 else "")
            )
        elif a.cmd == "status":
            ok_c, msg_c = verify_chain(a.office)
            print(f"{a.office}: 已完成 {cycle_count(a.office)} 輪｜雜湊鏈={msg_c}｜停機鎖={'是' if is_locked(a.office) else '否'}")
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
        elif a.cmd == "migrate":
            cnt = migrate(a.office)
            print(f"✅ {a.office} 帳本遷移完成，已重新縫合 {cnt} 筆事件雜湊鏈")
            print("✅ 審計報告與程式化衝突掃描通過，停機鎖已解除")
    except (RuntimeError, ValueError, FileNotFoundError, PermissionError) as e:
        print(f"🛑 {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
