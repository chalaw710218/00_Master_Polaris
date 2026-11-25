---
name: atom-supplychain-layer-deconstructor
description: "供應鏈四層摩擦與毛利精算底座原子技能。專門針對各級供應商開出的批發報價，建立嚴謹數學倒推模型：從中盤報價逆向剝離『L3 中盤加成』、『L2 進口大盤利潤』、『物理加工修清/失水損耗 (5%~20%)』、『跨國海空運與關稅檢疫摩擦』，精準還原『L1 產地出貨價 (FOB/EXW)』，並量化其虛報溢價率 (Markup Inflation Rate)。"
---

# ⚓ 供應鏈四層摩擦與毛利精算底座原子技能 (Supply Chain Layer Deconstructor Atom)

> **所屬技能組**：選品審計 / 算盤財務工匠  
> **核心職責**：專精於「四層供應鏈數學倒推、產地出貨價 (FOB) 精算、加工修清耗損率量化、國際物流與關稅摩擦剝離、虛報溢價率審計」。  
> **原技能母體**：`ai-pricing-auditor`

---

## 核心功能與深度特性
1. **四層階層毛利數學倒推架構 (4-Layer Supply Chain Decomposition)**：
   - $\text{L3 中盤價 (Quoted Price)}$ ➔ 剝離中盤毛利 (15%~25%) ➔ $\text{L2 大盤批發價}$。
   - 剝離物理加工耗損（肉品修清失水 12%~18%、水產包冰 10%~15%、乾貨篩選 5%）。
   - 剝離國際物流摩擦（跨國貨櫃運費 4%~8%、進口關稅 5%~15%、報驗檢疫與冷凍倉儲 3%）。
   - 還原 $\text{L1 產地出貨底價 (FOB/EXW)}$。
2. **虛報溢價率量化 (Markup Inflation Rate)**：
   - 當廠商報價高於「合理成本＋大中盤健康利潤 (共 30%~35%)」時，精準算出灌水金額與灌水百分比，為老闆提供實質降價空間指標。
3. **生鮮/肉品/乾貨專屬參數矩陣**：
   - 內建進口牛肉、智利鮭魚、進口堅果、台灣高麗菜等產業常態係數庫。
4. **乾跑防呆 (Dry-Run Support)**：
   - 支援 `--dry-run` 模擬全鏈條推算，輸出結構化數值報表與 JSON。

---

## 執行腳本
```bash
python scripts/layer_deconstructor.py --item "智利冷凍鮭魚 (整尾原箱)" --quote 420 --category "seafood" --dry-run
```
