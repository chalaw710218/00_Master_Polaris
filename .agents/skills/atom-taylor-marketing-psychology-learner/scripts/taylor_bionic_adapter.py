"""泰勒絲 (Taylor) 專屬仿生特化轉接器 (Role-Specific Adapter)
職責：執行泰勒絲的行銷特徵學習腳本，依消費者心理學與敘事特徵提名候選規則，輸出標準 JSON 供萬用母版 bionic_core 驗算。
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


def main() -> None:
    learn_script = SCRIPT_DIR / "taylor_real_learning.py"
    state_file = SKILL_DIR / "vaults" / "taylor_marketing_state.json"
    if learn_script.exists():
        res = subprocess.run([sys.executable, str(learn_script), "--learn"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        if res.returncode != 0:
            sys.stderr.write(res.stderr or res.stdout)
            sys.exit(1)
    if not state_file.exists():
        sys.stderr.write(f"找不到狀態檔：{state_file}\n")
        sys.exit(1)

    data = json.loads(state_file.read_text(encoding="utf-8"))
    feats = data.get("feature_results", {})
    proposals = []

    q_stat = feats.get("好奇提問句", {})
    if q_stat.get("信心") == "OK" and q_stat.get("互動率倍數(有/無)", 1.0) < 0.75:
        ratio = q_stat["互動率倍數(有/無)"]
        n_q = int(q_stat.get("有此特徵", {}).get("n", 3))
        proposals.append({
            "kind": "regex_forbid",
            "pattern": r"^[^\n]{0,45}[？?]",
            "scope": "any",
            "risk": "low",
            "source_url": str(data.get("source", "insights_history.jsonl")),
            "tier": "A",
            "evidence": f"泰勒絲真實特徵矩陣：開頭首行反問句互動率倍數僅 {ratio}，禁止首行 45 字內使用反問句",
            "confidence": min(0.95, round(0.50 + n_q * 0.04, 2)),
        })

    w_stat = feats.get("天氣題材", {})
    if w_stat.get("信心") == "OK" and w_stat.get("互動率倍數(有/無)", 1.0) < 0.75:
        w_ratio = w_stat["互動率倍數(有/無)"]
        n_w = int(w_stat.get("有此特徵", {}).get("n", 3))
        proposals.append({
            "kind": "regex_forbid",
            "pattern": r"氣象預報|陸警|海警|颱風動態|豪雨特報|降雨機率",
            "scope": "any",
            "risk": "low",
            "source_url": str(data.get("source", "insights_history.jsonl")),
            "tier": "A",
            "evidence": f"泰勒絲真實特徵矩陣：純天氣播報題材互動率倍數僅 {w_ratio}（已收斂正則避免誤傷常民詞彙）",
            "confidence": min(0.95, round(0.50 + n_w * 0.04, 2)),
        })

    out = {
        "office": "taylor",
        "meta": {"state_file": str(state_file), "learned_at": data.get("learned_at")},
        "proposals": proposals,
    }
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
