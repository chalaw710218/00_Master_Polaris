# -*- coding: utf-8 -*-
"""
apply_round3_upgrades.py
執行第三輪整改需求：
- B 項：挑站前先抓全部今日路線班表 (prefetchTodaySchedules)
- C 項：雙收改用台東市專門回收車班表 (recycling_routes.json 注入 LOCAL_SEED_ROUTES，且依需求分流)
- D 項：卡片增加「⚠️ 提早出門提醒」
- F 項：卡片同時清晰展示「官方表定時間」與「預估實際抵達時間」
"""

import json
import re

INDEX_PATH = "05_Trash_Radar_Engine/index.html"
RECYCLE_JSON_PATH = "05_Trash_Radar_Engine/evidence/recycling_routes.json"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

with open(RECYCLE_JSON_PATH, "r", encoding="utf-8") as f:
    recycle_routes = json.load(f)

print(f"Loaded {len(recycle_routes)} recycling routes.")

# 1. 注入 RECYCLE_ROUTES 到 LOCAL_SEED_ROUTES 之前或合併
# 尋找 LOCAL_SEED_ROUTES 的結尾: const LOCAL_SEED_ROUTES = [ ... ];
# 檢查是否已經有 RECYCLE_ROUTES
if "/* RECYCLING_ROUTES_INJECTED */" not in content:
    # 格式化 recycle_routes 為 JS 陣列
    recycle_js = json.dumps(recycle_routes, ensure_ascii=False, indent=2)
    # 在 LOCAL_SEED_ROUTES 定義後附加
    seed_routes_anchor = "const LOCAL_SEED_ROUTES = ["
    if seed_routes_anchor in content:
        # 我們直接把 recycle_routes 拼接到 LOCAL_SEED_ROUTES 陣列內
        # 找到 LOCAL_SEED_ROUTES 的閉合方括號
        # 更好的方式：定義 const RECYCLING_SEED_ROUTES = ...; 並將 LOCAL_SEED_ROUTES = LOCAL_SEED_ROUTES.concat(RECYCLING_SEED_ROUTES);
        inject_code = f"""
    /* RECYCLING_ROUTES_INJECTED */
    const RECYCLING_SEED_ROUTES = {recycle_js};
    LOCAL_SEED_ROUTES.push(...RECYCLING_SEED_ROUTES);
"""
        # 找到 LOCAL_SEED_ROUTES 之後的第一個函數或變數
        match = re.search(r'(const LOCAL_SEED_ROUTES\s*=\s*\[[\s\S]*?\];)', content)
        if match:
            old_decl = match.group(1)
            new_decl = old_decl + inject_code
            content = content.replace(old_decl, new_decl, 1)
            print("Successfully injected RECYCLING_SEED_ROUTES into LOCAL_SEED_ROUTES!")
        else:
            print("ERROR: Could not find LOCAL_SEED_ROUTES array definition!")
else:
    print("RECYCLING_SEED_ROUTES already present in index.html.")

# 2. 升級 evaluateLiveTruckStatus 回傳值，確保包含 statusText
old_eval_return = """        return {
          status: 'RUNNING',
          label: `🟢 官方即時預估：${est}`,
          badgeBg: '#F0FDF4',
          border: '#86EFAC',
          badgeColor: '#166534',
          dotColor: '#22C55E',
          detail: `📡 中華電信即時班表回傳：此站<strong>${est}</strong>（車號：${livePlate}）`
        };"""

new_eval_return = """        return {
          status: 'RUNNING',
          label: `🟢 官方即時預估：${est}`,
          statusText: est,
          badgeBg: '#F0FDF4',
          border: '#86EFAC',
          badgeColor: '#166534',
          dotColor: '#22C55E',
          detail: `📡 官方車機即時預估：此站<strong>${est}</strong>（車號：${livePlate}）`
        };"""

if old_eval_return in content:
    content = content.replace(old_eval_return, new_eval_return)
    print("Upgraded evaluateLiveTruckStatus RUNNING return object.")

# 另外檢查 evaluateLiveTruckStatus 其他回傳的 statusText
# 包含：'已駛離' -> statusText: '已清運駛離'
# '依官方表定時間' -> statusText: '依表定'
# '離峰未發車' -> statusText: '離峰未發車'
old_departed = """      if (hasVisitedAndDeparted) {
        return {
          status: 'DEPARTED',
          label: '🔴 垃圾車已駛離',
          badgeBg: '#FEF2F2',
          border: '#FECACA',
          badgeColor: '#991B1B',
          dotColor: '#EF4444',
          detail: `車機紀錄顯示該車已完成清運並駛離現場超過 400m。`
        };
      }"""

