"""
zone_a_pricing_auditor.py
戴明首席品質長 · 防區 A：5D 報價與代墊款把關程式 (Zone A Pricing & Advance Payment Auditor)

職責：
落實防區 A 核心 QC 致命紅線硬阻斷：
1. 【分離律】：勞務服務費與代墊款 100% 分離標示，嚴禁混淆統包。
2. 【風控律】：代墊金額超過 NT$ 3,000 元且無預付定金者，一票否決。
3. 【知情律】：未獲顧客明確知情確認即承諾代墊者，一票否決。
4. 【毛利律】：勞務服務費不得為 0 或負數，嚴禁負毛利出勤。

判定原則：只認程式客觀提取與數值計算，對不上或不合格直接退回，不推測原因。
"""

import os
import sys
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from datetime import datetime

ADVANCE_LIMIT = Decimal("3000.00")

def extract_decimal(s: str):
    if not s:
        return None
    # 移除貨幣符號、千分位與空白
    cleaned = re.sub(r'[\$,NT\$nt\$\s]', '', str(s).strip())
    # 處理括號負數 (100) -> -100
    if cleaned.startswith('(') and cleaned.endswith(')'):
        cleaned = '-' + cleaned[1:-1]
    m = re.search(r'[-+]?\d+(?:\.\d+)?', cleaned)
    if m:
        try:
            return Decimal(m.group(0))
        except InvalidOperation:
            return None
    return None

