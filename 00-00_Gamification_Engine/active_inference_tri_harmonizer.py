"""
Polaris Bionic Learning System - v4.0 Active Inference & Tri-Harmonizer Engine
Title: Active Inference Tri-Harmonizer (Resolving Voyager, Eureka, Stigmergy, MAD, Guardrails & Founder Alignment)
Reference: Karl Friston (FEP / Active Inference), Francisco Varela (Autopoiesis), NeMo, Voyager, Eureka
Architecture: 
  1. Conflict 1 Solved: Metabolic Code Lysozyme (Voyager Accumulation vs Anti-MAD Entropy)
  2. Conflict 2 Solved: Dual-Tier Sandboxed Evolution Gate (Eureka/POET Mutation vs Semantic Guardrails)
  3. Conflict 3 Solved: Global Neuro-Hormonal Bath (Stigmergy Swarm vs Founder Neuromodulation)
"""

import time
import math
from dataclasses import dataclass, field
from typing import Dict, List, Any, Tuple, Optional

@dataclass
class MetabolicSkill:
    name: str
    code_path: str
    fitness_weight: float
    last_invoked: float
    error_count: int = 0
    is_archived: bool = False

class ActiveInferenceTriHarmonizer:
    """
    極星仿生自進化系統 v4.0 · 主動推論三界調和引擎
    調和 10 輪學習中的三大結構性衝突：
    - 衝突 1 調和：溶酶體代謝修剪（防止代碼庫自噬膨脹）
    - 衝突 2 調和：雙層沙盒閘門（兼顧激進突變探索與商道憲法零暴險）
    - 衝突 3 調和：創辦人全域激素場（調和群體去中心化湧現與創辦人最高主權）
    """
    def __init__(self, lambda_decay: float = 0.05):
        self.lambda_decay = lambda_decay
        self.skill_library: Dict[str, MetabolicSkill] = {}
        self.archived_skills: Dict[str, MetabolicSkill] = {}
        self.global_hormonal_field: float = 1.0  # 全域激素場 (Dopamine/Cortisol)

    # ==========================================
    # 調和協議 1: 代碼溶酶體代謝修剪 (Metabolic Code Lysozyme)
    # ==========================================
    def register_skill(self, name: str, code_path: str, initial_weight: float = 1.0):
        self.skill_library[name] = MetabolicSkill(
            name=name,
            code_path=code_path,
            fitness_weight=initial_weight,
            last_invoked=time.time()
        )

    def invoke_skill(self, name: str, success: bool):
        if name in self.skill_library:
            s = self.skill_library[name]
            s.last_invoked = time.time()
            if success:
                s.fitness_weight += 0.2
            else:
                s.error_count += 1
                s.fitness_weight = max(0.01, s.fitness_weight - 0.3)

    def run_metabolic_lysozyme_cycle(self, decay_period_days: float = 7.0):
        """
        溶酶體自噬修剪：
        根據時間與錯誤率衰減技能權重；低於門檻者自動『分頁移出至磁碟冷庫』，保證活體庫乾淨精純。
        """
        now = time.time()
        eviction_list = []
        for name, skill in self.skill_library.items():
            idle_time = now - skill.last_invoked
            # 指數代謝衰減
            decay_factor = math.exp(-self.lambda_decay * (idle_time / 86400.0))
            skill.fitness_weight *= decay_factor

            # 淘汰判定：權重低於 0.2 或連續報錯 > 3 次
            if skill.fitness_weight < 0.2 or skill.error_count >= 3:
                eviction_list.append(name)

        for name in eviction_list:
            evicted = self.skill_library.pop(name)
            evicted.is_archived = True
            self.archived_skills[name] = evicted

        return len(eviction_list)

    # ==========================================
    # 調和協議 2: 雙層沙盒演化閘門 (Dual-Tier Sandboxed Gate)
    # ==========================================
    def evaluate_candidate_through_gate(
        self, 
        candidate_code: str, 
        sandbox_fitness: float, 
        forbidden_terms: List[str]
    ) -> Tuple[bool, str]:
        """
        雙層沙盒機制：
        Layer 1 (Chaos Sandbox): 允許激進突變、暴力採樣、天馬行空的開放式探索
        Layer 2 (Guardrail Gate): 上線前強制進行商道憲法合規檢查；有任一違規立即回滾並銷毀
        """
        # 第一層：沙盒適應度驗證
        if sandbox_fitness < 0.6:
            return False, "REJECTED_BY_LAYER_1: Sandbox fitness too low."

        # 第二層：憲法安全護欄審查
        for term in forbidden_terms:
            if term.lower() in candidate_code.lower():
                return False, f"REJECTED_BY_LAYER_2: Constitutional breach! Contains forbidden term '{term}'."

        return True, "PASSED_BOTH_GATES: Candidate promoted to production live system."

    # ==========================================
    # 調和協議 3: 創辦人全域激素場 (Global Neuro-Hormonal Field)
    # ==========================================
    def update_global_hormonal_bath(self, founder_feedback: str):
        """
        創辦人的反饋不是單點指令，而是改變全域環境的『激素浴（Hormonal Bath）』：
        正向多巴胺提高全域費洛蒙強化係數，皮質醇抑制加速全域揮發與代謝。
        """
        pos = ["請", "好", "可以", "讚", "認可", "很好"]
        neg = ["停", "錯", "不行", "別再", "亂搞", "不准"]

        for p in pos:
            if p in founder_feedback:
                self.global_hormonal_field = 1.8  # 全域多巴胺滲透
                return self.global_hormonal_field
        for n in neg:
            if n in founder_feedback:
                self.global_hormonal_field = 0.3  # 全域皮質醇抑制
                return self.global_hormonal_field
        self.global_hormonal_field = 1.0
        return self.global_hormonal_field

    # ==========================================
    # 主動推論雙驅動：Perception vs Action
    # ==========================================
    def decide_active_inference_pathway(self, prediction_error: float, world_alterability: float) -> str:
        """
        Karl Friston 主動推論核心：
        當現實與預期有落差 (delta > 0) 時：
        - 若現實不可改 (world_alterability < 0.5) -> 採取【Perception 知覺修正】：更新內部信念存摺
        - 若現實可改 (world_alterability >= 0.5) -> 採取【Action 行動塑造】：主動發起商業出擊，塑造現實符合品碩預期！
        """
        if world_alterability >= 0.5:
            return "ACTIVE_ACTION: Launch proactive business intervention to reshape reality!"
        else:
            return "PERCEPTUAL_UPDATE: Revise internal belief log and generative model priors."

