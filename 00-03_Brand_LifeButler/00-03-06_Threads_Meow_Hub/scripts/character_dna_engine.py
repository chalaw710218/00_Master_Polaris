#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
character_dna_engine.py — 極星雙主角視覺 DNA 與出圖一致性硬約束引擎
架構監製：首席視覺長約瑟夫 (Josef) ✕ 行銷長泰勒絲 (Taylor, CMO) ✕ 首席品質長戴明 (Dr. Deming)

【核心使命】：
徹底消滅角色出圖漂移（橘貓變三花、路人臉混入、動漫風干擾）！
將創辦人親定之「喵編」與「影」之生物型態、光學質感與視角鐵律程式化死鎖！
"""

import sys
import re

# 確保 Windows UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# 🐱 【喵編 (Meow) 法定視覺 DNA 常數】
MEOW_DNA = {
    "name": "喵編 (店貓)",
    "species": "台灣短毛米克斯銀灰古典虎斑貓",
    "coat": "銀灰底毛，背部與兩側有清晰立體的深灰/炭黑古典對稱虎斑紋路",
    "forehead": "額頭正中央有清晰端正的黑色「M」字斑紋",
    "eyes": "大而圓潤靈動的貓眼，眼珠為晶瑩透亮的翠綠翡翠色 (Emerald Green)",
    "bib_and_socks": "胸前純白無雜毛的白圍兜 (White bib)，四隻腳掌穿著乾淨純白的白手套與短襪 (White socks)",
    "paws": "粉紅色帶微小深色斑點的乾淨肉球",
    "body_type": "微圓厚實、骨架勻稱、健康飽滿且慵懶可愛的成年店貓體態",
    "props": "隨身常伴精緻金屬貓罐頭、新鮮海魚、或日式木質器皿，掛有木質「寶桑物流」掛牌",
    "photo_style": (
        "Fujifilm 35mm f/2.0 寫實常民生活攝影，柔和溫暖自然光，"
        "台東老宅原木地板、日式木窗框、亞麻布簾光影，"
        "毛髮纖毫畢現、質感真實，絕對禁止 AI 塑料油畫感、禁止卡通動漫臉、禁止文字浮水印。"
    ),
    "required_keywords": [
        "虎斑", "銀灰", "白手套", "綠", "寫實"
    ]
}


# 👤 【生活管家 影 (Shadow) 法定視覺 DNA 常數】
SHADOW_DNA = {
    "name": "生活管家 影 (Shadow)",
    "identity": "28歲東方知性女性，生活管家 Threads 首席操盤官兼官方生活小編（影）",
    "hair": "俐落柔順肩頸微捲黑曜深髮，優雅知性",
    "glasses": "極簡超輕薄細鈦框眼鏡",
    "attire": "深夜海軍藍西裝外套、深石墨灰真絲襯衫、或生活感深色針織衫",
    "pov_rule": (
        "【官方小編出鏡主權（創辦人親定）】：影是生活管家官方小編，完全可以正大光明出現在畫面鏡頭中！"
        "畫面可以是影本人的專注工作姿態、老木桌前品茶閱讀、生活記帳、走廊遠眺等自然寫實人物照，"
        "亦可為生活微觀 POV 視角（端茶、手作）。"
        "核心人物唯一性約束：畫面中的人物主角只能是「生活管家 影 本人」，"
        "100% 絕對禁止出現任何男人！100% 絕對禁止出現隨機陌生路人！"
    ),
    "photo_style": (
        "Fujifilm 35mm f/1.8 寫實生活氛圍感攝影，藍調時刻 (Blue Hour) 或午後溫暖側光，"
        "真實台東生活紋理（老木窗、陶杯、鐵花步道、藍色太平洋海岸線），"
        "無 AI 塑料感、色彩克制高級、光影通透。"
    ),
    "required_keywords": [
        "生活管家", "寫實", "台東"
    ]
}


def build_character_prompt(hero: str, action_scene: str) -> str:
    """
    程式化合成符合角色法定 DNA 的高保真生圖提示詞
    hero: 'meow' / 'cat' ➔ 喵編；'shadow' ➔ 生活管家影
    action_scene: 當篇貼文的具體情境（如：在清晨木地板上伸懶腰）
    """
    is_cat = hero.lower() in ("meow", "cat", "喵編", "店貓")

    if is_cat:
        dna = MEOW_DNA
        prompt = (
            f"【極星品牌官方角色 DNA 規範 · 喵編】：\n"
            f"主體：{dna['species']}「喵編」，體態{dna['body_type']}。\n"
            f"毛色特徵：{dna['coat']}，額頭特徵為「{dna['forehead']}」，"
            f"眼睛為「{dna['eyes']}」，四肢具有「{dna['bib_and_socks']}」，肉墊為「{dna['paws']}」。\n"
            f"場景動作：{action_scene}。\n"
            f"道具常伴：{dna['props']}。\n"
            f"攝影風格：{dna['photo_style']}"
        )
    else:
        dna = SHADOW_DNA
        prompt = (
            f"【極星品牌官方角色 DNA 規範 · 生活管家 影】：\n"
            f"身份特徵：{dna['identity']}。\n"
            f"外觀標配：{dna['hair']}，佩戴{dna['glasses']}，著裝為{dna['attire']}。\n"
            f"視角約束（防臉部漂移）：{dna['pov_rule']}\n"
            f"場景動作：{action_scene}。\n"
            f"攝影風格：{dna['photo_style']}"
        )

    return prompt


def verify_character_dna(hero: str, prompt_text: str) -> tuple[bool, list[str]]:
    """
    出圖前程式化檢驗：檢查 Prompt 是否包含法定 DNA 核心關鍵詞。
    若缺少核心特徵詞，一票否決！
    """
    is_cat = hero.lower() in ("meow", "cat", "喵編", "店貓")
    dna = MEOW_DNA if is_cat else SHADOW_DNA

    missing = []
    for kw in dna["required_keywords"]:
        if kw not in prompt_text:
            missing.append(kw)

    if missing:
        return False, [f"缺少角色法定 DNA 關鍵特徵詞: {', '.join(missing)}（恐導致角色外貌漂移）"]

    return True, []


if __name__ == "__main__":
    print("🧪 正在驗證角色 DNA 引擎...")
    p_meow = build_character_prompt("meow", "在台東老宅原木地板上迎著金色晨光伸大懶腰，旁邊放著一罐剛開好的貓罐頭")
    ok, errs = verify_character_dna("meow", p_meow)
    print(f"👉 喵編 DNA 生成檢驗: {'✅ 合格' if ok else '❌ 違規: ' + str(errs)}")

    p_shadow = build_character_prompt("shadow", "第一人稱視角 (POV)，雙手端著剛沖泡好的溫熱在地紅烏龍茶，放在木質老桌上")
    ok_s, errs_s = verify_character_dna("shadow", p_shadow)
    print(f"👉 影 DNA 生成檢驗: {'✅ 合格' if ok_s else '❌ 違規: ' + str(errs_s)}")
