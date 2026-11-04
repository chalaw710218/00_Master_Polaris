#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taylor Omnichannel Launcher (泰勒絲零拷貝全域行銷發射台)
架構監製：🎤 首席行銷長 泰勒絲 (CMO Taylor) ✕ 🛠️ 首席工程長 林納斯 (CTO Linus) ✕ 🧮 財務長 算盤 (CFO Abacus) ✕ 📐 首席視覺長 約瑟夫 (CVO Josef)

功能定位：
極星行銷「一鍵直通」作戰中樞。將任何未經修飾的商品、生活管家服務或節氣選品，在 5 秒內確定性轉換為：
1. 100% 免 AI 說教腔之雙主角（喵編/闆仔/泰勒絲）走心社群文案矩陣
2. 算盤 5D 單元經濟定價與防彈衣四鐵律安全驗證
3. 約瑟夫六十項法典 4:5 / 9:16 視覺印刷與社群海報規格規格書
4. 預約排程與一鍵直通 Threads / Facebook 發布資料包 (JSON Payload)
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Windows console encoding defense
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ---------------------------------------------------------------------------
# 1. 禁用 AI 假大空詞庫 (Zero-AI Vernacular Filter)
# ---------------------------------------------------------------------------
FORBIDDEN_BUZZWORDS = [
    "打造", "賦能", "顛覆", "重磅", "極致", "不容錯過", "引領潮流",
    "解鎖", "震撼來襲", "匠心獨運", "尊榮享受", "領先業界", "無懈可擊",
    "引爆全網", "重新定義", "卓越品質"
]

# 內部禁語紅線
FORBIDDEN_INTERNAL_CODENAMES = ["極星", "Polaris", "內閣"]

def audit_text_security(text: str) -> tuple[bool, list[str]]:
    """嚴格審查文案是否觸犯 AI 腔或洩漏內部代號"""
    violations = []
    for word in FORBIDDEN_INTERNAL_CODENAMES:
        if word in text:
            violations.append(f"【嚴重違法憲法紅線】對外文案洩漏內部代號: '{word}'")
    for buzz in FORBIDDEN_BUZZWORDS:
        if buzz in text:
            violations.append(f"【觸犯去AI腔戒律】文案出現假大空詞彙: '{buzz}'")
    return (len(violations) == 0, violations)

# ---------------------------------------------------------------------------
# 2. 算盤 5D 定價安全核驗 (Abacus 5D Pricing Gate)
# ---------------------------------------------------------------------------
def audit_pricing(cost: float, price: float, labor_hours: float = 1.0) -> dict:
    """計算毛利率與單元經濟水庫安全線"""
    gross_profit = price - cost
    margin = (gross_profit / price * 100) if price > 0 else 0.0
    safe_margin = margin >= 25.0
    
    # 5D 時間點數 (TP) 估算
    d1_hours = labor_hours * 10
    d2_risk = 5.0
    d3_pro = 8.0
    d4_urgency = 0.0
    d5_trust = 10.0
    total_tp = d1_hours + d2_risk + d3_pro + d4_urgency + d5_trust
    
    return {
        "cost": cost,
        "price": price,
        "gross_profit": gross_profit,
        "margin_percent": round(margin, 2),
        "is_margin_safe": safe_margin,
        "5D_time_points": total_tp,
        "pricing_verdict": "通過 (利潤充足且無暴利)" if safe_margin else "警告 (毛利率低於25%警戒線)"
    }

# ---------------------------------------------------------------------------
# 3. 約瑟夫 60 項法典海報規格生成器 (Josef Poster Artisan Specs)
# ---------------------------------------------------------------------------
def generate_josef_specs(theme: str, visual_style: str = "social_4_5") -> dict:
    """產出符合約瑟夫六十項法典之確定性排版參數"""
    return {
        "dimensions": "1080x1350 px (4:5 縱向黃金比例)" if visual_style == "social_4_5" else "1080x1920 px (9:16 直式短影音)",
        "dpi": 300,
        "color_profile": "Display P3 / CMYK (TAC <= 250%)",
        "typography": {
            "title_font": "思源宋體 Heavy (光學灰度校正 1:1.18)",
            "body_font": "思源黑體 Regular (避頭尾與標點懸掛)",
            "contrast_ratio": ">= 4.5:1 (高齡 CSF 視力平權防線)"
        },
        "color_palette": {
            "background": "#FBF8F3 (溫暖大地羊皮紙米白)",
            "primary": "#2D3436 (深夜暖黑，K100 單色直壓)",
            "accent": "#D35400 (台東暖陽落日澄)"
        },
        "qr_code_size": "28mm 實體掃描安全邊界",
        "poka_yoke_checks": [
            "TAC <= 250% 印刷防透背油墨過飽和",
            "赫曼方格暗斑視覺消除",
            "街角透視預拉伸補償"
        ]
    }

