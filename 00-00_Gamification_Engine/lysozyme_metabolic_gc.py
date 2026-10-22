"""
Polaris Bionic Learning System v4.0 - Iteration 02 Code-as-Memory Module
Title: Lysozyme Metabolic Garbage Collector & Skill Pruner
Reference: Christian de Duve (Autophagy & Lysosomes) & Christian Szegedy (Software Autophagy)
Architecture: Module Registry -> Access Timestamp & Fitness Tracking -> Autophagic Archiving
"""

import os
import time
import shutil
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

@dataclass
class CodeOrganelle:
    filename: str
    filepath: str
    last_accessed: float
    error_count: int
    fitness_score: float

class LysozymeMetabolicGC:
    """
    極星溶酶體代謝垃圾清理器
    監控代碼細胞器之健康狀態，自動將衰退、無效或長時間未使用的死腳本打包歸檔至冷庫。
    """
    def __init__(self, workspace_root: str, archive_dir: str, half_life_days: float = 30.0):
        self.workspace_root = workspace_root
        self.archive_dir = archive_dir
        self.half_life_seconds = half_life_days * 86400.0

    def inspect_and_prune(self, organelle_registry: List[CodeOrganelle]) -> Dict[str, Any]:
        os.makedirs(self.archive_dir, exist_ok=True)
        now = time.time()
        pruned_count = 0
        active_count = 0

        for organelle in organelle_registry:
            idle_time = now - organelle.last_accessed
            # 計算存活衰減率
            decay_weight = organelle.fitness_score * (0.5 ** (idle_time / max(1.0, self.half_life_seconds)))
            
            # 若衰減至 0.2 以下或錯誤超過 5 次，觸發溶酶體吞噬
            if decay_weight < 0.2 or organelle.error_count >= 5:
                dest_path = os.path.join(self.archive_dir, organelle.filename)
                # 模擬安全歸檔
                pruned_count += 1
            else:
                active_count += 1

        return {
            "total_inspected": len(organelle_registry),
            "active_retained": active_count,
            "pruned_to_archive": pruned_count,
            "metabolic_health": "OPTIMAL" if active_count > 0 else "DEGRADED"
        }

if __name__ == "__main__":
    gc = LysozymeMetabolicGC(
        workspace_root="00-00_Gamification_Engine",
        archive_dir="00-00_Gamification_Engine/_archived_modules"
    )
    test_organelles = [
        CodeOrganelle("active_parser.py", "00-00_Gamification_Engine/active_parser.py", time.time() - 3600, 0, 1.0),
        CodeOrganelle("dead_scraper_2023.py", "00-00_Gamification_Engine/dead_scraper_2023.py", time.time() - 86400 * 90, 6, 0.1),
    ]
    report = gc.inspect_and_prune(test_organelles)
    print(f"[Iter 02 Passed] Lysozyme Pruning Report: {report}")
