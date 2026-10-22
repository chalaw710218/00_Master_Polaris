"""
Polaris Bionic Learning System - Cycle 05 Code-as-Memory Module
Title: Stigmergy Swarm Router (Indirect Pheromone Coordination for Multi-Agent Swarms)
Reference: Pierre-Paul Grassé (1959), Marco Dorigo (Ant Colony Optimization 1992 / Nature)
Architecture: Environmental Modification -> Digital Pheromone Gradient -> Autonomous Swarm Convergence
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class DigitalPheromone:
    channel: str
    target_node: str
    intensity: float
    last_updated: float
    evaporation_rate: float = 0.05  # 揮發衰減率

class StigmergySwarmRouter:
    """
    仿生 Stigmergy 費洛蒙間接通訊路由器 (Polaris Edition)
    不依賴中央單點瓶頸式調度，所有 Agent 透過在工作區留存與感知「數位費洛蒙梯度」進行自組織協作。
    """
    def __init__(self, swarm_name: str):
        self.swarm_name = swarm_name
        self.pheromones: Dict[str, DigitalPheromone] = {}

    def _key(self, channel: str, node: str) -> str:
        return f"{channel}:{node}"

    def deposit_pheromone(self, channel: str, target_node: str, delta_intensity: float):
        """留存/強化數位費洛蒙（正向回饋）"""
        k = self._key(channel, target_node)
        now = time.time()
        if k in self.pheromones:
            p = self.pheromones[k]
            # 先計算自然揮發
            elapsed = now - p.last_updated
            p.intensity = p.intensity * ((1.0 - p.evaporation_rate) ** elapsed) + delta_intensity
            p.last_updated = now
        else:
            self.pheromones[k] = DigitalPheromone(
                channel=channel,
                target_node=target_node,
                intensity=delta_intensity,
                last_updated=now
            )

    def sense_gradient(self, channel: str) -> List[DigitalPheromone]:
        """感知特定通道中的費洛蒙梯度排序（高強度優先湧現）"""
        now = time.time()
        active = []
        for p in self.pheromones.values():
            if p.channel == channel:
                elapsed = now - p.last_updated
                curr_intensity = p.intensity * ((1.0 - p.evaporation_rate) ** elapsed)
                if curr_intensity > 0.01:
                    p.intensity = curr_intensity
                    p.last_updated = now
                    active.append(p)
        active.sort(key=lambda x: x.intensity, reverse=True)
        return active

if __name__ == "__main__":
    router = StigmergySwarmRouter("Polaris_Cabinet_Swarm")
    # 泰勒絲在行銷發行通道留存熱度費洛蒙
    router.deposit_pheromone("Promotion_Task", "Task_Womens_Curator_Post", 5.0)
    router.deposit_pheromone("Promotion_Task", "Task_Frozen_Edamame_Push", 2.0)

    # 喵編與特務影感知環境費洛蒙梯度，自動鎖定最火熱的節點
    hot_nodes = router.sense_gradient("Promotion_Task")
    print("Sensed Pheromone Gradients:")
    for h in hot_nodes:
        print(f" Node: {h.target_node} | Intensity: {h.intensity:.3f}")