new_departed = """      if (hasVisitedAndDeparted) {
        return {
          status: 'DEPARTED',
          label: '🔴 垃圾車已駛離',
          statusText: '已清運駛離',
          badgeBg: '#FEF2F2',
          border: '#FECACA',
          badgeColor: '#991B1B',
          dotColor: '#EF4444',
          detail: `車機紀錄顯示該車已完成清運並駛離現場超過 400m。`
        };
      }"""

if old_departed in content:
    content = content.replace(old_departed, new_departed)
    print("Upgraded evaluateLiveTruckStatus DEPARTED return object.")

old_fallback = """      return {
        status: 'SCHEDULED',
        label: '🟡 依官方表定時間',
        badgeBg: '#FFFBEB',
        border: '#FDE68A',
        badgeColor: '#92400E',
        dotColor: '#F59E0B',
        detail: `目前依官方表定時間（${formatMinToTimeStr(stopMin)}）運行，建議提早 3 分鐘出門。`
      };"""

new_fallback = """      return {
        status: 'SCHEDULED',
        label: '🟡 依官方表定時間',
        statusText: '依官方表定',
        badgeBg: '#FFFBEB',
        border: '#FDE68A',
        badgeColor: '#92400E',
        dotColor: '#F59E0B',
        detail: `目前依官方表定時間（${formatMinToTimeStr(stopMin)}）運行，建議提早 3~5 分鐘出門。`
      };"""

if old_fallback in content:
    content = content.replace(old_fallback, new_fallback)
    print("Upgraded evaluateLiveTruckStatus SCHEDULED return object.")

old_offpeak = """        return {
          status: 'OFFPEAK',
          label: '⚪ 離峰時段（未出勤）',
          badgeBg: '#F8FAFC',
          border: '#E2E8F0',
          badgeColor: '#64748B',
          dotColor: '#94A3B8',
          detail: `垃圾車傍晚出勤時段（約 16:30 起）將自動切換為即時 GPS 定位。`
        };"""

new_offpeak = """        return {
          status: 'OFFPEAK',
          label: '⚪ 離峰時段（未出勤）',
          statusText: '離峰未發車',
          badgeBg: '#F8FAFC',
          border: '#E2E8F0',
          badgeColor: '#64748B',
          dotColor: '#94A3B8',
          detail: `垃圾車傍晚出勤時段（約 16:30 起）將自動切換為即時 GPS 定位。`
        };"""

if old_offpeak in content:
    content = content.replace(old_offpeak, new_offpeak)
    print("Upgraded evaluateLiveTruckStatus OFFPEAK return object.")

# 3. 升級 B 項 (挑站前先抓全部今日路線班表 prefetchTodaySchedules) 與 C 項 (雙收路線篩選)
# 尋找 renderRadar 開頭
old_route_loop_start = """      LOCAL_SEED_ROUTES.forEach(route => {
        // 星期出勤防呆：該車次今日若無排班則略過
        if (route.trash_day && !route.trash_day.includes(currentDayChar)) {
          return;
        }

        const runId = (route.route_id || '').replace(/^TT_OFFICIAL_/, '');
        const officialSchedule = (liveRouteSchedules && liveRouteSchedules[runId]) ? liveRouteSchedules[runId] : null;

        route.stops.forEach(stop => {
          // 條目 11.b: 時間一律以當下抓到的官方 stime 為準；estimate 用來顯示「約 X 分到」與「已清運」
          let stopTime = stop.time;
          let isOffline = true;
          let officialEst = "";

          if (officialSchedule && officialSchedule.stops) {
            const offInfo = officialSchedule.stops[stop.name] || officialSchedule.stops[`${Number(stop.lat).toFixed(4)},${Number(stop.lon).toFixed(4)}`] || officialSchedule.stops[`${stop.lat},${stop.lon}`];
            if (offInfo && offInfo.stime) {
              stopTime = offInfo.stime;
              isOffline = false;
              officialEst = offInfo.estimate || "";
            }
          }

          const [sh, sm] = stopTime.split(':').map(Number);
          const stopMin = sh * 60 + sm;
          if (stopMin < todayAllRouteMinStop) todayAllRouteMinStop = stopMin;
          if (stopMin > todayAllRouteMaxStop) todayAllRouteMaxStop = stopMin;

          // 第 10 項：以站點層 recycle_day 判斷今日是否有資源回收
          const stopRecycleDay = stop.recycle_day || route.recycle_day || "無";
          const stopHasRecyclingToday = (stopRecycleDay !== "無" && stopRecycleDay.includes(currentDayChar));
          if (wantRecycle && !stopHasRecyclingToday) {
            return;
          }"""

