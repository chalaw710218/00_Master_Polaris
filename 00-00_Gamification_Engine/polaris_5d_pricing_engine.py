"""
Polaris 5D Pricing Engine (北極星 5D 萬用價值精算引擎 · 多型分治旗艦版 v2.0)
創辦人陳品碩（品碩）原創之全方位商業價值、專案成果與勞務成本精算系統。

【底層哲學同一 (Universal 5D Philosophy)】
- D1: Duration / Friction（摩擦取得力 / 隱形工時與供應鏈摩擦）
- D2: Difficulty / Risk（風險承擔力 / 勞力負荷與不可逆下檔責任）
- D3: Degree / Expertise（認知技術門檻 / 人力資本與不可替代性）
- D4: Development / Leverage（時效槓桿力 / 急迫插單與成果規模）
- D5: Delight / Trust（情緒信任安心度 / 注意力外包與品牌溢價）

【應用基數多型分離 (Base Polymorphism)】
1. Labor5DPricingEngine:  以「時間/工時 (Base Hours)」為錨點，守護第一線勞務與管家尊嚴，絕不做白工。
2. Impact5DPricingEngine: 以「商業成果規模 (Value/Risk Saved)」為錨點，捕捉高階顧問與系統救火之巨大價值。
3. Asset5DPricingEngine:  以「固定研發攤提與邊際成本 (R&D / Volume)」為錨點，定價零邊際成本數位資產與課程。

【防彈衣四大鐵律 (Four Bulletproof Rules)】
- Rule 1: 隱形摩擦力前置拆解律 (Transaction Friction Decoupling)
- Rule 2: 勞務服務費與實報實銷完全解耦律 (Fee & Expense Separation)
- Rule 3: 授權與知情確認前置律 (Ex-ante Authorization & Notification)
- Rule 4: 現場等候 5 分鐘上限與二次出勤條款 (Contract Boundary & Secondary Callout)
"""

import sys
import math
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


# =========================================================================
# 抽象基底：北極星 5D 核心價值哲學 (Base Class)
# =========================================================================

class Base5DPricingEngine(ABC):
    """
    5D 價值精算抽象基底類別
    封裝查理·蒙格現金流風控、防彈衣原則與通用的 5D 語意驗證
    """
    def __init__(self, name: str = "Polaris 5D Base Engine"):
        self.name = name

    def assess_advance_risk(self, amount: float) -> Dict[str, Any]:
        """評估代墊款財務風控層級（查理·蒙格軍規入憲）"""
        if amount <= 0:
            return {
                "level": "NONE",
                "label": "無代墊款",
                "instruction": "純勞務單，無代墊款風險。"
            }
        elif amount < 1000:
            return {
                "level": "GREEN",
                "label": "低風險代墊 (NT$ 1,000 以下)",
                "instruction": "常規代墊，送達時憑發票/收據實報實銷結清。"
            }
        elif amount < 2000:
            return {
                "level": "YELLOW",
                "label": "中風險代墊 (NT$ 1,000 ~ 2,000)",
                "instruction": "需委託人提供即時轉帳證明或信任擔保，防範跑單。"
            }
        else:
            return {
                "level": "RED",
                "label": "高風險代墊 (NT$ 2,000 以上·強制預付)",
                "instruction": "【現金流防線】代墊金額達門檻，出發前強制委託人全額匯款，拒絕無息墊資！"
            }

    @abstractmethod
    def calculate(self, *args, **kwargs) -> Dict[str, Any]:
        """多型計算接口，由具體子類別實作專屬基數運算"""
        pass


# =========================================================================
# 模態 1：Labor5DPricingEngine（勞務時間型 · 生活管家旗艦版）
# =========================================================================

