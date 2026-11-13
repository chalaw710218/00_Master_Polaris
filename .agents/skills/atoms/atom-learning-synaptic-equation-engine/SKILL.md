---
name: atom-learning-synaptic-equation-engine
description: 突觸-代謝動態方程與全域激素場運算原子 (Synaptic-Metabolic Equation & Hormonal Field Engine Atom)。專職負責計算全域突觸權重調整方程，精算創辦人情感/指令浴（多巴胺強化 vs 皮質醇修剪）、PRM 物理驗證誤差、活動合格跡因果分配與溶酶體半衰期自噬衰減。
---

# 🧮 atom-learning-synaptic-equation-engine (突觸-代謝動態方程與全域激素場運算原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-system`（第五章｜突觸-代謝-驗證方程）  
> **核心職責**：專門執行「全域突觸-代謝方程 $\Delta w$ 浮點數精算、創辦人全域激素場（多巴胺 vs 皮質醇）調控、PRM 物理驗證誤差折射、因果活動合格跡分配、以及溶酶體衰減自噬判定」。

---

## 核心設計哲學：全域控制論方程

全域系統權重調整與認知存活受控於動態微分方程：

$$\Delta w = \eta \cdot \Pi_{global} \cdot \delta_{verifier} \cdot e - \lambda_{decay} \cdot w$$

### 核心參數矩陣：
1. **$\eta$ (學習率)**：控制更新步伐（常規 0.05，架構突變 0.20）。
2. **$\Pi_{global}$ (創辦人全域激素場)**：
   * **創辦人認可 / 「核准」 / 點頭讚許** ➔ 注入**多巴胺 ($1.5 \sim 2.0$)**，大幅強化當前活躍突觸！
   * **創辦人示警 / 糾正 / 叫停** ➔ 注入**皮質醇 ($0.2 \sim 0.5$)**，加速衰減與自噬切除！
3. **$\delta_{verifier}$ (PRM 物理驗證落差)**：由終點驗證器客觀給出（Exit Code 0 ➔ 1.0；異常 ➔ 0.0）。
4. **$e$ (活動合格跡)**：因果時間追溯分配，集中獎勵決定性動作。
5. **$\lambda_{decay} \cdot w$ (溶酶體衰減項)**：長期未調用或半衰期超標者，自動衰減歸入冷庫。

---

## 執行腳本與參數

專屬腳本位於 `scripts/synaptic_equation_engine.py`。

### 命令行介面 (CLI)

```bash
python scripts/synaptic_equation_engine.py --founder-feedback "核准" --prm-score 1.0 --weight 0.8
python scripts/synaptic_equation_engine.py --founder-feedback "叫停" --prm-score 0.0 --weight 0.9
```

### 核心參數
- `--founder-feedback`：創辦人回饋情感/指令（"核准" / "讚" / "糾正" / "叫停"）。
- `--prm-score`：PRM 過程驗證分數 (0.0 ~ 1.0)。
- `--weight`：當前模組或突觸初始權重 $w$。
- `--learning-rate`：學習率 $\eta$ (預設 0.05)。
- `--decay-rate`：溶酶體衰減率 $\lambda$ (預設 0.02)。