new_route_loop_start = """      LOCAL_SEED_ROUTES.forEach(route => {
        // 星期出勤防呆：該車次今日若無排班則略過
        const routeDays = route.is_recycling_truck ? (route.recycle_day || route.trash_day) : route.trash_day;
        if (routeDays && !routeDays.includes(currentDayChar)) {
          return;
        }

        // C 項：雙收（資源回收）模式分流
        // 若勾選雙收：優先納入專門回收車路線 (is_recycling_truck) 或站點有回收的路線
        // 若勾選純一般垃圾：排除專門回收車路線 (is_recycling_truck)，只留主力垃圾車
        if (wantRecycle) {
          if (!route.is_recycling_truck && !route.has_recycling) return;
        } else {
          if (route.is_recycling_truck) return;
        }

        const runId = (route.route_id || '').replace(/^TT_OFFICIAL_/, '').replace(/^TT_RECYCLE_/, '');
        const officialSchedule = (liveRouteSchedules && liveRouteSchedules[runId]) ? liveRouteSchedules[runId] : null;

        route.stops.forEach(stop => {
          // 條目 11.b: 時間一律以當下抓到的官方 stime 為準；estimate 用來顯示「約 X 分到」與「已清運」
          let stopTime = stop.time;
          let isOffline = true;
          let officialEst = "";

          if (officialSchedule && officialSchedule.stops) {
            const offInfo = officialSchedule.stops[stop.name] || officialSchedule.stops[`${Number(stop.lat).toFixed(4)},${Number(stop.lon).toFixed(4)}`] || officialSchedule.stops[`${stop.lat},${stop.lon}`];
            if (offInfo && offInfo.stime) {
              stopTime = offInfo.stime;
              isOffline = false;
              officialEst = offInfo.estimate || "";
            }
          }

          const [sh, sm] = stopTime.split(':').map(Number);
          const stopMin = sh * 60 + sm;
          if (stopMin < todayAllRouteMinStop) todayAllRouteMinStop = stopMin;
          if (stopMin > todayAllRouteMaxStop) todayAllRouteMaxStop = stopMin;

          // C 項 & 第 10 項：回收日判斷
          const stopRecycleDay = stop.recycle_day || route.recycle_day || "無";
          const stopHasRecyclingToday = route.is_recycling_truck || (stopRecycleDay !== "無" && stopRecycleDay.includes(currentDayChar));
          if (wantRecycle && !stopHasRecyclingToday) {
            return;
          }"""

if old_route_loop_start in content:
    content = content.replace(old_route_loop_start, new_route_loop_start)
    print("Upgraded route loop with C item (recycling truck specialization).")
else:
    print("WARNING: Could not find old_route_loop_start in content.")

# 4. 注入 B 項 prefetchTodaySchedules 函數與調用
prefetch_code = """
    // B 項：挑站前先抓全部今日出勤路線班表 (全量並行預載)
    let isPrefetchingSchedules = false;
    async function prefetchTodaySchedules() {
      if (isPrefetchingSchedules) return;
      const targetTimeVal = document.getElementById('targetTime').value;
      const [th, tm] = targetTimeVal.split(':').map(Number);
      const targetMin = th * 60 + tm;
      const now = new Date();
      const currentMin = now.getHours() * 60 + now.getMinutes();
      const day = now.getDay();
      if (day === 0 || day === 3) return; // 停收日不抓

      const DAY_CHARS = ["日", "一", "二", "三", "四", "五", "六"];
      const currentDayChar = DAY_CHARS[day];
      const wantRecycle = document.getElementById('wantRecycle').checked;

      // 挑出今日有出勤的路線 runId
      const todayRunIds = [];
      LOCAL_SEED_ROUTES.forEach(r => {
        const routeDays = r.is_recycling_truck ? (r.recycle_day || r.trash_day) : r.trash_day;
        if (routeDays && routeDays.includes(currentDayChar)) {
          if (wantRecycle && !r.is_recycling_truck && !r.has_recycling) return;
          if (!wantRecycle && r.is_recycling_truck) return;
          const rid = (r.route_id || '').replace(/^TT_OFFICIAL_/, '').replace(/^TT_RECYCLE_/, '');
          if (rid && !todayRunIds.includes(rid)) todayRunIds.push(rid);
        }
      });

      const missingRunIds = todayRunIds.filter(rid => !liveRouteSchedules[rid] || (Date.now() - liveRouteSchedules[rid].timestamp >= SCHEDULE_CACHE_TTL));
      if (missingRunIds.length === 0) return;

      isPrefetchingSchedules = true;
      try {
        await Promise.allSettled(missingRunIds.map(rid => fetchRouteSchedule(rid)));
        renderRadar(); // 抓完自動以最新官方班表重新精準演算挑站
      } catch (err) {
        console.warn("prefetchTodaySchedules error:", err);
      } finally {
        isPrefetchingSchedules = false;
      }
    }
"""

