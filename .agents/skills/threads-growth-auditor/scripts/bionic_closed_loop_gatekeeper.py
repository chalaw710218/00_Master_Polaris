"""仿生學習閉環守門員 (Bionic Closed-Loop Gatekeeper · v6.2 Fail-Closed 硬化版)

v6.2 重大硬化（對應外部紅隊代碼審計修補）：
  1. 強制 Fail-Closed（失敗即阻斷）：
     - 若找不到極星專案根目錄或無法載入 `bionic_core/enforce.py`，立即輸出錯誤並 `sys.exit(1)`，嚴禁設為 `None` 靜默放行！
  2. 廢除寫死常數（零硬編碼數字）：
     - 移除寫死的 `0.48`、`0.82` 文字，100% 動態讀取 `taylor_marketing_state.json` 內的真實 `互動率倍數(有/無)`。
     - 同時兼容 `"信心"` 與 `"confidence"` 欄位鍵名。
  3. 樣本數分級處置（防早期小樣本永久死鎖）：
     - 低效鉤子若 `3 <= N < 5` 採軟性扣分（`-12` 分）保留探索空間；`N >= 5` 或已通過 `bionic_core` 留出集驗證轉正者採硬阻斷。
  4. 支援幕僚長派工單號核驗 (`--task-id`)：
     - 若傳入 `--task-id T-...`，自動查驗雪的 `yuki_dispatch.jsonl` 帳本是否存在該筆合法派工。

用法：
  python bionic_closed_loop_gatekeeper.py --text "我就問這合理嗎..." (預期攔截打回)
  python bionic_closed_loop_gatekeeper.py --text "誰能想到台東深夜..." (預期通過)
  python bionic_closed_loop_gatekeeper.py --constraints (輸出動態提示詞約束)
"""
from __future__ import annotations

import argparse
import json
import re
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
    sys.stderr.write("🛑 [Fail-Closed 阻斷] 找不到極星工作區根目錄 (00-01_Master_Polaris_Map.md)，拒絕放行！\n")
    sys.exit(1)


ROOT = find_workspace_root()
BIONIC_CORE_DIR = ROOT / ".agents" / "skills" / "bionic-learning-system" / "bionic_core"
if str(BIONIC_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(BIONIC_CORE_DIR))
try:
    import enforce as bionic_enforce  # type: ignore
except Exception as e:
    sys.stderr.write(f"🛑 [Fail-Closed 阻斷] 無法載入 bionic_core/enforce.py ({e})，拒絕靜默放行！\n")
    sys.exit(1)

KAGE_VAULT = (
    ROOT
    / ".agents"
    / "skills"
    / "atom-kage-synaptic-metabolic-learner"
    / "vaults"
    / "kage_synaptic_state.json"
)
TAYLOR_VAULT = (
    ROOT
    / ".agents"
    / "skills"
    / "atom-taylor-marketing-psychology-learner"
    / "vaults"
    / "taylor_marketing_state.json"
)
YUKI_DISPATCH_SCRIPT_DIR = (
    ROOT
    / ".agents"
    / "skills"
    / "atom-yuki-autonomous-executive-learner"
    / "scripts"
)
if str(YUKI_DISPATCH_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(YUKI_DISPATCH_SCRIPT_DIR))
import dispatch as yuki_dispatch  # type: ignore

YUKI_DISPATCH_LEDGER = (
    ROOT
    / ".agents"
    / "skills"
    / "atom-yuki-autonomous-executive-learner"
    / "vaults"
    / "yuki_dispatch.jsonl"
)

# 基礎通用合規黑名單（物理不可碰觸紅線）
BAIT_WORDS = ["留言+1", "留言 +1", "+1", "快來買", "限時搶購", "限時", "搶購", "手慢無", "最後機會", "錯過可惜"]
HARD_SELL = ["特價", "滿千免運", "點擊購買", "下單連結", "優惠碼"]
STALE_GREETINGS = ["大家好", "哈囉大家", "今天小編要", "推薦大家"]
BOSS_WORDS = ["闆仔", "老闆", "品碩"]
CAT_WORDS = ["喵", "貓", "本喵", "罐罐", "爪"]
PERSONA_AGENT_MAP = {
    "meow": {"kage", "taylor", "meow"},
    "shadow": {"kage", "taylor"},
}


