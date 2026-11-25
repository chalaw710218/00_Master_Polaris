"""單一閉環總控調度器 (Run Evolution Cycle · Master v6.2 第十一章 ⑦)

v6.2 重大硬化升級：
  1. 子進程失敗不吞錯：`subprocess.run` 強制檢查 `returncode != 0`，失敗立即拋錯中止，絕不讀取殘留舊檔充數。
  2. 精準收斂正則與範疇：
     - 影 (`kage`) 的開頭鉤子規則強制帶 `scope="prefix"`，確保驗算與守門一致。
     - 泰勒絲 (`taylor`) 天氣播報正則收斂為 `氣象預報|陸警|海警|颱風動態|豪雨特報|降雨機率`，杜絕誤傷『海風/風格/風險』。
  3. 區分合規基準與經驗規則：
     - 約瑟夫 (`josef`) WCAG 7:1 與戴明 (`deming`) `defects:0` 改以 `baseline_standard` 登記，不偽造 A/B 對照。
  4. 接線執行長雪 (`yuki`) 幕僚長派工帳本：
     - 驗證 `yuki_dispatch.jsonl` 雜湊鏈完整性，並當特定類別結案樣本達標時自動提名 `route` 規則（`risk="high"` 交由董事長簽核）。
  5. 防空轉刷輪次：證據快照經 `cycle_ledger` 去時間戳計算實質內容 SHA-256，資料與規則狀態未變時直接拒絕虛增輪次。

用法：
  python run_evolution_cycle.py --office kage
  python run_evolution_cycle.py --office taylor
  python run_evolution_cycle.py --office josef
  python run_evolution_cycle.py --office deming
  python run_evolution_cycle.py --office yuki
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


def _run_learner_script(script: Path, args: list[str], timeout: int = 90) -> None:
    if not script.exists():
        raise FileNotFoundError(f"找不到學習腳本：{script}")
    res = subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    if res.returncode != 0:
        raise RuntimeError(f"學習腳本執行失敗 (exit={res.returncode}): {script.name}\n{res.stderr or res.stdout}")


def _sync_kage() -> tuple[list[str], dict]:
    state_file = SKILLS_DIR / "atom-kage-synaptic-metabolic-learner" / "vaults" / "kage_synaptic_state.json"
    script = SKILLS_DIR / "atom-kage-synaptic-metabolic-learner" / "scripts" / "kage_real_learning.py"
    if script.exists():
        _run_learner_script(script, ["--learn"], timeout=60)
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
        dyn_conf = min(0.95, round(0.50 + n * 0.05, 2))
        if avg_er < median_er * 0.7:
            rid = rule_store.propose(
                office="kage",
                kind="forbid_phrase",
                pattern=hook,
                scope="prefix",
                risk="low",
                source_url=str(data.get("source", "insights_history.jsonl")),
                tier="A",
                evidence=f"真實 Threads 快照 N={n}，開頭『{hook}』平均 ER={avg_er}% < 帳號中位數 {median_er}%*0.7",
                confidence=dyn_conf,
            )
            proposed_ids.append(rid)
        elif avg_er >= median_er * 1.3:
            rid = rule_store.propose(
                office="kage",
                kind="prefer_phrase",
                pattern=hook,
                scope="prefix",
                risk="low",
                source_url=str(data.get("source", "insights_history.jsonl")),
                tier="A",
                evidence=f"真實 Threads 快照 N={n}，開頭『{hook}』平均 ER={avg_er}% >= 帳號中位數 {median_er}%*1.3",
                confidence=dyn_conf,
            )
            proposed_ids.append(rid)
    return proposed_ids, {"state_file": str(state_file), "learned_at": data.get("learned_at"), "median_er": median_er}


def _sync_taylor() -> tuple[list[str], dict]:
    state_file = SKILLS_DIR / "atom-taylor-marketing-psychology-learner" / "vaults" / "taylor_marketing_state.json"
    script = SKILLS_DIR / "atom-taylor-marketing-psychology-learner" / "scripts" / "taylor_real_learning.py"
    if script.exists():
        _run_learner_script(script, ["--learn"], timeout=60)
    if not state_file.exists():
        raise FileNotFoundError(f"找不到泰勒絲狀態檔：{state_file}")
    data = json.loads(state_file.read_text(encoding="utf-8"))
    proposed_ids: list[str] = []
    feats = data.get("feature_results", {})

    q_stat = feats.get("好奇提問句", {})
    if q_stat.get("信心") == "OK" and q_stat.get("互動率倍數(有/無)", 1.0) < 0.75:
        ratio = q_stat["互動率倍數(有/無)"]
        n_q = int(q_stat.get("有此特徵", {}).get("n", 3))
        rid = rule_store.propose(
            office="taylor",
            kind="regex_forbid",
            pattern=r"^[^\n]{0,45}[？?]",
            risk="low",
            source_url=str(data.get("source", "insights_history.jsonl")),
            tier="A",
            evidence=f"泰勒絲真實特徵矩陣：開頭首行反問句互動率倍數僅 {ratio} (開頭有問號 ER={q_stat['有此特徵']['avg_er']}% vs 開頭無問號={q_stat['無此特徵']['avg_er']}%)，禁止首行 45 字內使用反問句（保留文末互動提問）",
            confidence=min(0.95, round(0.50 + n_q * 0.04, 2)),
        )
        proposed_ids.append(rid)

    w_stat = feats.get("天氣題材", {})
    if w_stat.get("信心") == "OK" and w_stat.get("互動率倍數(有/無)", 1.0) < 0.75:
        w_ratio = w_stat["互動率倍數(有/無)"]
        n_w = int(w_stat.get("有此特徵", {}).get("n", 3))
        rid_w = rule_store.propose(
            office="taylor",
            kind="regex_forbid",
            pattern=r"氣象預報|陸警|海警|颱風動態|豪雨特報|降雨機率",
            risk="low",
            source_url=str(data.get("source", "insights_history.jsonl")),
            tier="A",
            evidence=f"泰勒絲真實特徵矩陣：純天氣播報題材互動率倍數僅 {w_ratio} (已收斂正則避免誤傷『海風/風格/風險』)",
            confidence=min(0.95, round(0.50 + n_w * 0.04, 2)),
        )
        proposed_ids.append(rid_w)

    return proposed_ids, {"state_file": str(state_file), "learned_at": data.get("learned_at")}


def _sync_josef() -> tuple[list[str], dict]:
    script = SKILLS_DIR / "atom-josef-visual-aesthetics-learner" / "scripts" / "josef_real_learning.py"
    hist_file = SKILLS_DIR / "atom-josef-visual-aesthetics-learner" / "vaults" / "josef_contrast_history.jsonl"
    if script.exists():
        _run_learner_script(script, ["--audit-palette"], timeout=60)
    if not hist_file.exists():
        raise FileNotFoundError(f"找不到約瑟夫對比度存摺：{hist_file}")
    rid = rule_store.propose(
        office="josef",
        kind="baseline_standard",
        pattern="contrast_ratio:7.0",
        risk="low",
        source_url=str(hist_file),
        tier="A",
        evidence="WCAG 2.1 AAA 高齡視力友善內文相對亮度對比度強制 >= 7.0:1（合規基準標準）",
        confidence=0.95,
    )
    return [rid], {"state_file": str(hist_file)}


def _sync_deming() -> tuple[list[str], dict]:
    hist_file = SKILLS_DIR / "atom-deming-quality-sopk-learner" / "vaults" / "deming_quality_history.jsonl"
    if not hist_file.exists():
        script = SKILLS_DIR / "atom-deming-quality-sopk-learner" / "scripts" / "deming_real_learning.py"
        if script.exists():
            _run_learner_script(script, ["--audit"], timeout=180)
    if not hist_file.exists():
        raise FileNotFoundError(f"找不到戴明品質存摺：{hist_file}")
    rid = rule_store.propose(
        office="deming",
        kind="baseline_standard",
        pattern="defects:0",
        risk="low",
        source_url=str(hist_file),
        tier="A",
        evidence="全域原子腳本語法編譯與 --help 測試缺陷數上限為 0（合規基準標準）",
        confidence=0.95,
    )
    return [rid], {"state_file": str(hist_file)}


def _sync_yuki() -> tuple[list[str], dict]:
    disp_script = SKILLS_DIR / "atom-yuki-autonomous-executive-learner" / "scripts" / "dispatch.py"
    ledger_file = SKILLS_DIR / "atom-yuki-autonomous-executive-learner" / "vaults" / "yuki_dispatch.jsonl"
    if not disp_script.exists():
        raise FileNotFoundError(f"找不到雪的派工帳本腳本：{disp_script}")
    res = subprocess.run([sys.executable, str(disp_script), "status"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    if res.returncode != 0:
        raise RuntimeError(f"雪派工帳本鏈檢查失敗：{res.stdout or res.stderr}")
    proposed_ids: list[str] = []
    event_count = 0
    if ledger_file.exists():
        lines = [json.loads(x) for x in ledger_file.read_text(encoding="utf-8").splitlines() if x.strip()]
        event_count = len(lines)
        # 盤點各類別被派工對象
        cats = {e.get("category") for e in lines if e.get("type") == "dispatch" and e.get("category")}
        for cat in sorted(cats):
            # 找出該類別出現次數最多的被指派者作為候選路由假說（高風險規則，需董事長簽核）
            counts: dict[str, int] = {}
            for e in lines:
                if e.get("type") == "dispatch" and e.get("category") == cat:
                    for a in e.get("assigned", []):
                        counts[a] = counts.get(a, 0) + 1
            if counts:
                top_agent, cnt = max(counts.items(), key=lambda kv: kv[1])
                if cnt >= 3:
                    rid = rule_store.propose(
                        office="yuki",
                        kind="route",
                        pattern=f"{cat}->{top_agent}",
                        risk="high",
                        source_url=str(ledger_file),
                        tier="A",
                        evidence=f"幕僚長派工帳本實測：『{cat}』類任務指派 {top_agent} 共 {cnt} 筆，提請驗證一次通過率",
                        confidence=min(0.90, round(0.40 + cnt * 0.05, 2)),
                    )
                    proposed_ids.append(rid)
    return proposed_ids, {"dispatch_ledger": str(ledger_file), "events": event_count, "status_output": res.stdout.strip()}


SYNC_DISPATCH = {
    "kage": _sync_kage,
    "taylor": _sync_taylor,
    "josef": _sync_josef,
    "deming": _sync_deming,
    "yuki": _sync_yuki,
}


def run_cycle(office: str, with_discover: bool = False) -> dict:
    if cycle_ledger.is_locked(office):
        raise RuntimeError(f"🛑 子版 '{office}' 目前處於十輪停機鎖定狀態！請先完成衝突審計報告並呼叫 cycle_ledger.py audit-done。")

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
        f"run_evolution_cycle v6.2: proposed={len(proposed_ids)}, promoted={len(promoted_ids)}, active={len(active_now)}",
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
    ap = argparse.ArgumentParser(description="單一閉環總控調度器 (v6.2)")
    ap.add_argument("--office", choices=list(SYNC_DISPATCH.keys()), help="執行單一首長閉環")
    ap.add_argument("--all-ready", action="store_true", help="依序執行所有已備妥真實資料集之首長閉環")
    ap.add_argument("--with-discover", action="store_true", help="同時啟動 perceive_web 主動探索")
    a = ap.parse_args()

    targets = [k for k in ("kage", "taylor", "josef", "deming") if k in SYNC_DISPATCH] if a.all_ready else ([a.office] if a.office else [])
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