if "function prefetchTodaySchedules" not in content:
    # 插入在 renderRadar 之前
    anchor = "function renderRadar() {"
    if anchor in content:
        content = content.replace(anchor, prefetch_code + "\n    " + anchor)
        print("Injected prefetchTodaySchedules function.")

# 5. 更新卡片 1：加入 D 項（提早出門提醒）與 F 項（官方表定時間 ✕ 預估動態抵達並列）
old_card1_header = """              <div class="card-title-row">
                <div>
                  <div style="font-size: 11px; color: #DC2626; font-weight: 800; letter-spacing: 0.5px;">${isIntercept ? '🔥 火速攔截點' : '首選攔截點'}</div>
                  <div class="stop-name" style="font-size: 21px;">${topFastest.name}</div>
                </div>
                <div style="text-align: right; background: #FFF5F5; padding: 6px 12px; border-radius: 12px; border: 1px solid #FECACA;">
                  <div style="font-size: 11px; color: #991B1B; font-weight: 700;">車次表定</div>
                  <div style="font-size: 20px; font-weight: 900; color: #DC2626; line-height: 1.1;">${topFastest.time}</div>
                  ${topFastest.isOffline ? '<div style="font-size: 10px; color: #D97706; font-weight: 700; margin-top: 2px;">⚠️ 離線表定，可能不準</div>' : '<div style="font-size: 10px; color: #059669; font-weight: 700; margin-top: 2px;">🟢 官方最新班表</div>'}
                </div>
              </div>"""

new_card1_header = """              <div class="card-title-row">
                <div>
                  <div style="font-size: 11px; color: #DC2626; font-weight: 800; letter-spacing: 0.5px;">${isIntercept ? '🔥 火速攔截點' : '首選攔截點'}</div>
                  <div class="stop-name" style="font-size: 21px;">${topFastest.name}</div>
                </div>
                <!-- F 項：同時清晰展示「官方表定時間」與「預估實際抵達時間」 -->
                <div style="display: flex; gap: 6px; align-items: stretch;">
                  <div style="text-align: right; background: #FFF5F5; padding: 6px 10px; border-radius: 12px; border: 1px solid #FECACA; min-width: 76px;">
                    <div style="font-size: 10px; color: #991B1B; font-weight: 700;">官方表定</div>
                    <div style="font-size: 18px; font-weight: 900; color: #DC2626; line-height: 1.1;">${topFastest.time}</div>
                    ${topFastest.isOffline ? '<div style="font-size: 9px; color: #D97706; font-weight: 700; margin-top: 2px;">⚠️ 離線預排</div>' : '<div style="font-size: 9px; color: #059669; font-weight: 700; margin-top: 2px;">🟢 官方最新</div>'}
                  </div>
                  <div style="text-align: right; background: #F0FDF4; padding: 6px 10px; border-radius: 12px; border: 1px solid #BBF7D0; min-width: 82px;">
                    <div style="font-size: 10px; color: #166534; font-weight: 700;">預估抵達</div>
                    <div style="font-size: 15px; font-weight: 900; color: #15803D; line-height: 1.2; margin-top: 2px;">${fastestLive.statusText || fastestLive.label}</div>
                  </div>
                </div>
              </div>

              <!-- D 項：提早出門提醒 -->
              <div style="background: #FFFBEB; border: 1px solid #FCD34D; border-radius: 10px; padding: 6px 12px; margin-bottom: 10px; font-size: 12px; color: #92400E; font-weight: 700; display: flex; align-items: center; gap: 6px;">
                <span>⚠️</span>
                <span>垃圾車常因路況提早 3~5 分鐘抵達，強烈建議提早前往候車！</span>
              </div>"""