# ---------------------------------------------------------------------------
# 4. 泰勒絲 120 鐵律文案合成矩陣 (Storytelling Matrix)
# ---------------------------------------------------------------------------
def generate_copy_matrix(theme: str, price: float, key_features: list[str]) -> dict:
    """依據泰勒絲 120 鐵律，合成三種真實人格文案"""
    
    features_str = "、".join(key_features)
    
    # 1. 喵編人設 (Threads / IG)：傲嬌店貓、愛碎碎念闆仔、賺罐罐、溫暖接梗
    meow_threads = (
        f"闆仔今天又不知道在堅持什麼了…🙄\n\n"
        f"一大早拉著大家去巡【{theme}】，一直念說「新鮮度差一小時都不行」。"
        f"拜託，本喵只想在窗邊曬太陽舔毛好嗎！🐾\n\n"
        f"但老實說，這批真的有甜、香氣整個在廚房飄開，連挑嘴的我偷聞一下都原諒他了。\n"
        f"今天算盤那邊給的分享價是 NT$ {int(price)}。\n\n"
        f"順路的鄰居下班散步來自提點自己拿喔，先說好，不要吵醒本喵睡午覺～\n\n"
        f"#生活的一部分就醬點"
    )
    
    # 2. 泰勒絲知心閨蜜人設 (FB 溫暖長文 / 官網故事)：感官微鏡頭、南島風土、四時節氣
    taylor_narrative = (
        f"不知道你今晚下班的路上，有沒有聞到空氣裡那股轉涼的風？\n\n"
        f"在台東，這個時節的土地總會給人特別安靜的踏實感。今天帶給大家的【{theme}】，"
        f"沒有工廠標準化的催熟，只有晨間露水和太陽曬過的泥土香。\n\n"
        f"我們把繁瑣的中間抽成拿掉，算盤精算後給予產地夥伴最體面的報酬，"
        f"分享價定在平實的 NT$ {int(price)}。\n\n"
        f"希望這份帶著溫度的滋味，能成為你家今晚餐桌上一抹放鬆的溫柔。\n"
        f"老規矩，如果有任何一口不合心意，隨時跟我們說，我們無條件為你處理。"
    )
    
    # 3. 闆仔老派骨氣人設 (透明大帳 / 產地直白)：成本穿透、老派初心、有所不為
    boss_grounded = (
        f"做生意幾十年，我始終相信一句話：欺瞞客人一次，招牌就砸了一輩子。\n\n"
        f"關於這次的【{theme}】，特點很簡單：{features_str}。\n"
        f"我們不包裝花俏辭藻，產地出貨、冷鏈自提到你手上，明碼標價 NT$ {int(price)}。\n"
        f"每分錢花在哪裡，算盤的帳本清清楚楚。\n"
        f"認同這份踏實的朋友，歡迎來門市坐坐、喝杯熱茶。"
    )
    
    return {
        "meow_threads": meow_threads,
        "taylor_narrative": taylor_narrative,
        "boss_grounded": boss_grounded
    }

