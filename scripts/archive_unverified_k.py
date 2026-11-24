import re
from pathlib import Path

kb_file = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\pending_knowledge_base.md")
archive_dir = Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\data\_未驗證封存")
archive_dir.mkdir(parents=True, exist_ok=True)
archive_file = archive_dir / "archived_unverified_k.md"

txt = kb_file.read_text(encoding='utf-8')
sections = [s for s in re.split(r'\n(?=###\s*【K-\d+)', txt) if s.strip().startswith('### 【K-')]
initial_count = len(sections)

verified_kids = ["K-002", "K-005", "K-007", "K-008", "K-009", "K-012", "K-017"]
experimental_kids = ["K-014", "K-025", "K-031"]

verified_sections = []
archived_sections = []
experimental_sections = []

for s in sections:
    header = s.splitlines()[0]
    kid = re.search(r'K-\d+', header).group(0)
    
    if kid in verified_kids:
        verified_sections.append(s)
    elif kid in experimental_kids:
        # Move literature version to archive
        archived_sections.append(s)
        
        # Build clean experimental hypothesis for pending_knowledge_base.md
        if kid == "K-014":
            exp_text = """### 【K-014・實驗假說：常民生活文案具身認知與微小感官描摹】（進行中實戰假說）
* **研習輪次**：Cycle 22（2026-11-24 轉為實測實驗假說）
* **假說類型**：實驗假說
* **出處狀態**：【無文獻支持，由 feedback_loop 實測數據判定】（原 Medium 網址無法驗證，文獻出處已移至封存區）
* **假說內容**：以微小具體的物理名詞與生活動作（如撕開紙膠帶、洗淨菜葉、端起鐵盒），還原台東生活現場，比抽象宣傳詞更能建立讀者真實感與信任。
* **生活管家應用要點**：發文聚焦生活白描與具身微小感官細節，由 feedback_loop.py 每週比對 ER 與互動深度判定成效。"""
            experimental_sections.append(exp_text)
        elif kid == "K-025":
            exp_text = """### 【K-025・實驗假說：服務代勞努力啟發式與作業透明度】（進行中實戰假說）
* **研習輪次**：Cycle 33（2026-11-24 轉為實測實驗假說）
* **假說類型**：實驗假說
* **出處狀態**：【無文獻支持，由 feedback_loop 實測數據判定】（原哈佛網址為臉書論文對不上，文獻出處已移至封存區）
* **假說內容**：主動向讀者展示生活管家後台代勞的實際付出、奔波路線與細節（如代倒垃圾分類、雨天配送防護），能觸發努力啟發式認知，提升對生活管家服務價值的信賴。
* **生活管家應用要點**：發文呈現生活管家真實代勞與備餐/跑腿流程，由 feedback_loop.py 每週比對 ER 與回頭互動判定成效。"""
            experimental_sections.append(exp_text)
        elif kid == "K-031":
            exp_text = """### 【K-031・實驗假說：未來服務需求前置探測與互動徵詢】（進行中實戰假說）
* **研習輪次**：Cycle 39（2026-11-24 轉為實測實驗假說）
* **假說類型**：實驗假說
* **出處狀態**：【無文獻支持，由 feedback_loop 實測數據判定】（原 Steve Blank 部落格彙整頁查無具體支持原文，文獻出處已移至封存區）
* **假說內容**：在推出新服務或生鮮前，以謙遜、徵詢口吻詢問受眾需求（如「我們正在規劃某項服務，您或身邊朋友是否有此需要」），能探測真實痛點並啟動雙向互動。
* **生活管家應用要點**：發文採用互動徵詢句型，由 feedback_loop.py 每週比對讀者留言質量與需求轉換判定成效。"""
            experimental_sections.append(exp_text)
    else:
        archived_sections.append(s)

# Write archive file
archive_header = """# 📦 生活管家儲備知識庫・未驗證與對不上條目封存區

> ⚠️ **【嚴格封存警戒線 · 2026-11-24 依 Claude 審計指示建立】**  
> 1. 本檔案收錄之 24 條 K（21 條【未驗證】+ 3 條【對不上】），經 2026-11-24 物理真值反查，確認多數網址為 404 死鏈、權限阻擋或內容對不上。  
> 2. **嚴格禁止引用**：本區所有條目終生不得再引用、不得作為任何對外貼文宣稱「有研究證明」之依據、不得作為規則庫升級之法理出處。  
> 3. 保留本檔僅作為系統演化之歷史負面資產存證，供日後複查。

---
"""
archive_content = archive_header + "\n\n---\n\n".join(archived_sections)
archive_file.write_text(archive_content, encoding='utf-8')

# Write updated pending_knowledge_base.md
kb_header = """# 📥 生活管家儲備知識庫（已驗證文獻 ＋ 實測實驗假說）

> **層級定位**：外部研習與文獻檢索之儲備知識，以及進行中之實測實驗假說。  
> **晉級鐵律**：嚴禁直接升級為公理！只有在未來社群漫遊、貼文發布或生活管家實體服務中「實際解決過物理問題並取得脆真實後台驗證」，方可經創辦人（品碩）審查後晉升為公理。  
> **審查標準（2026-11-24 審計修訂）**：
> 1. 儲備知識必須經 `evidence_gate.py` 物理驗證通過（具有真實可存取之網址與逐字原文）。
> 2. 未通過文獻驗證者一律移入 `data/_未驗證封存/`，不得對外宣稱有文獻支持。
> 3. 實測實驗假說（K-014、K-025、K-031）無文獻支持，成效完全由 `feedback_loop.py` 依每週真實數據客觀判定。

---
## 一、 文獻已驗證之儲備知識（共 7 條）
"""

# Reconstruct verified sections
v_text = "\n\n---\n\n".join(verified_sections)

exp_header = """\n\n---
## 二、 進行中實測實驗假說（共 3 條 · 無文獻支持，由 feedback_loop 實測數據判定）
"""
exp_text = "\n\n---\n\n".join(experimental_sections)

new_kb_content = kb_header + "\n\n" + v_text + exp_header + "\n\n" + exp_text
kb_file.write_text(new_kb_content, encoding='utf-8')

# Count verification
final_txt = kb_file.read_text(encoding='utf-8')
final_sections = [s for s in re.split(r'\n(?=###\s*【K-\d+)', final_txt) if s.strip().startswith('### 【K-')]

archived_txt = archive_file.read_text(encoding='utf-8')
archived_sections_final = [s for s in re.split(r'\n(?=###\s*【K-\d+)', archived_txt) if s.strip().startswith('### 【K-')]

print("=== 條數計算結果 ===")
print(f"搬移前 pending_knowledge_base.md 總條數: {initial_count} 條")
print(f"移入 data/_未驗證封存/ 總條數: {len(archived_sections_final)} 條（含 21 條未驗證 + 3 條對不上）")
print(f"搬移後 pending_knowledge_base.md 總條數: {len(final_sections)} 條")
print(f"  - 文獻已驗證儲備知識: {len([s for s in final_sections if any(k in s for k in verified_kids)])} 條")
print(f"  - 進行中實測實驗假說: {len([s for s in final_sections if any(k in s for k in experimental_kids)])} 條")
