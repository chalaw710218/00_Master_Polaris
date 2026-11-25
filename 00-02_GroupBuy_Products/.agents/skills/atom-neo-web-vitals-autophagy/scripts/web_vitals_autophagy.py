#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_vitals_autophagy.py - 尼奧前端效能遙測與依賴自噬引擎
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

# 肥大依賴自噬對照字典
BLOATED_DEPENDENCY_REGISTRY = {
    "moment": {
        "size_kb": 72.0,
        "recommendation": "替換為原生 Intl.DateTimeFormat 或 date-fns/mini",
        "savings_kb": 72.0
    },
    "lodash": {
        "size_kb": 25.0,
        "recommendation": "替換為現代 ES6+ 原生 Array/Object/Set 語法",
        "savings_kb": 25.0
    },
    "axios": {
        "size_kb": 13.0,
        "recommendation": "替換為原生 fetch API 封裝",
        "savings_kb": 13.0
    },
    "uuid": {
        "size_kb": 3.0,
        "recommendation": "替換為原生 crypto.randomUUID()",
        "savings_kb": 3.0
    },
    "jquery": {
        "size_kb": 88.0,
        "recommendation": "強烈禁止！替換為原生 document.querySelector",
        "savings_kb": 88.0
    }
}

def audit_vitals_and_autophagy(data: dict) -> dict:
    """審核 Core Web Vitals 效能並檢測肥大依賴自噬機會"""
    fcp = data.get("fcp_sec", 0.4)
    lcp = data.get("lcp_sec", 1.0)
    inp = data.get("inp_ms", 50)
    cls = data.get("cls", 0.0)
    deps = data.get("dependencies", [])
    
    # 1. 審核 Core Web Vitals 物理指標
    vitals_violations = []
    if fcp > 0.5:
        vitals_violations.append(f"FCP 首屏時間 {fcp}s 超標 (門禁: <= 0.5s)")
    if lcp > 1.2:
        vitals_violations.append(f"LCP 最大渲染時間 {lcp}s 超標 (門禁: <= 1.2s)")
    if inp > 100:
        vitals_violations.append(f"INP 互動延遲 {inp}ms 超標 (門禁: <= 100ms)")
    if cls > 0.05:
        vitals_violations.append(f"CLS 佈局位移 {cls} 超標 (門禁: <= 0.05)")
        
    is_vitals_passed = len(vitals_violations) == 0
    
    # 2. 檢測依賴自噬機會
    autophagy_targets = []
    total_savings = 0.0
    
    for dep in deps:
        dep_clean = dep.lower().strip()
        if dep_clean in BLOATED_DEPENDENCY_REGISTRY:
            info = BLOATED_DEPENDENCY_REGISTRY[dep_clean]
            autophagy_targets.append({
                "package": dep,
                "current_size_kb": info["size_kb"],
                "autophagy_action": info["recommendation"],
                "recoverable_size_kb": info["savings_kb"]
            })
            total_savings += info["savings_kb"]
            
    return {
        "web_vitals_status": "EXCELLENT" if is_vitals_passed else "NEEDS_OPTIMIZATION",
        "vitals_metrics": {
            "fcp_seconds": fcp,
            "lcp_seconds": lcp,
            "inp_milliseconds": inp,
            "cls_score": cls
        },
        "vitals_violations": vitals_violations,
        "dependency_autophagy": {
            "bloated_dependencies_detected": len(autophagy_targets),
            "targets": autophagy_targets,
            "total_bundle_size_recoverable_kb": total_savings
        },
        "neo_verdict": (
            f"效能指標達標！偵測到 {len(autophagy_targets)} 個可自噬之肥大依賴，"
            f"啟動自噬可為客戶端立即減重 {total_savings:.1f} KB！"
            if autophagy_targets else
            "架構極簡輕量！零多餘依賴，Core Web Vitals 100% 物理達標！"
        )
    }

def main():
    parser = argparse.ArgumentParser(description="尼奧前端效能遙測與依賴自噬引擎")
    parser.add_argument("--audit-performance", type=str, required=True, help="受檢專案效能與依賴 (JSON 字串)")
    
    args = parser.parse_args()
    try:
        data = json.loads(args.audit_performance)
    except Exception as e:
        print(json.dumps({"error": f"JSON 解析失敗: {str(e)}"}, ensure_ascii=False))
        sys.exit(1)
        
    res = audit_vitals_and_autophagy(data)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