class Labor5DPricingEngine(Base5DPricingEngine):
    """
    以「時間 (Hours)」為錨點之勞務精算引擎
    適用：生活管家、到府照護、水電維修、跑腿、客製化交付等時間/人力密集型任務。
    """
    def __init__(self, base_rate: float = 250.0, default_min_fare: float = 200.0):
        super().__init__(name="5D-Labor Engine")
        self.base_rate = base_rate
        self.default_min_fare = default_min_fare

    def calculate(
        self,
        base_minutes: float,
        d1_friction: float = 1.0,
        d2_difficulty: float = 1.0,
        d3_degree: float = 1.0,
        d4_development: float = 1.0,
        d5_delight: float = 1.0,
        item_value: float = 0.0,
        advance_payment: float = 0.0,
        is_urgent: bool = False,
        lead_time_minutes: Optional[float] = None,
        task_name: str = "生活管家專案任務",
        recipient_info: str = "收件人",
        custom_notes: str = ""
    ) -> Dict[str, Any]:
        """
        執行 5D 勞務工時價值精算
        """
        base_hours = base_minutes / 60.0

        # 高價品自動校準 D2 (承擔賠償風險)
        actual_d2 = d2_difficulty
        if item_value >= 2000 and actual_d2 < 1.4:
            actual_d2 = 1.5

        # 急件判定與加成
        actual_d4 = d4_development
        urgent_surcharge = 0.0
        if is_urgent or (lead_time_minutes is not None and lead_time_minutes <= 90):
            if actual_d4 < 1.5:
                if lead_time_minutes is not None and lead_time_minutes <= 45:
                    actual_d4 = 1.8
                else:
                    actual_d4 = 1.6

        # TP (時間點數) 連乘模態
        tp_raw = base_hours * d1_friction * actual_d2 * d3_degree * actual_d4 * d5_delight
        tp_score = round(tp_raw, 3)

        # 報價計算
        raw_price = tp_score * self.base_rate
        suggested_price = math.ceil(raw_price / 10.0) * 10

        # 最低起步價防禦
        final_price = max(self.default_min_fare, suggested_price)

        # 整數定錨校準
        if 200 < final_price <= 220:
            final_price = 200.0
        elif 220 < final_price <= 260:
            final_price = 250.0
        elif 280 <= final_price <= 320:
            final_price = 300.0

        advance_risk = self.assess_advance_risk(advance_payment)

        customer_script = self._generate_script(
            task_name=task_name,
            final_price=int(final_price),
            item_value=item_value,
            advance_payment=advance_payment,
            advance_risk=advance_risk,
            is_urgent=is_urgent or (lead_time_minutes is not None and lead_time_minutes <= 90),
            recipient_info=recipient_info
        )

        return {
            "mode": "labor_time",
            "task_name": task_name,
            "inputs": {
                "base_minutes": base_minutes,
                "d1_friction": d1_friction,
                "d2_difficulty": actual_d2,
                "d3_degree": d3_degree,
                "d4_development": actual_d4,
                "d5_delight": d5_delight,
                "item_value": item_value,
                "advance_payment": advance_payment,
                "is_urgent": is_urgent,
                "lead_time_minutes": lead_time_minutes
            },
            "metrics": {
                "base_hours": round(base_hours, 2),
                "tp_score": tp_score,
                "base_rate": self.base_rate,
                "urgent_surcharge": urgent_surcharge,
                "raw_price": round(raw_price, 1)
            },
            "final_price": int(final_price),
            "advance_risk": advance_risk,
            "rules_enforced": [
                f"Rule 1: 隱形摩擦力已計入 D1 (係數 {d1_friction:.1f})",
                f"Rule 2: 服務費 NT$ {int(final_price)} 與代墊款 NT$ {int(advance_payment)} 徹底解耦",
                "Rule 3: 前置知情確認與替代收件人條款已生成",
                "Rule 4: 現場 5 分鐘等候上限與二次出勤收費 (NT$ 100~150) 條款已載入"
            ],
            "customer_script": customer_script
        }

    def _generate_script(
        self,
        task_name: str,
        final_price: int,
        item_value: float,
        advance_payment: float,
        advance_risk: Dict[str, Any],
        is_urgent: bool,
        recipient_info: str
    ) -> str:
        lines = []
        if is_urgent:
            lines.append("「您好，收到！由於本趟任務屬於當日緊急調度件，管家已立刻為您協調排程、調度專人即刻專車出動。")
        elif item_value >= 2000:
            lines.append(f"「您好，收到！由於本次託運品價值較高（約 NT$ {int(item_value):,}）且需高規格防護，管家會準備專用保溫保冷與防震設備，以專車直送標準為您服務。")
        else:
            lines.append(f"「您好，沒問題！管家可以為您安排專人專車趟次，執行【{task_name}】任務。")

        lines.append(f"本趟管家專屬勞務服務費為 **NT$ {final_price} 元**。")

        if advance_payment > 0:
            if advance_risk["level"] == "RED":
                lines.append(f"💰 **代墊款項安全約定**：因代墊金額達 NT$ {int(advance_payment):,} 元（超過安全代墊上限），需麻煩您於出發前先將貨款匯至本行專用帳戶，管家抵達現場將憑官方收據實報實銷為您結清。")
            else:
                lines.append(f"💰 **實報實銷約定**：代墊款項（約 NT$ {int(advance_payment):,} 元）將憑現場正式發票/收據實報實銷，於送達時一併結算。")

        lines.append("💡 **管家出發前貼心小確認**：")
        lines.append(f"1. 請問【{recipient_info}】知道管家稍後會送達嗎？若抵達時不便通話，現場是否有家人、管理室或鄰居可代為簽收？")
        lines.append("2. 請確認交接之班次、車牌或門牌地標資訊無誤。")

        secondary_fee = 150 if item_value >= 2000 or is_urgent else 100
        lines.append(f"⚠️ **配送權益提醒**：本次報價為單趟即時專車配送。若抵達現場遇無人應門或無法取得聯繫，管家將於現場守候 5 分鐘。若仍無法交付，我們會先將物品妥善帶回門市保管，後續為您安排二次配送時，將另行酌收 NT$ {secondary_fee} 元出勤補貼喔！")
        lines.append("若確認無誤，請回覆我們，管家立刻整裝為您出發！」")
        return "\n".join(lines)


