# 測試案例 001：省略號跳過數字

判定：【應退回】
網址：https://arxiv.org/abs/2403.09629
出處：https://arxiv.org/abs/2403.09629
摘句：we find zero-shot improvements on GSM8K ... and CommonsenseQA ... and observe a perplexity improvement of difficult tokens in natural text.
說明：摘句中使用省略號切割，其中片段「and CommonsenseQA」長度僅 17 字元（< 20 字元），導致關鍵數字被省略號跳過且規避了驗證。
