#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-learning-synaptic-equation-engine: 突觸-代謝動態方程與全域激素場運算原子腳本
專職負責精算全域微分方程 Δw = η * Π_global * δ_verifier * e - λ_decay * w
"""

import sys
import os
import argparse
import json
import math

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def compute_hormonal_field(feedback: str) -> dict:
    """依據創辦人反饋映射全域激素場 Π_global"""
    dopamine_triggers = ["核准", "好", "讚", "通過", "同意", "准", "漂亮", "完美"]
    cortisol_triggers = ["叫停", "停", "錯", "糾正", "退回", "太粗", "不行", "重寫", "漏洞"]

    feedback_lower = feedback.lower()
    if any(t in feedback_lower for t in dopamine_triggers):
        pi_val = 1.85
        hormone_type = "多巴胺高位湧浪 (Dopamine Surge)"
        desc = "創辦人明確認可，注入全域多巴胺，強烈激勵活躍突觸權重！"
    elif any(t in feedback_lower for t in cortisol_triggers):
        pi_val = 0.35
        hormone_type = "皮質醇警報湧浪 (Cortisol Surge)"
        desc = "創辦人示警叫停，注入全域皮質醇，加速陳舊假說衰減自噬！"
    else:
        pi_val = 1.0
        hormone_type = "中性體內穩態 (Homeostatic Neutral)"
        desc = "常規推論無外源激素刺激，保持標準突觸更新節奏。"

    return {"pi_global": pi_val, "type": hormone_type, "desc": desc}

def calculate_synaptic_update(
    weight: float,
    founder_feedback: str,
    prm_score: float = 1.0,
    trace_e: float = 1.0,
    learning_rate: float = 0.05,
    decay_rate: float = 0.02
) -> dict:
    """精算突觸權重增量 Δw"""
    hormone = compute_hormonal_field(founder_feedback)
    pi_val = hormone["pi_global"]

    # 方程主體：Δw = η * Π_global * δ_verifier * e - λ_decay * w
    potentiation = learning_rate * pi_val * prm_score * trace_e
    depression = decay_rate * weight
    delta_w = potentiation - depression

    new_weight = max(0.0, min(1.0, weight + delta_w))

    # 模組命運判定
    if new_weight >= 0.70:
        fate = "ACTIVE_STRENGTHENED (高活躍核心 · 固化常駐)"
    elif new_weight >= 0.35:
        fate = "MAINTAINED (穩態維持 · 中層調用)"
    else:
        fate = "AUTOPHAGIC_PRUNED (溶酶體自噬 · 移入深層冷庫)"

    return {
        "initial_weight": round(weight, 4),
        "founder_feedback": founder_feedback,
        "hormonal_field": hormone,
        "prm_score": round(prm_score, 4),
        "trace_e": round(trace_e, 4),
        "learning_rate_eta": learning_rate,
        "decay_rate_lambda": decay_rate,
        "potentiation_term": round(potentiation, 4),
        "depression_term": round(depression, 4),
        "delta_w": round(delta_w, 4),
        "new_weight": round(new_weight, 4),
        "synaptic_fate": fate
    }

def main():
    parser = argparse.ArgumentParser(description="突觸-代謝動態方程與全域激素場運算原子")
    parser.add_argument("--founder-feedback", type=str, default="核准", help="創辦人指令/情感反饋")
    parser.add_argument("--prm-score", type=float, default=1.0, help="PRM 物理客觀評分 (0.0~1.0)")
    parser.add_argument("--weight", type=float, default=0.75, help="當前突觸權重 w (0.0~1.0)")
    parser.add_argument("--trace-e", type=float, default=1.0, help="因果活動合格跡 (0.0~1.0)")
    parser.add_argument("--learning-rate", type=float, default=0.05, help="學習率 eta")
    parser.add_argument("--decay-rate", type=float, default=0.02, help="溶酶體衰減率 lambda")

    args = parser.parse_args()

    print("=== [atom-learning-synaptic-equation-engine] 啟動全域突觸代謝方程精算 ===")
    res = calculate_synaptic_update(
        weight=args.weight,
        founder_feedback=args.founder_feedback,
        prm_score=args.prm_score,
        trace_e=args.trace_e,
        learning_rate=args.learning_rate,
        decay_rate=args.decay_rate
    )

    print(f"\n創辦人反饋: 『{res['founder_feedback']}』 ➔ 全域激素場: {res['hormonal_field']['type']} (Π = {res['hormonal_field']['pi_global']})")
    print(f"計算公式: Δw = η({res['learning_rate_eta']}) * Π({res['hormonal_field']['pi_global']}) * δ({res['prm_score']}) * e({res['trace_e']}) - λ({res['decay_rate_lambda']}) * w({res['initial_weight']})")
    print(f"增益項 (Potentiation): +{res['potentiation_term']} | 衰減項 (Depression): -{res['depression_term']}")
    print(f"權重淨變化 (Δw): {res['delta_w']:+} ➔ 新突觸權重 (w_new): {res['new_weight']}")
    print(f"突觸命運裁決: {res['synaptic_fate']}")

    print("\n[+] 突觸代謝微分方程精算完成 (Exit Code: 0)！")
    sys.exit(0)

if __name__ == "__main__":
    main()
