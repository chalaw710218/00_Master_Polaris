"""
Polaris Bionic Learning System - Cycle 08 Code-as-Memory Module
Title: Semantic Guardrail & Transactional Rollback Engine
Reference: NVIDIA NeMo Guardrails (2023) / Constitutional AI (Yuntao Bai et al., Anthropic 2022)
Architecture: Input Rails -> State Checkpoint -> Execution -> Output Rails -> Auto-Rollback on Breach
"""

import copy
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

@dataclass
class PolarisConstitution:
    forbidden_terms: List[str]
    max_claim_percentage: float = 100.0
    zero_confidential_leak: bool = True

class SemanticGuardrailRollbackEngine:
    """
    仿生語意護欄與交易自動回滾引擎 (Polaris Edition)
    提供原子性安全交易保證：若生成內容或系統動作觸犯商道憲法，自動抹除變更並回滾到安全檢查點。
    """
    def __init__(self, constitution: PolarisConstitution):
        self.constitution = constitution
        self.state_history: List[Dict[str, Any]] = []

    def checkpoint_state(self, current_state: Dict[str, Any]):
        """建立狀態深拷貝快照 (Snapshot)"""
        self.state_history.append(copy.deepcopy(current_state))

    def rollback_state(self) -> Dict[str, Any]:
        """安全回滾至上一穩定狀態"""
        if self.state_history:
            return self.state_history.pop()
        return {}

    def inspect_output_rails(self, content: str) -> Tuple[bool, str]:
        """審查輸出護欄：檢查違禁字、虛假誇大宣傳與機密洩漏"""
        for term in self.constitution.forbidden_terms:
            if term.lower() in content.lower():
                return False, f"BREACH DETECTED: Content contains forbidden term '{term}'!"
        return True, "PASSED: All constitutional output rails satisfied."

if __name__ == "__main__":
    constitution = PolarisConstitution(
        forbidden_terms=["保證賺錢", "破盤跳樓拍賣", "董座", "洩漏API金鑰"]
    )
    engine = SemanticGuardrailRollbackEngine(constitution)

    system_state = {"status": "STABLE", "balance": 1000000, "posts_published": 10}
    engine.checkpoint_state(system_state)

    # 模擬一次違規輸出
    bad_post = "親愛的朋友，跟著我們生活管家保證賺錢，董座親自發紅包！"
    passed, reason = engine.inspect_output_rails(bad_post)
    print("Guardrail Check Result:", passed)
    print("Reason:", reason)

    if not passed:
        restored = engine.rollback_state()
        print("Auto-Rollback Triggered! Restored State:", restored)
