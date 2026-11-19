"""
three_gates_auditor.py
戴明通用三道審查把關程式 (Deming Universal Three-Gate Audit Guard v2.2)

【審查原則】
1. 零硬編碼：程式碼中絕不寫死任何受審文件之金額或業務結論，全數自文件動態讀取解析。
2. 重算關：
   - 動態解析文件表格，辨識「合計／小計／淨額／淨變動額／總計」等列，將上方各項數值加總並與表列數值比對。
   - 支援「分部小計加總為總合計」（如現金流量表之三大活動小計加總為淨變動額）。
   - 支援「毛利／淨損」等分組界標區隔。
3. 禁語關：動態掃描全文，發現「無風險、絕無、穩健、保證」等詞彙時，精確輸出「第幾行、哪個禁語、該行原文」，無死板模板。
4. 出處關：若文件提及外部資料來源（如試算表、總帳、進貨紀錄等），檢查是否具備精確列號 (Row)；缺少者予以退回。
5. 防自審機制：若文件作者為戴明本人，強制拋出例外拒絕審查。
"""

import os
import sys
import re
import argparse
import zipfile
import xml.etree.ElementTree as ET
from decimal import Decimal
from pathlib import Path
from datetime import datetime

AUDIT_LOG_DIR = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CQO_Deming\04_Audit_Certificates")

class SelfReviewProhibitedError(Exception):
    """當試圖審查自己寫的文件時拋出"""
    pass

def extract_number_from_cell(text: str):
    """
    從儲存格字串中提取十進位數值。
    支援普通數字、貨幣符號、逗號分隔、括號負數：
    - '100' -> Decimal('100')
    - '$ 1,427.00' -> Decimal('1427.00')
    - '($ 60,019.80)' -> Decimal('-60019.80')
    - '$-2,014.05' -> Decimal('-2014.05')
    """
    if not text or not isinstance(text, str):
        return None
    
    t = text.strip()
    t_clean = t.replace('NT$', '').replace('$', '').replace('\\$', '').replace(',', '').replace('*', '').strip()
    
    # 括號負數 (123.45) 或 ($ 123.45)
    m_paren = re.match(r'^\((.+)\)$', t_clean)
    if m_paren:
        inner = m_paren.group(1).replace('$', '').replace('\\$', '').replace(',', '').strip()
        try:
            return -Decimal(inner)
        except Exception:
            pass

    try:
        return Decimal(t_clean)
    except Exception:
        m_num = re.search(r'(-?\d+(?:\.\d+)?)', t_clean)
        if m_num:
            try:
                val = Decimal(m_num.group(1))
                if '(' in t and ')' in t:
                    return -val
                return val
            except Exception:
                return None
        return None

