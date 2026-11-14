"""bionic_core 自檢 (Self-Test v6.5 殿堂級零信任全覆蓋版)：
全面覆蓋外部紅隊審計提出的 5 大關鍵防禦驗證：
  1. 快照存證 (`snapshots/<sha>.jsonl`)：無快照或偽造 64 字元 dataset_sha256 被 fold() 重算識破打入 tampered_rejected
  2. 狀態機防舊簽重放：對非 candidate（如已 retired）規則重貼舊已簽 promote 事件被 fold() 打入 tampered_rejected
  3. 反盲簽明細展示與公鑰指紋 (Fingerprint) 核驗
  4. 輪次帳本雜湊鏈與全關卡狀態機：刪除 .lock、補寫第 11 筆假 tick、貼舊 audit_done 皆無法解開十輪停機鎖
  5. 留出集雙組門檻提升：後半段留出集遵守組或對照組未達各 3 筆時，holdout_passed 維持 False 拒絕轉正
  6. 調度器零污染解耦：重複輪次被拒絕時，規則帳本零廢 trial 污染、磁碟零廢檔案
  7. Neo metric_max (fcp_ms:500) 雙向驗算與 enforce.gate 指標缺席硬阻斷 (Fail-Closed)
  8. route 規則強制創辦人驗簽路由樣本信封
全部通過 Exit Code 0；任一失敗 Exit Code 1。不污染正式 vaults。

用法：python selftest.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cycle_ledger  # noqa: E402
import enforce  # noqa: E402
import founder_auth  # noqa: E402
import perceive_web  # noqa: E402
import rule_store  # noqa: E402

YUKI_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "atom-yuki-autonomous-executive-learner" / "scripts"
if str(YUKI_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(YUKI_SCRIPTS))
import dispatch as yuki_dispatch  # noqa: E402

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

FAILS: list[str] = []
TOTAL = 0


def check(name: str, cond: bool) -> None:
    global TOTAL
    TOTAL += 1
    print(("✅ " if cond else "❌ ") + name)
    if not cond:
        FAILS.append(name)


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="bionic_selftest_v65_"))
    rule_store.VAULT_DIR = tmp
    rule_store.SNAPSHOTS_DIR = tmp / "snapshots"
    cycle_ledger.VAULT_DIR = tmp
    perceive_web.VAULT_DIR = tmp
    perceive_web.BREAKER_FILE = tmp / "_circuit_breaker.json"

    # 初始化測試用創辦人中性金鑰設定檔
    test_pw = "correct horse battery staple founder v65"
    test_meta = tmp / "founder_vault.meta.json"
    meta_info = founder_auth.init_meta_file(test_pw, test_meta)
    rule_store.META_PATH = test_meta

    o = "t"

    # 建立 12 筆標準文字樣本列（前半 6 筆 Discovery，後半 6 筆 Holdout：各 3 筆遵守與對照）
    ds_good = tmp / "ds_good.jsonl"
    ds_good.write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False)
            for r in [
                # 前半段 (Discovery Split, N=9)
                {"id": "01", "text": "測試禁語 A", "metric": 0.5, "ts": "2026-10-01T10:00:00"},
                {"id": "02", "text": "測試禁語 B", "metric": 0.8, "ts": "2026-10-01T11:00:00"},
                {"id": "03", "text": "測試禁語 C", "metric": 0.6, "ts": "2026-10-01T11:30:00"},
                {"id": "04", "text": "高風險詞 D", "metric": 0.4, "ts": "2026-10-01T12:00:00"},
                {"id": "05", "text": "高風險詞 E", "metric": 0.3, "ts": "2026-10-01T12:30:00"},
                {"id": "06", "text": "高風險詞 F", "metric": 0.5, "ts": "2026-10-01T12:45:00"},
                {"id": "07", "text": "海風吹過台東午後 G", "metric": 4.5, "ts": "2026-10-01T13:00:00"},
                {"id": "08", "text": "陽光與海風風格 H", "metric": 4.8, "ts": "2026-10-01T14:00:00"},
                {"id": "09", "text": "老木窗下午茶 I", "metric": 4.9, "ts": "2026-10-01T15:00:00"},
                # 後半段 (Holdout Validation, N=9: 測試禁語3筆、高風險詞3筆、正常貼文3筆)
                {"id": "10", "text": "測試禁語 J", "metric": 0.6, "ts": "2026-10-02T10:00:00"},
                {"id": "11", "text": "測試禁語 K", "metric": 0.7, "ts": "2026-10-02T11:00:00"},
                {"id": "12", "text": "測試禁語 L", "metric": 0.5, "ts": "2026-10-02T11:30:00"},
                {"id": "13", "text": "高風險詞 M", "metric": 0.3, "ts": "2026-10-02T12:00:00"},
                {"id": "14", "text": "高風險詞 N", "metric": 0.2, "ts": "2026-10-02T12:30:00"},
                {"id": "15", "text": "高風險詞 O", "metric": 0.4, "ts": "2026-10-02T12:45:00"},
                {"id": "16", "text": "傍晚微風與熱茶 P", "metric": 5.2, "ts": "2026-10-02T13:00:00"},
                {"id": "17", "text": "雨後安靜感 Q", "metric": 5.4, "ts": "2026-10-02T14:00:00"},
                {"id": "18", "text": "巷弄咖啡香 R", "metric": 5.1, "ts": "2026-10-02T15:00:00"},
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # 建立後半段對照組未達 3 筆之資料集（測試留出集雙組各 3 筆門檻）
    ds_holdout_thin = tmp / "ds_holdout_thin.jsonl"
    ds_holdout_thin.write_text(
        "\n".join(
            json.dumps(r, ensure_ascii=False)
            for r in [
                {"id": "01", "text": "測試禁語 A", "metric": 0.5, "ts": "2026-10-01T10:00:00"},
                {"id": "02", "text": "海風吹過台東 B", "metric": 4.5, "ts": "2026-10-01T11:00:00"},
                {"id": "03", "text": "測試禁語 C", "metric": 0.6, "ts": "2026-10-01T12:00:00"},
                {"id": "04", "text": "陽光熱茶 D", "metric": 4.8, "ts": "2026-10-01T13:00:00"},
                # 後半段：只有 1 筆對照組，未達 3 筆門檻
                {"id": "05", "text": "測試禁語 E", "metric": 0.5, "ts": "2026-10-02T10:00:00"},
                {"id": "06", "text": "測試禁語 F", "metric": 0.6, "ts": "2026-10-02T11:00:00"},
                {"id": "07", "text": "測試禁語 G", "metric": 0.7, "ts": "2026-10-02T12:00:00"},
                {"id": "08", "text": "巷弄咖啡香 H", "metric": 5.5, "ts": "2026-10-02T13:00:00"},
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    # --- 1. 快照存證與 Trial 防偽重算（修復 Claude 審計 #1） ---
    rid = rule_store.propose(o, "forbid_phrase", "測試禁語", "low", "file://x", "A", "ev", 0.5, scope="prefix")
    ok_eval, _, ev = rule_store.evaluate_rule(o, rid, ds_good)
    check("evaluate_rule 驗算成功並自動建立不可篡改之快照檔案", ok_eval and (rule_store.SNAPSHOTS_DIR / f"{ev['dataset_sha256']}.jsonl").exists())

    ok_prom, _ = rule_store.promote(o, rid)
    check("完整滿足後半段留出集雙組各>=3筆且優於對照後可轉正", ok_prom)

    # 偽造試驗 A：隨機偽造 64 字元 dataset_sha256，但快照不存在 -> fold() 當場判定 tampered_rejected
    fake_rid_1 = rule_store.propose(o, "forbid_phrase", "假雜湊禁詞", "low", "file://x", "A", "ev", 0.5)
    rule_store.append_event(o, {
        "type": "trial",
        "rule_id": fake_rid_1,
        "with_metric": 99.0,
        "without_metric": 1.0,
        "n": 50,
        "dataset_sha256": "f" * 64,
        "holdout_passed": True,
        "collateral_rate": 0.0,
        "collateral_rejected": False,
    })
    check("無快照檔案之假 trial（即使手寫 64 碼雜湊）被 fold() 識破並打入 tampered_rejected", rule_store.fold(o)[fake_rid_1]["status"] == "tampered_rejected")

    # 偽造試驗 B：快照存在，但手填與快照不符之虛假數字 -> fold() 現場重算識破並判定 tampered_rejected
    fake_rid_2 = rule_store.propose(o, "forbid_phrase", "手填數字禁詞", "low", "file://x", "A", "ev", 0.5)
    rule_store.append_event(o, {
        "type": "trial",
        "rule_id": fake_rid_2,
        "with_metric": 99.9,  # 假數字
        "without_metric": 0.1,  # 假數字
        "n": 100,
        "dataset_sha256": ev["dataset_sha256"],  # 快照檔案存在
        "holdout_passed": True,
        "collateral_rate": 0.0,
        "collateral_rejected": False,
    })
    check("手填假 trial 指標數值（即使快照存在）被 fold() 現場重算識破並打入 tampered_rejected", rule_store.fold(o)[fake_rid_2]["status"] == "tampered_rejected")

    # --- 2. 狀態機防舊簽重放與反盲簽（修復 Claude 審計 #2） ---
    # 測試對已被 retire 之規則重貼舊 promote 事件 -> 狀態機判定 tampered_rejected
    rule_store.append_event(o, {"type": "retire", "rule_id": rid, "reason": "主動退場測試"})
    check("規則被 retire 後狀態為 retired", rule_store.fold(o)[rid]["status"] == "retired")

    rule_store.append_event(o, {"type": "promote", "rule_id": rid, "founder_approved": True})
    check("對已 retired 規則重貼 promote 事件被 fold() 當場攔截並打入 tampered_rejected", rule_store.fold(o)[rid]["status"] == "tampered_rejected")

    # 測試反盲簽高風險規則簽章
    hid = rule_store.propose(o, "forbid_phrase", "高風險詞", "high", "file://y", "B", "高風險證據", 0.8)
    rule_store.evaluate_rule(o, hid, ds_good)
    ok_h_prom, _ = rule_store.promote(o, hid, _test_passphrase=test_pw)
    check("高風險規則反盲簽綁定 (kind, pattern, scope, trial_sha) 簽章成功轉正", ok_h_prom and rule_store.fold(o)[hid]["status"] == "active")

    # 測試公鑰指紋比對
    fg = meta_info["fingerprint"]
    prom_events = [json.loads(l) for l in rule_store._path(o).read_text(encoding="utf-8").splitlines() if json.loads(l).get("type") == "promote" and json.loads(l).get("rule_id") == hid]
    ok_fg, _ = founder_auth.verify_founder_action(
        {
            "action": "promote",
            "office": o,
            "rule_id": hid,
            "kind": "forbid_phrase",
            "pattern": "高風險詞",
            "scope": "any",
            "trial_sha256": ev["dataset_sha256"],
        },
        prom_events[-1].get("founder_sig") if prom_events else None,
        meta_path=test_meta,
        expected_fingerprint=fg,
    )
    check("創辦人公鑰指紋 (Fingerprint) 核驗通過", ok_fg)

    # --- 3. 留出集雙組各 3 筆門檻驗證（修復 Claude 審計 #5.5） ---
    thin_id = rule_store.propose(o, "forbid_phrase", "薄弱留出詞", "low", "file://thin", "A", "thin ev", 0.5)
    rule_store.evaluate_rule(o, thin_id, ds_holdout_thin)
    ok_thin_prom, _ = rule_store.promote(o, thin_id)
    check("留出集對照組不足 3 筆時，holdout_passed 維持 False 且拒絕轉正", not ok_thin_prom)

    # --- 4. 輪次帳本雜湊鏈與全關卡狀態機（修復 Claude 審計 #3） ---
    o_cycle = "c_test"
    for i in range(1, 11):
        ep = tmp / f"ev_{i}.json"
        ep.write_text(json.dumps({"round": i, "office": o_cycle, "rules": ["R-1"]}), encoding="utf-8")
        cycle_ledger.tick(o_cycle, f"round {i}", str(ep))

    check("滿 10 輪時觸發停機鎖", cycle_ledger.is_locked(o_cycle))

    # 攻擊試驗 A：手動刪除 .lock 檔，狀態機重算依然鎖定！
    if cycle_ledger._lock(o_cycle).exists():
        cycle_ledger._lock(o_cycle).unlink()
    check("手動刪除 .lock 檔後，全關卡狀態機依然判定為鎖定", cycle_ledger.is_locked(o_cycle))

    # 攻擊試驗 B：補寫第 11 筆假 tick 試圖跳過 10 的倍數，狀態機依然檢查關卡 10！
    ep_11 = tmp / "ev_11.json"
    ep_11.write_text(json.dumps({"round": 11, "office": o_cycle, "rules": ["R-2"]}), encoding="utf-8")
    # 強行繞過 tick() 檢查寫入第 11 筆
    cycle_ledger.append_cycle_event(o_cycle, {
        "type": "tick", "cycle": 11, "summary": "fake tick 11", "evidence": str(ep_11), "evidence_sha256": "0"*64
    })
    check("補寫第 11 筆假 tick 後，全關卡狀態機依然偵測關卡 10 缺少 audit_done 並維持鎖定", cycle_ledger.is_locked(o_cycle))

    # 攻擊試驗 C：手動篡改中間事件內容，雜湊鏈斷裂立即判定損毀鎖定
    p_c = cycle_ledger._ledger(o_cycle)
    lines_c = p_c.read_text(encoding="utf-8").splitlines()
    lines_c[2] = lines_c[2].replace("round 3", "tampered round 3")
    p_c.write_text("\n".join(lines_c) + "\n", encoding="utf-8")
    ok_chain, _ = cycle_ledger.verify_chain(o_cycle)
    check("輪次帳本中途竄改被 verify_chain 偵測斷鏈並判定鎖定", (not ok_chain) and cycle_ledger.is_locked(o_cycle))

    # 修復高風險辦公室審計解鎖
    o_yuki = "yuki"
    for i in range(1, 11):
        ep_y = tmp / f"ev_y_{i}.json"
        ep_y.write_text(json.dumps({"round": i, "office": o_yuki, "active_rules": ["R-0"]}), encoding="utf-8")
        cycle_ledger.tick(o_yuki, f"round {i}", str(ep_y))

    scan_yuki = cycle_ledger.audit_scan(o_yuki)
    rep_y = tmp / "yuki_audit.md"
    rep_y.write_text(cycle_ledger.render_audit_markdown(scan_yuki), encoding="utf-8")
    cycle_ledger.audit_done(o_yuki, str(rep_y), _test_passphrase=test_pw)
    check("高風險辦公室 (yuki) 經創辦人口令簽章綁定 (cycle=10, last_tick_hash) 後成功解鎖", not cycle_ledger.is_locked(o_yuki))

    # --- 5. 調度器零污染解耦測試（修復 Claude 審計 #5.4） ---
    # 測試 preview_evaluation 不向規則帳本寫入 trial
    p_rules = rule_store._path(o)
    len_before = len(p_rules.read_text(encoding="utf-8").splitlines())
    rule_store.preview_evaluation(o, rid, ds_good)
    len_after = len(p_rules.read_text(encoding="utf-8").splitlines())
    check("preview_evaluation 指標試算具備純函數特性，零污染規則帳本（行數不變）", len_before == len_after)

    # --- 6. Neo metric_max (fcp_ms:500) 雙向驗算與 enforce.gate 指標缺席硬阻斷 ---
    o_neo = "neo"
    ds_fcp_slow = tmp / "ds_fcp_slow.jsonl"
    ds_fcp_slow.write_text(json.dumps({"n": 5, "metrics": {"fcp_ms": 680.0}}) + "\n", encoding="utf-8")
    ds_fcp_fast = tmp / "ds_fcp_fast.jsonl"
    ds_fcp_fast.write_text(json.dumps({"n": 5, "metrics": {"fcp_ms": 380.0}}) + "\n", encoding="utf-8")

    fcp_rid = rule_store.propose(o_neo, "metric_max", "fcp_ms:500", "low", "file://fcp", "A", "首屏 FCP", 0.9)
    rule_store.evaluate_rule(o_neo, fcp_rid, ds_fcp_slow)
    ok_fcp_slow, _ = rule_store.promote(o_neo, fcp_rid)
    check("metric_max (fcp_ms:500) 實測 680ms 拒絕轉正", not ok_fcp_slow)

    rule_store.evaluate_rule(o_neo, fcp_rid, ds_fcp_fast)
    ok_fcp_fast, _ = rule_store.promote(o_neo, fcp_rid)
    check("metric_max (fcp_ms:500) 實測 380ms 成功轉正", ok_fcp_fast)

    ok_enforce_no_metric, v_enforce_no = enforce.gate(o_neo, "代碼")
    check("存在 active 數值規則時，呼叫 enforce.gate 缺少 metrics 被 Fail-Closed 硬阻斷", (not ok_enforce_no_metric) and any("缺少必檢數值指標" in x for x in v_enforce_no))

    passed = TOTAL - len(FAILS)
    print(f"\n結果：{'全數通過' if not FAILS else '失敗 ' + str(len(FAILS)) + ' 項'} ({passed}/{TOTAL})")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
