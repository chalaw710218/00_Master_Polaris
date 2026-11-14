"""單一閉環總控調度器 (Run Evolution Cycle · Master v6.1 第十一章 ⑦)

核心使命：
徹底消滅「母版 bionic_core 與 11 首長學習引擎互不連通」的斷路問題！
單一命令串聯完整自進化閉環：
  1. 檢查 `cycle_ledger.is_locked(office)`（若滿 10 輪未審計則硬阻斷）。
  2. （選用 `--with-discover`）呼叫 `perceive_web.discover(office)` 主動巡檢 A/B 級探索源。
  3. 執行或同步該首長之真實學習引擎狀態檔，萃取具統計顯著性之發現並 `propose` 入 `rule_store`。
  4. 呼叫 `rule_store.evaluate_rule()` 直接對真實資料集計算 `with_metric` / `without_metric` 與 `dataset_sha256`（零人工填分）。
  5. 若通過真值門檻且為 `low` 風險，自動呼叫 `rule_store.promote()` 升為 `active`（立即生效於 `enforce.py` 閘門）。
  6. 執行 `rule_store.sweep()` 溶酶體 TTL 代謝。
  7. 產出當輪具名不可篡改之周期證據快照並呼叫 `cycle_ledger.tick()` 驗算 SHA-256 入帳。

用法：
  python run_evolution_cycle.py --office kage
  python run_evolution_cycle.py --office taylor
  python run_evolution_cycle.py --office josef
  python run_evolution_cycle.py --office deming
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
SKILLS_DIR = BASE_DIR.parent.parent
sys.path.insert(0, str(BASE_DIR))

import cycle_ledger  # noqa: E402
import perceive_web  # noqa: E402
import rule_store  # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def _sync_kage() -> tuple[list[str], dict]:
    state_file = SKILLS_DIR / "atom-kage-synaptic-metabolic-learner" / "vaults" / "kage_synaptic_state.json"
    script = SKILLS_DIR / "atom-kage-synaptic-metabolic-learner" / "scripts" / "kage_real_learning.py"
    if script.exists():
        subprocess.run([sys.executable, str(script), "--learn"], capture_output=True, timeout=60)
    if not state_file.exists():
        raise FileNotFoundError(f"找不到影存摺狀態檔：{state_file}")
    data = json.loads(state_file.read_text(encoding="utf-8"))
    median_er = float(data.get("account_median_er", 2.0))
    proposed_ids: list[str] = []
    for hook, stat in data.get("hook_weights", {}).items():
        if stat.get("confidence") != "OK":
            continue
        avg_er = float(stat.get("avg_er", 0.0))
        n = int(stat.get("n", 0))
        if avg_er < median_er * 0.7:
            rid = rule_store.propose(
                office="kage",
                kind="forbid_phrase",
                pattern=hook,
                risk="low",
                source_url=str(data.get("source", "insights_history.jsonl")),
                tier="A",
                evidence=f"真實 Threads 快照 N={n}，開頭『{hook}』平均 ER={avg_er}% < 帳號中位數 {median_er}%*0.7",
                confidence=0.85,
            )
            proposed_ids.append(rid)
        elif avg_er >= median_er * 1.3:
            rid = rule_store.propose(
                office="kage",
                kind="prefer_phrase",
                pattern=hook,
                risk="low",
                source_url=str(data.get("source", "insights_history.jsonl")),
                tier="A",
                evidence=f"真實 Threads 快照 N={n}，開頭『{hook}』平均 ER={avg_er}% >= 帳號中位數 {median_er}%*1.3",
                confidence=0.85,
            )
            proposed_ids.append(rid)
    return proposed_ids, {"state_file": str(state_file), "learned_at": data.get("learned_at"), "median_er": median_er}


def _sync_taylor() -> tuple[list[str], dict]:
    state_file = SKILLS_DIR / "atom-taylor-marketing-psychology-learner" / "vaults" / "taylor_marketing_state.json"
    script = SKILLS_DIR / "atom-taylor-marketing-psychology-learner" / "scripts" / "taylor_real_learning.py"
    if script.exists():
        subprocess.run([sys.executable, str(script), "--learn"], capture_output=True, timeout=60)
    if not state_file.exists():
        raise FileNotFoundError(f"找不到泰勒絲狀態檔：{state_file}")
    data = json.loads(state_file.read_text(encoding="utf-8"))
    proposed_ids: list[str] = []
    feats = data.get("feature_results", {})

    q_stat = feats.get("好奇提問句", {})
    if q_stat.get("信心") == "OK" and q_stat.get("互動率倍數(有/無)", 1.0) < 0.75:
        ratio = q_stat["互動率倍數(有/無)"]
        rid = rule_store.propose(
            office="taylor",
            kind="regex_forbid",
            pattern=r"^[^\n]{0,45}[？?]",
            risk="low",
            source_url=str(data.get("source", "insights_history.jsonl")),
            tier="A",
            evidence=f"泰勒絲真實特徵矩陣：開頭首行反問句互動率倍數僅 {ratio} (開頭有問號 ER={q_stat['有此特徵']['avg_er']}% vs 開頭無問號={q_stat['無此特徵']['avg_er']}%)，禁止首行 45 字內使用反問句（保留文末互動提問）",
            confidence=0.85,
        )
        proposed_ids.append(rid)

    w_stat = feats.get("天氣題材", {})
    if w_stat.get("信心") == "OK" and w_stat.get("互動率倍數(有/無)", 1.0) < 0.75:
        w_ratio = w_stat["互動率倍數(有/無)"]
        rid_w = rule_store.propose(
            office="taylor",
            kind="regex_forbid",
            pattern=r"氣象|陸警|風|雨|太陽|颱",
            risk="low",
            source_url=str(data.get("source", "insights_history.jsonl")),
            tier="A",
            evidence=f"泰勒絲真實特徵矩陣：純天氣播報題材互動率倍數僅 {w_ratio} (有此特徵 ER={w_stat['有此特徵']['avg_er']}% vs 無={w_stat['無此特徵']['avg_er']}%)",
            confidence=0.80,
        )
        proposed_ids.append(rid_w)

    return proposed_ids, {"state_file": str(state_file), "learned_at": data.get("learned_at")}


def _sync_josef() -> tuple[list[str], dict]:
    script = SKILLS_DIR / "atom-josef-visual-aesthetics-learner" / "scripts" / "josef_real_learning.py"
    hist_file = SKILLS_DIR / "atom-josef-visual-aesthetics-learner" / "vaults" / "josef_contrast_history.jsonl"
    if script.exists():
        subprocess.run([sys.executable, str(script), "--audit-palette"], capture_output=True, timeout=60)
    if not hist_file.exists():
        raise FileNotFoundError(f"找不到約瑟夫對比度存摺：{hist_file}")
    rid = rule_store.propose(
        office="josef",
        kind="metric_min",
        pattern="contrast_ratio:7.0",
        risk="low",
        source_url=str(hist_file),
        tier="A",
        evidence="WCAG 2.1 AAA 高齡視力友善內文相對亮度對比度強制 >= 7.0:1",
        confidence=0.95,
    )
    return [rid], {"state_file": str(hist_file)}


def _sync_deming() -> tuple[list[str], dict]:
    hist_file = SKILLS_DIR / "atom-deming-quality-sopk-learner" / "vaults" / "deming_quality_history.jsonl"
    if not hist_file.exists():
        script = SKILLS_DIR / "atom-deming-quality-sopk-learner" / "scripts" / "deming_real_learning.py"
        if script.exists():
            subprocess.run([sys.executable, str(script), "--audit"], capture_output=True, timeout=180)
    if not hist_file.exists():
        raise FileNotFoundError(f"找不到戴明品質存摺：{hist_file}")
    rid = rule_store.propose(
        office="deming",
        kind="metric_max",
        pattern="defects:0",
        risk="low",
        source_url=str(hist_file),
        tier="A",
        evidence="全域原子腳本語法編譯與 --help 測試缺陷數上限為 0",
        confidence=0.95,
    )
    return [rid], {"state_file": str(hist_file)}


SYNC_DISPATCH = {
    "kage": _sync_kage,
    "taylor": _sync_taylor,
    "josef": _sync_josef,
    "deming": _sync_deming,
}


def run_cycle(office: str, with_discover: bool = False) -> dict:
    if cycle_ledger.is_locked(office):
        raise RuntimeError(f"🛑 子版 '{office}' 目前處於十輪停機鎖定狀態！請先完成衝突審計報告並呼叫 cycle_ledger.py audit_done。")

    if office not in SYNC_DISPATCH:
        raise ValueError(f"子版 '{office}' 尚未接線至自動閉環調度器（目前已接線：{list(SYNC_DISPATCH.keys())}）")

    discover_res = None
    if with_discover:
        discover_res = perceive_web.discover(office)

    proposed_ids, meta = SYNC_DISPATCH[office]()
    eval_results = []
    promoted_ids = []

    for rid in proposed_ids:
        ok_eval, msg_eval, ev_data = rule_store.evaluate_rule(office, rid)
        eval_results.append({"rule_id": rid, "ok": ok_eval, "message": msg_eval})
        if ok_eval:
            r_state = rule_store.fold(office).get(rid, {})
            if r_state.get("status") == "candidate" and r_state.get("risk") == "low":
                ok_prom, msg_prom = rule_store.promote(office, rid, founder_approved=False)
                if ok_prom:
                    promoted_ids.append(rid)

    retired_ids = rule_store.sweep()

    # 寫入當輪不可篡改之周期證據快照，供 cycle_ledger 計算真實唯一 SHA-256
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
        f"run_evolution_cycle v6.1: proposed={len(proposed_ids)}, promoted={len(promoted_ids)}, active={len(active_now)}",
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
    ap = argparse.ArgumentParser(description="單一閉環總控調度器 (v6.1)")
    ap.add_argument("--office", choices=list(SYNC_DISPATCH.keys()), help="執行單一首長閉環")
    ap.add_argument("--all-ready", action="store_true", help="依序執行所有已備妥真實資料集之首長閉環 (kage, taylor, josef, deming)")
    ap.add_argument("--with-discover", action="store_true", help="同時啟動 perceive_web 主動探索")
    a = ap.parse_args()

    targets = list(SYNC_DISPATCH.keys()) if a.all_ready else ([a.office] if a.office else [])
    if not targets:
        ap.error("請指定 --office <首長> 或 --all-ready")

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
