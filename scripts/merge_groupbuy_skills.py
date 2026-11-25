# -*- coding: utf-8 -*-
"""
scripts/merge_groupbuy_skills.py
執行【管家選品】合併與【發臉書】金鑰脫敏：
1. 建立 _proposed/管家選品/
2. 母體 sharp-groupbuy-analyzer/SKILL.md 植入防重審查第 0 步與 4 個 atom 調用說明
3. 移入並更新 4 個 atom 的 metadata (group: 管家選品, parent: sharp-groupbuy-analyzer, description 結尾)
4. 移除 _proposed/選品行銷 與 _proposed/選品審計
5. 脫敏 _proposed/發臉書/facebook-publisher/SKILL.md 的明文 Token
"""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(".")
PROPOSED_DIR = BASE_DIR / "_proposed"
GROUPBUY_PROPOSED = PROPOSED_DIR / "管家選品"
FB_PROPOSED = PROPOSED_DIR / "發臉書" / "facebook-publisher" / "SKILL.md"

ORIG_SHARP_117 = BASE_DIR / "00-02_GroupBuy_Products" / ".agents" / "skills" / "sharp-groupbuy-analyzer" / "SKILL.md"
ORIG_FB_138 = BASE_DIR / "00-02_GroupBuy_Products" / ".agents" / "skills" / "facebook-publisher" / "SKILL.md"

# 1. 確保 _proposed/管家選品 目錄存在
GROUPBUY_PROPOSED.mkdir(parents=True, exist_ok=True)

# 2. 構建 sharp-groupbuy-analyzer 母體
# 讀取 117 行原檔
raw_sharp = ORIG_SHARP_117.read_text(encoding="utf-8")

# 分離 frontmatter 與 body
parts = raw_sharp.split("---", 2)
sharp_body = parts[2].lstrip() if len(parts) >= 3 else raw_sharp

# 定義標準 frontmatter
sharp_frontmatter = """---
name: sharp-groupbuy-analyzer
description: 執行利刃商品七步分析、逆推上游成本與產出喵編社群圖文。在取得商品照片進行選品調研與行銷企劃時使用；非實體商品專案時不用。
metadata:
  group: 管家選品
  owner: 泰勒絲
  status: draft
  version: "1.0"
---

## 🧩 所屬原子技能與調用順序 (Atom Sequence)

本母體按以下先後順序協同 4 大專精原子技能完成全閉環運作：

1. **執行 `atom-supplychain-layer-deconstructor`**（第 5 步成本逆推前置）：
   - **調用時機**：在取得商品報價或查得市價後、進入定價策略前調用。
   - **必要性說明**：以四層（L1 產地出貨價 FOB/EXW ➔ L2 進口大盤 ➔ L3 中盤 ➔ 物理加工與損耗 5%~20%）數學倒推模型，嚴謹剝離國際物流、關稅檢疫與中盤加成摩擦，精準量化廠商虛報溢價率，算出上游真實底牌成本。
2. **執行 `atom-groupbuy-cost-auditor`**（第 2、3 步市調與第 5 步定價）：
   - **調用時機**：在規格價格市調、廠商背景新聞搜尋，以及制定階梯式定價時調用。
   - **必要性說明**：比對主流電商零售與批發行情，嚴格排查廠商負面食安新聞與工廠合規性，並結合逆推極限成本，設計強調「品質越級」而非廉價折扣的管家階梯定價策略。
3. **執行 `atom-supplychain-tactical-negotiator`**（第 5 步商務談判準備）：
   - **調用時機**：在掌握底牌數據與真實毛利後、向供應商採購議價前調用。
   - **必要性說明**：深度解析盤商操盤手三大心理動機（恐慌溢價/庫存週轉/試探開高），產出溫和堅定、給予對方台階下並精準爭取到底價之老闆專用高情商談判話術。
4. **執行 `atom-groupbuy-four-prism-copy`**（第 6 步專屬品牌文案）：
   - **調用時機**：在定價策略確立後、產出社群發文與商城上架素材時調用。
   - **必要性說明**：遵循「四大面向折射輸出鐵律 (The 4-Prism Rule)」，以喵編生活管家人設同時折射【專業知識】、【成長歷程】、【三觀哲學】與【選品宣告】四篇文案及商城精簡規格，嚴格過濾「團購、便宜、CP值、+1」等廉價禁語。

---

"""

# 組裝母體內容
new_sharp_content = sharp_frontmatter + sharp_body
sharp_dest_dir = GROUPBUY_PROPOSED / "sharp-groupbuy-analyzer"
sharp_dest_dir.mkdir(parents=True, exist_ok=True)
(sharp_dest_dir / "SKILL.md").write_text(new_sharp_content, encoding="utf-8")
print("✅ 已生成 _proposed/管家選品/sharp-groupbuy-analyzer/SKILL.md")

# 3. 處理 4 個 atom
# Atom 1: atom-groupbuy-cost-auditor
src_a1 = PROPOSED_DIR / "選品行銷" / "atom-groupbuy-cost-auditor" / "SKILL.md"
a1_content = src_a1.read_text(encoding="utf-8")
a1_content = a1_content.replace("group: 選品行銷", "group: 管家選品")
if "只由 sharp-groupbuy-analyzer 呼叫，不單獨使用。" not in a1_content:
    a1_content = a1_content.replace(
        "社群文案折射時不用。",
        "社群文案折射時不用。只由 sharp-groupbuy-analyzer 呼叫，不單獨使用。"
    )