class ZoneAPricingAuditor:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"受審檔案不存在：{filepath}")
        
        self.content = self.filepath.read_text(encoding="utf-8")
        self.lines = [line.strip() for line in self.content.splitlines() if line.strip()]
        
        self.records = {
            "file": self.filepath.name,
            "filepath": str(self.filepath.resolve()),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "passed": True,
            "gates": {
                "separation": {"passed": True, "details": []},
                "advance_limit": {"passed": True, "details": []},
                "customer_consent": {"passed": True, "details": []},
                "profit_margin": {"passed": True, "details": []}
            },
            "reasons": []
        }

    def _extract_fields(self) -> dict:
        data = {
            "service_fee": None,
            "advance_amount": None,
            "deposit_amount": Decimal("0.00"),
            "has_advance": False,
            "customer_confirmed": None,
            "cost_base": Decimal("0.00")
        }

        # 掃描表格或鍵值對
        for line in self.lines:
            clean = line.replace('*', '').replace('|', ':').replace('：', ':')
            parts = [p.strip() for p in clean.split(':') if p.strip()]
            if len(parts) >= 2:
                key = parts[0].lower()
                val_str = parts[1]

                # 勞務服務費
                if any(k in key for k in ['勞務服務費', '服務費', '勞務費', '跑腿費', 'service fee']):
                    num = extract_decimal(val_str)
                    if num is not None:
                        data["service_fee"] = num

                # 代墊款項
                elif any(k in key for k in ['代墊款', '代墊金額', '代採購款', '商品代墊', 'advance payment']):
                    num = extract_decimal(val_str)
                    if num is not None:
                        data["advance_amount"] = num
                        data["has_advance"] = True

                # 預付定金
                elif any(k in key for k in ['定金', '訂金', '預收款', '預付定金', 'deposit']):
                    num = extract_decimal(val_str)
                    if num is not None:
                        data["deposit_amount"] = num

                # 顧客知情確認
                elif any(k in key for k in ['顧客知情確認', '知情確認', '客戶確認', '顧客同意', 'customer confirmation']):
                    if any(pos in val_str.lower() for pos in ['是', '已確認', '已同意', 'yes', 'true', '完成']):
                        data["customer_confirmed"] = True
                    elif any(neg in val_str.lower() for neg in ['否', '未確認', '未同意', 'no', 'false', '無']):
                        data["customer_confirmed"] = False

                # 基礎成本（若有列出）
                elif any(k in key for k in ['基礎成本', '油資成本', '工時成本', '成本底線', 'cost base']):
                    num = extract_decimal(val_str)
                    if num is not None:
                        data["cost_base"] = num

        # 若在文字中發現有代墊事實（例如代買商品）但代墊款為 None，標記有代墊未拆分
        if data["advance_amount"] is None:
            if any(k in self.content for k in ['代買', '代墊', '代購', '代付']):
                data["has_advance"] = True

        return data

    def audit(self) -> tuple[str, str]:
        data = self._extract_fields()
        passed = True

        # 關卡 1：勞務服務費與代墊款分離檢查
        if data["has_advance"]:
            if data["advance_amount"] is None or data["service_fee"] is None:
                self.records["gates"]["separation"]["passed"] = False
                self.records["gates"]["separation"]["details"].append(
                    "❌【未分列標示】業務涉及代墊或代採購，但未明確拆分『勞務服務費』與『代墊款』金額（不可報統包價）！"
                )
                self.records["reasons"].append("防區A退回：代墊款與勞務服務費未拆開分列！")
                passed = False
            else:
                self.records["gates"]["separation"]["details"].append(
                    f"【合規拆分】勞務服務費 NT$ {data['service_fee']}，代墊款 NT$ {data['advance_amount']} 分列清晰。"
                )
        else:
            if data["service_fee"] is None:
                self.records["gates"]["separation"]["passed"] = False
                self.records["gates"]["separation"]["details"].append("❌【缺少定價】報價單未標明勞務服務費！")
                self.records["reasons"].append("防區A退回：未標明勞務服務費！")
                passed = False
            else:
                self.records["gates"]["separation"]["details"].append(
                    f"【純勞務合規】勞務服務費 NT$ {data['service_fee']}（無代墊項目）。"
                )

        # 關卡 2：代墊金額上限風控檢查（上限 3,000 元）
        if data["has_advance"] and data["advance_amount"] is not None:
            adv = data["advance_amount"]
            dep = data["deposit_amount"]
            net_risk = adv - dep  # 實際由管家承擔之淨代墊風險

            if net_risk > ADVANCE_LIMIT:
                self.records["gates"]["advance_limit"]["passed"] = False
                self.records["gates"]["advance_limit"]["details"].append(
                    f"❌【代墊金額超標】代墊款 NT$ {adv}，扣除預付定金 NT$ {dep} 後，淨代墊 NT$ {net_risk} 超過風控上限 NT$ {ADVANCE_LIMIT}！"
                )
                self.records["reasons"].append(f"防區A退回：淨代墊款 ({net_risk}) 超過風控上限 NT$ {ADVANCE_LIMIT}！")
                passed = False
            else:
                self.records["gates"]["advance_limit"]["details"].append(
                    f"【代墊風控合格】代墊款 NT$ {adv}（預付定金 NT$ {dep}，淨代墊 NT$ {net_risk} <= NT$ {ADVANCE_LIMIT}）。"
                )
        else:
            self.records["gates"]["advance_limit"]["details"].append("【免檢】無代墊款項，不適用代墊上限風控。")

        # 關卡 3：顧客知情確認檢查
        if data["has_advance"]:
            if data["customer_confirmed"] is not True:
                self.records["gates"]["customer_consent"]["passed"] = False
                self.records["gates"]["customer_consent"]["details"].append(
                    "❌【缺少顧客知情確認】未獲顧客明確確認即承諾代墊，觸犯防區A致命紅線！"
                )
                self.records["reasons"].append("防區A退回：缺少顧客知情確認！")
                passed = False
            else:
                self.records["gates"]["customer_consent"]["details"].append("【知情合格】顧客已明確知情並確認代墊事項。")
        else:
            self.records["gates"]["customer_consent"]["details"].append("【免檢】無代墊款項，不涉及代墊知情確認。")

        # 關卡 4：零負毛利檢查
        if data["service_fee"] is not None:
            fee = data["service_fee"]
            cost = data["cost_base"]
            if fee <= Decimal("0.00"):
                self.records["gates"]["profit_margin"]["passed"] = False
                self.records["gates"]["profit_margin"]["details"].append(
                    f"❌【負毛利或零服務費】勞務服務費為 NT$ {fee}，禁止義務免費或負毛利出勤！"
                )
                self.records["reasons"].append("防區A退回：勞務服務費小於或等於 0！")
                passed = False
            elif fee < cost:
                self.records["gates"]["profit_margin"]["passed"] = False
                self.records["gates"]["profit_margin"]["details"].append(
                    f"❌【低於基礎成本】勞務服務費 NT$ {fee} 低於基礎時間油料成本 NT$ {cost}！"
                )
                self.records["reasons"].append(f"防區A退回：勞務費 ({fee}) 低於基礎成本 ({cost})！")
                passed = False
            else:
                self.records["gates"]["profit_margin"]["details"].append(
                    f"【毛利合格】勞務服務費 NT$ {fee}（基礎成本 NT$ {cost}），邊際貢獻大於零。"
                )

        self.records["passed"] = passed
        verdict = "PASSED (審查通過)" if passed else "REJECTED (審查退回)"
        record_path = self._save_report(verdict)
        return verdict, record_path

    def _save_report(self, verdict: str) -> str:
        cert_dir = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CQO_Deming\04_Audit_Certificates")
        cert_dir.mkdir(parents=True, exist_ok=True)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        record_name = f"Pricing_Audit_Record_{stamp}_{self.filepath.stem}.md"
        out_path = cert_dir / record_name

        md = []
        md.append("# 📋 戴明品質審查紀錄單 (防區 A：5D 報價專屬)")
        md.append(f"\n> **受審文件**：`{self.filepath.name}`  ")
        md.append(f"> **審查主管**：CQO 戴明 (Dr. Deming)  ")
        md.append(f"> **審查時間**：{self.records['time']}  ")
        md.append(f"> **最終判定**：**{verdict}**\n")
        md.append("---\n")

        if not self.records["passed"]:
            md.append("## 🚨 審查退件原因摘要")
            for r in self.records["reasons"]:
                md.append(f"- ❌ {r}")
            md.append("\n---\n")

        md.append("## 🔍 防區 A 四道檢驗細項\n")
        labels = [
            ("separation", "1. 勞務與代墊款分離關 (Separation Gate)"),
            ("advance_limit", "2. 代墊風控上限關 (Advance Limit Gate <= NT$ 3,000)"),
            ("customer_consent", "3. 顧客知情確認關 (Customer Consent Gate)"),
            ("profit_margin", "4. 零負毛利關 (Profit Margin Gate)")
        ]

        for key, title in labels:
            gate_info = self.records["gates"][key]
            res = "【通過】" if gate_info["passed"] else "【退回】"
            md.append(f"### {title} —— {res}")
            for d in gate_info["details"]:
                md.append(f"- {d}")
            md.append("")

        md.append("---\n*本紀錄由戴明防區A把關程式 (zone_a_pricing_auditor.py) 自動產生，具備確定性客觀效力。*")

        out_path.write_text("\n".join(md), encoding="utf-8")
        return str(out_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python zone_a_pricing_auditor.py <受審報價單路徑>")
        sys.exit(1)

    auditor = ZoneAPricingAuditor(sys.argv[1])
    verdict, record_path = auditor.audit()

    print(f"\n=======================================================")
    print(f"   受審文件：{auditor.filepath.name}")
    print(f"   審查判定：{verdict}")
    print(f"   紀錄存檔：{record_path}")
    print(f"=======================================================\n")

    for k, info in auditor.records["gates"].items():
        status = "PASSED" if info["passed"] else "REJECTED"
        print(f"[{status}] {k}:")
        for d in info["details"]:
            print(f"  {d}")
        print()

    sys.exit(0 if auditor.records["passed"] else 1)
