import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
SKILL_PATH = WORKSPACE / ".agents" / "skills" / "bionic-learning-falcon" / "SKILL.md"

text = SKILL_PATH.read_text(encoding="utf-8")

# 1. 更新 frontmatter
frontmatter_pat = r"^---\s*\n(.*?)\n---"
def repl_frontmatter(m):
    return """---
name: bionic-learning-falcon
description: 🦅 首席法務顧問兼市場情報長特化版，第 2–5 章依母版 v6.5 執行。
base_master: .agents/skills/bionic-learning-system/SKILL.md (v6.5 Master，第 2–5 章依母版 v6.5 執行，不在此複製)
version: v6.5 (Clean Ground-Truth Edition)
role_key: falcon
is_daughter_variant: true
can_evolve_independently: true
authorized_by: 陳品碩 (Pinshuo)
---"""

text = re.sub(frontmatter_pat, repl_frontmatter, text, count=1, flags=re.DOTALL)

# 2. 修改前言鎖定說明與標題區塊
top_section_pat = r"---\n\n> 🔒 \*\*【創辦人品碩親定鋼鐵法規.*?## 🏛️ 第一章"
new_top_section = """---

> 🔒 **【母版繼承架構】**  
> 第 2–5 章依母版 v6.5 執行，不在此複製。本特化知識體系自第六章開展。


# 🦅 首席法務顧問兼市場情報長特化版 (Chief Legal & Strategic Radar Variant)

> **特化角色**：首席法務顧問兼市場情報長 (CIO) · 獵鷹 (Falcon / Sheryl Sandberg 原型)  
> **法定責任領地**：[`00-07_TWQR_Promotion/`](file:///C:/Users/lenovo/我的雲端硬碟/00_Master_Polaris/00-07_TWQR_Promotion/00-07-00_TWQR_and_Commercial_Intelligence_Overview.md)（TWQR 金流推廣、B2B 商戰情資與特約店家換碼防線）  
> **核心使命**：外部環境預警、法規地雷排查、大盤底價逆推、競品情報解構、數據多維交叉驗證。  
> **基石繼承**：第 2–5 章依母版 v6.5 執行，不在此複製。

---

## 🏛️ 第一章"""

text = re.sub(top_section_pat, new_top_section, text, count=1, flags=re.DOTALL)

# 3. 替換第八章與第九章
ch8_pat = r"## ⚖️ 第八章.*"
new_ch8_ch9 = """## ⚖️ 第八章｜十二代大審計時空解耦憲則
已移至 _未驗證封存，待逐條反查。

---

## 🎯 第九章｜極星跨內閣三位一體戰略架構
已移至 _未驗證封存，待逐條反查。
"""

text = re.sub(ch8_pat, new_ch8_ch9, text, count=1, flags=re.DOTALL)

# 寫入兩個檔案
target1 = WORKSPACE / ".agents" / "skills" / "bionic-learning-falcon" / "SKILL.md"
target2 = WORKSPACE / "00-00_Gamification_Engine" / "Office_of_the_CIO_Falcon" / "bionic-learning-falcon.md"

target1.write_text(text, encoding="utf-8")
target2.write_text(text, encoding="utf-8")
print("成功清洗並更新兩份技能檔！")