if old_card1_header in content:
    content = content.replace(old_card1_header, new_card1_header)
    print("Upgraded Card 1 with D item (early warning) & F item (dual time display).")
else:
    print("WARNING: Could not find old_card1_header in content.")

# 6. 更新卡片 2（離家最近）：加入 D 項與 F 項
old_card2_render = """            <div class="card-title-row">
              <div class="stop-name">${topNearest.name}</div>
              ${distanceNoticeHtml}
            </div>"""

new_card2_render = """            <!-- F 項：卡片 2 表定與動態抵達並列 -->
            <div class="card-title-row">
              <div>
                <div class="stop-name">${topNearest.name}</div>
                ${distanceNoticeHtml}
              </div>
              <div style="display: flex; gap: 6px; align-items: stretch;">
                <div style="text-align: right; background: #F8FAFC; padding: 6px 10px; border-radius: 12px; border: 1px solid #E2E8F0; min-width: 76px;">
                  <div style="font-size: 10px; color: #475569; font-weight: 700;">官方表定</div>
                  <div style="font-size: 17px; font-weight: 900; color: #1E293B; line-height: 1.1;">${topNearest.time}</div>
                </div>
                <div style="text-align: right; background: #F0FDF4; padding: 6px 10px; border-radius: 12px; border: 1px solid #BBF7D0; min-width: 82px;">
                  <div style="font-size: 10px; color: #166534; font-weight: 700;">預估抵達</div>
                  <div style="font-size: 14px; font-weight: 900; color: #15803D; line-height: 1.2; margin-top: 2px;">${nearestLive.statusText || nearestLive.label}</div>
                </div>
              </div>
            </div>

            <!-- D 項：提早出門提醒 -->
            <div style="background: #FFFBEB; border: 1px solid #FCD34D; border-radius: 10px; padding: 6px 12px; margin-bottom: 10px; font-size: 12px; color: #92400E; font-weight: 700; display: flex; align-items: center; gap: 6px;">
              <span>⚠️</span>
              <span>垃圾車常因路況提早 3~5 分鐘抵達，強烈建議提早前往候車！</span>
            </div>"""

# 在卡片 2 渲染前計算 nearestLive
nearest_live_calc = """        const nearestLive = evaluateLiveTruckStatus(topNearest.plate, topNearest.lat, topNearest.lon, topNearest.stopMin, topNearest.runId, topNearest.name);
"""
if "const nearestLive =" not in content:
    card2_calc_anchor = "if (topNearest) {\n        topNearest.travelMin = Math.max(1, Math.round(topNearest.dist / profile.speedMpm));"
    if card2_calc_anchor in content:
        content = content.replace(card2_calc_anchor, card2_calc_anchor + "\n" + nearest_live_calc)
        print("Added nearestLive evaluation calculation.")

if old_card2_render in content:
    content = content.replace(old_card2_render, new_card2_render)
    print("Upgraded Card 2 with D item & F item.")
else:
    print("WARNING: Could not find old_card2_render in content.")

# 7. 在 initTimeInput 與 targetTime/wantRecycle 監聽器加入 prefetchTodaySchedules
time_change_anchor = "document.getElementById('targetTime').addEventListener('change', () => { renderRadar(); });"
new_time_change = "document.getElementById('targetTime').addEventListener('change', () => { prefetchTodaySchedules(); renderRadar(); });"
if time_change_anchor in content:
    content = content.replace(time_change_anchor, new_time_change)

recycle_change_anchor = "document.getElementById('wantRecycle').addEventListener('change', () => { renderRadar(); });"
new_recycle_change = "document.getElementById('wantRecycle').addEventListener('change', () => { prefetchTodaySchedules(); renderRadar(); });"
if recycle_change_anchor in content:
    content = content.replace(recycle_change_anchor, new_recycle_change)

init_call_anchor = "initTimeInput();\n    renderRadar();"
new_init_call = "initTimeInput();\n    prefetchTodaySchedules();\n    renderRadar();"
if init_call_anchor in content:
    content = content.replace(init_call_anchor, new_init_call)
    print("Connected prefetchTodaySchedules to init and change events.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully updated {INDEX_PATH} with all Round 3 requirements!")