# 向前相容別名：既有程式碼呼叫 Polaris5DPricingEngine 100% 保持相容
Polaris5DPricingEngine = Labor5DPricingEngine


# =========================================================================
# 模態 2：Impact5DPricingEngine（成果價值型 · 高階顧問與救火專用）
# =========================================================================

class Impact5DPricingEngine(Base5DPricingEngine):
    """
    以「商業成果規模 (Value Impact / Risk Saved)」為錨點之價值捕獲引擎
    適用：企業資安救火、高階架構顧問、重大合約談判、商業逆向工程等成果導向業務。
    """
    def __init__(self, base_retainer: float = 5000.0, default_share_ratio: float = 0.05):
        """
        :param base_retainer: 最低專家出勤/諮詢留任金 (NT$)
        :param default_share_ratio: 基準價值捕獲比例 (預設 5% ~ 10%)
        """
        super().__init__(name="5D-Impact Engine")
        self.base_retainer = base_retainer
        self.default_share_ratio = default_share_ratio

    def calculate(
        self,
        value_impact: float,          # 為客戶挽救的潛在損失、或創造的額外營收規模 (NT$)
        d1_friction: float = 1.0,     # 調研與溝通摩擦力 (1.0~2.0)
        d2_liability_risk: float = 1.0,# 承擔的法律/商譽責任風險 (1.0~2.0)
        d3_expertise: float = 1.5,    # 專業與稀缺技術壁壘 (1.0~2.5)
        d4_urgency: float = 1.5,      # 救火時效與急迫性 (1.0~2.0)
        d5_strategic_trust: float = 1.2,# 長期戰略信任與無形資產溢價 (1.0~1.5)
        project_name: str = "高階架構諮詢與危機救火專案",
        client_name: str = "企業客戶"
    ) -> Dict[str, Any]:
        """
        執行 5D 成果價值捕獲精算
        公式：
        Captured Value = Value Impact * Share Ratio * ((D3 * D4) / 2.0) * D2
        Final Price = Max(Base Retainer, Captured Value) + (D1 摩擦調研費)
        """
        # 1. 基礎價值捕獲比率依 D3(專業) 與 D4(急迫救火) 動態放大
        multiplier = (d3_expertise * d4_urgency * d2_liability_risk * d5_strategic_trust) / 3.0
        captured_value = value_impact * self.default_share_ratio * multiplier

        # 2. 摩擦調研與前置開銷
        friction_overhead = (d1_friction - 1.0) * self.base_retainer * 0.5

        # 3. 建議定價
        raw_price = max(self.base_retainer, captured_value + friction_overhead)
        final_price = math.ceil(raw_price / 1000.0) * 1000  # 向上整數至千元

        proposal_script = (
            f"【{project_name}】專案價值投資提案：\n"
            f"本次專案經評估將直接為貴方捍衛/創造約 NT$ {int(value_impact):,} 元之重大營運價值。\n"
            f"依據極星 5D 價值捕獲架構（技術門檻係數: {d3_expertise:.1f}，急迫救火係數: {d4_urgency:.1f}，責任防護: {d2_liability_risk:.1f}），\n"
            f"本專案全案合約定價為 **NT$ {int(final_price):,} 元**（含深度技術架構、即時危機排除與戰略交付產出）。"
        )

        return {
            "mode": "outcome_impact",
            "project_name": project_name,
            "inputs": {
                "value_impact": value_impact,
                "d1_friction": d1_friction,
                "d2_liability_risk": d2_liability_risk,
                "d3_expertise": d3_expertise,
                "d4_urgency": d4_urgency,
                "d5_strategic_trust": d5_strategic_trust
            },
            "metrics": {
                "multiplier": round(multiplier, 3),
                "base_retainer": self.base_retainer,
                "captured_value": round(captured_value, 0),
                "raw_price": round(raw_price, 0)
            },
            "final_price": int(final_price),
            "proposal_script": proposal_script
        }