dst_a1_dir = GROUPBUY_PROPOSED / "atom-groupbuy-cost-auditor"
dst_a1_dir.mkdir(parents=True, exist_ok=True)
(dst_a1_dir / "SKILL.md").write_text(a1_content, encoding="utf-8")
print("✅ 已生成 atom-groupbuy-cost-auditor/SKILL.md")

# Atom 2: atom-groupbuy-four-prism-copy
src_a2 = PROPOSED_DIR / "選品行銷" / "atom-groupbuy-four-prism-copy" / "SKILL.md"
a2_content = src_a2.read_text(encoding="utf-8")
a2_content = a2_content.replace("group: 選品行銷", "group: 管家選品")
if "只由 sharp-groupbuy-analyzer 呼叫，不單獨使用。" not in a2_content:
    a2_content = a2_content.replace(
        "上游成本逆推時不用。",
        "上游成本逆推時不用。只由 sharp-groupbuy-analyzer 呼叫，不單獨使用。"
    )
dst_a2_dir = GROUPBUY_PROPOSED / "atom-groupbuy-four-prism-copy"
dst_a2_dir.mkdir(parents=True, exist_ok=True)
(dst_a2_dir / "SKILL.md").write_text(a2_content, encoding="utf-8")
print("✅ 已生成 atom-groupbuy-four-prism-copy/SKILL.md")

# Atom 3: atom-supplychain-layer-deconstructor
src_a3 = PROPOSED_DIR / "選品審計" / "atom-supplychain-layer-deconstructor" / "SKILL.md"
a3_content = src_a3.read_text(encoding="utf-8")
a3_content = a3_content.replace("group: 選品審計", "group: 管家選品")
a3_content = a3_content.replace("parent: 待品碩決定", "parent: sharp-groupbuy-analyzer")
a3_content = a3_content.replace("只由 待品碩決定 呼叫，不單獨使用。", "只由 sharp-groupbuy-analyzer 呼叫，不單獨使用。")
# 移除 blockquote
a3_lines = [l for l in a3_content.splitlines() if not l.startswith("> **所屬技能組**") and not l.startswith("> **原技能母體**")]
a3_content = "\n".join(a3_lines) + "\n"
dst_a3_dir = GROUPBUY_PROPOSED / "atom-supplychain-layer-deconstructor"
dst_a3_dir.mkdir(parents=True, exist_ok=True)
(dst_a3_dir / "SKILL.md").write_text(a3_content, encoding="utf-8")
print("✅ 已生成 atom-supplychain-layer-deconstructor/SKILL.md")

# Atom 4: atom-supplychain-tactical-negotiator
src_a4 = PROPOSED_DIR / "選品審計" / "atom-supplychain-tactical-negotiator" / "SKILL.md"
a4_content = src_a4.read_text(encoding="utf-8")
a4_content = a4_content.replace("group: 選品審計", "group: 管家選品")
a4_content = a4_content.replace("parent: 待品碩決定", "parent: sharp-groupbuy-analyzer")
a4_content = a4_content.replace("只由 待品碩決定 呼叫，不單獨使用。", "只由 sharp-groupbuy-analyzer 呼叫，不單獨使用。")
# 移除 blockquote
a4_lines = [l for l in a4_content.splitlines() if not l.startswith("> **所屬技能組**") and not l.startswith("> **原技能母體**")]
a4_content = "\n".join(a4_lines) + "\n"
dst_a4_dir = GROUPBUY_PROPOSED / "atom-supplychain-tactical-negotiator"
dst_a4_dir.mkdir(parents=True, exist_ok=True)
(dst_a4_dir / "SKILL.md").write_text(a4_content, encoding="utf-8")
print("✅ 已生成 atom-supplychain-tactical-negotiator/SKILL.md")

# 4. 脫敏 _proposed/發臉書/facebook-publisher/SKILL.md
fb_content = FB_PROPOSED.read_text(encoding="utf-8")
# 找出明文 token 行
import re
fb_content_new = re.sub(
    r"TOKEN\s*=\s*['\"]EAAP[A-Za-z0-9_-]+['\"]",
    '''# 從環境變數或設定檔讀取 Meta Page Access Token (資安防護：嚴禁代碼中出現明文金鑰)
def load_fb_page_token():
    # 1. 優先自系統環境變數讀取
    token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
    if token:
        return token
    # 2. 次選讀取根目錄 .secrets.env、.env 或 config/fb_token.txt
    for env_path in [Path(".secrets.env"), Path(".env"), Path("config/fb_token.txt")]:
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("FB_PAGE_ACCESS_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
                elif env_path.suffix == ".txt" and line and not line.startswith("#"):
                    return line
    raise ValueError("找不到 FB_PAGE_ACCESS_TOKEN！請於 .secrets.env 或環境變數中設定。")

TOKEN = load_fb_page_token()''',
    fb_content
)

# 確保 import os 與 Path
if "from pathlib import Path" not in fb_content_new:
    fb_content_new = fb_content_new.replace("import datetime", "import datetime\nimport os\nfrom pathlib import Path")

FB_PROPOSED.write_text(fb_content_new, encoding="utf-8")
print("✅ 已脫敏 _proposed/發臉書/facebook-publisher/SKILL.md")

# 5. 移除舊提案目錄 _proposed/選品行銷 與 _proposed/選品審計
for old_dir in [PROPOSED_DIR / "選品行銷", PROPOSED_DIR / "選品審計"]:
    if old_dir.exists():
        shutil.rmtree(old_dir)
        print(f"🗑️ 已刪除舊提案目錄 {old_dir}")

print("🎉 合併與脫敏處理全部完成！")