class DocumentParser:
    """解析受審文件：提取文字行與表格結構"""
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.lines = []
        self.tables = []
        self._parse()

    def _parse(self):
        ext = self.filepath.suffix.lower()
        if ext == ".docx":
            self._parse_docx()
        else:
            self._parse_text()

    def _parse_text(self):
        content = self.filepath.read_text(encoding="utf-8")
        raw_lines = content.splitlines()
        self.lines = [(i + 1, line) for i, line in enumerate(raw_lines)]

        # 解析 Markdown 表格
        current_table = []
        for line_no, line in self.lines:
            s = line.strip()
            if s.startswith('|') and s.endswith('|'):
                if re.match(r'^\|[\s\-:]+(\|[\s\-:]+)+\|$', s):
                    continue
                cells = [c.strip() for c in s.split('|')[1:-1]]
                current_table.append(cells)
            else:
                if current_table:
                    self.tables.append(current_table)
                    current_table = []
        if current_table:
            self.tables.append(current_table)

    def _parse_docx(self):
        with zipfile.ZipFile(self.filepath) as z:
            xml_content = z.read("word/document.xml")
            tree = ET.fromstring(xml_content)

            p_idx = 1
            for p in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
                texts = [node.text for node in p.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
                if texts:
                    self.lines.append((p_idx, "".join(texts)))
                    p_idx += 1

            for tbl in tree.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl"):
                table = []
                for tr in tbl.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr"):
                    row = []
                    for tc in tr.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc"):
                        texts = [node.text for node in tc.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
                        row.append("".join(texts).strip())
                    if row:
                        table.append(row)
                if table:
                    self.tables.append(table)

class ThreeGatesAuditor:
    def __init__(self, filepath_str: str):
        self.filepath = Path(filepath_str)
        if not self.filepath.exists():
            raise FileNotFoundError(f"受審文件不存在：{self.filepath}")

        self.filename = self.filepath.name
        self.doc = DocumentParser(self.filepath)
        self.records = {
            "target_file": str(self.filepath),
            "filename": self.filename,
            "audit_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "auditor": "CQO 戴明 (Dr. Deming)",
            "gate1": {"name": "出處關 (Provenance Gate)", "passed": True, "details": []},
            "gate2": {"name": "重算關 (Recalculation Gate)", "passed": True, "details": []},
            "gate3": {"name": "禁語關 (Forbidden Words Gate)", "passed": True, "details": []},
            "gate4": {"name": "防區 A 5D 報價風控關 (Zone A Pricing Gate)", "passed": True, "details": []},
            "final_verdict": "UNKNOWN",
            "reasons": []
        }

    def check_self_review(self):
        """防自審機制"""
        all_text = " ".join(l for _, l in self.doc.lines).lower()
        if ("cqo 戴明" in all_text or "author: deming" in all_text or "作者：戴明" in all_text):
            if "審計主官：財務長" not in all_text and "查理·蒙格" not in all_text:
                raise SelfReviewProhibitedError("【安燈硬攔截】依品質把關鐵律：戴明不能審查自己撰寫的文件！")

    def run_gate1_provenance(self) -> bool:
        """
        第一道關：出處關
        若文件聲明引用外部試算表/總帳資料，必須標明精確列號 (Row)；缺少者退回。
        若文件自帶完整推導算式（如測試 B），則通過。
        """
        all_text = "\n".join(l for _, l in self.doc.lines)
        has_external_ref = bool(re.search(r'(Google\s*雲端試算表|\.xlsx?|\.csv|總帳|訂單紀錄|進貨紀錄)', all_text))
        has_row_ref = bool(re.search(r'([第\b]\s*\d+\s*列|列號|Row\s*\d+|![A-Z]+\d+)', all_text))

        passed = True
        details = []

        if has_external_ref:
            details.append("檢測到文件引用外部數據庫/試算表來源。")
            if not has_row_ref:
                details.append("❌ 未標明來源檔案之具體列號 (Row/列號)！各項金額缺少精確出處定位。")
                passed = False
            else:
                details.append("具備來源試算表之具體列號標註。")
        else:
            details.append("文件未聲明引用外部數據檔案，屬於內部表格推導。")

        if not passed:
            self.records["gate1"]["passed"] = False
            self.records["reasons"].append("出處關退回：文件聲明引用外部數據來源，但金額數字未標明具體列號出處。")

        self.records["gate1"]["details"] = details
        return passed

    def run_gate2_recalculation(self) -> bool:
        """
        第二道關：重算關
        動態讀取表格中的「合計／小計／淨額／淨變動額／總計」列，加總上方數字並與表列數字比對。
        支援分部小計至總合計加總。
        完全零硬編碼！
        """
        details = []
        passed = True
        summary_keywords = ['合計', '小計', '淨額', '淨變動額', '總計', '淨現金流量']
        section_break_keywords = ['營業毛利', 'Gross Profit', '淨利', '淨損']

        checked_count = 0

        for t_idx, table in enumerate(self.doc.tables, 1):
            if len(table) < 2:
                continue

            # 動態偵測各欄位中哪一欄含有連續金額數字
            numeric_cols = []
            for col_idx in range(len(table[0])):
                nums = [extract_number_from_cell(row[col_idx]) for row in table if len(row) > col_idx]
                valid_nums = [n for n in nums if n is not None]
                if len(valid_nums) >= 2:
                    numeric_cols.append(col_idx)

            if not numeric_cols:
                continue

            for target_col in numeric_cols:
                current_items = []
                subtotals = []  # 記錄該表格中的各個分部小計
                for row_idx, row in enumerate(table):
                    if len(row) <= target_col:
                        continue
                    
                    row_title = row[0].strip() if len(row) > 0 else ""
                    if target_col >= 2 and len(row) > target_col - 1:
                        neighbor_text = row[target_col - 1].strip()
                        if neighbor_text:
                            row_title = neighbor_text

                    cell_val_str = row[target_col].strip()
                    val = extract_number_from_cell(cell_val_str)

                    # 剝除 Markdown 粗體標記以利精確匹配
                    clean_title = re.sub(r'^\*+|\*+$', '', row_title).strip()

                    # 判斷是否為明細縮排子項（如 • 或以星號空格開頭），子項不重複作為獨立匯總項累加
                    is_sub_bullet = clean_title.startswith('•') or clean_title.startswith('　•') or bool(re.match(r'^\s*[-*]\s+', row_title))
                    if is_sub_bullet:
                        continue

                    # 判斷是否為獨立分組段落標界（如營業毛利）
                    if any(sb in clean_title for sb in section_break_keywords):
                        current_items = []
                        continue

                    # 判斷是否為合計/小計/淨變動額列
                    is_summary = any(k in clean_title for k in summary_keywords)

                    if is_summary:
                        if val is not None:
                            # 情況 A：上方有子項目累加列表
                            if current_items:
                                calc_sum = sum(x['val'] for x in current_items)
                                checked_count += 1
                                items_repr = " + ".join(f"{x['val']}" for x in current_items)
                                
                                if calc_sum == val:
                                    details.append(f"【表格加總吻合】第 {t_idx} 表『{row_title}』：{items_repr} = {val}")
                                else:
                                    diff = calc_sum - val
                                    details.append(
                                        f"❌【表格加總算式矛盾】第 {t_idx} 表『{row_title}』：重算為 {calc_sum} ({items_repr})，但表列 {val}，差額：{diff}"
                                    )
                                    passed = False
                                subtotals.append({"title": row_title, "val": val})
                                current_items = []
                            # 情況 B：上方子項已清空，但存在分部小計列表（如三大活動淨現金流 -> 淨變動額）
                            elif subtotals:
                                calc_sum = sum(x['val'] for x in subtotals)
                                checked_count += 1
                                items_repr = " + ".join(f"{x['val']}" for x in subtotals)
                                if calc_sum == val:
                                    details.append(f"【分部小計總合計吻合】第 {t_idx} 表『{row_title}』：{items_repr} = {val}")
                                else:
                                    diff = calc_sum - val
                                    details.append(
                                        f"❌【分部小計總合計矛盾】第 {t_idx} 表『{row_title}』：分部小計重算加總為 {calc_sum} ({items_repr})，但表列 {val}，差額：{diff}"
                                    )
                                    passed = False
                                subtotals = []
                    else:
                        if val is not None:
                            current_items.append({"title": row_title, "val": val})

        if checked_count == 0:
            details.append("文件中未發現包含合計列之表格，略過表格加總重算。")
        else:
            details.append(f"共完成 {checked_count} 處表格加總動態驗算。")

        # === 2. 跨表勾稽動態檢驗 (Cross-Table Articulation Check) ===
        # 依信念 38 與母版第四章之一：
        # - 對得上放行
        # - 對不上退回並附原始資料
        # - 同時有資產負債表與現金流量表但科目無法配對或缺少期末且缺少期初現金：輸出「跨表勾稽：無法檢查」並判定退回！

        # 檢測文件中各表格之會計屬性
        table_types = {}
        for t_idx, table in enumerate(self.doc.tables, 1):
            table_content = " ".join(r[0] for r in table if r).lower()
            if any(k in table_content for k in ['營業活動', '投資活動', '籌資活動', '現金流量', '淨現金流', 'cash flow', 'net change in cash']):
                table_types[t_idx] = 'CASH_FLOW'
            elif any(k in table_content for k in ['資產', '負債', '權益', '流動資產', '固定資產', '業主權益', 'balance sheet', 'assets', 'liabilities']):
                table_types[t_idx] = 'BALANCE_SHEET'
            else:
                table_types[t_idx] = 'OTHER'

        has_bs = any(tt == 'BALANCE_SHEET' for tt in table_types.values())
        has_cf = any(tt == 'CASH_FLOW' for tt in table_types.values())

        bs_cash_items = []
        cf_cash_items = []
        cf_net_changes = []
        cf_begin_cashes = []

        # 資產負債表現金科目名稱
        bs_keywords = ['庫存營運現金', '營運現金', '庫存現金', '現金及約當現金', '現金與約當現金', 'operating cash', '現金', 'cash']
        # 嚴格排除詞：名稱中含有「期初、期末、淨變動、流量」的列一律排除
        bs_exclude_keywords = ['期初', '期末', '淨變動', '流量', '淨增加', '淨減少', '活動', 'flow', '折舊', '應收', '應付', '注資', '盈餘']

        # 現金流量表現金科目名稱
        cf_ending_keywords = ['期末現金及約當現金餘額', '期末現金及約當現金', '期末現金餘額', '期末現金', 'ending cash']
        cf_begin_keywords = ['期初現金及約當現金餘額', '期初現金及約當現金', '期初現金餘額', '期初現金', 'beginning cash']
        cf_net_keywords = ['現金及約當現金淨變動額', '現金淨變動額', '現金及約當現金淨增加額', '現金淨增加額', 'net change in cash', '淨現金變動']

        for t_idx, table in enumerate(self.doc.tables, 1):
            t_type = table_types.get(t_idx, 'OTHER')
            for row in table:
                if len(row) < 2:
                    continue
                row_title = row[0].strip()
                clean_title = re.sub(r'^\*+|\*+$', '', row_title).strip()
                clean_lower = clean_title.lower()

                nums = [extract_number_from_cell(c) for c in row[1:]]
                valid_nums = [n for n in nums if n is not None]
                if not valid_nums:
                    continue
                val = valid_nums[-1]

                # 1. 資產負債表現金：只能從資產負債表找，且排除期初/期末/淨變動/流量
                if t_type == 'BALANCE_SHEET':
                    if not any(k in clean_lower for k in bs_exclude_keywords):
                        if any(k.lower() in clean_lower for k in bs_keywords):
                            bs_cash_items.append({'table': t_idx, 'title': clean_title, 'val': val})

                # 2. 現金流量表現金：只能從現金流量表找
                elif t_type == 'CASH_FLOW':
                    if any(k.lower() in clean_lower for k in cf_ending_keywords):
                        cf_cash_items.append({'table': t_idx, 'title': clean_title, 'val': val})
                    elif any(k.lower() in clean_lower for k in cf_begin_keywords):
                        cf_begin_cashes.append({'table': t_idx, 'title': clean_title, 'val': val})
                    elif any(k.lower() in clean_lower for k in cf_net_keywords):
                        cf_net_changes.append({'table': t_idx, 'title': clean_title, 'val': val})

        # 若同時具備資產負債表與現金流量表
        if has_bs and has_cf:
            # 嘗試推導期末現金（必須同時有期初現金與淨變動額才能推算；缺少期初現金則不得自作主張推算）
            if not cf_cash_items and cf_net_changes and cf_begin_cashes:
                begin_val = cf_begin_cashes[0]['val']
                net_val = cf_net_changes[0]['val']
                calc_ending = begin_val + net_val
                cf_cash_items.append({
                    'table': cf_net_changes[0]['table'],
                    'title': f"期末現金(由期初{begin_val}+淨變動{net_val}推算)",
                    'val': calc_ending
                })

            # 檢查是否能夠執行勾稽
            if not bs_cash_items or not cf_cash_items:
                passed = False
                details.append(
                    "❌【跨表勾稽：無法檢查】文件同時包含資產負債表與現金流量表，但缺少期末現金科目且缺少期初現金科目（或無法配對現金科目），無法執行跨表勾稽驗算（依母版第四章之一規則 3：判定退回並附原始資料）。"
                )
                if "重算關退回：跨表勾稽無法檢查（缺少期末現金且缺少期初現金）！" not in self.records["reasons"]:
                    self.records["reasons"].append("重算關退回：跨表勾稽無法檢查（缺少期末現金且缺少期初現金）！")
            else:
                # 執行跨表勾稽比對（強制要求跨不同表格）
                for bs in bs_cash_items:
                    for cf in cf_cash_items:
                        if bs['table'] != cf['table']:
                            diff = bs['val'] - cf['val']
                            if diff != Decimal("0.0"):
                                passed = False
                                details.append(
                                    f"❌【跨表勾稽矛盾】第 {bs['table']} 表『{bs['title']}』({bs['val']}) 與 第 {cf['table']} 表『{cf['title']}』({cf['val']}) 對不上，差額：{diff}（依母版第四章之一：判定為對不上，退回並附原始資料）"
                                )
                                if "重算關退回：跨表勾稽數字對不上！" not in self.records["reasons"]:
                                    self.records["reasons"].append("重算關退回：跨表勾稽數字對不上！")
                            else:
                                details.append(
                                    f"【跨表勾稽吻合】第 {bs['table']} 表『{bs['title']}』({bs['val']}) 與 第 {cf['table']} 表『{cf['title']}』({cf['val']}) 一致。"
                                )

        if not passed:
            self.records["gate2"]["passed"] = False
            if not any("重算關退回" in r for r in self.records["reasons"]):
                self.records["reasons"].append("重算關退回：算式結果與表列數字不一致！")

        self.records["gate2"]["details"] = details
        return passed

    def run_gate3_forbidden_words(self) -> bool:
        """
        第三道關：禁語關
        純動態輸出：「第幾行、哪個禁語、該行原文」。
        不寫死任何業務形容或解讀文字。
        """
        details = []
        passed = True
        forbidden_targets = ["無風險", "絕無", "穩健", "保證"]

        found_violations = []
        for line_no, line_text in self.doc.lines:
            stripped = line_text.strip()
            for word in forbidden_targets:
                if word in stripped:
                    found_violations.append((line_no, word, stripped))

        if found_violations:
            passed = False
            for l_no, word, text in found_violations:
                details.append(f"第 {l_no} 行、禁語『{word}』：{text}")
            self.records["gate3"]["passed"] = False
            self.records["reasons"].append(f"禁語關退回：發現 {len(found_violations)} 處包含絕對化禁語。")
        else:
            details.append("未發現違規禁語。")

        self.records["gate3"]["details"] = details
        return passed


    def run_gate4_pricing_zone_a(self) -> bool:
        """
        第四道關：防區 A 5D 報價與外送防彈衣風控關
        當受審文件涉及「防區 A」或「5D 報價」或「代墊」時強制啟動物理攔截：
        1. 勞務服務費與代墊款 100% 分離標示
        2. 代墊風控上限 <= NT$ 3,000 元（扣除定金後）
        3. 顧客明確知情確認
        4. 零負毛利底線
        """
        all_text = " ".join(line for _, line in self.doc.lines).lower()
        is_zone_a = any(k in all_text for k in ['防區 a', '防區a', '5d 報價', '5d報價', '代墊', '代購', '代買', '代採購', '跑腿費', '勞務服務費'])

        details = []
        passed = True

        if not is_zone_a:
            details.append("【免檢】非防區 A 報價業務，略過 5D 報價風控審查。")
            self.records["gate4"]["details"] = details
            return True

        # 提取報價欄位
        data = {
            "service_fee": None,
            "advance_amount": None,
            "deposit_amount": Decimal("0.00"),
            "has_advance": False,
            "customer_confirmed": None,
            "cost_base": Decimal("0.00")
        }

        for _, raw_line in self.doc.lines:
            clean = raw_line.replace('*', '').replace('|', ':').replace('：', ':')
            parts = [p.strip() for p in clean.split(':') if p.strip()]
            if len(parts) >= 2:
                key = parts[0].lower()
                val_str = parts[1]

                if any(k in key for k in ['勞務服務費', '服務費', '勞務費', '跑腿費', 'service fee']):
                    num = extract_number_from_cell(val_str)
                    if num is not None:
                        data["service_fee"] = num

                elif any(k in key for k in ['代墊款', '代墊金額', '代採購款', '商品代墊', 'advance payment']):
                    num = extract_number_from_cell(val_str)
                    if num is not None:
                        data["advance_amount"] = num
                        data["has_advance"] = True

                elif any(k in key for k in ['定金', '訂金', '預收款', '預付定金', 'deposit']):
                    num = extract_number_from_cell(val_str)
                    if num is not None:
                        data["deposit_amount"] = num

                elif any(k in key for k in ['顧客知情確認', '知情確認', '客戶確認', '顧客同意', 'customer confirmation']):
                    if any(pos in val_str.lower() for pos in ['是', '已確認', '已同意', 'yes', 'true', '完成']):
                        data["customer_confirmed"] = True
                    elif any(neg in val_str.lower() for neg in ['否', '未確認', '未同意', 'no', 'false', '無']):
                        data["customer_confirmed"] = False

                elif any(k in key for k in ['基礎成本', '油資成本', '工時成本', '成本底線', 'cost base']):
                    num = extract_number_from_cell(val_str)
                    if num is not None:
                        data["cost_base"] = num

        if data["advance_amount"] is None:
            if any(k in all_text for k in ['代買', '代墊', '代購', '代付', '代採購']):
                data["has_advance"] = True

        # 檢驗 1：分離律
        if data["has_advance"]:
            if data["advance_amount"] is None or data["service_fee"] is None:
                passed = False
                details.append("❌【未分列標示】業務涉及代墊或代採購，但未明確拆分『勞務服務費』與『代墊款』金額（不可報統包價）！")
                self.records["reasons"].append("防區A退回：代墊款與勞務服務費未拆開分列！")
            else:
                details.append(f"【合規拆分】勞務服務費 NT$ {data['service_fee']}，代墊款 NT$ {data['advance_amount']} 分列清晰。")
        else:
            if data["service_fee"] is None:
                passed = False
                details.append("❌【缺少定價】報價單未標明勞務服務費！")
                self.records["reasons"].append("防區A退回：未標明勞務服務費！")
            else:
                details.append(f"【純勞務合規】勞務服務費 NT$ {data['service_fee']}（無代墊項目）。")

        # 檢驗 2：代墊上限風控 (NT$ 3,000)
        advance_limit = Decimal("3000.00")
        if data["has_advance"] and data["advance_amount"] is not None:
            adv = data["advance_amount"]
            dep = data["deposit_amount"]
            net_risk = adv - dep
            if net_risk > advance_limit:
                passed = False
                details.append(f"❌【代墊金額超標】代墊款 NT$ {adv}，扣除預付定金 NT$ {dep} 後，淨代墊 NT$ {net_risk} 超過風控上限 NT$ {advance_limit}！")
                self.records["reasons"].append(f"防區A退回：淨代墊款 ({net_risk}) 超過風控上限 NT$ {advance_limit}！")
            else:
                details.append(f"【代墊風控合格】代墊款 NT$ {adv}（預付定金 NT$ {dep}，淨代墊 NT$ {net_risk} <= NT$ {advance_limit}）。")

        # 檢驗 3：顧客知情確認
        if data["has_advance"]:
            if data["customer_confirmed"] is not True:
                passed = False
                details.append("❌【缺少顧客知情確認】未獲顧客明確確認即承諾代墊，觸犯防區A致命紅線！")
                self.records["reasons"].append("防區A退回：缺少顧客知情確認！")
            else:
                details.append("【知情合格】顧客已明確知情並確認代墊事項。")

        # 檢驗 4：零負毛利
        if data["service_fee"] is not None:
            fee = data["service_fee"]
            cost = data["cost_base"]
            if fee <= Decimal("0.00"):
                passed = False
                details.append(f"❌【負毛利或零服務費】勞務服務費為 NT$ {fee}，禁止義務免費或負毛利出勤！")
                self.records["reasons"].append("防區A退回：勞務服務費小於或等於 0！")
            elif fee < cost:
                passed = False
                details.append(f"❌【低於基礎成本】勞務服務費 NT$ {fee} 低於基礎時間油料成本 NT$ {cost}！")
                self.records["reasons"].append(f"防區A退回：勞務費 ({fee}) 低於基礎成本 ({cost})！")
            else:
                details.append(f"【毛利合格】勞務服務費 NT$ {fee}（基礎成本 NT$ {cost}），邊際貢獻大於零。")

        if not passed:
            self.records["gate4"]["passed"] = False
        self.records["gate4"]["details"] = details
        return passed

    def audit_all(self) -> str:
        self.check_self_review()

        g1_ok = self.run_gate1_provenance()
        g2_ok = self.run_gate2_recalculation()
        g3_ok = self.run_gate3_forbidden_words()
        g4_ok = self.run_gate4_pricing_zone_a()

        if g1_ok and g2_ok and g3_ok and g4_ok:
            self.records["final_verdict"] = "PASSED (審查通過)"
        else:
            self.records["final_verdict"] = "REJECTED (審查退回)"

        record_path = self._generate_certificate()
        return self.records["final_verdict"], record_path

    def _generate_certificate(self) -> Path:
        AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Audit_Record_{timestamp_str}_{self.filepath.stem}.md"
        record_path = AUDIT_LOG_DIR / filename

        md_content = f"""# 📋 戴明品質審查紀錄單 (Quality Audit Certificate)

> **受審文件**：`{self.records['filename']}`  
> **受審檔案完整路徑**：`{self.records['target_file']}`  
> **審查主管**：{self.records['auditor']}  
> **審查時間**：{self.records['audit_time']}  
> **最終判定**：**{self.records['final_verdict']}**

---

## 🚨 審查退件原因摘要
"""
        if self.records["reasons"]:
            for r in self.records["reasons"]:
                md_content += f"- ❌ {r}\n"
        else:
            md_content += "- ✅ 全數三道把關檢驗通過，無退件事由。\n"

        md_content += f"""
---

## 🔍 三道把關程式審查明細

### 1. {self.records['gate1']['name']} —— 【{'通過' if self.records['gate1']['passed'] else '退回'}】
"""
        for d in self.records['gate1']['details']:
            md_content += f"- {d}\n"

        md_content += f"""
### 2. {self.records['gate2']['name']} —— 【{'通過' if self.records['gate2']['passed'] else '退回'}】
"""
        for d in self.records['gate2']['details']:
            md_content += f"- {d}\n"

        md_content += f"""
### 3. {self.records['gate3']['name']} —— 【{'通過' if self.records['gate3']['passed'] else '退回'}】
"""
        for d in self.records['gate3']['details']:
            md_content += f"- {d}\n"

        md_content += f"""
---
*本紀錄由戴明三道審查把關程式 (three_gates_auditor.py) 自動產生，具備確定性客觀效力。*
"""
        record_path.write_text(md_content, encoding="utf-8")
        return record_path

def main():
    parser = argparse.ArgumentParser(description="戴明通用三道審查把關程式")
    parser.add_argument("file", help="受審文件路徑")
    args = parser.parse_args()

    auditor = ThreeGatesAuditor(args.file)
    verdict, record_path = auditor.audit_all()

    print(f"\n=======================================================")
    print(f"   受審文件：{auditor.filename}")
    print(f"   審查判定：{verdict}")
    print(f"   紀錄存檔：{record_path}")
    print(f"=======================================================\n")

    for gate_key in ["gate1", "gate2", "gate3"]:
        g = auditor.records[gate_key]
        status = "PASSED" if g["passed"] else "REJECTED"
        print(f"[{status}] {g['name']}:")
        for d in g["details"]:
            print(f"  {d}")
        print()

    if "REJECTED" in verdict:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
