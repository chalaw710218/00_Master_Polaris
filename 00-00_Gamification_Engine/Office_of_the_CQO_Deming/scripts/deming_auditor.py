"""
威廉·愛德華茲·戴明博士 (Dr. W. Edwards Deming) 萬用品質審計與安燈繩硬攔截引擎
=================================================================================
極星全域 QA/QC 總稽核與品質管制中樞。
負責執行雙盲黑箱檢驗、產出結構化 Markdown 審計憑證，並在評分未達 90 分或觸犯紅線時物理阻斷流程。
"""

import sys
import os
import re
import json
from datetime import datetime
from pathlib import Path

# Windows 終端 UTF-8 安全防護
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEMING_OFFICE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = DEMING_OFFICE_DIR / "02_Audit_Reports"
NOTEBOOK_FILE = DEMING_OFFICE_DIR / "00_Deming_Notebook.md"

class AndonBlockError(Exception):
    """安燈繩硬攔截異常：當品質未達 90 分或觸犯致命紅線時拋出，物理阻斷交付管線"""
    pass

class DemingUniversalAuditor:
    def __init__(self):
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        
    def _generate_audit_id(self) -> str:
        today_str = datetime.now().strftime("%Y%m%d")
        existing_reports = list(REPORTS_DIR.glob(f"AUD-{today_str}-*.md"))
        next_serial = len(existing_reports) + 1
        return f"AUD-{today_str}-{next_serial:03d}"

    def audit_deliverable(
        self,
        domain: str, # "pricing", "social", "engineering"
        title: str,
        author: str,
        content: str,
        qa_checks: dict, # {"QA-01": True, ...}
        qc_scores: dict, # {"dimension_name": score (0-100), ...}
        qc_weights: dict, # {"dimension_name": weight (0.0-1.0), ...}
        red_lines: list, # List of triggered red lines, e.g. ["未獲知情確認即代墊"]
        deming_thoughts: str, # <thought> 內部校準
        deming_verdict: str  # 戴明具體裁決與整改指南
    ) -> dict:
        """
        執行全面品質審查並產出結構化審計報告
        """
        audit_id = self._generate_audit_id()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 計算 QC 加權總分
        total_score = 0.0
        for dim, weight in qc_weights.items():
            score = qc_scores.get(dim, 0)
            total_score += score * weight
        total_score = round(total_score, 1)
        
        # 判斷是否合格
        has_red_line = len(red_lines) > 0
        is_passed = (total_score >= 90.0) and (not has_red_line)
        status_text = "PASSED ✅" if is_passed else "ANDON BLOCKED 🚨"
        
        # 組合結構化 Markdown 審計報告
        slug = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')[:30]
        report_filename = f"{audit_id}_{domain.capitalize()}_{slug}.md"
        report_path = REPORTS_DIR / report_filename
        
        markdown_content = f"""# 📐 戴明品質審計報告 ({audit_id})
## 【{status_text}】{title}

> **審計編號**：`{audit_id}`  
> **審查時間**：`{timestamp}`  
> **受審防區**：`{domain.upper()}`  
> **產物負責人**：`{author}`  
> **主管審查官**：CQO 威廉·愛德華茲·戴明博士 (Dr. W. Edwards Deming)

---

### 🧐 一、 戴明博士內部心智校準 (<thought>)

```markdown
{deming_thoughts.strip()}
```

---

### 📋 二、 QA 過程審查檢核 (Pre-flight Verification)

| 檢驗項目 | 檢驗標準內容 | 查核狀態 |
| :--- | :--- | :---: |
"""
        for check_id, state in qa_checks.items():
            mark = "✅ 通過" if state else "❌ 未達標"
            markdown_content += f"| `{check_id}` | 依據防區 SOP 基準核驗 | {mark} |\n"

        markdown_content += f"""
---

### 🔬 三、 QC 產物加權評分 (Outcome Inspection)

| 評分維度 | 權重 | 單項評分 | 加權得分 |
| :--- | :---: | :---: | :---: |
"""
        for dim, weight in qc_weights.items():
            score = qc_scores.get(dim, 0)
            weighted = round(score * weight, 1)
            markdown_content += f"| **{dim}** | {int(weight*100)}% | {score} 分 | {weighted} 分 |\n"

        markdown_content += f"""
* **QC 綜合品質得分**：**`{total_score} / 100 分`**  
* **合格基準線**：`90.0 分`
"""

        if red_lines:
            markdown_content += f"\n### 🚨 致命紅線觸發警告 (Fatal Red Lines)\n"
            for rl in red_lines:
                markdown_content += f"- ❌ **{rl}**\n"
        else:
            markdown_content += f"\n* **致命紅線查核**：✅ 未觸犯任何系統紅線\n"

        markdown_content += f"""
---

### 🏛️ 四、 戴明博士權威裁決與整改指南 (Grand Verdict)

> *"{deming_verdict.strip()}"*

---

### 📦 五、 受審產物快照存檔 (Deliverable Snapshot)

```text
{content.strip()}
```
"""
        # 寫入報告
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(markdown_content.strip() + "\n")
            
        # 同步更新 Notebook
        self._append_to_notebook(audit_id, timestamp[:10], domain, title, total_score, status_text, report_filename)
        
        print(f"\n=======================================================")
        print(f"📊 戴明品質審計完成 [{audit_id}]")
        print(f"🎯 綜合評分：{total_score} 分 ｜ 裁決狀態：{status_text}")
        print(f"📁 審計報告已歸檔至：{report_path}")
        print(f"=======================================================\n")
        
        # 若未通過，觸發安燈繩物理中斷
        if not is_passed:
            err_msg = f"安燈繩已拉下 (Andon Cord Triggered)！[{title}] 未達 90 分或觸犯致命紅線，系統物理阻斷發布！"
            if red_lines:
                err_msg += f" 觸犯紅線：{', '.join(red_lines)}"
            raise AndonBlockError(err_msg)
            
        return {
            "audit_id": audit_id,
            "status": status_text,
            "score": total_score,
            "report_path": str(report_path)
        }

    def _append_to_notebook(self, audit_id, date_str, domain, title, score, status, filename):
        if not NOTEBOOK_FILE.exists():
            return
        try:
            with open(NOTEBOOK_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            table_row = f"| `{audit_id}` | {date_str} | 防區 {domain.upper()} | {title} | {score} / 100 | {status} | `02_Audit_Reports/{filename}` |\n"
            
            with open(NOTEBOOK_FILE, "a", encoding="utf-8") as f:
                f.write(table_row)
        except Exception as e:
            print(f"⚠️ 更新戴明筆記本索引時發生非致命錯誤: {e}")

if __name__ == "__main__":
    auditor = DemingUniversalAuditor()
    print("【戴明萬用品質審計與安燈繩引擎】已初始化就緒。")