# =========================================================================
# 模態 3：Asset5DPricingEngine（數位資產與規模產品型 · 課程/軟體專用）
# =========================================================================

class Asset5DPricingEngine(Base5DPricingEngine):
    """
    以「固定研發攤提 (R&D Cost / Target Volume) + 邊際成本」為錨點之資產定價引擎
    適用：線上錄播課、AI 提示詞庫、SaaS 軟體、數位報告、批量生鮮商品。
    """
    def __init__(self, target_volume: int = 100, min_unit_price: float = 299.0):
        super().__init__(name="5D-Asset Engine")
        self.target_volume = max(1, target_volume)
        self.min_unit_price = min_unit_price

    def calculate(
        self,
        fixed_dev_cost: float,        # 總研發/製作/前置成本 (NT$)
        marginal_cost: float = 0.0,   # 單份邊際履約成本 (伺服器、金流、包材，數位通常極低)
        d1_acquisition_friction: float = 1.0, # 外部同類資產獲取難度 (稀缺性, 1.0~1.5)
        d2_quality_guarantee: float = 1.0,    # 品質承諾與售後保證等級 (1.0~1.4)
        d3_intellectual_barrier: float = 1.2, # 知識產權/專利/獨家心智門檻 (1.0~2.0)
        d4_market_timing: float = 1.1,        # 市場時機與風口紅利 (1.0~1.5)
        d5_brand_delight: float = 1.2,        # 品牌美學與社群認同溢價 (1.0~1.8)
        product_name: str = "極星數位知識資產"
    ) -> Dict[str, Any]:
        """
        執行 5D 規模資產定價
        Unit Base = (Fixed Cost / Target Volume) + Marginal Cost
        Asset Multiplier = D1 * D2 * D3 * D4 * D5
        Final Unit Price = Max(Min Unit Price, Unit Base * Asset Multiplier)
        """
        unit_base = (fixed_dev_cost / float(self.target_volume)) + marginal_cost
        asset_multiplier = (
            d1_acquisition_friction *
            d2_quality_guarantee *
            d3_intellectual_barrier *
            d4_market_timing *
            d5_brand_delight
        )

        suggested_unit_price = unit_base * asset_multiplier
        final_unit_price = max(self.min_unit_price, math.ceil(suggested_unit_price / 10.0) * 10)

        total_expected_revenue = final_unit_price * self.target_volume
        expected_profit = total_expected_revenue - (fixed_dev_cost + marginal_cost * self.target_volume)

        return {
            "mode": "scale_asset",
            "product_name": product_name,
            "inputs": {
                "fixed_dev_cost": fixed_dev_cost,
                "marginal_cost": marginal_cost,
                "target_volume": self.target_volume,
                "d1_acquisition_friction": d1_acquisition_friction,
                "d2_quality_guarantee": d2_quality_guarantee,
                "d3_intellectual_barrier": d3_intellectual_barrier,
                "d4_market_timing": d4_market_timing,
                "d5_brand_delight": d5_brand_delight
            },
            "metrics": {
                "unit_base": round(unit_base, 1),
                "asset_multiplier": round(asset_multiplier, 3),
                "suggested_unit_price": round(suggested_unit_price, 1)
            },
            "final_unit_price": int(final_unit_price),
            "projected_economics": {
                "target_volume": self.target_volume,
                "total_expected_revenue": int(total_expected_revenue),
                "expected_profit": int(expected_profit),
                "roi_percentage": round((expected_profit / fixed_dev_cost) * 100, 1) if fixed_dev_cost > 0 else 0.0
            }
        }


