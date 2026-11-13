---
name: atom-slimming-4d-dispatcher
description: 🧘‍♀️ 極星三層心智·四維真值動態調用方程式運算原子 (Polaris Cognitive 4D Dispatch Calculator Atom v1.0)。創辦人（品碩）親自賜名「瘦身」。嚴格恪守工作區憲則《規則 6：三層心智架構與動態調用方程式永久死鎖憲則》。專門在接收創辦人提問 Q 時，計算 S(D_i|Q) = w_r*R + w_u*U + w_a*A - w_c*C，即時篩選出分數最高之 Top-3 中層精確切片 (300~500字) 動態注入推論，用畢即釋。
---

# 🧘‍♀️ 極星四維真值動態調用方程式運算原子 (atom-slimming-4d-dispatcher)

由技術長林納斯 (Linus) 確定性架構主政、品質長戴明 (Dr. Deming) 安燈驗收、創辦人（品碩）最高授權。

## 核心定位與職責
專門解決推論時「全量加載海量歷史 Markdown 導致 Token 負載爆發、信噪比雪崩」之痛點。
本原子作為中層記憶線上調度運算終端，提供：
1. **四維真值方程式精準裁決**：
   $$S(D_i \mid Q) = w_r \cdot R(D_i, Q) + w_u \cdot U(D_i) + w_a \cdot A(D_i) - w_c \cdot C(D_i)$$
   - $R$（語義關聯）：提問與候選知識點的高維關聯度。
   - $U$（公理效用）：實戰置信度與代碼化驗證加權。
   - $A$（時間衰減活性）：近期驗證鮮活度指數衰減 $e^{-\lambda t}$。
   - $C$（衝突懲罰）：已廢棄或邏輯矛盾之巨額抑制。
2. **天王專屬權重向量特化**：為雪、林納斯、算盤、戴明、影等注入專屬 $\vec{W} = [w_r, w_u, w_a, w_c]$。
3. **Top-3 輕量片段毫秒級提取**：只回傳前 3 名最高分片段（合計 $\le 500$ 字），用畢即釋，確保推論零負擔。

## 輸入參數規範
- `--query`: 創辦人當前輸入之問題或決策命題
- `--agent-role`: 接收提問之天王角色（如 `yuki`, `linus`, `abacus`, `deming`, `kage`，預設 `yuki`）
- `--dry-run`: 物理演練模式，輸出四維分數計算矩陣與 Top-3 抽脂片段預覽

## 執行腳本
```bash
python scripts/dispatch_calculator.py --query "我們這週的工作坊開課席次到底要設幾席？" --agent-role "yuki" --dry-run
```
