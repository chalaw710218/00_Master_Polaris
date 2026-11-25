#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
synaptic_metabolic_learner.py - 影之突觸代謝與殘酷遺忘自噬引擎
版權所有 (c) 2026 極星內閣 - 首席特務兼生活管家影 (Kage)
"""

import sys
import json
import argparse

# 強制 Windows 環境標準輸出採用 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def calculate_synaptic_update(data: dict) -> dict:
    """計算神經突觸權重更新與溶酶體代謝自噬"""
    tid = data.get("template_id", "TEMPLATE_DEFAULT")
    views = data.get("views", 0)
    profile_visits = data.get("profile_visits", 0)
    net_followers = data.get("net_followers", 0)
    replies = data.get("replies", 0)
    consecutive_low = data.get("consecutive_low_count", 0)
    founder_approval = data.get("founder_approval", None)
    
    # 1. 創辦人激素場 Pi
    if founder_approval is True:
        pi = 1.8  # 多巴胺爆發
        pi_status = "DOPAMINE_BOOST (創辦人認可)"
    elif founder_approval is False:
        pi = 0.3  # 皮質醇警示
        pi_status = "CORTISOL_BRAKE (創辦人叫停糾偏)"
    else:
        pi = 1.0  # 中性自然演化
        pi_status = "NEUTRAL_FIELD"
        
    # 2. 檢驗低效連續計數
    is_low_performing = (views < 30 and replies == 0)
    if is_low_performing:
        consecutive_low += 1
    else:
        consecutive_low = 0
        
    # 3. 溶酶體代謝自噬三振判決 (Three-Strike Autophagy)
    if consecutive_low >= 3:
        return {
            "template_id": tid,
            "status": "AUTOPHAGY_PURGED (溶酶體殘酷自噬淘汰)",
            "synaptic_weight": 0.0,
            "consecutive_low_count": consecutive_low,
            "hormonal_field": pi_status,
            "action_directive": (
                f"模板 '{tid}' 連續 {consecutive_low} 次發布表現平淡 (<30瀏覽且無人互動)！"
                f"溶酶體機制已強制清空該模板突觸權重，實施殘酷遺忘，嚴禁炒冷飯！"
            ),
            "kage_resolution": "已遺忘失效死知識，清空大腦緩衝區，重構真實生活切片！"
        }
        
    # 4. 正常突觸權重強化計算
    conversion_rate = (net_followers / profile_visits) if profile_visits > 0 else 0.0
    engagement_rate = (replies / views) if views > 0 else 0.0
    
    # delta_verifier: 綜合表現評分 (0.0 ~ 2.0)
    delta_v = (conversion_rate * 5.0) + (engagement_rate * 10.0) + (min(views, 500) / 500.0)
    weight_gain = 0.1 * pi * delta_v
    
    return {
        "template_id": tid,
        "status": "SYNAPSE_STRENGTHENED (突觸強化刻印)",
        "weight_gain": round(weight_gain, 4),
        "consecutive_low_count": consecutive_low,
        "telemetry_metrics": {
            "views": views,
            "profile_visits": profile_visits,
            "net_followers": net_followers,
            "profile_conversion_rate": f"{conversion_rate:.1%}",
            "replies": replies
        },
        "hormonal_field": pi_status,
        "action_directive": (
            f"成功提煉核心基因！轉化率達 {conversion_rate:.1%}，"
            f"在 {pi_status} 沐浴下，神經突觸獲得 +{weight_gain:.4f} 權重增長！"
        ),
        "kage_resolution": "持續將此真實生活切片與互動神韻沉澱為永久肌肉記憶！"
    }

def main():
    parser = argparse.ArgumentParser(description="影之突觸代謝與殘酷遺忘自噬引擎")
    parser.add_argument("--update-synapse", type=str, required=True, help="貼文遙測數據 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.update_synapse)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = calculate_synaptic_update(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
