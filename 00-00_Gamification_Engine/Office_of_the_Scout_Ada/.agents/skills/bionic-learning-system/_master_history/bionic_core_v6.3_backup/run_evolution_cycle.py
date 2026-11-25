"""萬用單一閉環總控調度器 (Universal Evolution Cycle Runner · Master v6.3 萬用解耦版)

v6.3 萬用解耦憲則（董事長親定）：
  • 本調度器屬於母版 `bionic_core`，100% 角色無關（Role-Agnostic）！
  • 內部不寫死任何單一閣員（無 `_sync_kage`, `_sync_taylor` 等硬編碼函數）。
  • 執行時動態讀取 `verifier_registry.json` 中各子版登記的 `adapter_script`：
    1. 呼叫子版專屬轉接器 (`adapter_script`) 取得該子版依其專業特性提名的候選規則 (`proposals`)。
    2. 交由母版萬用狀態機 `rule_store.propose()` -> `rule_store.evaluate_rule()` -> `rule_store.promote()` -> `rule_store.sweep()` 執行零信任驗算。
    3. 寫入周期證據快照並由 `cycle_ledger.tick()` 驗算去時間戳實質 SHA-256 入帳。

用法：
  python run_evolution_cycle.py --office <子版代號> [--with-discover]
  python run_evolution_cycle.py --all-ready
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent.parent.parent.parent
REGISTRY_FILE = BASE_DIR / "verifier_registry.json"
sys.path.insert(0, str(BASE_DIR))

import cycle_ledger  # noqa: E402
import perceive_web  # noqa: E402
import rule_store  # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_registered_adapters() -> dict[str, dict]:
    if not REGISTRY_FILE.exists():
        return {}
    reg = json.loads(REGISTRY_FILE.read_text(encoding="utf-8")).get("registry", {})
    return {k: v for k, v in reg.items() if v.get("adapter_script")}


def invoke_child_adapter(office: str, adapter_rel_path: str) -> tuple[list[str], dict]:
    """呼叫子版專屬的特化轉接器，將其輸出的候選規則送入母版 rule_store.propose。"""
    script = ROOT_DIR / adapter_rel_path
    if not script.is_file():
        raise FileNotFoundError(f"找不到子版 '{office}' 登記之特化轉接器：{script}")
    res = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )
    if res.returncode != 0:
        raise RuntimeError(f"子版轉接器執行失敗 ({script.name}, exit={res.returncode}):\n{res.stderr or res.stdout}")
    try:
        payload = json.loads(res.stdout.strip().splitlines()[-1])
    except Exception as e:
        raise RuntimeError(f"子版轉接器輸出非合法 JSON ({script.name}): {e}\nOutput: {res.stdout}") from e

    proposed_ids: list[str] = []
    for item in payload.get("proposals", []):
        rid = rule_store.propose(
            office=office,
            kind=item["kind"],
            pattern=item["pattern"],
            risk=item.get("risk", "low"),
            source_url=item.get("source_url", "adapter"),
            tier=item.get("tier", "A"),
            evidence=item.get("evidence", ""),
            confidence=float(item.get("confidence", 0.5)),
            ttl_days=int(item.get("ttl_days", 90)),
            scope=item.get("scope", "any"),
        )
        proposed_ids.append(rid)
    return proposed_ids, payload.get("meta", {})


def run_cycle(office: str, with_discover: bool = False) -> dict:
    if cycle_ledger.is_locked(office):
        raise RuntimeError(f"🛑 子版 '{office}' 目前處於十輪停機鎖定狀態！請先完成衝突審計報告並呼叫 cycle_ledger.py audit-done。")

    adapters = load_registered_adapters()
    if office not in adapters:
        raise ValueError(f"子版 '{office}' 尚未在 verifier_registry.json 註冊 adapter_script（已註冊：{list(adapters.keys())}）")

    discover_res = None
    if with_discover:
        discover_res = perceive_web.discover(office)

    proposed_ids, meta = invoke_child_adapter(office, adapters[office]["adapter_script"])
    eval_results = []
    promoted_ids = []

    for rid in proposed_ids:
        ok_eval, msg_eval, _ = rule_store.evaluate_rule(office, rid)
        eval_results.append({"rule_id": rid, "ok": ok_eval, "message": msg_eval})
        if ok_eval:
            r_state = rule_store.fold(office).get(rid, {})
            if r_state.get("status") == "candidate" and r_state.get("risk") == "low":
                ok_prom, _ = rule_store.promote(office, rid, founder_approved=False)
                if ok_prom:
                    promoted_ids.append(rid)

    retired_ids = rule_store.sweep()

    evidence_dir = BASE_DIR / "vaults" / "cycle_evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    ts_slug = datetime.now().strftime("%Y%m%dT%H%M%S_%f")
    evidence_path = evidence_dir / f"{office}_cycle_{ts_slug}.json"
    active_now = [r["rule_id"] for r in rule_store.fold(office).values() if r["status"] == "active"]
    cycle_snapshot = {
        "office": office,
        "executed_at": datetime.now().isoformat(timespec="microseconds"),
        "meta": meta,
        "discover": discover_res,
        "proposed_or_verified_rules": proposed_ids,
        "evaluations": eval_results,
        "newly_promoted": promoted_ids,
        "active_rules": active_now,
        "retired_by_sweep": retired_ids,
    }
    evidence_path.write_text(json.dumps(cycle_snapshot, ensure_ascii=False, indent=2), encoding="utf-8")

    cycle_num = cycle_ledger.tick(
        office,
        f"run_evolution_cycle v6.3: proposed={len(proposed_ids)}, promoted={len(promoted_ids)}, active={len(active_now)}",
        str(evidence_path),
    )
    history = cycle_ledger.read(office)
    cycle_snapshot["evidence_file"] = str(evidence_path)
    cycle_snapshot["ledger_state"] = {
        "cycle": cycle_num,
        "locked_for_audit": cycle_ledger.is_locked(office),
        "evidence_sha256": history[-1]["evidence_sha256"] if history else "",
    }
    return cycle_snapshot


def main() -> None:
    adapters = load_registered_adapters()
    ap = argparse.ArgumentParser(description="萬用單一閉環總控調度器 (v6.3 萬用解耦版)")
    ap.add_argument("--office", choices=list(adapters.keys()), help="執行單一子版閉環")
    ap.add_argument("--all-ready", action="store_true", help="依序執行所有已註冊 adapter_script 且低風險就緒之子版")
    ap.add_argument("--with-discover", action="store_true", help="同時啟動 perceive_web 主動探索")
    a = ap.parse_args()

    targets = [k for k, v in adapters.items() if v.get("risk_class") == "low"] if a.all_ready else ([a.office] if a.office else [])
    if not targets:
        ap.error("請指定 --office <子版代號> 或 --all-ready")

    all_out = {}
    for off in targets:
        try:
            all_out[off] = run_cycle(off, with_discover=a.with_discover)
        except Exception as e:
            print(f"🛑 [{off}] 閉環執行失敗：{e}")
            sys.exit(1)

    print(json.dumps(all_out if len(targets) > 1 else all_out[targets[0]], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
