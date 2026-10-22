"""
Polaris Bionic Learning System v4.0 - Iteration 01 Code-as-Memory Module
Title: Expected Free Energy (EFE) Router for Active Inference
Reference: Karl Friston, Thomas Parr, Giovanni Pezzulo (MIT Press 2022)
Formula: G(pi) = Pragmatic Value (Goal Alignment) + Epistemic Value (Uncertainty Reduction / Curiosity)
"""

import math
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ActionPolicy:
    policy_id: str
    description: str
    expected_margin: float       # 實用價值：目標達成預期
    target_margin: float         # 創辦人預期基準
    uncertainty_entropy: float   # 認識價值：對未知環境的資訊增益潛力

class ExpectedFreeEnergyRouter:
    """
    仿生預期自由能 (EFE) 決策路由
    根據 G(pi) = Pragmatic Value + Epistemic Value 自動權衡「確定性收益」與「好奇心探索」。
    """
    def __init__(self, epistemic_weight: float = 0.5):
        self.gamma_epistemic = epistemic_weight

    def calculate_efe(self, policy: ActionPolicy) -> float:
        # Pragmatic Value: 偏離創辦人目標的懲罰（負值越大越差）
        pragmatic_val = - abs(policy.expected_margin - policy.target_margin)
        # Epistemic Value: 消除不確定性之資訊增益 (Shannon Entropy reduction)
        epistemic_val = self.gamma_epistemic * policy.uncertainty_entropy
        # Expected Free Energy: 最小化 G(pi)
        efe_score = -(pragmatic_val + epistemic_val)
        return efe_score

    def select_optimal_policy(self, policies: List[ActionPolicy]) -> ActionPolicy:
        # 尋找自由能最小的政策 (Minimizing EFE)
        best_policy = min(policies, key=lambda p: self.calculate_efe(p))
        return best_policy

if __name__ == "__main__":
    router = ExpectedFreeEnergyRouter(epistemic_weight=0.8)
    p1 = ActionPolicy("Policy_Conservative_Reorder", "維持原樣進貨已知特產", expected_margin=0.25, target_margin=0.30, uncertainty_entropy=0.1)
    p2 = ActionPolicy("Policy_Exploratory_Sourcing", "探索台東深山未知野生香料", expected_margin=0.28, target_margin=0.30, uncertainty_entropy=0.9)

    best = router.select_optimal_policy([p1, p2])
    print(f"[Iter 01 Passed] Optimal Policy: {best.policy_id} ({best.description})")
