---
name: atom-yuki-brand-redline-gate
description: 品牌法定名稱零洩漏與出廠安全閘門原子 (Brand Red-Line Firewall & Outbound Gate Atom)。專門為執行長雪 (Yuki) 嚴格執行《全域工作區憲則·規則 5》品牌法定名稱防火牆，在任何對外文案（社群、LINE、表單、海報）中一票否決「極星/Polaris」代號洩漏，強制校準品牌全稱「生活的一部分，就醬點！」與「生活管家」。
---

# 🛡️ atom-yuki-brand-redline-gate (品牌法定名稱零洩漏與出廠安全閘門原子)

> **所屬梯隊**：第六梯隊（仿生自進化與天王特化演化群 · Cohort 6）  
> **母技能來源**：`bionic-learning-yuki`（第二章三相物理驗證器之紅隊閘門 ＆ 工作區憲則《規則 5》）  
> **核心職責**：專門執行「對外文案（FB、Threads、LINE OA、表單、印刷海報、客戶話術）之品牌法定名稱硬性門禁審查，一票否決內部研發代號（極星、Polaris）對外洩漏，強制校準法定全稱與業務稱謂」。

---

## 核心設計哲學：《規則 5》品牌法定名稱零洩漏防火牆

1. **對外防護罩**：
   * 在任何對外公開或面對常民客戶的文本中：
   * **官方品牌全稱**：強制為**「生活的一部分，就醬點！」**。
   * **日常業務自稱**：強制為**「生活管家」**。
2. **絕對紅線（一票否決）**：
   * **絕對嚴禁出現「極星」、「Polaris」、「北極星」等內部研發代號**！
   * 內部技術機密與算盤永遠在後台安靜運轉。
   * 任何對外草案若含有違規內部代號，安燈門禁將直接阻斷出廠（Exit Code 1）。

---

## 執行腳本與參數

專屬腳本位於 `scripts/yuki_brand_redline_gate.py`。

### 命令行介面 (CLI)

```bash
python scripts/yuki_brand_redline_gate.py --text "歡迎來到生活的一部分，就醬點！我是您的生活管家..."
python scripts/yuki_brand_redline_gate.py --file-path "outbound_post.txt"
```

### 核心參數
- `--text`：待審查之對外文案純文字。
- `--file-path`：待審查之對外檔案路徑。
- `--auto-fix`：自動修復違規詞，將內部代號替換為法定名稱。
- `--dry-run`：預演模式。
