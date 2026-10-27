#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
🦅 ✕ 🛠️ Polaris Forensic & Cyber Reconnaissance CLI (極星黑色穿透調查套件)
================================================================================
業務定義: 首席黑色調查官 渡鴉 (Raven)
工程架構: 技術工程長 林納斯 (Linus Torvalds)
最高授權: 極星創辦人 陳品碩 (Pinshuo)
版本: v1.0 (Deterministic Industrial Edition · 工業確定性旗艦版)
規範: RFC #001 三態熔斷 / 60秒超時防禦 / UTF-8 強制編碼 / Exit Code 0
================================================================================
"""

import sys
import os
import re
import json
import argparse
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# 確保 Windows PowerShell 下標準輸出與錯誤輸出為 UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


class LinusDeterministicValidator:
    """林納斯確定性身分與代碼校驗器 (Zero-Hallucination Ground-Truth)"""

    @staticmethod
    def validate_taiwan_tax_id(tax_id: str) -> bool:
        """
        台灣統一編號 (8碼) 加權模數校驗算法
        加權數: [1, 2, 1, 2, 1, 2, 4, 1]
        """
        if not re.match(r"^\d{8}$", tax_id):
            return False
        weights = [1, 2, 1, 2, 1, 2, 4, 1]
        digits = [int(c) for c in tax_id]
        
        sums = []
        for d, w in zip(digits, weights):
            prod = d * w
            sums.append((prod // 10) + (prod % 10))
            
        total = sum(sums)
        if total % 10 == 0:
            return True
        # 若第七位數是 7，可有另一種餘數特例
        if digits[6] == 7 and (total + 1) % 10 == 0:
            return True
        return False

    @staticmethod
    def validate_taiwan_national_id(id_str: str) -> bool:
        """
        台灣身分證字號 (1碼英文 + 9碼數字) 校驗算法
        """
        if not re.match(r"^[A-Z][12]\d{8}$", id_str):
            return False
        letter_map = {
            'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17,
            'I': 34, 'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22, 'O': 35, 'P': 23,
            'Q': 24, 'R': 25, 'S': 26, 'T': 27, 'U': 28, 'V': 29, 'W': 32, 'X': 30,
            'Y': 31, 'Z': 33
        }
        first_num = letter_map[id_str[0]]
        digits = [first_num // 10, first_num % 10] + [int(c) for c in id_str[1:]]
        weights = [1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1]
        check_sum = sum(d * w for d, w in zip(digits, weights))
        return check_sum % 10 == 0


class RavenPinyinDetector:
    """渡鴉漢語拼音漏洞偵測器 (Chinese Pinyin Heuristic Mask Stripper)"""

    PINYIN_SYLLABLES = {
        "teng", "jing", "xue", "nai", "chen", "huang", "lin", "li", "zhang", "wang",
        "liu", "yang", "zhao", "wu", "zhou", "xu", "sun", "ma", "zhu", "hu", "guo",
        "he", "gao", "luo", "zheng", "liang", "xie", "song", "tang", "xu", "han",
        "feng", "deng", "cao", "peng", "zeng", "xiao", "tian", "dong", "yuan", "pan",
        "yu", "jiang", "cai", "yu", "du", "su", "ye", "cheng", "lv", "wei", "shi",
        "bai", "fan", "jin", "long", "hao", "wen", "ming", "hua", "jun", "xin", "yi"
    }

    @classmethod
    def analyze_handle(cls, handle: str) -> Dict[str, Any]:
        """
        分析帳號 Handle 是否含有漢語拼音特徵（戳破假洋人、假日本人偽裝）
        """
        cleaned = re.sub(r"[^a-zA-Z]", "", handle).lower()
        if not cleaned:
            return {"is_pinyin_suspect": False, "score": 0.0, "matched_syllables": []}

        matched = []
        remainder = cleaned
        for syll in sorted(cls.PINYIN_SYLLABLES, key=len, reverse=True):
            if syll in remainder:
                matched.append(syll)
                remainder = remainder.replace(syll, "", 1)

        coverage = (len(cleaned) - len(remainder)) / len(cleaned)
        is_suspect = coverage >= 0.6 or len(matched) >= 3

        return {
            "handle": handle,
            "cleaned": cleaned,
            "matched_syllables": matched,
            "coverage_ratio": round(coverage, 2),
            "is_pinyin_suspect": is_suspect,
            "verdict": "高度疑似華語拼音母語者（假日本人/假外籍偽裝破綻）" if is_suspect else "拼音特徵不顯著"
        }


class RavenJudicialParser:
    """渡鴉司法裁判書案號與風險解析器"""

    HIGH_RISK_TYPES = {
        "司票": ("本票裁定", "極高風險 (票據欠款未還，聲請法院強制執行扣押)"),
        "司促": ("支付命令", "高風險 (債務逾期未還，債權人聲請命令清償)"),
        "重訴": ("重大民事訴訟", "極高風險 (通常涉案金額在數百萬至數千萬元以上)"),
        "金重訴": ("重大金融訴訟", "極限高危 (涉及銀行法、洗錢、證交法吸金)"),
        "拍": ("拍賣抵押物", "極高風險 (擔保品如房地產即將遭法院法拍)"),
        "訴": ("一般訴訟", "中度風險 (民刑事本案審理)"),
        "簡上": ("簡易二審", "中度風險"),
        "執": ("強制執行", "極高風險 (已進入查封拍賣財產程序)")
    }

    @classmethod
    def parse_case_number(cls, case_str: str) -> Dict[str, Any]:
        """
        解析台灣法院裁判案號，例如：'112年度司票字第1026號' 或 '臺灣高雄地方法院 112年度司票字第1026號'
        """
        pattern = r"(?:(?:臺灣)?(\w+地方法院|\w+高等法院|\w+高分院))?\s*(\d+)年度?([^\d]+)字第(\d+)號"
        match = re.search(pattern, case_str)
        if not match:
            return {"valid": False, "raw": case_str, "error": "無法識別符合台灣法院規範之案號"}

        court = match.group(1) or "未知法院"
        year = int(match.group(2))
        case_type = match.group(3).strip()
        case_seq = match.group(4)

        risk_info = cls.HIGH_RISK_TYPES.get(case_type, ("一般案件", "常態程序"))

        return {
            "valid": True,
            "court": court,
            "republic_year": year,
            "ad_year": year + 1911,
            "case_type": case_type,
            "case_type_name": risk_info[0],
            "risk_assessment": risk_info[1],
            "case_seq": case_seq,
            "normalized_case_number": f"{year}年度{case_type}字第{case_seq}號"
        }


class PolarisDossierBuilder:
    """全景穿透式因果卷宗生成器 (遵照品碩至高知情權與微觀事實鋪開憲則)"""

    @staticmethod
    def generate_dossier_markdown(
        target_name: str,
        target_type: str,
        threat_tier: int,
        judicial_records: List[Dict[str, Any]],
        social_footprints: List[Dict[str, Any]],
        pinyin_analysis: Optional[Dict[str, Any]],
        timeline_events: List[Dict[str, str]],
        investigator: str = "渡鴉 (Raven)",
        supervisor: str = "林納斯 (Linus)"
    ) -> str:
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_date = datetime.now().strftime("%Y%m%d")
        
        md = []
        md.append(f"# 【機密鑑識卷宗 · STRICTLY CONFIDENTIAL】")
        md.append(f"## 案號：DOSSIER-{file_date}-{target_name}-AUTO")
        md.append(f"### 調查標的：{target_name}（類型：{target_type} ｜ 威脅分流：Tier {threat_tier}）")
        md.append(f"- **主辦調查官**：{investigator}（業務情報定義）")
        md.append(f"- **架構監製**：{supervisor}（確定性工程驗證）")
        md.append(f"- **最高呈報對象**：創辦人 陳品碩（品碩）")
        md.append(f"- **生成時間**：{date_str} (UTC+8)")
        md.append(f"- **安全級別**：極星最高機密（受 .gitignore 永久物理屏蔽，嚴禁外流）")
        md.append("\n---\n")

        # 第一層：宏觀因果拓撲
        md.append("## 🏛️ 第一層｜全域因果脈絡骨架 (Macro Topology & Motives)")
        if threat_tier == 1:
            md.append("> 🚨 **【Tier 1 核心高危預警】**：標的涉及高額金流或核心合約，存在潛在債務違約、法律訴訟或人設包裝風險。")
        elif threat_tier == 2:
            md.append("> ⚠️ **【Tier 2 一般商業快篩】**：常態特約商戶與合作夥伴，監控基礎合規與票據信譽。")
        else:
            md.append("> 🛡️ **【Tier 3 社交防火牆】**：非商業玩伴對象，啟動三零防火牆（零借貸/零代墊/零私密），維護品碩生活隱私。")
        
        if pinyin_analysis and pinyin_analysis.get("is_pinyin_suspect"):
            md.append(f"\n* **核心破綻診斷**：帳號 `{pinyin_analysis.get('handle')}` 經語義演算法檢出華語拼音音節 `{pinyin_analysis.get('matched_syllables')}`（覆蓋率 {pinyin_analysis.get('coverage_ratio')}），徹底打破其外籍/混血人設面具。")

        md.append("\n---\n")

        # 第二層：微觀全景硬證據鏈
        md.append("## 🔍 第二層｜微觀全景硬證據鏈 (Micro Ground-Truth Chain · 100% 詳細呈現)")
        
        # 1. 司法裁判明細
        md.append("### 1. 司法裁判與票據執行案號全景")
        if judicial_records:
            md.append("| 裁判年份 | 承辦法院 | 完整案號 | 案由性質 | 風險定性評級 | 裁定金額/標的 |")
            md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for rec in judicial_records:
                md.append(f"| {rec.get('year', '-')} | {rec.get('court', '-')} | {rec.get('case_no', '-')} | {rec.get('type', '-')} | {rec.get('risk', '-')} | {rec.get('amount', '待強制執行查估')} |")
        else:
            md.append("*目前資料庫查無一審以上高風險裁判案號。*")

        # 2. 數位足跡與社群碰撞
        md.append("\n### 2. 數位足跡與跨域社群碰撞紀錄")
        if social_footprints:
            md.append("| 平台名稱 | 帳號 Handle | 註冊時戳/狀態 | 語義破綻/關聯依據 | 連結/來源 |")
            md.append("| :--- | :--- | :--- | :--- | :--- |")
            for soc in social_footprints:
                md.append(f"| {soc.get('platform', '-')} | `{soc.get('handle', '-')}` | {soc.get('timestamp', '-')} | {soc.get('notes', '-')} | {soc.get('url', '-')} |")
        else:
            md.append("*未發現公開外洩社交帳號或無公開足跡。*")

        # 3. 因果時間軸重構
        md.append("\n### 3. 因果時空演進時間軸 (Timeline Reconstruction)")
        if timeline_events:
            md.append("```mermaid\nflowchart TD")
            for idx, evt in enumerate(timeline_events):
                node_id = f"T{idx+1}"
                md.append(f'    {node_id}["📅 {evt.get("date")}: {evt.get("title")}\\n({evt.get("desc")})"]')
                if idx > 0:
                    md.append(f"    T{idx} --> {node_id}")
            md.append("```\n")
            md.append("| 精確日期 (年月日) | 關鍵事件節點 | 微觀事實與推導依據 |")
            md.append("| :--- | :--- | :--- |")
            for evt in timeline_events:
                md.append(f"| {evt.get('date')} | **{evt.get('title')}** | {evt.get('desc')} |")
        else:
            md.append("*時間軸節點不足，等待增量資料。*")

        # 第三層：創辦人決策建議
        md.append("\n---\n")
        md.append("## 👑 第三層｜呈報創辦人品碩之防禦決策建言")
        md.append("1. **金流鐵壁阻絕**：嚴禁任何私下借貸、代墊款、帳戶過水，全數推由公司標準會計流程審核。")
        md.append("2. **知情威壓儲備**：已將上述客觀法院案號與時序整理成法定證據包，品碩需要時可隨時調用。")
        md.append("3. **看透不說破**：維持社交體面，不主動激化矛盾，將風險隔絕在極星水庫之外。")
        md.append("\n---\n*卷宗已完成本地物理隔離封存。*")

        return "\n".join(md)


def run_self_test() -> int:
    """林納斯 DOD 確定性單元測試套件"""
    print("=" * 60)
    print("🛠️ 正在執行林納斯工程驗收與確定性單元測試 (Linus DOD Test Suite)...")
    print("=" * 60)

    # 1. 測試統一編號驗證 (以台積電 22099131 為例)
    assert LinusDeterministicValidator.validate_taiwan_tax_id("22099131") is True, "統編驗證失敗"
    assert LinusDeterministicValidator.validate_taiwan_tax_id("12345678") is False, "無效統編誤判"
    print("  [PASS] 台灣統一編號 (Tax ID) 加權模數算法驗證通過")

    # 2. 測試身分證字號驗證
    assert LinusDeterministicValidator.validate_taiwan_national_id("A123456789") is True, "身分證驗證失敗"
    assert LinusDeterministicValidator.validate_taiwan_national_id("A123456788") is False, "無效身分證誤判"
    print("  [PASS] 台灣身分證字號 (National ID) 算法驗證通過")

    # 3. 測試漢語拼音漏洞偵測 (以藤井雪奈 tengjingxuenai1 為例)
    res_pinyin = RavenPinyinDetector.analyze_handle("tengjingxuenai1")
    assert res_pinyin["is_pinyin_suspect"] is True, "藤井雪奈拼音漏抓"
    assert "teng" in res_pinyin["matched_syllables"], "音節匹配遺漏"
    print(f"  [PASS] 渡鴉拼音撕裂器 (Pinyin Stripper) 驗證通過: {res_pinyin['verdict']}")

    # 4. 測試司法裁判案號解析 (以 112年度司票字第1026號 為例)
    res_case = RavenJudicialParser.parse_case_number("臺灣高雄地方法院 112年度司票字第1026號")
    assert res_case["valid"] is True, "案號解析失敗"
    assert res_case["case_type"] == "司票", "案由字別解析錯誤"
    assert res_case["ad_year"] == 2023, "民國轉西元計算錯誤"
    print(f"  [PASS] 司法裁判案號解析器驗證通過: {res_case['normalized_case_number']} -> {res_case['risk_assessment']}")

    # 5. 測試卷宗生成器
    sample_dossier = PolarisDossierBuilder.generate_dossier_markdown(
        target_name="測試標的",
        target_type="person",
        threat_tier=1,
        judicial_records=[{"year": "112", "court": "高雄地院", "case_no": "112年度司票字第1026號", "type": "本票裁定", "risk": "極高風險", "amount": "NT$22,420"}],
        social_footprints=[{"platform": "Twitter/X", "handle": "tengjingxuenai1", "timestamp": "2022-04", "notes": "漢語拼音假外籍破綻", "url": "https://x.com"}],
        pinyin_analysis=res_pinyin,
        timeline_events=[
            {"date": "2022-03-10", "title": "簽署小額分期本票", "desc": "裕富數位資融 67,260 元"},
            {"date": "2022-04-01", "title": "建立推特分身", "desc": "帳號 @tengjingxuenai1"},
            {"date": "2023-02-04", "title": "法院強制執行裁定", "desc": "剩餘 22,420 元欠款准予扣押"}
        ]
    )
    assert "# 【機密鑑識卷宗 · STRICTLY CONFIDENTIAL】" in sample_dossier
    assert "112年度司票字第1026號" in sample_dossier
    print("  [PASS] 全景穿透式因果卷宗生成器 (Dossier Builder) 驗證通過")

    print("\n" + "=" * 60)
    print("🎯 林納斯 DOD 確定性全套驗收 100% 通過！(Exit Code 0)")
    print("=" * 60)
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="🦅 ✕ 🛠️ Polaris Forensic & Cyber Reconnaissance CLI (極星黑色穿透調查套件)"
    )
    parser.add_argument("--self-test", action="store_true", help="執行林納斯 DOD 確定性單元測試與自我診斷")
    parser.add_argument("--target", type=str, help="調查標的名稱 (人名 / 公司名 / 案件名)")
    parser.add_argument("--type", choices=["person", "company", "handle"], default="person", help="標的類型")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3], default=2, help="動態威脅分級 (1:核心高危, 2:一般快篩, 3:社交防火牆)")
    parser.add_argument("--handle", type=str, help="社群帳號 Handle (進行拼音漏洞與社群碰撞)")
    parser.add_argument("--tax-id", type=str, help="台灣統一編號 (驗證並進行商工穿透)")
    parser.add_argument("--case-no", type=str, help="司法裁判案號 (如 '112年度司票字第1026號')")
    parser.add_argument("--output-dossier", action="store_true", help="自動輸出標準格式之全景因果卷宗到 05_Case_Dossiers/")

    args = parser.parse_args()

    if args.self_test:
        sys.exit(run_self_test())

    if not args.target:
        parser.print_help()
        sys.exit(1)

    print(f"🦅 [渡鴉] 正在啟動極星穿透調查: 標的【{args.target}】 ｜ 威脅等級: Tier {args.tier} ｜ 類型: {args.type}")

    # 1. 拼音分析
    pinyin_result = None
    if args.handle:
        pinyin_result = RavenPinyinDetector.analyze_handle(args.handle)
        print(f"  * Handle 拼音漏洞檢測: {pinyin_result['verdict']} (匹配音節: {pinyin_result['matched_syllables']})")

    # 2. 統編分析
    if args.tax_id:
        tax_valid = LinusDeterministicValidator.validate_taiwan_tax_id(args.tax_id)
        status_text = "合法統編" if tax_valid else "無效/偽造統編"
        print(f"  * 統一編號檢驗: {args.tax_id} -> {status_text}")

    # 3. 司法案號解析
    judicial_list = []
    if args.case_no:
        case_info = RavenJudicialParser.parse_case_number(args.case_no)
        if case_info["valid"]:
            print(f"  * 司法裁判案號: {case_info['normalized_case_number']} (案由: {case_info['case_type_name']} ｜ 評級: {case_info['risk_assessment']})")
            judicial_list.append({
                "year": str(case_info["republic_year"]),
                "court": case_info["court"],
                "case_no": case_info["normalized_case_number"],
                "type": case_info["case_type_name"],
                "risk": case_info["risk_assessment"],
                "amount": "依法強制執行中"
            })

    # 4. 輸出卷宗
    if args.output_dossier:
        dossiers_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "05_Case_Dossiers")
        )
        os.makedirs(dossiers_dir, exist_ok=True)
        file_date = datetime.now().strftime("%Y%m%d")
        safe_name = re.sub(r'[\\/*?:"<>| ]', "_", args.target)
        file_path = os.path.join(dossiers_dir, f"DOSSIER_{file_date}_{safe_name}.md")

        content = PolarisDossierBuilder.generate_dossier_markdown(
            target_name=args.target,
            target_type=args.type,
            threat_tier=args.tier,
            judicial_records=judicial_list,
            social_footprints=[{"platform": "OSINT Target", "handle": args.handle or args.target, "timestamp": "動態抓取", "notes": "跨域足跡碰撞", "url": "-"}] if args.handle else [],
            pinyin_analysis=pinyin_result,
            timeline_events=[
                {"date": datetime.now().strftime("%Y-%m-%d"), "title": "極星穿透調查建檔", "desc": f"發起 Tier {args.tier} 黑色背景審查"}
            ]
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"🛠️ [林納斯] 全景穿透因果卷宗已生成並物理封存: {file_path}")

    print("🦅 ✕ 🛠️ 調查管線執行完畢 (Exit Code 0)。")
    return 0


if __name__ == "__main__":
    main()
