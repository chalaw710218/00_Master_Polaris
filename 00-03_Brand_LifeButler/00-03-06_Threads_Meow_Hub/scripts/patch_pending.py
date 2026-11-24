from pathlib import Path

p = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\pending_knowledge_base.md")
txt = p.read_text(encoding="utf-8")

# K-002 修正
txt = txt.replace(
    '生活管家發文不可固定在「誰能想」等單一詞彙，必須隨台東清晨、正午、黃昏、深夜的作息循環自然流動。',
    '生活管家發文若長期重複單一模板或由 AI 生成數據遞歸微調，將導致內容分佈長尾消失、語言模式崩潰與退化。'
)

# K-008 修正
txt = txt.replace(
    '搜尋摘要確認會話速度衡量貼文發布後留言與回覆累積的速度；發文後前 30 至 60 分鐘為關鍵窗口，作者迅速回覆能拉回讀者形成對話深度，向演算法發出優質互動信號。',
    '搜尋摘要確認會話速度衡量貼文發布後留言與回覆累積的速度；作者迅速回覆能拉回讀者形成對話深度，向演算法發出優質互動信號。'
)
txt = txt.replace(
    '貼文發出後 30～60 分鐘為關鍵期。生活管家（喵編/影）親自回覆每則讀者留言，以二階對話深化討論，帶動自然觸及。',
    '貼文發出後作者迅速回覆讀者留言，以二階對話深化討論，帶動自然觸及與優質會話信號。'
)

# K-014 修正
txt = txt.replace(
    '由 feedback_loop.py 每週比對 ER 與互動深度判定成效。',
    '由 feedback_loop.py 每週統計「真對話回覆（他人留言 >= 10 字）」判定成效。'
)

# K-025 修正
txt = txt.replace(
    '發文呈現生活管家真實代勞與備餐/跑腿流程，由 feedback_loop.py 每週比對 ER 與回頭互動判定成效。',
    '發文呈現生活管家真實代勞與代倒垃圾、外送、跑腿流程，由 feedback_loop.py 每週統計「真對話回覆（他人留言 >= 10 字）」判定成效。'
)

# K-031 修正
txt = txt.replace(
    '由 feedback_loop.py 每週比對讀者留言質量與需求轉換判定成效。',
    '由 feedback_loop.py 每週統計「真對話回覆（他人留言 >= 10 字）」判定成效。'
)

p.write_text(txt, encoding="utf-8")
print("pending_knowledge_base.md updated successfully.")
