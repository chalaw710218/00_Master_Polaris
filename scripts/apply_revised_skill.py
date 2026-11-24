import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
SKILL_PATH = WORKSPACE / ".agents" / "skills" / "bionic-learning-falcon" / "SKILL.md"
REVISED_PATH = HERE / "chapter6_13_24_revised.md"

revised_ch6_text = REVISED_PATH.read_text(encoding="utf-8").strip()
skill_text = SKILL_PATH.read_text(encoding="utf-8")

# 1. 更新 frontmatter 的 base_master
skill_text = re.sub(
    r"base_master:.*",
    "base_master: .agents/skills/bionic-learning-system/SKILL.md (v6.5 Master，第 2–5 章依母版 v6.5 執行，不在此複製)",
    skill_text
)

# 2. 刪除複製進來的第 2–5 章 (從 '## 🔒 第二章' 到 '## ⚡ 第六章' 之前)
pat_ch2_to_5 = r"## 🔒 第二章｜外部物理驗證器.*?(---\s*)+## ⚡ 第六章"
replacement_bridge = """🔒 **【母版繼承架構】**  
第 2–5 章依母版 v6.5 執行，不在此複製。本特化知識體系自第六章開展。

---

## ⚡ 第六章"""

new_text, n = re.subn(pat_ch2_to_5, replacement_bridge, skill_text, flags=re.DOTALL)
print(f"刪除第 2-5 章替換結果匹配次數: {n}")

# 3. 替換第六章的第 13–24 條
# 從 '### 13. 產生源產權邊界死守律' 到 '## 🔬 第七章' 之前
pat_13_to_24 = r"### 13\. 產生源產權邊界死守律.*?(---\s*)+## 🔬 第七章"
replacement_rules = revised_ch6_text + "\n\n---\n\n## 🔬 第七章"

new_text, n2 = re.subn(pat_13_to_24, replacement_rules, new_text, flags=re.DOTALL)
print(f"替換第 13-24 條匹配次數: {n2}")

# 寫入兩個檔案
target1 = WORKSPACE / ".agents" / "skills" / "bionic-learning-falcon" / "SKILL.md"
target2 = WORKSPACE / "00-00_Gamification_Engine" / "Office_of_the_CIO_Falcon" / "bionic-learning-falcon.md"

target1.write_text(new_text, encoding="utf-8")
target2.write_text(new_text, encoding="utf-8")
print("成功寫入兩個技能檔！")
