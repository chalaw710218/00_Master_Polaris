# 🧠 參考卷一｜仿生自進化底層理論：FEP 主動推論、過程級自檢、自對弈與突觸代謝方程

> **定位**：本文件為 `bionic-learning-system` 母版之附屬理論參考檔（`references/01_cognitive_theories_fep_prm_spin.md`），平時不佔用主對話上下文，僅於設計新子版或進行十輪認知審計時按需讀取。

---

## 1. 自主導航與主動推論雙路徑 (Active Inference Pathways)
基於卡爾·弗里斯頓（Karl Friston）自由能原理（Free Energy Principle, FEP），任何閣員面對未知或誤差時，僅有兩條合法減熵路徑：
1. **知覺修正路徑 (Perception / Epistemic Update)**：
   - 當外部物理或法規邊界不可變動時，修正內部信念與規則庫（呼叫 `rule_store.py propose` 建立候選規則）。
2. **行動塑造路徑 (Action / Pragmatic Execution)**：
   - 當外部環境具備可塑性時，透過具體工具、腳本或行動改變外部狀態，再由外部驗證器採集新真值。

---

## 2. 過程級逐步自檢 (Step-by-Step Process Self-Check)
- **核心原則**：不在最後一刻才看結果，而是在推導的每一個中間步驟檢查前提是否成立。
- **誠實界定**：在未額外訓練獨立獎勵模型（PRM）前，模型於思考鏈內執行的逐步檢查統稱為**「過程級自檢」**；凡可列舉之規則（黑名單、數值上下限、正則、字數）一律移交 `bionic_core/enforce.py` 由確定性程式執行。

---

## 3. 內部自對弈去 AI 腔 (Self-Play Critique)
- 生成對外或對上草稿前，於內部模擬「挑剔受眾 / 紅隊審計員」視角挑出說教腔、空洞排比與塑料套版詞彙，並將高頻違規詞沉澱為子版專屬之 `forbid_phrase` 或 `regex_forbid` 規則。

---

## 4. 突觸代謝與溶酶體自噬方程 (Synaptic Metabolism & Autophagy)
$$\Delta w_i = \eta \cdot \Pi_{\text{global}} \cdot \delta_{\text{truth}} \cdot e_i - \lambda_{\text{decay}} \cdot (1 - \text{utility}_i)$$
- **$\Pi_{\text{global}}$（創辦人主權訊號）**：以創辦人簽收詞（`收` / `退` / `改派`）或 `--founder-approved` 為最高權重。
- **$\delta_{\text{truth}}$（外部真值誤差）**：由 `rule_store.py evaluate` 讀取真實資料集計算之 `with_metric - without_metric`（含留出驗證與誤傷率檢查）。
- **$\lambda_{\text{decay}}$（溶酶體自噬）**：由 `rule_store.py sweep` 自動淘汰超過 `ttl_days` 或最新真值驗算轉負之規則。
