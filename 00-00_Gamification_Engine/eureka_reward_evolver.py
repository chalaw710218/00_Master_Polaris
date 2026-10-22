"""
Polaris Bionic Learning System - Cycle 03 Code-as-Memory Module
Title: Eureka Reward Evolver (LLM-Driven Evolutionary Reward Optimization)
Reference: Yecheng Jason Ma et al., NVIDIA & Caltech (ICLR 2024 / arXiv:2310.12931)
Architecture: Environment Code -> Reward Generation -> Simulation Eval -> Policy Reflection -> Evolutionary Mutation
"""

import os
import sys
import inspect
from dataclasses import dataclass
from typing import Callable, Dict, List, Any, Optional

@dataclass
class RewardCandidate:
    candidate_id: int
    generation: int
    code_str: str
    reward_fn: Callable[..., float]
    fitness_score: float = 0.0
    metrics: Optional[Dict[str, float]] = None
    critique: str = ""

class EurekaRewardEvolver:
    """
    仿生 Eureka 獎勵函數演化器 (Polaris Edition)
    遵循 Code-as-Memory 原則，將抽象的獎勵指標轉化為可演化、可執行的代碼空間搜索。
    """
    def __init__(self, objective_name: str, baseline_metrics: Dict[str, float]):
        self.objective_name = objective_name
        self.baseline_metrics = baseline_metrics
        self.population: List[RewardCandidate] = []
        self.generation_count = 0
        self.best_candidate: Optional[RewardCandidate] = None

    def register_candidate(self, code_str: str, reward_fn: Callable[..., float]) -> RewardCandidate:
        """註冊新一代獎勵函數候選者"""
        candidate = RewardCandidate(
            candidate_id=len(self.population) + 1,
            generation=self.generation_count,
            code_str=code_str,
            reward_fn=reward_fn
        )
        self.population.append(candidate)
        return candidate

    def evaluate_candidate(self, candidate: RewardCandidate, test_cases: List[Dict[str, Any]]) -> float:
        """
        在環境測試集上評估候選獎勵函數，計算適應度與物理回饋指標
        """
        total_reward = 0.0
        success_count = 0
        
        for case in test_cases:
            try:
                r = candidate.reward_fn(case)
                total_reward += r
                # 若獎勵與目標正相關且超過閥值，視為成功
                if r > case.get("threshold", 0.0):
                    success_count += 1
            except Exception as e:
                candidate.critique = f"Runtime Error in execution: {str(e)}"
                candidate.fitness_score = -999.0
                return candidate.fitness_score

        avg_reward = total_reward / max(1, len(test_cases))
        success_rate = success_count / max(1, len(test_cases))
        
        candidate.fitness_score = avg_reward * 0.4 + success_rate * 0.6
        candidate.metrics = {
            "avg_reward": avg_reward,
            "success_rate": success_rate,
            "sample_size": len(test_cases)
        }
        
        # 形成 Eureka 式語意反思報告 (Textual Policy Reflection)
        candidate.critique = (
            f"Gen {candidate.generation} Candidate {candidate.candidate_id}: "
            f"Success Rate = {success_rate:.2%}, Avg Reward = {avg_reward:.4f}. "
            f"Correlation: {'Strong' if success_rate > 0.7 else 'Weak/Suboptimal'}."
        )

        if self.best_candidate is None or candidate.fitness_score > self.best_candidate.fitness_score:
            self.best_candidate = candidate

        return candidate.fitness_score

    def get_evolutionary_reflection_prompt(self, top_k: int = 2) -> str:
        """
        提取表現最佳之獎勵代碼與物理指標，編譯為給 LLM 的演化提示詞
        """
        sorted_pop = sorted(self.population, key=lambda c: c.fitness_score, reverse=True)[:top_k]
        prompt = [
            f"=== EUREKA EVOLUTIONARY REWARD PROMPT (Objective: {self.objective_name}) ===",
            "Below are the top-performing reward functions and their simulation feedback:",
        ]
        for c in sorted_pop:
            prompt.append(f"\n[Candidate #{c.candidate_id} | Gen {c.generation}] Fitness: {c.fitness_score:.4f}")
            prompt.append(f"Reflection: {c.critique}")
            prompt.append("Code:\n```python")
            prompt.append(c.code_str)
            prompt.append("```")
        prompt.append(
            "\nTask: Analyze the correlation between reward components and success rate. "
            "Propose a mutated reward function that penalizes exploitation and rewards smooth convergence."
        )
        return "\n".join(prompt)

if __name__ == "__main__":
    # 單元驗證：以極星「社群貼文品質與互動率」為測試標的
    evolver = EurekaRewardEvolver(
        objective_name="Community_Post_Engagement_Reward",
        baseline_metrics={"expected_ctr": 0.05, "target_sentiment": 0.8}
    )

    # 候選獎勵 1 (人類直覺：純字數與點擊)
    code_v1 = "def reward_v1(post):\n    return post.get('clicks', 0) * 0.1 + post.get('word_count', 0) * 0.001"
    fn_v1 = lambda p: p.get('clicks', 0) * 0.1 + p.get('word_count', 0) * 0.001
    c1 = evolver.register_candidate(code_v1, fn_v1)

    # 候選獎勵 2 (仿生 Eureka 突變：考慮停留率、真誠度與扣減農場字眼)
    code_v2 = (
        "def reward_v2(post):\n"
        "    retention = post.get('retention_rate', 0.0)\n"
        "    sincerity = 1.0 if not post.get('clickbait_flag', False) else 0.1\n"
        "    return retention * 2.0 * sincerity"
    )
    fn_v2 = lambda p: p.get('retention_rate', 0.0) * 2.0 * (1.0 if not p.get('clickbait_flag', False) else 0.1)
    c2 = evolver.register_candidate(code_v2, fn_v2)

    # 模擬測試集
    test_env = [
        {"clicks": 100, "word_count": 800, "retention_rate": 0.2, "clickbait_flag": True, "threshold": 0.5},
        {"clicks": 40, "word_count": 250, "retention_rate": 0.85, "clickbait_flag": False, "threshold": 0.5},
        {"clicks": 60, "word_count": 300, "retention_rate": 0.75, "clickbait_flag": False, "threshold": 0.5},
    ]

    evolver.evaluate_candidate(c1, test_env)
    evolver.evaluate_candidate(c2, test_env)

    print("Best Candidate ID:", evolver.best_candidate.candidate_id)
    print("Best Fitness:", evolver.best_candidate.fitness_score)
    print("\nGenerated Prompt for Next Generation:")
    print(evolver.get_evolutionary_reflection_prompt())