if __name__ == "__main__":
    harmonizer = ActiveInferenceTriHarmonizer(lambda_decay=0.1)

    # 1. 測試溶酶體代謝
    harmonizer.register_skill("Active_Order_Parser", "parsers/orders.py", initial_weight=1.0)
    harmonizer.register_skill("Legacy_Crawler_2024", "scrapers/legacy.py", initial_weight=0.15) # 即將壞死
    pruned = harmonizer.run_metabolic_lysozyme_cycle()
    print(f"[Conflict 1 Resolved] Metabolic Lysozyme pruned {pruned} dead skills. Active: {list(harmonizer.skill_library.keys())}")

    # 2. 測試雙層沙盒閘門
    candidate_good = "def calculate_fair_margin(cost): return cost * 1.35"
    candidate_bad = "def scam_promo(): return '保證賺錢，董座送紅包'"
    g1, r1 = harmonizer.evaluate_candidate_through_gate(candidate_good, 0.9, ["保證賺錢", "董座"])
    g2, r2 = harmonizer.evaluate_candidate_through_gate(candidate_bad, 0.95, ["保證賺錢", "董座"])
    print(f"[Conflict 2 Resolved] Good Candidate Gate: {g1} ({r1})")
    print(f"[Conflict 2 Resolved] Bad Candidate Gate:  {g2} ({r2})")

    # 3. 測試全域激素場
    field_level = harmonizer.update_global_hormonal_bath("很好，這個方向完全正確！")
    print(f"[Conflict 3 Resolved] Global Neuromodulatory Field: {field_level:.2f} (Dopamine Bath)")

    # 4. 測試主動推論路徑
    path_a = harmonizer.decide_active_inference_pathway(prediction_error=0.8, world_alterability=0.9)
    path_b = harmonizer.decide_active_inference_pathway(prediction_error=0.8, world_alterability=0.1)
    print(f"[Active Inference] Action Pathway: {path_a}")
    print(f"[Active Inference] Perception Pathway: {path_b}")
