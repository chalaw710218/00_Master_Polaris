import json
from pathlib import Path

vault = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\.agents\skills\bionic-learning-system\bionic_core\vaults\cycle_evidence")

data = {
    "kage_cycle_09_real.json": {
        "source_url": "https://www.standard.co.uk/news/tech/threads-app-feed-meta-engagement-bait-spam-adam-mosseri-b1158482.html",
        "quote_status": "verbatim",
        "quote": "We've seen an increase in engagement bait on Threads and we're working to get it under control. More to come."
    },
    "kage_cycle_10_real.json": {
        "source_url": "https://arxiv.org/abs/2305.17493",
        "quote_status": "verbatim",
        "quote": "We find that use of model-generated content in training causes irreversible defects in the resulting models, where tails of the original content distribution disappear. We refer to this effect as Model Collapse and show that it can occur in Variational Autoencoders, Gaussian Mixture Models and LLMs."
    },
    "kage_cycle_11_real.json": {
        "source_url": "https://traversingtradition.com/2021/04/19/the-beauty-of-everyday-things-soetsu-yanagi/",
        "quote_status": "summary_only",
        "quote": "探討柳宗悅民藝運動，核心在於真之美源於日用與質樸工藝，由無名匠人為日常需要製作的器物具有深厚人情連結。"
    },
    "kage_cycle_12_real.json": {
        "source_url": "https://developerux.com/mobile-typography-ux-guide/",
        "quote_status": "summary_only",
        "quote": "行動端最佳閱讀參數：行長建議控制在 35 至 50 字元，行高至少設為字級的 1.5 倍，透過留白減少滑動疲勞。"
    },
    "kage_cycle_13_real.json": {
        "source_url": "https://www.brookings.edu/articles/third-places-as-community-builders/",
        "quote_status": "summary_only",
        "quote": "依據 Ray Oldenburg 理論，家庭與工作之外的中立非正式場所為第三空間，是建立社區弱連結與互助的關鍵紐帶。"
    },
    "kage_cycle_14_real.json": {
        "source_url": "https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview",
        "quote_status": "summary_only",
        "quote": "消除 AI 腔之道在於要求模型使用直接的主動動詞、明確的陳述句結構與具體現場觀察，而非抽象形容詞與宣傳修辭。"
    },
    "kage_cycle_15_real.json": {
        "source_url": "https://www.slowfood.com/about-us/our-philosophy/",
        "quote_status": "summary_only",
        "quote": "慢食三原則為美味季節性、友善環境與生產者經濟尊嚴，將被動消費者轉化為在地共同生產者。"
    },
    "kage_cycle_16_real.json": {
        "source_url": "https://sproutsocial.com/insights/social-media-algorithms/",
        "quote_status": "summary_only",
        "quote": "會話速度衡量貼文發布後留言與回覆累積的速度；發文後前 30 至 60 分鐘為關鍵窗口，作者迅速回覆能拉回讀者形成對話深度。"
    },
    "kage_cycle_17_real.json": {
        "source_url": "https://extranet.who.int/agefriendlyworld/",
        "quote_status": "summary_only",
        "quote": "世界衛生組織八大高齡友善範疇，核心在於消除環境障礙，支援長輩在熟悉社區自立並在地安老。"
    },
    "kage_cycle_18_real.json": {
        "source_url": "https://fstoppers.com/originals/why-authenticity-photography-matters-more-ever-634912",
        "quote_status": "summary_only",
        "quote": "受眾因生成圖氾濫而對無瑕疵畫面產生防衛心理；自然光線、真實環境與不完美細節，已成為建立真實信任的先決條件。"
    }
}

for fname, content in data.items():
    p = vault / fname
    p.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Updated:", fname)
