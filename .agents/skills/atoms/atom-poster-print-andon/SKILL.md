---
name: atom-poster-print-andon
description: "海報印刷出廠前戴明十重安燈防呆閘門原子技能。專門在送廠印製（如健豪、藍格）或公開發布前，嚴格檢驗 300 DPI 物理解析度、3mm 出血線、總油墨覆蓋率 (TAC <= 250%)、K100 單色黑直壓、28mm 最小二維碼掃描邊界與品牌法定名稱零洩漏防火牆。"
---

# 🛑 海報印刷出廠前戴明十重安燈防呆閘門原子技能 (Poster Print Preflight Andon Gate Atom)

> **所屬技能組**：做海報 / 戴明品質工匠  
> **核心職責**：專精於海報印刷出廠前的「物理工程參數質檢、總油墨量 TAC 防背印、二維碼可掃描性、品牌零洩漏防火牆」。  
> **原技能母體**：`polaris-poster-artisan`

---

## 核心功能與深度特性
1. **印刷物理規範安燈 (Print Physics Gate)**：
   - 實體海報強制檢驗 300 DPI，防止鋸齒狀模糊。
   - 3mm 物理出血線檢驗（A4/A3 預留 85px），防止裁切白邊。
2. **總油墨覆蓋率 TAC 審計 (Total Area Coverage <= 250%)**：
   - 審計 CMYK 數值總和，硬性攔截 TAC > 250% 之過重色塊，避免台灣潮濕氣候大豆油墨慢乾與背印污染。
3. **K100 單色黑直壓防呆 (Overprint Black Gate)**：
   - 標籤文字硬性要求使用單色黑 (C0 M0 Y0 K100)，嚴禁四色混合黑 (C75 M68 Y67 K90) 導致細字套印不準與重影毛邊。
4. **28mm 二維碼可讀性防線 (QR Code Readability Gate)**：
   - 實體二維碼區塊寬度必須 >= 28mm (300 DPI 下 >= 330px)，四周具備 4 模組以上留白靜區 (Quiet Zone)。
5. **品牌法定名稱零洩漏防火牆 (Brand Red Line Gate)**：
   - 強制全域掃描海報文案與標籤，嚴禁對外出現「極星」、「Polaris」字樣；法定品牌名稱必須為「生活的一部分，就醬點！」或自稱「生活管家」。
6. **台灣正體中文語境驗證 (Taiwan Traditional Chinese Gate)**：
   - 攔截簡體字（如「门」、「关」）與大陸用語（如「視頻」、「走心」對外直出）。

---

## 執行腳本
```bash
python scripts/print_andon.py --input-spec path/to/poster_spec.json --dry-run
```
