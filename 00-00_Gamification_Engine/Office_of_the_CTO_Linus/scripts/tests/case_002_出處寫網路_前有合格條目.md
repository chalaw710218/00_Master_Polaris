# 測試事實庫：出處寫網路_前有合格條目【應退回】

> 本案例測試 check 時，第 1 條為合格條目，第 2 條出處不合格（填寫為「網路」）且帶有證據網址與原文摘句的情境。
> 預期：第 2 條之證據網址與摘句不得錯誤污染覆蓋第 1 條，正常印出「出處不合格」並 Exit Code 1。

---

1. **[TEST] 合格前置條目**：
   - **核心事實**：這是一條出處與格式皆合規的前置有效條目。
   - **出處**：https://arxiv.org/abs/1706.03762
   - **證據網址**：https://arxiv.org/abs/1706.03762
   - **原文摘句**：The dominant sequence transduction models are based on complex recurrent or convolutional neural networks.

2. **[TEST] 出處寫網路測試條目**：
   - **核心事實**：出處填寫為網路之假條目。
   - **出處**：網路
   - **證據網址**：https://arxiv.org/abs/2401.00002
   - **原文摘句**：This sentence is meant to test whether invalid source contaminates previous entry evidence fields.
