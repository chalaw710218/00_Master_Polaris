---
name: atom-abacus-munger-inversion-veto
description: 財務長算盤·查理·蒙格逆向致死缺陷一票否決原子 (Munger Inversion Failure-Mode Veto Protocol v1.0)。貫徹「反向思考，永遠反向思考 (Invert, always invert)」。在採購或上架前，主動審查五大致死缺陷（解凍失水率、魚刺客訴、料理門檻、庫存死線、邊際貢獻不足）。若任一致死缺陷缺乏確定性物理防呆措施，堅決行使一票否決權！
role_key: abacus
type: atomic_skill
parent_skill: bionic-learning-abacus
version: v1.0
exit_code_verified: true
---

# ⚔️ 查理·蒙格逆向致死缺陷一票否決原子 (Munger Inversion Veto)

> 🧮 **原子使命**：貫徹查理·蒙格最經典的哲學——**「如果我知道我會死在哪裡，我就永遠不去那裡。」** 大多數商業失敗不是因為缺少熱情，而是因為對顯而易見的致死缺陷視而不見。本原子在上架、採購與報價前夕，化身冷酷無情的反向審計官，排查五大致死威脅，凡無具體防呆方案者，一票否決阻斷出廠！

---

## 🏛️ 五大逆向致死缺陷審查清單 (Five Fatal Failure Modes)

```mermaid
flowchart TD
    Product["受檢選品 / 採購品項"] --> F1{"1. 解凍失水率 > 2%？\n(肉質變柴、口感崩潰)"}
    Product --> F2{"2. 刺多刺軟易卡喉？\n(引發長輩與家庭客訴)"}
    Product --> F3{"3. 料理手續過度繁瑣？\n(顧客買回家積灰不回購)"}
    Product --> F4{"4. 庫存停留 DSI > 15 天？\n(吃電費、壓資金、變死貨)"}
    Product --> F5{"5. 邊際貢獻 < 30%？\n(常態品<30% / 孤品<45%)"}
    
    F1 & F2 & F3 & F4 & F5 -->|存在致命傷且無解| Veto["❌ 一票否決 (HARD_VETO)\n• 蒙格封印，禁止上架採購"]
    F1 & F2 & F3 & F4 & F5 -->|全數具備物理防呆| Pass["✅ 逆向審查通過 (INVERSION_PASSED)\n• 具備物理免疫力，准予發行"]
```

### 1. 解凍失水超標（> 2.0%）
* **風險**：解凍後組織液流失，魚肉乾柴，客訴率飆升 40%。
* **解法**：必須配備 -50°C 急速冷凍與磚型真空包裝，現場實測失水 $\le 1.1\%$。

### 2. 多刺難挑刺
* **風險**：家有幼兒長輩者極易噎刺，造成信任崩塌。
* **解法**：必須人工二次去刺檢驗，或提供專業去刺骨切片，否則標註「料理高手專用」降級。

### 3. 料理繁瑣度
* **風險**：需去鱗、去鰓、清內臟者，常民家庭抗拒處理。
* **解法**：產地三去（去鱗、去鰓、去內臟）完成，附 3 分鐘電鍋/香煎圖卡食譜。

### 4. 庫存停留時間（DSI）
* **風險**：超過 15 天未消化，吃電費並排擠容積。
* **解法**：100% 走預售集單制，或設置 20 天警報、25 天保本自噬銷毀。

### 5. 邊際貢獻率底線
* **風險**：常態品邊際貢獻率 $< 30\%$，孤品 $< 45\%$。
* **解法**：毛利不足一律砍單，拒絕為供應商白打工。

---

## 🛠️ 命令列工具 (CLI Usage)

```powershell
# 執行五大逆向致死缺陷審核
python scripts/munger_inversion_veto.py --audit '{"item_name": "野生青甘魚排", "drip_loss_rate": 0.012, "has_pin_bones": false, "kitchen_prep_minutes": 5, "projected_dsi_days": 3, "contribution_margin": 0.36, "is_rare_item": false}'
```
