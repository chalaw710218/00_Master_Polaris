---
name: atom-onboarding-office-scaffolder
description: 👑 極星新首長入閣·總部大腦辦公室與實體主權目錄拓荒原子 (Polaris Cabinet Office & Domain Scaffolder Atom v1.0)。由執行長雪 (Yuki) 組織主政、CTO 林納斯 (Linus) 架構監製。專門在新夥伴入閣時，於 00-00 總部拓荒大腦辦公室 (Office_of_the_<職稱>_<Name>) 與隨身戰略筆記本 (00_<Name>_Notebook.md)，並於系統根目錄精算流水號劃定 00-XX 實體主權業務目錄及 5 大支柱業務子結構。
---

# 👑 極星大腦辦公室與實體主權目錄拓荒原子 (atom-onboarding-office-scaffolder)

由執行長雪 (Yuki) 業務主政、CTO 林納斯 (Linus) 架構監製、首席品質長戴明 (Dr. Deming) 防呆驗收。

## 核心定位與職責
專門解決新幹部加入時「領地劃定混亂、目錄命名不規範、缺少大腦辦公室或隨身筆記本、主權邊界與現有天王衝突」之痛點。
本原子作為主權拓荒物理終端，提供：
1. **00-00 總部大腦辦公室拓荒**：建立 `Office_of_the_<Title>_<Name>/`，內嵌總部憲章 `README.md` 與隨身戰略筆記本 `00_<Name>_Notebook.md`。
2. **根目錄實體主權資料夾劃定**：自動巡視系統根目錄，計算下一個序號（如 `00-14`），建立 `00-XX_<Domain>/`，並配置 5 大支柱業務子目錄結構。
3. **主權衝突戴明安燈防呆**：硬性防護既有 10 大首長辦公室與現有 00-01 至 00-13 領地，嚴禁覆蓋覆寫。

## 輸入參數規範
- `--member-name`: 首長英文代號（如 `Feynman`、`Oppenheimer`）
- `--member-title`: 首長職銜（如 `Chief_Scientific_Advisor`）
- `--domain-name`: 實體主權名稱（如 `Deep_Science_Lab`）
- `--dry-run`: 物理演練模式，輸出目錄規劃拓撲與檔案生成預覽

## 執行腳本
```bash
python scripts/office_scaffolder.py --member-name "Feynman" --member-title "Chief_Scientific_Advisor" --domain-name "Deep_Science_Lab" --dry-run
```
