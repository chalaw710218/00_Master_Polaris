# 測試事實庫：出處寫網路_單條【應退回】

> 本案例測試 check 時，單一條目出處不合格（填寫為「網路」），但後續帶有證據網址與原文摘句的情境。
> 預期：不可出現 IndexError 或 list index out of range，正常印出「出處不合格」並 Exit Code 1。

---

1. **[TEST] 單條出處寫網路測試**：
   - **核心事實**：出處填寫為網路之假條目。
   - **出處**：網路
   - **證據網址**：https://arxiv.org/abs/2401.00001
   - **原文摘句**：This sentence is meant to test whether check crashes with IndexError when valid_entries is empty.