def verify_task_id(task_id: str, persona: str = "meow") -> tuple[bool, str]:
    """核驗幕僚長雪的派工單號：驗雜湊鏈、驗存在性、驗指派對象匹配、防已結案單號重用。"""
    if not YUKI_DISPATCH_LEDGER.exists():
        return False, f"找不到雪的派工帳本：{YUKI_DISPATCH_LEDGER}"
    events = yuki_dispatch.read_events()
    ok_chain, msg_chain = yuki_dispatch.verify_chain(events)
    if not ok_chain:
        return False, f"派工帳本雜湊鏈損毀（{msg_chain}），拒絕放行"

    target_disp = None
    signoffs_for_tid = []
    for ev in events:
        if ev.get("type") == "dispatch" and ev.get("task_id") == task_id:
            target_disp = ev
        elif ev.get("type") == "signoff" and ev.get("task_id") == task_id:
            signoffs_for_tid.append(ev)

    if not target_disp:
        return False, f"派工帳本查無單號：{task_id}（無 task_id 之黑工分派視為未發生）"

    assigned_set = set(target_disp.get("assigned", []))
    allowed_agents = PERSONA_AGENT_MAP.get(persona, {persona})
    if not (assigned_set & allowed_agents):
        return False, f"派工單 {task_id} 指派對象為 {sorted(assigned_set)}，與當前角色 ({persona}) 不符"

    if signoffs_for_tid:
        last_word = str(signoffs_for_tid[-1].get("word", ""))
        if last_word == "收" or last_word.startswith("改派:"):
            return False, f"派工單 {task_id} 已結案（最新狀態：{last_word}），禁止重複盜用舊單號"

    return True, f"已核驗派工單 {task_id} ({target_disp.get('category')} -> {target_disp.get('assigned')}，雜湊鏈完整且未結案)"


def load_bionic_vaults() -> dict:
    """載入影與泰勒絲的真實學習存摺並提取行為約束準則。"""
    profile = {
        "kage_loaded": False,
        "taylor_loaded": False,
        "account_median_er": 2.0,
        "boost_hooks": [],
        "low_hooks": [],
        "feature_penalties": {},
    }

    if KAGE_VAULT.exists():
        try:
            with open(KAGE_VAULT, "r", encoding="utf-8") as f:
                kage_data = json.load(f)
            profile["kage_loaded"] = True
            median_er = float(kage_data.get("account_median_er", 2.0))
            profile["account_median_er"] = median_er
            hooks = kage_data.get("hook_weights", {})
            for hook, stat in hooks.items():
                conf = stat.get("confidence", stat.get("信心", ""))
                avg_er = float(stat.get("avg_er", 0.0))
                if conf == "OK":
                    if avg_er >= median_er * 1.3:
                        profile["boost_hooks"].append({
                            "hook": hook,
                            "avg_er": avg_er,
                            "n": int(stat.get("n", 0)),
                        })
                    elif avg_er < median_er * 0.7:
                        profile["low_hooks"].append({
                            "hook": hook,
                            "avg_er": avg_er,
                            "n": int(stat.get("n", 0)),
                        })
        except Exception as e:
            sys.stderr.write(f"[WARN] 載入影存摺失敗: {e}\n")

    if TAYLOR_VAULT.exists():
        try:
            with open(TAYLOR_VAULT, "r", encoding="utf-8") as f:
                taylor_data = json.load(f)
            profile["taylor_loaded"] = True
            features = taylor_data.get("feature_results", {})
            for feat_name, stat in features.items():
                conf = stat.get("信心", stat.get("confidence", ""))
                ratio = stat.get("互動率倍數(有/無)")
                if conf == "OK" and ratio is not None:
                    ratio_f = float(ratio)
                    if ratio_f < 0.75:
                        profile["feature_penalties"][feat_name] = {
                            "ratio": ratio_f,
                            "rule": "顯著負面（互動率大幅低於對照組），嚴格限制或禁止",
                        }
                    elif ratio_f < 0.90:
                        profile["feature_penalties"][feat_name] = {
                            "ratio": ratio_f,
                            "rule": "微弱負面，建議壓低使用頻率",
                        }
        except Exception as e:
            sys.stderr.write(f"[WARN] 載入泰勒絲存摺失敗: {e}\n")

    return profile


