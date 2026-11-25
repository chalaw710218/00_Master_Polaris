#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vault_hypothesis_reflector.py - 影之選題假設實驗與認知存摺反思引擎
版權所有 (c) 2026 極星內閣 - 首席特務兼生活管家影 (Kage)
"""

import sys
import json
import argparse
from datetime import datetime

# 強制 Windows 環境標準輸出採用 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def process_hypothesis_reflection(data: dict) -> dict:
    """處理貼文假設驗證並產出認知存摺反思刻印記錄"""
    hid = data.get("hypothesis_id", "EXP_UNKNOWN")
    topic = data.get("topic", "未命名題材")
    hook = data.get("assumed_hook", "")
    exp_rate = data.get("expected_profile_visit_rate", 0.04)
    views = data.get("actual_views", 0)
    visits = data.get("actual_profile_visits", 0)
    followers = data.get("actual_net_followers", 0)
    top_comment = data.get("top_comment", "無特殊留言")
    
    act_visit_rate = (visits / views) if views > 0 else 0.0
    act_follow_rate = (followers / visits) if visits > 0 else 0.0
    
    is_confirmed = act_visit_rate >= exp_rate
    verdict = "HYPOTHESIS_CONFIRMED (假設成立)" if is_confirmed else "HYPOTHESIS_REFUTED (假設被駁回)"
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 產出刻印用 Markdown 片段
    markdown_entry = (
        f"### [{now_str}] 實驗反思 #{hid}：{topic}\n"
        f"* **選題假設鉤子**：『{hook}』\n"
        f"* **預期轉化率**：主頁造訪率 $\\ge {exp_rate:.1%}$\n"
        f"* **實測物理數據**：瀏覽 {views} 次 ➔ 主頁造訪 {visits} 次 ({act_visit_rate:.1%}) ➔ 淨增粉 {followers} 人 ({act_follow_rate:.1%})\n"
        f"* **假設檢定判定**：**{verdict}**\n"
        f"* **代表性讀者迴響**：「{top_comment}」\n"
        f"* **影的自主學習總結**："
        f"{( '此生活反差白描精準擊中讀者好奇心，成功引流主頁，固化為常態神經突觸！' if is_confirmed else '此鉤子未能激發足夠造訪慾望，列入代謝清單，下次強化情境張力。' )}\n"
    )

    return {
        "hypothesis_id": hid,
        "topic": topic,
        "assumed_hook": hook,
        "verdict": verdict,
        "performance": {
            "expected_visit_rate": f"{exp_rate:.1%}",
            "actual_visit_rate": f"{act_visit_rate:.1%}",
            "actual_views": views,
            "actual_profile_visits": visits,
            "actual_net_followers": followers
        },
        "vault_markdown_entry": markdown_entry,
        "kage_autonomous_reflection": "科學假設驗證完成，反思結論已準備沉澱入認知存摺！"
    }

def main():
    parser = argparse.ArgumentParser(description="影之選題假設實驗與認知存摺反思引擎")
    parser.add_argument("--reflect-experiment", type=str, required=True, help="實驗與實測數據 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.reflect_experiment)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = process_hypothesis_reflection(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
