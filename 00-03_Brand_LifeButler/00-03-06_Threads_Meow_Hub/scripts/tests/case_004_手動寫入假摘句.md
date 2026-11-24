<!-- test_mode: check -->
# 測試事實庫：手動寫入假摘句【應退回】

預期原因：免簽模式發現未經連網驗證（或摘句不符）

> 本檔案模擬手動繞過 prepare 直接寫入事實庫的情境。

---

1. **[K-002] 遞歸模型崩潰與數據分佈長尾消失**：
  - **核心事實**：以模型生成的內容進行訓練會對產生的模型造成不可逆的缺陷，導致原始內容分佈的長尾消失（稱為模型崩潰，發生於 VAE、GMM 與 LLM）。
  - **出處**：https://arxiv.org/abs/2305.17493
  - **證據網址**：https://arxiv.org/abs/2305.17493
  - **原文摘句**：We find that use of model-generated content in training causes irreversible defects in the resulting models, where tails of the original content distribution disappear. We refer to this effect as Model Collapse and show that it can occur in Variational Autoencoders, Gaussian Mixture Models and LLMs.

2. **[K-FAKE] 手動塞入之假條目**：
  - **核心事實**：手動捏造之假事實。
  - **出處**：https://example.com/fake
  - **證據網址**：https://example.com/fake
  - **原文摘句**：This is a totally fabricated sentence that does not exist on example.com at all.
