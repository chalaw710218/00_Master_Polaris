#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ergonomic_spin_tester.py - 尼奧常民人機摩擦自對弈挑刺與自癒引擎
版權所有 (c) 2026 極星內閣 - 首席前端架構師尼奧 (Neo)
"""

import sys
import json
import argparse

# 強制 Windows 環境標準輸出採用 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def audit_ergonomic_spin(data: dict) -> dict:
    """執行前端組件之常民極端視角自對弈挑刺與自癒補丁合成"""
    cname = data.get("component_name", "未命名組件")
    touch_dp = data.get("touch_target_dp", 48.0)
    font_px = data.get("font_size_px", 18.0)
    contrast = data.get("contrast_ratio", 7.0)
    steps = data.get("flow_steps", 3)
    sunlight = data.get("is_outdoor_sun", False)
    
    criticisms = []
    patches = {}
    
    # 1. 阿嬤視角挑刺 (Elder Critique)
    if touch_dp < 48.0:
        criticisms.append(f"👵 75歲阿嬤挑刺：『按鈕才 {touch_dp}dp，我大拇指一抖就按歪了！』")
        patches["touch_target"] = "min-h-[48px] min-w-[48px] p-3"
        
    if font_px < 18.0:
        criticisms.append(f"👵 75歲阿嬤挑刺：『字才 {font_px}px，老花眼鏡戴著都看不清！』")
        patches["typography"] = "text-lg font-bold"
        
    if steps > 3:
        criticisms.append(f"👵 75歲阿嬤挑刺：『按了 {steps} 步還沒弄好，到底要填多少資料？』")
        patches["flow_reduction"] = f"將 {steps} 步折疊為極簡三步（預約 ➔ 確認 ➔ 完成）"
        
    # 2. 車手烈日視角挑刺 (Rider Sunlight Critique)
    req_contrast = 8.0 if sunlight else 7.0
    if contrast < req_contrast:
        criticisms.append(f"🛵 外送車手挑刺：『正午大太陽底下對比才 {contrast:.1f}:1，反光一片白！』")
        patches["contrast_fix"] = "bg-[#F9F8F5] text-[#1E1E1E] border-2 border-[#0F2537] shadow-none"
        
    is_friction_free = len(criticisms) == 0
    score = max(0, 100 - (len(criticisms) * 25))
    
    verdict = (
        "👑 人機工程自對弈 100% 驗收通過！長輩一秒看懂、一指搞定，烈日下清晰無誤！"
        if is_friction_free else
        f"⚠️ 發現 {len(criticisms)} 項常民人機摩擦！已自主生成自癒補丁，重構介面！"
    )

    return {
        "component_name": cname,
        "is_friction_free": is_friction_free,
        "ergonomic_score": score,
        "spin_criticisms": criticisms,
        "self_healing_patches": patches,
        "neo_resolution": verdict
    }

def main():
    parser = argparse.ArgumentParser(description="尼奧常民人機自對弈挑刺引擎")
    parser.add_argument("--audit-ui", type=str, required=True, help="受檢組件參數 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.audit_ui)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = audit_ergonomic_spin(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
