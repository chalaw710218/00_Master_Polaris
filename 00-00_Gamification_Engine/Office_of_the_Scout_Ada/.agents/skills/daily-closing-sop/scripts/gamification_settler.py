"""極星遊戲化確定性結算器 (Gamification Deterministic Settler)

核心目的：
徹底消除大語言模型（LLM）手動修改 save_data.json 時發生的「討好型數值膨脹」與「心算幻覺」！
將 2026-11-08 創辦人親定之《我獨自升級 2.1》核心控制規章 V2 中的：
  1. 階梯阻尼係數 (Damping Multipliers: 1.0x, 0.7x, 0.4x, 0.15x, 0.05x)
  2. 單次結算硬性安燈熔斷線 (+0.25 cap)
  3. 升級公式 (EXP = 30 + 10 * (Level - 1))
100% 固化為不可被竄改的物理確定性代碼！

用法：
  python gamification_settler.py --epic --int-effort high --imp-effort high --will-effort mid --note "完成自進化閉環"
  python gamification_settler.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def find_workspace_root() -> Path:
    cur = Path(__file__).resolve()
    for p in [cur] + list(cur.parents):
        if (p / ".git").exists() or (p / "00-01_Master_Polaris_Map.md").exists():
            return p
    return Path.cwd()


ROOT = find_workspace_root()
SAVE_FILE = ROOT / "00-00_Gamification_Engine" / "save_data.json"

# 階梯阻尼係數表 (Deming Damping Multipliers)
DAMPING_TIERS = [
    (59.99, 1.00, "凡人區 (0~59.9)"),
    (74.99, 0.70, "好手區 (60~74.9)"),
    (84.99, 0.40, "精英區 (75~84.9)"),
    (94.99, 0.15, "大師區 (85~94.9)"),
    (99.99, 0.05, "宗師區 (95~99.9)"),
]

SINGLE_SESSION_CAP = 0.25  # 單次結算硬性安燈熔斷線


def calculate_damped_gain(current_val: float, raw_gain: float) -> tuple[float, float, str]:
    """根據當前屬性數值與階梯阻尼，計算最終合規增量。

    回傳：(最終增量, 阻尼係數, 區間名稱)
    """
    tier_mult = 0.05
    tier_name = "極限硬鎖區"
    for threshold, mult, name in DAMPING_TIERS:
        if current_val <= threshold:
            tier_mult = mult
            tier_name = name
            break

    damped = raw_gain * tier_mult
    final_gain = min(damped, SINGLE_SESSION_CAP)
    return round(final_gain, 4), tier_mult, tier_name


def exp_needed_for_level(lvl: int) -> int:
    """規章公式：下一級所需 EXP = 30 + 10 * (當前等級 - 1)"""
    return 30 + 10 * (lvl - 1)


def settle(
    is_epic: bool = False,
    effort: dict[str, str] | None = None,
    note: str = "",
    dry_run: bool = False,
) -> dict:
    if not SAVE_FILE.exists():
        sys.stderr.write(f"❌ 錯誤：找不到存檔檔案 {SAVE_FILE}\n")
        sys.exit(1)

    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if effort is None:
        effort = {}

    current_lvl = int(data.get("level", 1))
    current_exp = int(data["exp"]["current"])
    total_exp = int(data["exp"]["total"])

    # 1. EXP 計算
    if is_epic:
        # 史詩破局日：基底 60，視維度投入最高 80~100
        gained_exp = 65
    else:
        # 常規修煉日：基底 20~35
        gained_exp = 30

    current_exp += gained_exp
    total_exp += gained_exp

    # 升級判定迴圈
    level_ups = 0
    while True:
        req = exp_needed_for_level(current_lvl)
        if current_exp >= req:
            current_exp -= req
            current_lvl += 1
            level_ups += 1
        else:
            break

    next_req = exp_needed_for_level(current_lvl)

    # 2. 六維屬性阻尼結算
    # 基準推力：none=0, low=0.2, mid=0.5, high=1.0 (史詩破局基數可達 1.5)
    effort_scale = {"none": 0.0, "low": 0.25, "mid": 0.6, "high": 1.2}
    if is_epic:
        effort_scale["high"] = 1.6

    attr_changes = {}
    attributes = data.get("attributes", {})

    for attr in ["STR", "INT", "AGI", "WILL", "CHA", "IMP"]:
        cur_v = float(attributes.get(attr, 50.0))
        eff_level = effort.get(attr.lower(), "none")
        raw_thrust = effort_scale.get(eff_level, 0.0)

        if raw_thrust > 0:
            final_delta, mult, tier_name = calculate_damped_gain(cur_v, raw_thrust)
        else:
            final_delta, mult, tier_name = 0.0, 1.0, "未修煉"

        new_v = round(cur_v + final_delta, 2)
        attr_changes[attr] = {
            "old": cur_v,
            "new": new_v,
            "delta": round(final_delta, 2),
            "mult": mult,
            "tier": tier_name,
        }
        if not dry_run:
            attributes[attr] = new_v

    # 3. 點數發放
    unspent = data.get("unspent_points", {})
    if level_ups > 0:
        unspent["level_points"] = unspent.get("level_points", 0) + (level_ups * 1)

    # 4. 金幣結算（依規章：總金幣上限 = floor(總EXP / 10)）
    calculated_gold_max = math.floor(total_exp / 10)
    current_gold = data.get("gold", 0)
    if is_epic:
        current_gold += 10
    else:
        current_gold += 2
    final_gold = min(current_gold, calculated_gold_max)

    # 5. 更新存檔
    if not dry_run:
        data["level"] = current_lvl
        data["exp"]["current"] = current_exp
        data["exp"]["next_level_requirement"] = next_req
        data["exp"]["total"] = total_exp
        data["gold"] = final_gold
        data["attributes"] = attributes
        data["unspent_points"] = unspent
        if note:
            data["notes"] = f"【{note}】"

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "level_before": data.get("level", 1) - level_ups if not dry_run else current_lvl,
        "level_after": current_lvl,
        "level_ups": level_ups,
        "exp_gained": gained_exp,
        "current_exp": current_exp,
        "next_req": next_req,
        "total_exp": total_exp,
        "gold": final_gold,
        "attr_changes": attr_changes,
        "dry_run": dry_run,
    }


def main():
    ap = argparse.ArgumentParser(description="極星遊戲化確定性結算器")
    ap.add_argument("--epic", action="store_true", help="史詩主線破局日 (高EXP與史詩基數)")
    ap.add_argument("--str-effort", choices=["none", "low", "mid", "high"], default="none")
    ap.add_argument("--int-effort", choices=["none", "low", "mid", "high"], default="none")
    ap.add_argument("--agi-effort", choices=["none", "low", "mid", "high"], default="none")
    ap.add_argument("--will-effort", choices=["none", "low", "mid", "high"], default="none")
    ap.add_argument("--cha-effort", choices=["none", "low", "mid", "high"], default="none")
    ap.add_argument("--imp-effort", choices=["none", "low", "mid", "high"], default="none")
    ap.add_argument("--note", default="", help="存檔備註")
    ap.add_argument("--dry-run", action="store_true", help="僅計算輸出，不寫入檔案")
    a = ap.parse_args()

    effort = {
        "str": a.str_effort,
        "int": a.int_effort,
        "agi": a.agi_effort,
        "will": a.will_effort,
        "cha": a.cha_effort,
        "imp": a.imp_effort,
    }

    res = settle(is_epic=a.epic, effort=effort, note=a.note, dry_run=a.dry_run)

    print("================ 🎮 極星遊戲化確定性物理結算 ================")
    if res["level_ups"] > 0:
        print(f"🎉【LEVEL UP!】榮耀晉升 Lv. {res['level_after']}！（原 Lv. {res['level_before']}）")
    else:
        print(f"當前等級：Lv. {res['level_after']}")
    print(f"經驗值發放：+{res['exp_gained']} EXP ➔ 當前 {res['current_exp']} / {res['next_req']} (累積總額: {res['total_exp']})")
    print(f"金幣存量：{res['gold']} Gold")
    print("------------------------------------------------------------")
    print("六維戴明階梯阻尼結算報告（硬鎖單次上限 +0.25）：")
    for attr, info in res["attr_changes"].items():
        delta_str = f"+{info['delta']:.2f}" if info["delta"] > 0 else "+0.00"
        print(f"  {attr:4s}: {info['old']:5.2f} ➔ {info['new']:5.2f} ({delta_str:6s}) | 阻尼: {info['mult']:4.2f}x | {info['tier']}")
    print("============================================================")
    if res["dry_run"]:
        print("🧪 [DRY-RUN 演練模式] 未寫入 save_data.json。")
    else:
        print("💾 [已存檔] save_data.json 物理寫入完成，100% 杜絕數值灌水與心算幻覺！")


if __name__ == "__main__":
    main()
