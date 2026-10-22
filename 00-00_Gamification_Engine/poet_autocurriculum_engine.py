"""
Polaris Bionic Learning System - Cycle 04 Code-as-Memory Module
Title: POET Auto-Curriculum Engine (Open-Ended Environment-Agent Co-Evolution)
Reference: Rui Wang, Jeff Clune et al., Uber AI Labs (ICML 2019 / NeurIPS 2020)
Architecture: Environmental Exploration -> Stepping Stone Discovery -> Cross-Environment Transfer
"""

import random
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class EnvironmentNiche:
    env_id: str
    difficulty: float
    parameters: Dict[str, Any]
    active_agent_id: Optional[str] = None
    best_score: float = 0.0

@dataclass
class AgentGenome:
    agent_id: str
    skills: List[str]
    fitness_history: Dict[str, float] = field(default_factory=dict)

class POETAutoCurriculumEngine:
    """
    仿生 POET 開放式課程演化引擎 (Polaris Edition)
    遵循環境與智能體共同演化（Co-Evolution），透過跨環境轉移（Transfer）打破局部最佳解。
    """
    def __init__(self, task_domain: str):
        self.task_domain = task_domain
        self.environments: Dict[str, EnvironmentNiche] = {}
        self.agents: Dict[str, AgentGenome] = {}
        self.transfer_log: List[str] = []

    def create_environment(self, env_id: str, difficulty: float, params: Dict[str, Any]) -> EnvironmentNiche:
        env = EnvironmentNiche(env_id=env_id, difficulty=difficulty, parameters=params)
        self.environments[env_id] = env
        return env

    def register_agent(self, agent_id: str, skills: List[str]) -> AgentGenome:
        agent = AgentGenome(agent_id=agent_id, skills=skills)
        self.agents[agent_id] = agent
        return agent

    def evaluate(self, agent: AgentGenome, env: EnvironmentNiche) -> float:
        """模擬評估：技能匹配度與環境難度之間的適應度"""
        match_power = sum(1.0 for s in agent.skills if s in env.parameters.get("required_skills", []))
        score = match_power * 10.0 - (env.difficulty * 2.0)
        score = max(0.0, score)
        agent.fitness_history[env.env_id] = score
        return score

    def step_coevolution(self):
        """執行一輪 POET 演化：突變環境 + 跨環境跳躍 (Transfer Check)"""
        # 1. 本地優化
        for env_id, env in self.environments.items():
            if env.active_agent_id and env.active_agent_id in self.agents:
                current_agent = self.agents[env.active_agent_id]
                score = self.evaluate(current_agent, env)
                if score > env.best_score:
                    env.best_score = score

        # 2. 跨環境轉移測試 (Transfer Mechanism · 踏腳石發現)
        for env_id, env in self.environments.items():
            for agent_id, agent in self.agents.items():
                if agent_id != env.active_agent_id:
                    transfer_score = self.evaluate(agent, env)
                    if transfer_score > env.best_score:
                        msg = (
                            f"[Stepping Stone] Agent {agent_id} transferred to Env {env_id} "
                            f"(Score improved: {env.best_score:.2f} -> {transfer_score:.2f})"
                        )
                        self.transfer_log.append(msg)
                        env.best_score = transfer_score
                        env.active_agent_id = agent_id

if __name__ == "__main__":
    poet = POETAutoCurriculumEngine("Polaris_Logistics_Delivery")
    # 建立三種難度漸進的台東外送情境
    e1 = poet.create_environment("Env_Downtown_Sunny", difficulty=1.0, params={"required_skills": ["nav_basic", "cash_flow"]})
    e2 = poet.create_environment("Env_Typhoon_Mountain", difficulty=4.0, params={"required_skills": ["nav_basic", "route_replan", "cold_chain"]})
    e3 = poet.create_environment("Env_Night_Rush", difficulty=3.0, params={"required_skills": ["nav_basic", "route_replan"]})

    # 註冊兩位不同技能樹的 Agent
    a1 = poet.register_agent("Agent_Courier_Alpha", ["nav_basic", "cash_flow"])
    a2 = poet.register_agent("Agent_Tactician_Beta", ["nav_basic", "route_replan", "cold_chain"])

    e1.active_agent_id = a1.agent_id
    e2.active_agent_id = a1.agent_id  # Alpha 卡在颱風山區

    poet.step_coevolution()
    print("POET Transfer Logs:")
    for log in poet.transfer_log:
        print(" ", log)
    print("Env 2 Best Score:", e2.best_score, "Active Agent:", e2.active_agent_id)
