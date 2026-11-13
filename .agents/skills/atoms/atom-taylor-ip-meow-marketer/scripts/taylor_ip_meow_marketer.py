#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-taylor-ip-meow-marketer: 吉祥物 IP 角色行銷與人格化流量原子腳本
專職負責行銷長泰勒絲 (Taylor) 操盤「喵編」IP 角色行銷、人設安燈審查與傲嬌生活文案。
"""

import sys
import os
import argparse
import json
import re

# Windows 控制台 UTF-8 編碼保證
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 喵編人設致命禁忌
MEOW_PERSONA_VIOLATIONS = [
    (r"小編", "嚴禁自稱『小編』，唯一法定自稱為『本喵』！"),
    (r"本貓", "嚴禁自稱『本貓』，必須使用傲嬌軟萌的『本喵』！"),
    (r"我今天代表公司", "嚴禁官僚客服腔，破壞店貓人設！"),
    (r"趕快點擊購買", "嚴禁生硬逼單，破壞傲嬌吃貨在場感！")
]

def audit_meow_copy(text: str) -> dict:
    """審核喵編文案人設合規度"""
    violations = []
    for pattern, reason in MEOW_PERSONA_VIOLATIONS:
        if re.search(pattern, text):
            violations.append({"pattern": pattern, "reason": reason})

    has_sole_pronoun = "本喵" in text
    has_feline_action = any(act in text for act in ["揣爪", "母雞蹲", "呼嚕", "尾巴", "肉球", "嗅聞", "踩奶", "打哈欠"])
    has_subtitle = "字幕" in text or "喵嗚" in text or "呼嚕" in text

    passed = (len(violations) == 0) and has_sole_pronoun and has_feline_action

    return {
        "passed": passed,
        "has_sole_pronoun_benmiao": has_sole_pronoun,
        "has_real_feline_action": has_feline_action,
        "has_vocalization_or_subtitle": has_subtitle,
        "violations_count": len(violations),
        "violations": violations
    }

def generate_meow_marketing_post(topic: str) -> str:
    """生成合規之喵編 IP 人格化行銷貼文"""
    post = (
        f"喵嗚～（字幕翻譯：今天冷空氣一吹，本喵的毛毛直接蓬了兩圈。）\n\n"
        f"剛才闆仔端出熱騰騰的【{topic}】，那股老薑跟魚油焦香剛飄過來，"
        f"本喵本來在木質長凳上揣爪母雞蹲，鼻子忍不住抽動了三下。\n\n"
        f"本喵親自伸長脖子嚴格嗅聞品檢過了：\n"
        f"沒有奇怪的化學油耗味，只有黑潮深海的自然清甜。\n"
        f"看在人類今天備餐還算勤奮的份上，本喵勉為其難准許你們下班順路去自提。\n\n"
        f"（尾巴在原木地板輕輕掃了一下，下巴搭回前爪繼續呼嚕嚕...💤）\n"
        f"#生活管家 #喵編日常 #生活的一部分就醬點"
    )
    return post

def main():
    parser = argparse.ArgumentParser(description="吉祥物 IP 角色行銷與人格化流量原子")
    parser.add_argument("--topic", type=str, default="成功港老薑慢煨野生旗魚骨原湯", help="行銷主題")
    parser.add_argument("--verify-text", type=str, help="待檢驗之喵編草案")
    parser.add_argument("--dry-run", action="store_true", default=False, help="預演模式")

    args = parser.parse_args()

    print("=== [atom-taylor-ip-meow-marketer] 泰勒絲 · 喵編 IP 角色行銷審查 ===")

    if args.verify_text:
        res = audit_meow_copy(args.verify_text)
        print(f"\n文案: 『{args.verify_text[:80]}...』")
        print(f"唯一自稱『本喵』: {'[符合]' if res['has_sole_pronoun_benmiao'] else '[缺失]'}")
        print(f"真貓生態動作: {'[符合]' if res['has_real_feline_action'] else '[缺失]'}")
        print(f"貓叫與字幕規範: {'[符合]' if res['has_vocalization_or_subtitle'] else '[缺失]'}")
        if not res["passed"]:
            print("\n❌ **【喵編人設安燈觸發：發現違規】**")
            for v in res["violations"]:
                print(f"  * {v['reason']}")
            sys.exit(1)
        else:
            print("\n[+] 喵編人設與真貓生態學檢驗 100% 通過 (Exit Code: 0)！")
            sys.exit(0)

    generated = generate_meow_marketing_post(args.topic)
    audit = audit_meow_copy(generated)

    print(f"\n行銷主題: 『{args.topic}』")
    print("\n🐾 **【喵編 IP 人格化行銷文案生成】**\n")
    print(generated)
    print(f"\n人設合規檢驗: {'[100% 通過 Exit Code: 0]' if audit['passed'] else '[未通過]'}")
    sys.exit(0 if audit["passed"] else 1)

if __name__ == "__main__":
    main()