def generate_prompt_constraints(profile: dict | None = None) -> str:
    """生成動態注入至文案生成 Prompt 的硬性約束文字。"""
    if profile is None:
        profile = load_bionic_vaults()

    lines = [
        "### 🧠 內閣仿生學習即時動態約束 (Real Bionic Feedback Loop v6.2)",
        f"（本規範動態編譯自真實 Threads 貼文歷史真值，帳號中位數 ER: {profile['account_median_er']:.1f}%）",
        "",
    ]

    low_names = [h["hook"] for h in profile["low_hooks"]]
    boost_names = [h["hook"] for h in profile["boost_hooks"]]

    if low_names:
        lines.append(f"🚫 **【低成效開頭鉤子警示】**：{low_names}")
        for h in profile["low_hooks"]:
            mode_str = "硬性禁止" if h["n"] >= 5 else "軟性降權（樣本探索期）"
            lines.append(f"   - {mode_str}「{h['hook']}」（N={h['n']}，歷史平均 ER 僅 {h['avg_er']:.2f}%）")
    if boost_names:
        lines.append(f"⭐ **【優先推薦強化鉤子】**：{boost_names}")
        for h in profile["boost_hooks"]:
            lines.append(f"   - 推薦採用「{h['hook']}」（N={h['n']}，歷史平均 ER 高達 {h['avg_er']:.2f}%）或客觀情境白描")

    penalties = profile.get("feature_penalties", {})
    if penalties:
        lines.append("\n⚖️ **【內容型態物理約束】**：")
        for feat, data in penalties.items():
            lines.append(f"   - **{feat}**：存摺實測互動倍數 {data['ratio']:.2f} ➔ {data['rule']}")

    core_rules = bionic_enforce.load_active_rules("kage") + bionic_enforce.load_active_rules("taylor")
    if core_rules:
        lines.append("\n" + bionic_enforce.compile_constraints(core_rules))

    lines.append("\n🛡️ **【出廠安燈標準】**：內文無外部連結、無硬廣誘餌、字數 <= 500 字、總品質評分 >= 90 分。")
    return "\n".join(lines)


