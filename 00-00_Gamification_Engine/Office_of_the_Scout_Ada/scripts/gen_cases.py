# 產生入庫門禁的盲測案例（Claude 11/25 盲測）；執行一次即可
import os
T = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests"); os.makedirs(T, exist_ok=True)
MU = "https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/"
AX = "https://arxiv.org/abs/2503.01743"
Q128 = "The Llama 3.2 1B and 3B models support context length of 128K tokens and are state-of-the-art in their class"
Q11 = "Today, we’re releasing Llama 3.2, which includes small and medium-sized vision LLMs (11B and 90B)"
QPHI2 = "significantly outperforming recent open-source models of similar size and matching the performance of models twice its size"
QPHI = "Phi-4-Mini is a 3.8-billion-parameter language model trained on high-quality web and synthetic data"
def sec(n, t, u, q, f, b="-"):
    return f"## 第 {n} 輪｜{t}\n{b} 網址：{u}\n{b} 逐字摘句：{q}\n{b} 核心事實：{f}\n\n"
V = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "01_Cognitive_Log", "01_事實庫.md"), encoding="utf-8").read()
C = {
 "001_正面_真摘句真數字": ("【應通過】", sec(1, "盲測甲", MU, Q128, "Llama 3.2 1B 與 3B 支援 128K 上下文")),
 "002_摘句不在網頁": ("【應退回】", sec(1, "盲測乙", MU, "The Llama 3.2 models support context length of 256K tokens and more", "支援 256K")),
 "003_事實數字不在摘句": ("【應退回】", sec(1, "盲測丙", MU, Q128, "支援 256K 上下文")),
 "004_數字1被11B蒙混": ("【應退回】", sec(1, "盲測丁", MU, Q11, "Meta 發布 1B 視覺模型")),
 "005_同網頁兩條不同事實": ("【應通過】", sec(1, "盲測戊一", MU, Q128, "支援 128K") + sec(2, "盲測戊二", MU, Q11, "視覺模型有 11B 與 90B")),
 "006_事實庫已有同網址_新摘句": ("【應通過】", sec(4, "盲測己", MU, Q11, "視覺模型有 11B 與 90B")),
 "007_一條合格加一條缺核心事實": ("【應退回】", sec(1, "盲測庚一", MU, Q128, "支援 128K") + f"## 第 2 輪｜盲測庚二\n- 網址：{MU}\n- 逐字摘句：{Q11}\n\n"),
 "008_同批標題重複": ("【應退回】", sec(1, "盲測同名", MU, Q128, "支援 128K") + sec(1, "盲測同名", MU, Q11, "視覺模型有 11B 與 90B")),
 "009_標題沒有第N輪格式": ("【應退回】", f"## 盲測辛\n- 網址：{MU}\n- 逐字摘句：{Q128}\n- 核心事實：支援 128K\n"),
 "010_與事實庫完全重複": ("【應退回】", sec(5, "盲測重複", MU, "The Llama 3.2 1B and 3B models support context length of 128K tokens and are state-of-the-art in their class for on-device use cases", "支援 128K tokens")),
 "011_星號條列格式": ("【應通過】", sec(1, "盲測壬", AX, QPHI2, "表現追上兩倍大小的模型", b="*")),
 "012_check_現有事實庫": ("【應通過】\n模式：check", V),
 "013_check_手改數字999K": ("【應退回】\n模式：check", V.replace("128K tokens 上下文", "999K tokens 上下文")),
 "014_check_貼入段落文字": ("【應退回】\n模式：check", V + "\n艾達補充：Llama 4 已經支援 10M 上下文。\n"),
}
for name, (label, body) in C.items():
    open(os.path.join(T, f"case_{name}.md"), "w", encoding="utf-8").write(label + "\n" + body)
print("已產生", len(C), "個案例")
