import sys
sys.path.append(r'c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine')
from polaris_5d_pricing_engine import Labor5DPricingEngine, Impact5DPricingEngine, Asset5DPricingEngine

print("==================================================")
print("📊 2026 秋季 AI 家教實戰系列班 · 5D 2.0 矩陣深度重新試算")
print("==================================================")

# ----------------------------------------------------
# 1. 模態 A：5D-Labor（工時防禦型 —— 單堂實體課總成本）
# ----------------------------------------------------
# 創辦人陳品碩親自主講 + 助教現場排錯
# 顯性工時 120 分鐘 (60分精講 + 60分一對一除錯)
# 隱性工時 90 分鐘 (課前場地投影測試 40分 + 課後個別學員諮詢 30分 + 審查通知 20分)
labor = Labor5DPricingEngine(base_rate=500.0, default_min_fare=1000.0)
res_labor = labor.calculate(
    base_minutes=210, # 3.5 小時
    d1_friction=1.3,  # 線下實體場地、10台筆電不同作業系統環境雜訊
    d2_difficulty=1.5, # 現場除錯壓力極大，不允許出糗
    d3_degree=2.0,    # 稀缺高階技術 (NotebookLM 提示詞 + Meta API 自動化 + 人格心智)
    d4_development=1.5, # 兩小時即時讓學員看到產出
    d5_delight=1.6,   # 手把手盯緊、不驗收過關不准下課之極致安心感
    task_name="2026秋季AI家教軍事班單堂實體授課"
)

single_session_cost = res_labor['final_price']
three_sessions_cost = single_session_cost * 3
cost_per_student_session = single_session_cost / 10.0
cost_per_student_series = three_sessions_cost / 10.0

print(f"\n【模態 A：5D-Labor 勞務工時防禦視角】")
print(f"- 單堂課全場 5D 總點數 (TP): {res_labor['metrics']['tp_score']}")
print(f"- 單堂課全場最低防禦成本: NT$ {single_session_cost:,} 元")
print(f"- 三週系列課全場總防禦成本: NT$ {three_sessions_cost:,} 元")
print(f"👉 滿班 10 人平攤，每位學員【單堂保底底線】: NT$ {cost_per_student_session:,.0f} 元")
print(f"👉 滿班 10 人平攤，每位學員【三堂全系列保底底線】: NT$ {cost_per_student_series:,.0f} 元")

# ----------------------------------------------------
# 2. 模態 B：5D-Impact（成果價值捕獲型 —— 學員終身商業價值）
# ----------------------------------------------------
# 學員學完後，為其在地店鋪或個人事業創造的具體成果：
# 1) 省下每月外包小編費用 (以台東在地行情兼職每月 8,000 元計，一年省 9.6 萬)
# 2) NotebookLM 建立私密智庫，省下每日找資料 1 小時 (一年 365 小時 * 200 = 7.3 萬)
# 3) 總經濟效益 (Value Impact) 保守估計達 NT$ 150,000 元/年
impact = Impact5DPricingEngine(base_retainer=3000.0, default_share_ratio=0.05)
res_impact = impact.calculate(
    value_impact=150000.0,
    d1_friction=1.2,
    d2_liability_risk=1.2,
    d3_expertise=2.0,
    d4_urgency=1.4,
    d5_strategic_trust=1.5,
    project_name="AI 家教系列課自動化賦能全案",
    client_name="店家學員"
)

print(f"\n【模態 B：5D-Impact 成果價值捕獲視角】")
print(f"- 學員一年獲得之實質商業價值 (Value Impact): NT$ 150,000 元")
print(f"- 依 5D 價值捕獲比例計算，每位學員三堂全系列公道定價: NT$ {res_impact['final_price']:,} 元")
print(f"👉 折合每堂課成果價值: NT$ {res_impact['final_price'] / 3:,.0f} 元")

# ----------------------------------------------------
# 3. 模態 C：5D-Asset（數位與實體知識資產規模型）
# ----------------------------------------------------
# 課綱研發投入：NotebookLM 模板、Meta 自動發文腳本、Google Form 自動化、圖卡生成腳本
# 研發製作成本保守估算 40,000 元，單班 10 人小班制交付
asset = Asset5DPricingEngine(target_volume=10, min_unit_price=1500.0)
res_asset = asset.calculate(
    fixed_dev_cost=40000.0,
    marginal_cost=300.0, # 現場冷氣、電費、教材影印茶水
    d1_acquisition_friction=1.3,
    d2_quality_guarantee=1.5,
    d3_intellectual_barrier=1.8,
    d4_market_timing=1.3,
    d5_brand_delight=1.5,
    product_name="2026秋季AI家教三週軍事班"
)

print(f"\n【模態 C：5D-Asset 知識資產攤提視角】")
print(f"- 研發與場地單人基底 (Unit Base): NT$ {res_asset['metrics']['unit_base']} 元")
print(f"- 資產溢價乘數 (Asset Multiplier): {res_asset['metrics']['asset_multiplier']}")
print(f"👉 建議每位學員三堂系列課定價: NT$ {res_asset['final_unit_price']:,} 元")
print(f"👉 折合每堂課資產單價: NT$ {res_asset['final_unit_price'] / 3:,.0f} 元")

print("\n==================================================")
