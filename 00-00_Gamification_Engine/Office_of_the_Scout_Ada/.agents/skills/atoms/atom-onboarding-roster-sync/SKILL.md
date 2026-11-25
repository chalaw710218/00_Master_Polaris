---
name: atom-onboarding-roster-sync
description: 👑 極星新首長入閣·四大法定通訊錄全域同步與角色 DNA 註冊原子 (Polaris Cabinet Roster Sync & Visual DNA Atom v1.0)。由執行長雪 (Yuki) 組織主政、首席視覺長約瑟夫 (Josef) 人設協同。專門向全域四大法定真理來源（CEO 筆記本、HR 人事庫、角色庫總綱、導航總地圖）進行原子化、無遺漏的新成員登錄，並於 00-03-04 註冊台前角色卡與真實照片視覺 DNA (Visual SSOT)。
---

# 👑 極星四大法定通訊錄同步與角色 DNA 註冊原子 (atom-onboarding-roster-sync)

由執行長雪 (Yuki) 業務主政、首席視覺長約瑟夫 (Josef) 視覺監製、首席品質長戴明 (Dr. Deming) 防呆驗收。

## 核心定位與職責
專門解決新首長入閣後「各處檔案記載不一、出現幽靈幹部、角色缺少真實照片 DNA 導致生圖面部走樣崩潰」之系統性混亂。
本原子作為全域神經登錄終端，提供：
1. **角色 DNA 註冊**：於 `00-03-04_Brand_Characters/<編號>_<中文名>_<英文名>/` 配置真實照片目錄、`persona.md`（神級標配道具、金句口頭禪、嚴格禁語表）與視覺法典。
2. **四大法定真理來源原子化同步**：
   - 來源 1：執行長戰略手冊 (`00-00_Gamification_Engine/Office_of_the_CEO_Yuki/00_CEO_Notebook.md`)
   - 來源 2：AI 人事總庫 (`00-00_Corporate_AI_HR_Directory.md`)
   - 來源 3：品牌角色庫總綱 (`00-03-04-00_Characters_Overview.md`)
   - 來源 4：全域導航總地圖 (`00-01_Master_Polaris_Map.md`)
3. **戴明安燈出廠驗收**：自動校驗四大通訊錄條目是否存在斷鏈或名稱歧義，確保 100% 同步合一。

## 輸入參數規範
- `--member-name-en`: 首長英文名（如 `Feynman`）
- `--member-name-zh`: 首長中文名（如 `費曼`）
- `--role-title`: 內閣職銜（如 `首席科學顧問`）
- `--serial-no`: 角色序號（如 `10`）
- `--dry-run`: 物理演練模式，輸出四大通訊錄同步 Payload 與角色卡預覽

## 執行腳本
```bash
python scripts/roster_sync.py --member-name-en "Feynman" --member-name-zh "費曼" --role-title "首席科學顧問" --serial-no 10 --dry-run
```
