import sys
sys.path.append(r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine')
from polaris_5d_pricing_engine import Labor5DPricingEngine, Impact5DPricingEngine

print("==================================================")
print("🎯 單堂 1 對 1 AI 家教課（VIP 尊榮私塾）· 5D 2.0 精算")
print("==================================================")

# 1. 勞務工時防禦視角
# 單堂 2 小時 (120 分鐘) + 課前需求診斷 25 分鐘 + 課後跟進 20 分鐘 = 165 分鐘
# 專家時薪以 NT$ 500 元計算（創辦人出勤）
labor_500 = Labor5DPricingEngine(base_rate=500.0, default_min_fare=2000.0)
res_500 = labor_500.calculate(
    base_minutes=165,
    d1_friction=1.2,   # 1對1專屬對接，溝通摩擦適中
    d2_difficulty=1.6, # 全場注意力 100% 聚焦在學員，現場客製除錯壓力極大
    d3_degree=2.0,     # 前沿 AI 技術 + 當場針對學員生意客製化架構
    d4_development=1.8,# 極高排他性與時效（創辦人這2小時無法排其他事）
    d5_delight=1.8,    # 1對1專屬隱私、現場手把手配到好之極致安心
    task_name="單堂1對1尊榮AI私人家教(2小時)"
)

print(f"【模態 A：5D-Labor 勞務防禦底線（以時薪 500 計）】")
print(f"- 5D 總點數 (TP): {res_500['metrics']['tp_score']}")
print(f"- 單堂建議定價: NT$ {res_500['final_price']:,} 元")

# 專家時薪以 NT$ 600 與 NT$ 800 元計算（資深顧問級）
labor_600 = Labor5DPricingEngine(base_rate=600.0, default_min_fare=2500.0)
res_600 = labor_600.calculate(base_minutes=165, d1_friction=1.2, d2_difficulty=1.6, d3_degree=2.0, d4_development=1.8, d5_delight=1.8)
print(f"👉 若以資深顧問時薪 NT$ 600 計算: NT$ {res_600['final_price']:,} 元")

labor_800 = Labor5DPricingEngine(base_rate=800.0, default_min_fare=3000.0)
res_800 = labor_800.calculate(base_minutes=165, d1_friction=1.2, d2_difficulty=1.6, d3_degree=2.0, d4_development=1.8, d5_delight=1.8)
print(f"👉 若以頂級專家時薪 NT$ 800 計算: NT$ {res_800['final_price']:,} 元")

# 2. 成果價值捕獲視角（針對學員店鋪的客製化產出）
# 例如：2小時內直接幫他的民宿打造好「私密智庫 + 自動發文機」，一年為他省下 60,000 元行銷費用
impact = Impact5DPricingEngine(base_retainer=3600.0, default_share_ratio=0.08)
res_impact = impact.calculate(
    value_impact=60000.0,
    d1_friction=1.1,
    d2_liability_risk=1.2,
    d3_expertise=2.0,
    d4_urgency=1.5,
    d5_strategic_trust=1.6,
    project_name="1對1專屬店鋪AI系統落地",
    client_name="VIP學員"
)

print(f"\n【模態 B：5D-Impact 商業成果價值捕獲視角】")
print(f"- 為學員店鋪解決問題之首年效益 (Value Impact): NT$ 60,000 元")
print(f"- 依成果捕獲建議定價: NT$ {res_impact['final_price']:,} 元")

print("\n==================================================")