def audit_draft(
    text: str,
    persona: str = "meow",
    profile: dict | None = None,
    task_id: str | None = None,
    allow_unassigned: bool = False,
) -> tuple[int, list[str], list[tuple[str, str]]]:
    """執行結合仿生學習動態真值的出廠品質審計。"""
    if profile is None:
        profile = load_bionic_vaults()

    score = 0
    fatal: list[str] = []
    items: list[tuple[str, str]] = []

    if task_id:
        ok_tid, msg_tid = verify_task_id(task_id, persona=persona)
        if not ok_tid:
            fatal.append(msg_tid)
            items.append(("❌", f"派工單核驗失敗：{msg_tid}"))
        else:
            items.append(("✅", msg_tid))
    elif not allow_unassigned:
        msg_no_tid = "無單號不派工：未提供幕僚長派工單號 (--task-id T-YYYYMMDD-xxxxxx)"
        fatal.append(msg_no_tid)
        items.append(("❌", f"致命：{msg_no_tid}（若為無派工本機草稿自檢請加 --standalone-draft）"))

    clean_text = text.strip()
    if not clean_text:
        return 0, ["內容為空"], [("❌", "內容為空")]

    lines = [l.strip() for l in clean_text.split("\n") if l.strip()]

    # 1. 動態鉤子審計 (20 分)
    first_two = " ".join(lines[:2])
    low_hit_objs = [h for h in profile["low_hooks"] if h["hook"] in first_two[:25]]
    boost_hit = [h["hook"] for h in profile["boost_hooks"] if h["hook"] in first_two[:25]]

    if any(g in first_two for g in STALE_GREETINGS):
        score += 5
        items.append(("⚠️", "開頭為陳舊推銷/問候語，大幅降低停留率 (+5)"))
    elif low_hit_objs:
        # 【v6.5 修正】：未轉正之學習狀態檔僅採軟性降權提示，硬阻斷 100% 委託 bionic_enforce.gate() 留出驗證規則
        score += 8
        items.append(("⚠️", f"命中學習觀察期鉤子：{[h['hook'] for h in low_hit_objs]}（採軟性降權提示，硬阻斷依據母版留出集轉正規則）"))
    elif boost_hit:
        score += 20
        items.append(("✅", f"開頭採用仿生學習強化高成效鉤子：{boost_hit} (+20)"))
    else:
        score += 15
        items.append(("🟡", "開頭為標準白描，未踩坑 (+15)"))

    # 2. 呼吸感與排版 (20 分)
    avg_len = sum(len(l) for l in lines) / len(lines) if lines else 0
    if avg_len <= 25 and len(lines) >= 4:
        score += 20
        items.append(("✅", f"短句多換行呼吸感佳，平均每行 {avg_len:.1f} 字 (+20)"))
    elif avg_len > 35:
        score += 8
        items.append(("⚠️", f"平均每行 {avg_len:.1f} 字，段落過長產生閱讀壓迫 (+8)"))
    else:
        score += 15
        items.append(("🟡", f"排版正常，平均每行 {avg_len:.1f} 字 (+15)"))

    # 3. 零外鏈與無硬廣 (20 分)
    if re.search(r"https?://|www\.", clean_text):
        fatal.append("內文含外部連結（觸發演算法降權）")
        items.append(("❌", "致命：內文含外部連結 (+0)"))
    elif any(w in clean_text for w in HARD_SELL):
        score += 8
        items.append(("⚠️", "含促銷硬廣字眼，易引發受眾心理防禦 (+8)"))
    else:
        score += 20
        items.append(("✅", "零外鏈、無推銷硬廣 (+20)"))

    # 4. 人設與語言溫度 (20 分)
    has_boss = any(k in clean_text for k in BOSS_WORDS)
    has_cat = any(k in clean_text for k in CAT_WORDS)
    if persona == "meow":
        if "本貓" in clean_text:
            fatal.append("喵編誤用「本貓」（唯一法定自稱：本喵）")
            items.append(("❌", "致命：喵編誤用「本貓」"))
        elif has_boss and has_cat:
            score += 20
            items.append(("✅", "貓咪 × 闆仔雙簧人設飽滿 (+20)"))
        elif has_cat or "本喵" in clean_text:
            score += 16
            items.append(("✅", "喵編人設立體 (+16)"))
        else:
            score += 10
            items.append(("🟡", "喵編貼文未見貓咪特徵詞，人設較平 (+10)"))
    else:
        score += 20 if (has_boss or "小編" in clean_text or "管家" in clean_text) else 15
        items.append(("✅", "生活管家視角人設核驗通過 (+20)"))

    # 5. 結尾對話互動 (20 分)
    last_two = " ".join(lines[-2:])
    cta_words = ["？", "?", "舉手", "留言區", "告訴我", "回報", "哪一種", "還是"]
    if any(k in last_two for k in cta_words):
        score += 20
        items.append(("✅", "結尾具備開放式對話鉤子，誘發自然交流 (+20)"))
    else:
        score += 8
        items.append(("⚠️", "結尾缺乏交流出口 (+8)"))

    # 6. 泰勒絲真實特徵動態核查（100% 讀取存摺動態數值，零寫死常數）
    penalties = profile.get("feature_penalties", {})
    if "好奇提問句" in penalties:
        q_ratio = penalties["好奇提問句"]["ratio"]
        q_count = clean_text.count("？") + clean_text.count("?")
        if q_count > 2:
            score -= 10
            items.append(("⚠️", f"內文出現 {q_count} 個問號。泰勒絲存摺動態實測互動倍數為 {q_ratio:.2f}，過多反問引發疲乏 (-10)"))

    if "含Emoji" in penalties:
        e_ratio = penalties["含Emoji"]["ratio"]
        emoji_count = len(re.findall(r"[\U00010000-\U0010ffff]", clean_text))
        if emoji_count > 3:
            score -= 5
            items.append(("⚠️", f"內文含 {emoji_count} 個 Emoji。存摺動態實測互動倍數為 {e_ratio:.2f}，過多產生廉價感 (-5)"))

    # 7. 致命紅線檢查
    hits = [w for w in BAIT_WORDS if w in clean_text]
    if hits:
        fatal.append(f"含急迫/誘餌字眼：{', '.join(hits)}")
        items.append(("❌", f"致命：誘餌字眼 {hits}"))

    if len(clean_text) > 500:
        fatal.append(f"字數 {len(clean_text)} 超過 Threads 500 字上限")
        items.append(("❌", f"致命：字數 {len(clean_text)} > 500"))

    # 8. 母版 bionic_core (v6.2) 轉正規則與停機鎖強制同步檢核（Fail-Closed）
    for off in ("kage", "taylor"):
        ok, v_list = bionic_enforce.gate(off, clean_text)
        if not ok:
            for v_msg in v_list:
                fatal.append(f"[bionic_core/{off}] {v_msg}")
                items.append(("❌", f"bionic_core 阻斷 ({off})：{v_msg}"))

    final_score = max(0, min(100, score))
    return final_score, fatal, items


