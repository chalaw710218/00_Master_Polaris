"""
Polaris Bionic Learning System - Cycle 06 Code-as-Memory Module
Title: Anti-MAD Synthetic Hygiene Auditor (Model Autophagy Disorder Defense)
Reference: Sina Alemohammad, Richard Baraniuk et al., Rice & Stanford (ICLR 2024)
Architecture: Synthetic-to-Real Ratio Monitor -> Variance Collapse Detector -> Real Grounding Injection
"""

import math
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

@dataclass
class DatasetSlice:
    source_name: str
    is_real_grounded: bool
    sample_count: int
    features: List[float]  # 抽取出的多維語意特徵值

class AntiMADHygieneAuditor:
    """
    仿生抗自噬衛生審計器 (Anti-MAD Auditor · Polaris Edition)
    防止 AI 在封閉自生成迴圈中發生方差崩潰（Variance Collapse）與均值漂移（Mean Drift）。
    """
    def __init__(self, synthetic_threshold: float = 0.30):
        self.synthetic_threshold = synthetic_threshold
        self.slices: List[DatasetSlice] = []

    def record_slice(self, source_name: str, is_real: bool, samples: List[float]):
        self.slices.append(DatasetSlice(
            source_name=source_name,
            is_real_grounded=is_real,
            sample_count=len(samples),
            features=samples
        ))

    def calculate_hygiene_metrics(self) -> Dict[str, Any]:
        total_samples = sum(s.sample_count for s in self.slices)
        if total_samples == 0:
            return {"status": "EMPTY", "synthetic_ratio": 0.0}

        synthetic_samples = sum(s.sample_count for s in self.slices if not s.is_real_grounded)
        synthetic_ratio = synthetic_samples / total_samples

        all_features = [f for s in self.slices for f in s.features]
        mean_val = sum(all_features) / len(all_features)
        variance = sum((x - mean_val) ** 2 for x in all_features) / len(all_features)

        # 判定是否處於 MAD 自噬高危險期
        is_mad_danger = (synthetic_ratio > self.synthetic_threshold) or (variance < 0.05)

        return {
            "synthetic_ratio": synthetic_ratio,
            "mean": mean_val,
            "variance": variance,
            "is_mad_danger": is_mad_danger,
            "prescribed_action": (
                "EMERGENCY: Inject fresh real-world human telemetry & unedited logs!"
                if is_mad_danger else "HEALTHY: Real data ratio is within safety margins."
            )
        }

if __name__ == "__main__":
    auditor = AntiMADHygieneAuditor(synthetic_threshold=0.30)
    # 注入真實生活管家訂單數據 (真實硬數據)
    auditor.record_slice("Real_Orders_LineOA", is_real=True, samples=[120.0, 150.0, 85.0, 210.0])
    # 注入 AI 模擬自生成合成貼文數據 (合成數據)
    auditor.record_slice("Synthetic_Chat_Logs", is_real=False, samples=[130.0, 131.0, 129.5, 130.2])

    metrics = auditor.calculate_hygiene_metrics()
    print("Anti-MAD Hygiene Audit:")
    for k, v in metrics.items():
        print(f" {k}: {v}")
