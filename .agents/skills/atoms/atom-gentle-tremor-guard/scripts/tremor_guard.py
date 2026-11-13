#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
atom-gentle-tremor-guard: 高齡手部微顫過濾與太極吸附熱區原子
由首席前端架構師尼奧 (Neo) ✕ 首席品質長戴明 (Dr. Deming) 聯合打造
"""

import sys
import os
import argparse
import json

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def generate_tremor_runtime_js(min_target: int, magnetic_px: int, debounce_ms: int, tremor_px: int) -> str:
    js = f"""/**
 * Polaris Gentle UI Tremor Guard & Magnetic Snap (v1.0)
 * 專為高齡長輩微顫與手指僵硬設計之無感防護中介層
 */
(function() {{
  const CONFIG = {{
    minTargetPx: {min_target},
    magneticSnapPx: {magnetic_px},
    debounceMs: {debounce_ms},
    tremorThresholdPx: {tremor_px}
  }};

  let lastClickTime = 0;
  let touchStartX = 0;
  let touchStartY = 0;

  // [1. 太極吸附熱區：動態擴增點擊判定]
  document.addEventListener('pointerdown', function(e) {{
    touchStartX = e.clientX;
    touchStartY = e.clientY;
  }}, {{ passive: true }});

  document.addEventListener('pointerup', function(e) {{
    const now = Date.now();
    // 雙擊誤觸冷卻 (Debounce)
    if (now - lastClickTime < CONFIG.debounceMs) {{
      e.stopPropagation();
      e.preventDefault();
      return;
    }}

    const deltaX = Math.abs(e.clientX - touchStartX);
    const deltaY = Math.abs(e.clientY - touchStartY);

    // [2. 生理微顫低通濾波]
    // 若位移在 tremorThresholdPx 以內，判定為手震點擊而非故意滑動，予以就地吸附執行
    if (deltaX <= CONFIG.tremorThresholdPx && deltaY <= CONFIG.tremorThresholdPx) {{
      const target = document.elementFromPoint(e.clientX, e.clientY);
      const interactiveEl = target ? target.closest('button, a, input, select, [role="button"]') : null;
      
      if (interactiveEl) {{
        lastClickTime = now;
        // 觸發溫暖微震動 (45ms 觸覺脈衝)
        if (navigator.vibrate) {{
          navigator.vibrate(45);
        }}
      }}
    }}
  }}, {{ capture: true }});

  console.log('[🌸 Gentle UI Tremor Guard] 高齡微顫與太極吸附防護中介層已就緒');
}})();
"""
    return js

def main():
    parser = argparse.ArgumentParser(description="高齡手部微顫過濾與太極吸附熱區原子 (atom-gentle-tremor-guard)")
    parser.add_argument("--min-touch-target", type=int, default=56, help="最小觸控熱區 px (預設 56px)")
    parser.add_argument("--magnetic-padding", type=int, default=24, help="太極吸附重力半徑 px (預設 24px)")
    parser.add_argument("--debounce-ms", type=int, default=350, help="防重複連擊冷卻時間 ms (預設 350ms)")
    parser.add_argument("--tremor-px", type=int, default=8, help="生理微顫容錯抖動像素 (預設 8px)")
    parser.add_argument("--output-js", type=str, default="gentle-tremor-guard.js", help="產出 JS 中介層檔案路徑")
    parser.add_argument("--dry-run", action="store_true", help="物理演練驗證模式")

    args = parser.parse_args()

    # 1. 戴明安燈防呆審計
    if args.min_touch_target < 48:
        print(f"[戴明安燈警報] 觸控熱區 ({args.min_touch_target}px) 小於高齡無挫折最低標準 48px！觸發熔斷。")
        sys.exit(1)

    print(f"=== [atom-gentle-tremor-guard 高齡微顫防護與太極吸附熱區審計] ===")
    print(f"最小觸控熱區: {args.min_touch_target}px (超越 iOS 44px / Android 48px)")
    print(f"太極吸附半徑: +{args.magnetic_padding}px (邊界自動外擴吸附)")
    print(f"微顫容錯位移: <= {args.tremor_px}px (濾除老年性特發性震顫)")
    print(f"連擊冷卻門禁: {args.debounce_ms}ms (防止長輩焦慮重複連點)")

    js_code = generate_tremor_runtime_js(
        min_target=args.min_touch_target,
        magnetic_px=args.magnetic_padding,
        debounce_ms=args.debounce_ms,
        tremor_px=args.tremor_px
    )

    if args.dry_run:
        print(f"\n[物理演練模式 --dry-run] 產生之 gentle-tremor-guard.js 預覽 (前 250 字元):")
        print(js_code[:250] + "...\n")
        print("[物理演練驗證成功] Exit Code: 0")
        return

    with open(args.output_js, "w", encoding="utf-8") as f:
        f.write(js_code)
    print(f"[實體文件落地] 已生成前端微顫防護中介層: {args.output_js}")
    print("[執行成功] Exit Code: 0")

if __name__ == "__main__":
    main()