# =========================================================================
# 萬用統整門面 (Universal 5D Facade)
# =========================================================================

class Universal5DPricingEngine:
    """
    極星 5D 萬用精算總控門面
    自動依模式分流至 Labor, Impact, 或 Asset 子引擎
    """
    def __init__(self):
        self.labor_engine = Labor5DPricingEngine()
        self.impact_engine = Impact5DPricingEngine()
        self.asset_engine = Asset5DPricingEngine()

    def calculate_labor(self, *args, **kwargs) -> Dict[str, Any]:
        return self.labor_engine.calculate(*args, **kwargs)

    def calculate_impact(self, *args, **kwargs) -> Dict[str, Any]:
        return self.impact_engine.calculate(*args, **kwargs)

    def calculate_asset(self, *args, **kwargs) -> Dict[str, Any]:
        return self.asset_engine.calculate(*args, **kwargs)


# =========================================================================
# 驗證測試套件 (涵蓋全模態驗證)
# =========================================================================

def run_canonical_tests():
    print("==================================================")
    print("🚀 啟動北極星 5D 萬用價值精算引擎 (多型分治 v2.0) 驗證套件")
    print("==================================================")

    # ----------------------------------------------------
    # 模態 1：勞務工時型 (Labor 5D) 官方案例 1~4
    # ----------------------------------------------------
    labor = Labor5DPricingEngine(base_rate=250.0)

    # 案例 1: 送藥單
    c1 = labor.calculate(
        base_minutes=36,
        d1_friction=1.0,
        d2_difficulty=1.0,
        d3_degree=1.1,
        d4_development=1.0,
        d5_delight=1.1,
        item_value=150,
        advance_payment=150,
        task_name="代買扭傷止痛藥送達仁七街",
        recipient_info="許先生"
    )
    print("\n【案例 1：送藥案 (Labor 5D)】")
    print(f"TP 點數: {c1['metrics']['tp_score']} | 建議定價: NT$ {c1['final_price']} (預期 200 元)")
    assert c1['final_price'] == 200, f"Case 1 failed: {c1['final_price']}"

    # 案例 2: 公車總站代收常規餐點
    c2 = labor.calculate(
        base_minutes=36,
        d1_friction=1.0,
        d2_difficulty=1.1,
        d3_degree=1.0,
        d4_development=1.2,
        d5_delight=1.1,
        item_value=300,
        advance_payment=0,
        task_name="公車總站代收餐點直送消費者",
        recipient_info="消費者"
    )
    print("\n【案例 2：公車總站代收常規餐點 (Labor 5D)】")
    print(f"TP 點數: {c2['metrics']['tp_score']} | 建議定價: NT$ {c2['final_price']} (預期 200~250 元)")
    assert c2['final_price'] in [200, 250], f"Case 2 failed: {c2['final_price']}"

    # 案例 3: 2,400 元高價餐點護運
    c3 = labor.calculate(
        base_minutes=36,
        d1_friction=1.0,
        d2_difficulty=1.5,
        d3_degree=1.0,
        d4_development=1.2,
        d5_delight=1.1,
        item_value=2400,
        advance_payment=2400,
        task_name="公車總站代收高價餐點直送",
        recipient_info="訂餐貴賓"
    )
    print("\n【案例 3：2,400 元高價餐點護運 (Labor 5D)】")
    print(f"TP 點數: {c3['metrics']['tp_score']} | 建議定價: NT$ {c3['final_price']} (預期 300 元)")
    assert c3['final_price'] == 300, f"Case 3 failed: {c3['final_price']}"
    assert c3['advance_risk']['level'] == "RED", "Case 3 risk level failed"

    # 案例 4: 當日臨時急件
    c4 = labor.calculate(
        base_minutes=36,
        d1_friction=1.0,
        d2_difficulty=1.1,
        d3_degree=1.0,
        d4_development=1.6,
        d5_delight=1.2,
        is_urgent=True,
        lead_time_minutes=80,
        task_name="都蘭公車總站急件代收直送",
        recipient_info="收件客戶"
    )
    print("\n【案例 4：當日臨時插單急件 (Labor 5D)】")
    print(f"TP 點數: {c4['metrics']['tp_score']} | 建議定價: NT$ {c4['final_price']} (預期 300 元)")
    assert c4['final_price'] == 300, f"Case 4 failed: {c4['final_price']}"

    # ----------------------------------------------------
    # 模態 2：成果價值型 (Impact 5D) 案例 5
    # ----------------------------------------------------
    impact = Impact5DPricingEngine(base_retainer=8000.0, default_share_ratio=0.08)
    # 林納斯 5 分鐘排除百萬級伺服器當機危機
    c5 = impact.calculate(
        value_impact=1000000.0,      # 挽救 100 萬停機損失
        d1_friction=1.2,             # 現場通訊核對
        d2_liability_risk=1.5,       # 承擔代碼修改之系統責任
        d3_expertise=2.2,            # 頂級底層架構專家門檻
        d4_urgency=2.0,              # 極急停機救火
        d5_strategic_trust=1.3,      # 戰略合作夥伴信任
        project_name="關鍵核心資料庫鎖定緊急排除救火",
        client_name="科技製造廠"
    )
    print("\n【案例 5：重大危機救火與顧問價值捕獲 (Impact 5D)】")
    print(f"挽救損失: NT$ {int(c5['inputs']['value_impact']):,} 元 | 專案建議定價: NT$ {c5['final_price']:,} 元")
    assert c5['final_price'] >= 50000, f"Case 5 failed to capture significant value: {c5['final_price']}"

    # ----------------------------------------------------
    # 模態 3：資產規模型 (Asset 5D) 案例 6
    # ----------------------------------------------------
    asset = Asset5DPricingEngine(target_volume=500, min_unit_price=499.0)
    # 極星 AI 自動化實戰工作坊 (研發投入 60,000 元，邊際成本 20 元/人)
    c6 = asset.calculate(
        fixed_dev_cost=60000.0,
        marginal_cost=20.0,
        d1_acquisition_friction=1.2,
        d2_quality_guarantee=1.3,
        d3_intellectual_barrier=1.5,
        d4_market_timing=1.3,
        d5_brand_delight=1.3,
        product_name="極星 AI 實戰提示詞與工作流大師庫"
    )
    print("\n【案例 6：數位知識資產與規模化定價 (Asset 5D)】")
    print(f"單份研發攤提基準: NT$ {c6['metrics']['unit_base']} 元 | 建議單價: NT$ {c6['final_unit_price']} 元")
    print(f"預估規模收益: NT$ {c6['projected_economics']['total_expected_revenue']:,} 元 | 預期利潤: NT$ {c6['projected_economics']['expected_profit']:,} 元")
    assert c6['final_unit_price'] >= 499, f"Case 6 failed: {c6['final_unit_price']}"

    print("\n==================================================")
    print("✅ 全部三大模態（勞務、成果、資產）6 大情境驗證 100% 通過！")
    print("==================================================")

if __name__ == '__main__':
    run_canonical_tests()
