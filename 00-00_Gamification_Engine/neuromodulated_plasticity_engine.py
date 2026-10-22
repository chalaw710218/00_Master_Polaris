"""
Polaris Bionic Learning System - Cycle 09 Code-as-Memory Module
Title: Neuromodulated Plasticity Engine (Three-Factor Synaptic Plasticity & Founder Alignment)
Reference: Wolfram Gerstner, Richard Kempter et al. (Frontiers in Synaptic Neuroscience 2018)
Architecture: Synaptic Weight Update: dw = eta * Pi * delta * e
"""

from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class SynapticTrace:
    action_key: str
    weight: float
    eligibility_trace: float = 0.0

class NeuromodulatedPlasticityEngine:
    """
    仿生三因子突觸可塑性引擎 (Polaris Edition)
    嚴格實踐 dw = eta * Pi * delta * e，將創辦人（品碩）的情緒與裁示直接映射為神經調質因子 Pi。
    """
    def __init__(self, learning_rate: float = 0.1, gamma_decay: float = 0.85):
        self.eta = learning_rate
        self.gamma = gamma_decay
        self.synapses: Dict[str, SynapticTrace] = {}

    def get_or_create_synapse(self, key: str, initial_weight: float = 1.0) -> SynapticTrace:
        if key not in self.synapses:
            self.synapses[key] = SynapticTrace(action_key=key, weight=initial_weight)
        return self.synapses[key]

    def record_action_eligibility(self, key: str, activity_impulse: float):
        """更新活動合格跡 e：標記特定決策或行為的因果貢獻"""
        syn = self.get_or_create_synapse(key)
        syn.eligibility_trace = syn.eligibility_trace * self.gamma + activity_impulse

    def parse_founder_neuromodulator(self, founder_reaction: str) -> float:
        """
        解析品碩的回饋為神經調質因子 Pi:
        - 點頭/認可/請/好 -> 正向多巴胺 (+1.5 ~ +2.0)
        - 中性/無意見 -> 基準 (1.0)
        - 質疑/叫停/糾正 -> 皮質醇抑制 (-1.5 ~ -2.0)
        """
        positive_tokens = ["請", "好", "可以", "讚", "認可", "很好", "推", "漂亮"]
        negative_tokens = ["停", "錯", "不行", "別再", "亂搞", "不准", "爛", "刪掉"]

        for t in positive_tokens:
            if t in founder_reaction:
                return 1.8  # Dopamine boost
        for t in negative_tokens:
            if t in founder_reaction:
                return -1.5  # Cortisol suppression
        return 1.0

    def apply_synaptic_update(self, key: str, founder_reaction: str, prediction_error: float) -> float:
        """
        計算突觸權重更新：dw = eta * Pi * delta * e
        """
        syn = self.get_or_create_synapse(key)
        pi = self.parse_founder_neuromodulator(founder_reaction)
        delta_w = self.eta * pi * prediction_error * syn.eligibility_trace
        syn.weight += delta_w
        # 衰減合格跡
        syn.eligibility_trace *= self.gamma
        return syn.weight

if __name__ == "__main__":
    brain = NeuromodulatedPlasticityEngine(learning_rate=0.1)
    
    # 決策 A：闆仔風格文案（真實零表情符號）
    brain.record_action_eligibility("Action_Boss_Zero_Emoji", activity_impulse=1.0)
    # 模擬品碩反饋「很好，就照這個做！」且實際訂單轉換超出預期 (delta = 0.8)
    new_w1 = brain.apply_synaptic_update("Action_Boss_Zero_Emoji", "很好，就照這個做！", prediction_error=0.8)

    # 決策 B：網路浮誇農場標題文案
    brain.record_action_eligibility("Action_Clickbait_Copy", activity_impulse=1.0)
    # 模擬品碩反饋「停！不要搞這種廉價叫賣！」(皮質醇抑制)
    new_w2 = brain.apply_synaptic_update("Action_Clickbait_Copy", "停！不要搞這種廉價叫賣！", prediction_error=0.5)

    print("Synaptic Plasticity Weights:")
    print(f" Action_Boss_Zero_Emoji: {new_w1:.4f} (Dopamine Reinforced)")
    print(f" Action_Clickbait_Copy:  {new_w2:.4f} (Cortisol Suppressed)")