def main():
    ap = argparse.ArgumentParser(description="仿生學習閉環守門員 (v6.4 Fail-Closed & Mandatory Task-ID)")
    ap.add_argument("--file", help="草稿檔案路徑")
    ap.add_argument("--text", help="直接輸入草稿文字")
    ap.add_argument("--persona", default="meow", choices=["meow", "shadow"])
    ap.add_argument("--threshold", type=int, default=90)
    ap.add_argument("--task-id", help="必填（除 --standalone-draft 外）：核驗幕僚長雪之派工單號 (T-YYYYMMDD-xxxxxx)")
    ap.add_argument("--standalone-draft", action="store_true", help="本機無派工草稿預檢模式")
    ap.add_argument("--constraints", action="store_true", help="輸出提示詞動態負面約束")
    ap.add_argument("--json", action="store_true", help="以 JSON 格式輸出")
    a = ap.parse_args()

    profile = load_bionic_vaults()

    if a.constraints:
        print(generate_prompt_constraints(profile))
        sys.exit(0)

    if a.file:
        with open(a.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif a.text:
        text = a.text
    else:
        text = sys.stdin.read()

    score, fatal, items = audit_draft(
        text,
        a.persona,
        profile,
        task_id=a.task_id,
        allow_unassigned=a.standalone_draft,
    )

    if a.json:
        res = {
            "score": score,
            "threshold": a.threshold,
            "passed": (not fatal) and (score >= a.threshold),
            "fatal_errors": fatal,
            "audit_items": [{"level": lvl, "message": msg} for lvl, msg in items],
            "bionic_profile_used": {
                "account_median_er": profile["account_median_er"],
                "boost_hooks": [h["hook"] for h in profile["boost_hooks"]],
                "low_hooks": [h["hook"] for h in profile["low_hooks"]],
            },
        }
        print(json.dumps(res, ensure_ascii=False, indent=2))
        sys.exit(0 if res["passed"] else 1)

    print(f"\n================ 🛡️ 仿生學習出廠質量審計 (v6.2 Fail-Closed) ================")
    print(f"📊 綜合出廠評分：{score} / 100（標準門檻：{a.threshold}）")
    print(f"🧬 動態真值依據：影存摺(中位數ER {profile['account_median_er']}%) ✕ 泰勒絲行銷特徵")
    print("---------------------------------------------------------")
    for lvl, msg in items:
        print(f"  {lvl} {msg}")
    print("=========================================================")

    if fatal or score < a.threshold:
        print("\n🛑 【安燈硬阻斷·打回重寫】")
        if fatal:
            for err in fatal:
                print(f"  ❌ {err}")
        if score < a.threshold:
            print(f"  ⚠️ 分數 {score} 未達出廠標準 {a.threshold}")
        sys.exit(1)
    else:
        print("\n🟢 【安燈放行·符合標準】具備高停留率與真實溫度，准予出廠發布！\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
