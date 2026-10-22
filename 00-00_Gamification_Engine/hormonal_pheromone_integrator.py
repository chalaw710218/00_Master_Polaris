"""
Polaris Bionic Learning System v4.0 - Iteration 04 Code-as-Memory Module
Title: Hormonal-Pheromone Environmental Field Integrator
Reference: Guy Theraulaz & Eric Bonabeau (Neuromodulated Swarm Stigmergy)
Architecture: Founder Reaction Bath -> Global Pheromone Half-Life & Gain Modulation -> Swarm Coordination
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class SwarmPheromoneChannel:
    channel_name: str
    base_intensity: float
    current_effective_intensity: float
    last_pulsed: float

class HormonalPheromoneIntegrator:
    """
    極星全域激素-費洛蒙場整合器
    將創辦人（品碩）的情緒場作為調質浴，動態放大或抑制分散式工作區中的數位費洛蒙傳播。
    """
    def __init__(self):
        self.channels: Dict[str, SwarmPheromoneChannel] = {}
        self.dopamine_level: float = 1.0  # 多巴胺 (認可)
        self.cortisol_level: float = 0.0  # 皮質醇 (警報)

    def register_channel(self, name: str, initial_intensity: float = 1.0):
        self.channels[name] = SwarmPheromoneChannel(
            channel_name=name,
            base_intensity=initial_intensity,
            current_effective_intensity=initial_intensity,
            last_pulsed=time.time()
        )

    def infuse_founder_feedback(self, feedback_text: str):
        """解析品碩回饋，更新激素浴濃度"""
        if any(w in feedback_text for w in ["好", "請", "讚", "可以", "推"]):
            self.dopamine_level = 1.8
            self.cortisol_level = 0.0
        elif any(w in feedback_text for w in ["停", "錯", "不行", "別"]):
            self.dopamine_level = 0.2
            self.cortisol_level = 1.5
        else:
            self.dopamine_level = 1.0
            self.cortisol_level = 0.0

        # 全域調質所有費洛蒙通道
        now = time.time()
        for ch in self.channels.values():
            if self.cortisol_level > 0.5:
                # 皮質醇加速費洛蒙揮發 (壓制錯誤路徑)
                ch.current_effective_intensity = ch.base_intensity * 0.1
            else:
                # 多巴胺增益活躍通道
                ch.current_effective_intensity = ch.base_intensity * self.dopamine_level
            ch.last_pulsed = now

    def get_effective_gradient(self) -> Dict[str, float]:
        return {k: v.current_effective_intensity for k, v in self.channels.items()}

if __name__ == "__main__":
    integrator = HormonalPheromoneIntegrator()
    integrator.register_channel("Promotion_Taitung_Edamame", 2.0)
    integrator.register_channel("Logistics_Route_Night_Run", 1.5)

    integrator.infuse_founder_feedback("請繼續，這個節奏非常好！")
    grad = integrator.get_effective_gradient()
    print(f"[Iter 04 Passed] Hormonal Gradient (Dopamine Enhanced): {grad}")
