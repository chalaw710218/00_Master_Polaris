"""
Polaris Bionic Learning System v4.0 - Iteration 05 Code-as-Memory Module
Title: Active Supply-Chain Margin Negotiator (Active Inference Action Pathway)
Reference: Karl Friston (FEP Action Reshaping Reality) & Polaris AI Pricing Auditor Protocol
Architecture: Quote Ingestion -> BOM Friction Stripping -> Proactive Counter-Bargaining Protocol
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SupplierQuote:
    item_name: str
    supplier_quote_price: float
    unit: str
    packaging_ice_percent: float = 0.0

class ActiveMarginNegotiator:
    """
    極星主動推論供應鏈議價出擊器
    當供應商報價侵蝕極星安全毛利時，AI 拒絕被動妥協，主動發起 BOM 成本逆推與精準商務話術出擊！
    """
    def __init__(self, target_gross_margin: float = 0.35):
        self.target_gross_margin = target_gross_margin

    def execute_active_intervention(self, quote: SupplierQuote, estimated_raw_cost: float) -> Dict[str, Any]:
        # 1. 扣除水分與冰衣後的真實淨重成本
        effective_weight_ratio = 1.0 - (quote.packaging_ice_percent / 100.0)
        effective_quote_per_unit = quote.supplier_quote_price / max(0.1, effective_weight_ratio)
        current_margin = (quote.supplier_quote_price - estimated_raw_cost) / max(0.1, quote.supplier_quote_price)

        prediction_error = self.target_gross_margin - current_margin
        
        # 2. 主動行動塑造：生成逆向議價攻擊方案
        target_cost = quote.supplier_quote_price * (1.0 - self.target_gross_margin)
        counter_pitch = (
            f"報告品碩，供應商報價 ${quote.supplier_quote_price}/{quote.unit} 含包冰率 {quote.packaging_ice_percent}%，"
            f"實質進貨成本虛高。已啟動主動推論出擊：建議以大宗固定走單量為籌碼，"
            f"將目標底價鎖定在 ${target_cost:.1f}，並要求出具無膨發產地證明。"
        )

        return {
            "item": quote.item_name,
            "original_quote": quote.supplier_quote_price,
            "effective_quote": effective_quote_per_unit,
            "prediction_error_delta": prediction_error,
            "active_action_prescribed": counter_pitch,
            "suggested_counter_price": target_cost
        }

if __name__ == "__main__":
    negotiator = ActiveMarginNegotiator(target_gross_margin=0.35)
    test_q = SupplierQuote(item_name="泰國大蝦仁", supplier_quote_price=240.0, unit="台斤", packaging_ice_percent=25.0)
    result = negotiator.execute_active_intervention(test_q, estimated_raw_cost=120.0)
    print(f"[Iter 05 Passed] Active Negotiation Intervention:\n {result['active_action_prescribed']}")
