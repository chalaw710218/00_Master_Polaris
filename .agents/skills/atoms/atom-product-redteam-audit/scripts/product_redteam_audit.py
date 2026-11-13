#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/product_redteam_audit.py
商品化多 Agent 四方黑臉交叉審查與戴明防呆安燈引擎
整合泰勒絲 (FB)、影 (Threads)、約瑟夫 (視覺)、戴明 (合規防呆) 四方獨立挑刺
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple

sys.stdout.reconfigure(encoding='utf-8')

FORBIDDEN_BRAND_TERMS = ["極星", "Polaris", "polaris", "POLARIS"]
PASS_SCORE_THRESHOLD = 85

def audit_taylor_facebook(text: str) -> Tuple[int, List[str], List[str]]:
    """泰勒絲 (FB 檢核 · 滿分 25 分)"""
    score = 25
    violations = []
    passes = []

    # 1. 內文外部超連結審查 (防降權)
    if "http://" in text or "https://" in text:
        score -= 10
        violations.append("【泰勒絲挑刺】FB 內文包含外部超連結！違反演算法防降權規範，應抽離至第一則留言。")
    else:
        passes.append("FB 內文零外部超連結，演算法權重保護良好。")

    # 2. 第一則留言閉環
    if "第一則留言" not in text and "第一留言" not in text:
        score -= 5
        violations.append("【泰勒絲挑刺】未見引導讀者前往『第一則留言』之閉環字句。")
    else:
        passes.append("具備前往第一則留言點擊導流引導。")

    # 3. 篇幅與資訊過載審查
    if len(text) > 1500:
        score -= 5
        violations.append("【泰勒絲挑刺】FB 內文過於冗長膨脹（> 1,500 字），手機易失去耐性。")
    else:
        passes.append("篇幅節奏適中，具備良好常民呼吸感。")

    return max(0, score), passes, violations

def audit_kage_threads(text: str) -> Tuple[int, List[str], List[str]]:
    """影 (Threads 檢核 · 滿分 25 分)"""
    score = 25
    violations = []
    passes = []

    # 1. 反 AI 塑料感審查 (空洞加油套話)
    ai_cliches = ["賦能", "閉環", "抓手", "底層邏輯", "加油每一天", "溫暖同行"]
    found_cliches = [c for c in ai_cliches if c in text]
    if found_cliches:
        score -= 8
        violations.append(f"【影挑刺】出現空洞 AI 塑料感詞彙：{found_cliches}，請換成生活管家接地氣的大白話！")
    else:
        passes.append("無 AI 塑料套話，呈現生活管家真實體溫。")

    # 2. 是否具備真實生活痛點或自嘲
    real_markers = ["長輩", "雨天", "外送", "跑腿", "等候", "熱湯", "電話", "正氣北路"]
    if not any(m in text for m in real_markers):
        score -= 7
        violations.append("【影挑刺】缺乏台東在地生活物證或管家工作微痛點，像一般官僚廣告。")
    else:
        passes.append("具備常民生活細節物證與工作真誠體溫。")

    return max(0, score), passes, violations

def audit_josef_visual(spec_text: str) -> Tuple[int, List[str], List[str]]:
    """約瑟夫 (視覺美學檢核 · 滿分 25 分)"""
    score = 25
    violations = []
    passes = []

    # 1. 留白率與排版秩序
    lines = [l.strip() for l in spec_text.split("\n") if l.strip()]
    if len(lines) > 0 and (spec_text.count("\n\n") / max(1, len(lines))) < 0.2:
        score -= 8
        violations.append("【約瑟夫挑刺】段落間距過於緊繃！缺少大面積呼吸留白（建議留白率 >= 35%）。")
    else:
        passes.append("段落節奏分明，具備良好視覺呼吸空間。")

    # 2. 視讀層級
    if "# " not in spec_text or "## " not in spec_text:
        score -= 7
        violations.append("【約瑟夫挑刺】標題層級梯隊不清晰，缺少標準 H1 / H2 視覺建築階層。")
    else:
        passes.append("標題層級建築嚴整，閱讀動線明確。")

    return max(0, score), passes, violations

