"""仿生學習閉環守門員 (Bionic Closed-Loop Gatekeeper)

核心使命：
徹底終結「只記日記、不改行為」的假自進化斷頭路！
動態載入影 (Kage) 與泰勒絲 (Taylor) 的真實歷史存摺：
  - kage_synaptic_state.json (鉤子真值與時段表現)
  - taylor_marketing_state.json (行銷特徵因果矩陣)
將真值轉化為：
  1. 提示詞動態負面約束 (Prompt Negative Constraints)
  2. 發布前物理安燈硬阻斷 (Pre-Flight Hard Interception)

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
    return Path.cwd()


ROOT = find_workspace_root()
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

# 基礎通用合規黑名單（物理不可碰觸紅線）
BAIT_WORDS = ["留言+1", "留言 +1", "+1", "快來買", "限時搶購", "限時", "搶購", "手慢無", "最後機會", "錯過可惜"]
HARD_SELL = ["特價", "滿千免運", "點擊購買", "下單連結", "優惠碼"]
STALE_GREETINGS = ["大家好", "哈囉大家", "今天小編要", "推薦大家"]
BOSS_WORDS = ["闆仔", "老闆", "品碩"]
CAT_WORDS = ["喵", "貓", "本喵", "罐罐", "爪"]


def load_bionic_vaults() -> dict:
    """載入影與泰勒絲的真實學習存摺並提取行為約束準則。"""
    profile = {
        "kage_loaded": False,
        "taylor_loaded": False,
        "account_median_er": 2.0,
        "boost_hooks": [],  # 高成效鉤子 (ER >= median * 1.3, confidence OK)
        "low_hooks": [],    # 低成效鉤子 (ER < median * 0.7, confidence OK)
        "feature_penalties": {},  # 特徵懲罰
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
                conf = stat.get("confidence", "")
                avg_er = float(stat.get("avg_er", 0.0))
                if conf == "OK":
                    if avg_er >= median_er * 1.3:
                        profile["boost_hooks"].append({
                            "hook": hook,
                            "avg_er": avg_er,
                            "n": stat.get("n", 0)
                        })
                    elif avg_er < median_er * 0.7:
                        profile["low_hooks"].append({
                            "hook": hook,
                            "avg_er": avg_er,
                            "n": stat.get("n", 0)
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
                conf = stat.get("confidence", "")
                ratio = stat.get("互動率倍數(有/無)")
                if conf == "OK" and ratio is not None:
                    if ratio < 0.75:
                        profile["feature_penalties"][feat_name] = {
                            "ratio": ratio,
                            "rule": "顯著負面（互動率大幅低於對照組），嚴格限制或禁止"
                        }
                    elif ratio < 0.90:
                        profile["feature_penalties"][feat_name] = {
                            "ratio": ratio,
                            "rule": "微弱負面，建議壓低使用頻率"
                        }
        except Exception as e:
            sys.stderr.write(f"[WARN] 載入泰勒絲存摺失敗: {e}\n")

    return profile


def generate_prompt_constraints(profile: dict | None = None) -> str:
    """生成動態注入至文案生成 Prompt 的硬性約束文字。"""
    if profile is None:
        profile = load_bionic_vaults()

    lines = [
        "### 🧠 內閣仿生學習即時動態約束 (Real Bionic Feedback Loop)",
        f"（本規範動態編譯自真實 Threads 貼文歷史真值，帳號中位數 ER: {profile['account_median_er']:.1f}%）",
        "",
    ]

    # 1. 鉤子約束
    low_names = [h["hook"] for h in profile["low_hooks"]]
    boost_names = [h["hook"] for h in profile["boost_hooks"]]

    if low_names:
        lines.append(f"🚫 **【硬性禁止開頭鉤子】**：{low_names}")
        for h in profile["low_hooks"]:
            lines.append(f"   - 嚴禁使用「{h['hook']}」（歷史平均 ER 僅 {h['avg_er']:.2f}%，大幅拉低互動）")
    if boost_names:
        lines.append(f"⭐ **【優先推薦強化鉤子】**：{boost_names}")
        for h in profile["boost_hooks"]:
            lines.append(f"   - 推薦採用「{h['hook']}」（歷史平均 ER 高達 {h['avg_er']:.2f}%）或客觀情境白描")

    # 2. 泰勒絲行銷特徵約束
    penalties = profile.get("feature_penalties", {})
    if penalties:
        lines.append("\n⚖️ **【內容型態物理約束】**：")
        for feat, data in penalties.items():
            lines.append(f"   - **{feat}**：互動倍數僅 {data['ratio']:.2f} ➔ {data['rule']}")

    lines.append("\n🛡️ **【出廠安燈標準】**：內文無外部連結、無硬廣誘餌、字數 <= 500 字、總品質評分 >= 90 分。")
    return "\n".join(lines)


def audit_draft(text: str, persona: str = "meow", profile: dict | None = None) -> tuple[int, list[str], list[tuple[str, str]]]:
    """執行結合仿生學習動態真值的出廠品質審計。

    回傳：(score, fatal_errors, audit_items)
    """
    if profile is None:
        profile = load_bionic_vaults()

    score = 0
    fatal: list[str] = []
    items: list[tuple[str, str]] = []

    clean_text = text.strip()
    if not clean_text:
        return 0, ["內容為空"], [("❌", "內容為空")]

    lines = [l.strip() for l in clean_text.split("\n") if l.strip()]

    # 1. 動態鉤子審計 (20 分)
    first_two = " ".join(lines[:2])
    low_hit = [h["hook"] for h in profile["low_hooks"] if h["hook"] in first_two]
    boost_hit = [h["hook"] for h in profile["boost_hooks"] if h["hook"] in first_two]

    if any(g in first_two for g in STALE_GREETINGS):
        score += 5
        items.append(("⚠️", "開頭為陳舊推銷/問候語，大幅降低停留率 (+5)"))
    elif low_hit:
        # 命中歷史低效鉤子（如「我就問」）
        score += 2
        items.append(("❌", f"命中仿生學習低成效黑名單鉤子：{low_hit}（歷史數據證實大幅拉低 ER，僅給 +2）"))
        fatal.append(f"使用歷史低效鉤子 {low_hit}，請改用強化鉤子或情境白描")
    elif boost_hit:
        score += 20
        items.append(("✅", f"開頭採用仿生學習強化高成效鉤子：{boost_hit} (+20)"))
    else:
        # 一般正常白描
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
        # shadow / general
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

    # 6. 泰勒絲真實特徵動態核查 (扣分項)
    penalties = profile.get("feature_penalties", {})
    if "好奇提問句" in penalties:
        # 若內文包含大量提問句（> 2 個問號）
        q_count = clean_text.count("？") + clean_text.count("?")
        if q_count > 2:
            score -= 10
            items.append(("⚠️", f"內文出現 {q_count} 個問號。泰勒絲實測好奇提問句互動倍數僅 0.48，過多反問引發疲乏 (-10)"))

    if "含Emoji" in penalties:
        # 計算 Emoji 數量（簡單以常見 Emoji Unicode 範圍偵測）
        emoji_count = len(re.findall(r"[\U00010000-\U0010ffff]", clean_text))
        if emoji_count > 3:
            score -= 5
            items.append(("⚠️", f"內文含 {emoji_count} 個 Emoji。實測 Emoji 互動倍數僅 0.82，過多產生廉價感 (-5)"))

    # 7. 致命紅線檢查
    hits = [w for w in BAIT_WORDS if w in clean_text]
    if hits:
        fatal.append(f"含急迫/誘餌字眼：{', '.join(hits)}")
        items.append(("❌", f"致命：誘餌字眼 {hits}"))

    if len(clean_text) > 500:
        fatal.append(f"字數 {len(clean_text)} 超過 Threads 500 字上限")
        items.append(("❌", f"致命：字數 {len(clean_text)} > 500"))

    final_score = max(0, min(100, score))
    return final_score, fatal, items


def main():
    ap = argparse.ArgumentParser(description="仿生學習閉環守門員")
    ap.add_argument("--file", help="草稿檔案路徑")
    ap.add_argument("--text", help="直接輸入草稿文字")
    ap.add_argument("--persona", default="meow", choices=["meow", "shadow"])
    ap.add_argument("--threshold", type=int, default=90)
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

    score, fatal, items = audit_draft(text, a.persona, profile)

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
            }
        }
        print(json.dumps(res, ensure_ascii=False, indent=2))
        sys.exit(0 if res["passed"] else 1)

    print(f"\n================ 🛡️ 仿生學習出廠質量審計 ================")
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