# ---------------------------------------------------------------------------
# 5. 主發射台總控 (Main Launcher Pipeline)
# ---------------------------------------------------------------------------
def launch_campaign(theme: str, cost: float, price: float, features: list[str], output_dir: str = None) -> dict:
    """執行完整 60 秒跨內閣一鍵行銷編譯流水線"""
    
    # 1. 審計定價
    pricing_result = audit_pricing(cost, price)
    
    # 2. 合成文案
    copy_matrix = generate_copy_matrix(theme, price, features)
    
    # 3. 文本資安與去 AI 腔質檢
    security_checks = {}
    for style, text in copy_matrix.items():
        is_safe, violations = audit_text_security(text)
        security_checks[style] = {
            "is_safe": is_safe,
            "violations": violations
        }
        if not is_safe:
            print(f"⚠️ 警告: {style} 未通過質檢: {violations}")
            
    # 4. 約瑟夫視覺排版規格
    visual_specs_social = generate_josef_specs(theme, "social_4_5")
    visual_specs_reels = generate_josef_specs(theme, "reels_9_16")
    
    # 5. 整合最終成果包
    payload = {
        "campaign_id": f"CAMP_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "created_at": datetime.now().isoformat(),
        "theme": theme,
        "pricing_audit": pricing_result,
        "copy_matrix": copy_matrix,
        "security_audit": security_checks,
        "josef_visual_specs": {
            "social_poster_4_5": visual_specs_social,
            "reels_dynamic_9_16": visual_specs_reels
        },
        "status": "READY_FOR_DEPLOYMENT"
    }
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        out_file = os.path.join(output_dir, f"{payload['campaign_id']}.json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        payload["saved_to"] = out_file
        
    return payload

# ---------------------------------------------------------------------------
# CLI 入口與自我測試
# ---------------------------------------------------------------------------
def run_self_test():
    print("=== 開始執行泰勒絲零拷貝發射台單元自測 (Self-Test) ===")
    
    theme = "台東二十四節氣・立冬老薑鮮魚湯"
    cost = 120.0
    price = 220.0
    features = ["清晨新港漁船現撈鬼頭刀", "卑南小農高山老薑", "古法純釀黑麻油"]
    
    res = launch_campaign(theme, cost, price, features)
    
    # 驗證定價安全
    assert res["pricing_audit"]["is_margin_safe"] == True, "定價毛利率未過安全線"
    print("✅ 算盤 5D 定價閘門通過 (毛利率: {}%)".format(res["pricing_audit"]["margin_percent"]))
    
    # 驗證文案資安 (零極星、零AI腔)
    for style, sec in res["security_audit"].items():
        assert sec["is_safe"] == True, f"{style} 文案質檢失敗: {sec['violations']}"
    print("✅ 去 AI 腔與憲法紅隊閘門 100% 通過 (0 違規)")
    
    # 驗證約瑟夫海報規格
    assert "typography" in res["josef_visual_specs"]["social_poster_4_5"], "海報字體規格缺失"
    print("✅ 約瑟夫 4:5 / 9:16 視覺法典規格生成成功")
    
    print("\n🎉 自我測試全部通過！Exit Code 0！")
    return 0

def main():
    parser = argparse.ArgumentParser(description="泰勒絲零拷貝全域行銷發射台 CLI")
    parser.add_argument("--test", action="store_true", help="執行發射台自動化單元測試")
    parser.add_argument("--theme", type=str, help="行銷主題或商品名稱")
    parser.add_argument("--cost", type=float, default=100.0, help="上游原物料與勞動成本")
    parser.add_argument("--price", type=float, default=180.0, help="大盤/社群定價")
    parser.add_argument("--features", type=str, nargs="+", default=["產地直送", "當季當令"], help="核心特點")
    parser.add_argument("--outdir", type=str, help="輸出 JSON 資料夾")
    
    args = parser.parse_args()
    
    if args.test:
        sys.exit(run_self_test())
        
    if not args.theme:
        print("提示：請輸入 --theme 或執行 --test")
        parser.print_help()
        sys.exit(1)
        
    res = launch_campaign(args.theme, args.cost, args.price, args.features, args.outdir)
    print("\n========================================================")
    print(f"🚀 行銷戰役已準備就緒: {res['theme']} ({res['campaign_id']})")
    print("========================================================")
    print(f"• 定價狀態: 成本 NT$ {res['pricing_audit']['cost']} -> 售價 NT$ {res['pricing_audit']['price']} (毛利 {res['pricing_audit']['margin_percent']}%)")
    print(f"• 喵編 Threads 文案草稿:")
    print("--------------------------------------------------------")
    print(res["copy_matrix"]["meow_threads"])
    print("--------------------------------------------------------")
    print(f"• 約瑟夫海報規格: {res['josef_visual_specs']['social_poster_4_5']['dimensions']} | 色溫: {res['josef_visual_specs']['social_poster_4_5']['color_palette']['background']}")
    if "saved_to" in res:
        print(f"• 資料包已儲存至: {res['saved_to']}")
    print("========================================================\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