def audit_deming_compliance(full_text: str) -> Tuple[int, List[str], List[str], bool]:
    """戴明 (合規與安燈檢核 · 滿分 25 分，品牌紅線一票否決)"""
    score = 25
    violations = []
    passes = []
    fatal_brand_violation = False

    # 1. 品牌法定名稱零洩漏防火牆 (一票否決！)
    for forbidden in FORBIDDEN_BRAND_TERMS:
        if forbidden in full_text:
            fatal_brand_violation = True
            violations.append(f"【戴明致命紅線】文案出現內部研發代號「{forbidden}」！觸發全域憲則最高安燈！對外嚴格僅能使用「生活的一部分，就醬點！」或自稱「生活管家」！")

    # 2. 明碼標價齊備度
    if "NT$" not in full_text and "元" not in full_text:
        score -= 10
        violations.append("【戴明安燈】未見明確明碼標價 (NT$)，違反商業透明安燈門禁！")
    else:
        passes.append("明碼標價完整具備，符合生活管家透明定價憲章。")

    # 3. 家宅門市座標
    if "正氣北路" not in full_text:
        score -= 5
        violations.append("【戴明安燈】未載明門市實體家宅座標（正氣北路166巷90號），客戶無法自取或查核實體。")
    else:
        passes.append("實體家宅地理座標齊備。")

    return max(0, score), passes, violations, fatal_brand_violation

def run_product_redteam_audit(full_content: str) -> Dict[str, Any]:
    """執行四方黑臉審查總控"""
    t_score, t_pass, t_viol = audit_taylor_facebook(full_content)
    k_score, k_pass, k_viol = audit_kage_threads(full_content)
    j_score, j_pass, j_viol = audit_josef_visual(full_content)
    d_score, d_pass, d_viol, fatal_brand = audit_deming_compliance(full_content)

    total_score = t_score + k_score + j_score + d_score

    andon_triggered = (total_score < PASS_SCORE_THRESHOLD) or fatal_brand

    all_passes = t_pass + k_pass + j_pass + d_pass
    all_violations = t_viol + k_viol + j_viol + d_viol

    return {
        "status": "PULL_ANDON_REJECT" if andon_triggered else "PASS_ANDON",
        "total_score": total_score,
        "pass_threshold": PASS_SCORE_THRESHOLD,
        "fatal_brand_violation": fatal_brand,
        "score_breakdown": {
            "taylor_fb": f"{t_score}/25",
            "kage_threads": f"{k_score}/25",
            "josef_visual": f"{j_score}/25",
            "deming_compliance": f"{d_score}/25"
        },
        "verdict": "❌ 觸發戴明安燈拉繩！商品化審查未過門禁，強制退件自癒修正！" if andon_triggered else "✅ 四方黑臉審查大圓滿！准予呈報創辦人一鍵批准！",
        "passes": all_passes,
        "violations": all_violations
    }

def main():
    parser = argparse.ArgumentParser(description="商品化多 Agent 四方黑臉交叉審查與戴明防呆安燈引擎")
    parser.add_argument("--sample-text", type=str, default="", help="待審核商品化文字內容 (預設使用標準樣本)")
    parser.add_argument("--dry-run", action="store_true", help="執行黑臉審查模擬")
    args = parser.parse_args()

    # 預設合格樣本
    sample = args.sample_text or """# 生活管家·到府長輩陪伴與居安守護

## 一、產品規格與定價
• 服務名稱：台東市區專人到府長輩守護
• 明碼標價：NT$ 350 元 / 次 (包含保溫保鮮與全程專人責任)
• 門市取貨座標：台東市正氣北路166巷90號

## 二、FB 社群長文故事
生活在台東，有時候想為家裡的阿公阿嬤買碗熱魚湯，卻因為人在外地抽不開身。
生活管家想幫大家做的，是把那份孝心親手送到客廳。
專人專車、全程低溫保鮮，親手將安心送到家門口。
👉 預約訂購與門市資訊，管家已整理在【第一則留言】中，點擊即可直達！

## 三、Threads 扎心日常
跑外送跑久了，最怕阿公一個人慢慢開門那種孤單的眼神。
幾百塊的服務費，買回來的其實是整個晚上的安心。
生活管家今天也在正氣北路上奔馳著。
生活的一部分，就醬點！
"""

    res = run_product_redteam_audit(sample)

    print("==================================================")
    print(f"🛑 商品化四方黑臉審查報告: {res['status']} (總分: {res['total_score']} / 100)")
    print(f"得分明細: {res['score_breakdown']}")
    print(res["verdict"])
    print("--------------------------------------------------")
    print("各角色檢驗合格項目:")
    for p in res["passes"]:
        print(f"  [✓] {p}")

    if res["violations"]:
        print("--------------------------------------------------")
        print("⚠️ 黑臉挑刺與違規修正建議:")
        for v in res["violations"]:
            print(f"  [✗] {v}")
        print("==================================================")
        sys.exit(1)
    else:
        print("==================================================")
        sys.exit(0)

if __name__ == "__main__":
    main()
