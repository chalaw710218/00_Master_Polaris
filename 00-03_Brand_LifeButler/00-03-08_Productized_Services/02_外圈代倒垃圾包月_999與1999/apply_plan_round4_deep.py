# -*- coding: utf-8 -*-
"""
apply_plan_round4_deep.py
嚴格落實品碩親傳之四大軍規級指令：
1. 【前置問題】清查修正回收車 1618 車號為 109-UL，並在前端以 run_id 雙向強制綁定車機 GPS
2. 【最快卡片：從車出發找站】抓出所有出勤車輛 GPS，只看未過站，算雙向時間，只留客人先到的站，以「最早攔得到」為準
3. 【所有卡片不得推薦已過站點】落實三級嚴格判定（官方已清運 > 站序軌跡 > 15分鐘防提早安全門禁）
4. 【卡片2離家最近嚴格過濾】未過站且非已清運
"""

import json
import re

INDEX_PATH = "05_Trash_Radar_Engine/index.html"
RECYCLE_JSON_PATH = "05_Trash_Radar_Engine/evidence/recycling_routes.json"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# -------------------------------------------------------------------------
# 1. 前置問題：修正 1618 回收車 truck_plate 為 109-UL
# -------------------------------------------------------------------------
# 修正 recycling_routes.json
with open(RECYCLE_JSON_PATH, "r", encoding="utf-8") as f:
    rec_routes = json.load(f)

for r in rec_routes:
    if r.get("run_id") == "1618":
        r["truck_plate"] = "109-UL"
        print("Updated 1618 truck_plate to 109-UL in recycling_routes.json")

with open(RECYCLE_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(rec_routes, f, ensure_ascii=False, indent=2)

# 同步修正 index.html 中的 RECYCLING_SEED_ROUTES
html = re.sub(
    r'("route_id":\s*"TT_RECYCLE_1618",\s*"run_id":\s*"1618",\s*"route_name":\s*"回KEH-5218\(一、五\)",\s*"truck_plate":\s*")[^"]+(")',
    r'\g<1>109-UL\g<2>',
    html
)
print("Updated 1618 truck_plate in index.html to 109-UL.")

# -------------------------------------------------------------------------
# 2. 升級 fetchLiveTruckLocations：以 run_id 和車號雙向綁定車機快取
# -------------------------------------------------------------------------
old_cache_store = """              if (normCar) nextCache[normCar] = record;
              if (normRoute) nextCache[normRoute] = record;
              if (rawCarNo) nextCache[rawCarNo] = record;
              if (rawRouteName) nextCache[rawRouteName] = record;"""

new_cache_store = """              if (normCar) nextCache[normCar] = record;
              if (normRoute) nextCache[normRoute] = record;
              if (rawCarNo) nextCache[rawCarNo] = record;
              if (rawRouteName) nextCache[rawRouteName] = record;
              if (runId) {
                nextCache[runId] = record;
                nextCache['RUN_' + runId] = record;
              }"""

if old_cache_store in html:
    html = html.replace(old_cache_store, new_cache_store)
    print("Upgraded fetchLiveTruckLocations cache keys with run_id.")
else:
    print("Notice: old_cache_store might have already been updated.")

# -------------------------------------------------------------------------
# 3. 升級 getLiveTruckForRoute 輔助函數
# -------------------------------------------------------------------------
truck_finder_func = """
    // 依路線資訊（優先 runId，次以車號或路線名）精確查找當前車機
    function getLiveTruckForRoute(route) {
      if (!liveTrucksCache) return null;
      const runId = (route.run_id || (route.route_id || '').replace(/^TT_OFFICIAL_/, '').replace(/^TT_RECYCLE_/, ''));
      if (runId && (liveTrucksCache[runId] || liveTrucksCache['RUN_' + runId])) {
        return liveTrucksCache[runId] || liveTrucksCache['RUN_' + runId];
      }
      const normPlate = normalizePlate(route.truck_plate);
      const normRoute = normalizePlate(route.route_name);
      return liveTrucksCache[normPlate] || liveTrucksCache[normRoute] || liveTrucksCache[route.truck_plate] || null;
    }
"""

if "function getLiveTruckForRoute" not in html:
    html = html.replace("function evaluateLiveTruckStatus", truck_finder_func + "\n    function evaluateLiveTruckStatus")
    print("Injected getLiveTruckForRoute helper.")

# -------------------------------------------------------------------------
# 4. 重構 renderRadar：
#    - 三級嚴格判定過站 (官方已清運 > 站序軌跡 > 15分鐘防提早門禁)
#    - 最快卡片：從車出發找站，只看未過站，只留客人先到的站，以「最早攔得到」為準
#    - 卡片2離家最近：嚴格排除已過站
# -------------------------------------------------------------------------

# 替換 renderRadar 運算主體
# 尋找從 let allStops = []; 開始到 cardsContainer.innerHTML 渲染卡片前
old_radar_calc_pattern = re.compile(
    r'(// 2\. 非停收日空間演算計算[\s\S]*?)(// 4\. 渲染 卡片 1：最快抵達)',
    re.MULTILINE
)

new_radar_calc_block = """// 2. 非停收日空間演算計算：落實創辦人親傳實戰演算法
      let allStops = [];
      let todayAllRouteMinStop = Infinity;
      let todayAllRouteMaxStop = -Infinity;
      const DAY_CHARS = ["日", "一", "二", "三", "四", "五", "六"];
      const currentDayChar = DAY_CHARS[day];

      const activeRoutes = wantRecycle ? LOCAL_SEED_ROUTES.concat(RECYCLING_SEED_ROUTES) : LOCAL_SEED_ROUTES;

      // 預處理：遍歷路線與官方班表，標記每條路線當前已清運的最新站序 (latestClearedIndex)
      activeRoutes.forEach(route => {
        const routeDays = route.is_recycling_truck ? (route.recycle_day || route.trash_day) : route.trash_day;
        if (routeDays && !routeDays.includes(currentDayChar)) return;

        if (wantRecycle) {
          if (!route.is_recycling_truck && !route.has_recycling) return;
        } else {
          if (route.is_recycling_truck) return;
        }

        const runId = (route.run_id || (route.route_id || '').replace(/^TT_OFFICIAL_/, '').replace(/^TT_RECYCLE_/, ''));
        const officialSchedule = (liveRouteSchedules && liveRouteSchedules[runId]) ? liveRouteSchedules[runId] : null;
        const liveTruck = getLiveTruckForRoute(route);

        // (2) 站序過站判定：找出這條路線目前已過站的最大站序索引
        let latestPassedIdx = -1;
        if (officialSchedule && officialSchedule.stops) {
          route.stops.forEach((st, idx) => {
            const offInfo = officialSchedule.stops[st.name] || officialSchedule.stops[`${Number(st.lat).toFixed(4)},${Number(st.lon).toFixed(4)}`] || officialSchedule.stops[`${st.lat},${st.lon}`];
            if (offInfo && offInfo.estimate && (offInfo.estimate.includes("已清運") || offInfo.estimate.includes("已駛離") || offInfo.estimate.includes("已離開"))) {
              if (idx > latestPassedIdx) latestPassedIdx = idx;
            }
          });
        }

        // 若車機 GPS 在路上，且曾進入某站點 120m 內且駛離 > 400m
        if (liveTruck && liveTruck.visitedStops) {
          route.stops.forEach((st, idx) => {
            const stopKey = makeStopKey(st.lat, st.lon);
            if (liveTruck.visitedStops[stopKey] && haversine(liveTruck.lat, liveTruck.lon, st.lat, st.lon) > 400) {
              if (idx > latestPassedIdx) latestPassedIdx = idx;
            }
          });
        }

        route.stops.forEach((stop, stopIdx) => {
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

          // 資源回收日嚴格判定
          let stopRecycleDay = stop.recycle_day || route.recycle_day || '無';
          const matchRecycleTag = stop.name.match(/\\(週([一二三四五六日、. ]+)回收車\\)/);
          if (matchRecycleTag) {
            stopRecycleDay = matchRecycleTag[1];
          }
          const stopHasRecyclingToday = (stopRecycleDay !== '無' && stopRecycleDay.includes(currentDayChar));
          if (wantRecycle && !stopHasRecyclingToday) {
            return;
          }

          const dist = haversine(currentLat, currentLon, stop.lat, stop.lon);
          const travelMin = Math.max(1, Math.round(dist / profile.speedMpm));
          const userArrivalMin = targetMinutes + travelMin;

          // =========================================================================
          // 【2｜所有卡片都不能推薦已過站的點】三級嚴格依可靠度排序判定
          // =========================================================================
          let isPassed = false;
          let isEarlyWarning = false; // 防提早安全門禁

          // (1) 官方 estimate 顯示「已清運」→ 已過站
          if (officialEst.includes("已清運") || officialEst.includes("已駛離") || officialEst.includes("已離開")) {
            isPassed = true;
          }

          // (2) 車的 GPS 位置已經過了這一站（依路線站序 latestPassedIdx）→ 已過站
          if (stopIdx <= latestPassedIdx) {
            isPassed = true;
          }

          // (3) 以上都拿不到時，不能只看表定時間 (11/16 實測車提早 14 分鐘)
          // 表定時間在現在起 15 分鐘內的站，要標「車可能已提早經過」，不得當首選！
          const isTruckOnDuty = Boolean(liveTruck && liveTruck.status !== '未執勤');
          if (!isPassed && !isTruckOnDuty) {
            if (stopMin < targetMinutes) {
              isPassed = true; // 時間已過
            } else if (stopMin <= targetMinutes + 15) {
              isEarlyWarning = true; // 15 分鐘內可能已提早經過
            }
          }

          // 每一站計算：車預估幾點到 (truckEtaMin)
          let truckEtaMin = stopMin;
          if (officialEst && officialEst.includes("分到")) {
            const m = officialEst.match(/約(\\d+)分到/);
            if (m) {
              truckEtaMin = targetMinutes + parseInt(m[1], 10);
            }
          } else if (officialEst === "已抵達") {
            truckEtaMin = targetMinutes;
          }

          // 只保留「客人能比車先到」的站
          const canCatch = (!isPassed && userArrivalMin <= truckEtaMin);
          const totalTaskMinutes = Math.max(travelMin, truckEtaMin - targetMinutes);
          const waitAtStopMin = Math.max(0, truckEtaMin - userArrivalMin);

          allStops.push({
            routeId: route.route_id,
            runId: runId,
            routeName: route.route_name,
            plate: (liveTruck && liveTruck.car_no) ? liveTruck.car_no : route.truck_plate,
            hasRecycling: stopHasRecyclingToday,
            recycleDay: stopRecycleDay,
            name: stop.name,
            stopIdx: stopIdx,
            lat: stop.lat,
            lon: stop.lon,
            time: stopTime,
            rawSeedTime: stop.time,
            isOffline: isOffline,
            officialEst: officialEst,
            isPassed: isPassed,
            isEarlyWarning: isEarlyWarning,
            stopMin: stopMin,
            truckEtaMin: truckEtaMin,
            dist: dist,
            travelMin: travelMin,
            userArrivalMin: userArrivalMin,
            canCatch: canCatch,
            totalTaskMinutes: totalTaskMinutes,
            waitAtStopMin: waitAtStopMin,
            liveTruck: liveTruck,
            notes: stop.notes
          });
        });
      });

      // 今日最晚與最早站點時間
      const minStopMin = allStops.length > 0 ? Math.min(...allStops.map(s => s.stopMin)) : (todayAllRouteMinStop !== Infinity ? todayAllRouteMinStop : 930);
      const maxStopMin = allStops.length > 0 ? Math.max(...allStops.map(s => s.stopMin)) : (todayAllRouteMaxStop !== -Infinity ? todayAllRouteMaxStop : 1280);
      const earliestTimeStr = formatMinToTimeStr(minStopMin);
      const latestTimeStr = formatMinToTimeStr(maxStopMin);

      // 全日離家最近站點 (僅用於判定家門口原班次是否已過)
      const allStopsByDist = [...allStops].sort((a, b) => a.dist - b.dist || a.stopMin - b.stopMin);
      const nearestAnyTime = allStopsByDist[0] || null;

      // =========================================================================
      // 【2｜卡片 2 離家最近】：嚴格排除已過站 (!s.isPassed)，只從「未過站且表定時間 ≥ 出門時間」挑最近的
      // =========================================================================
      const upcomingStopsByDist = allStops
        .filter(s => !s.isPassed && s.stopMin >= targetMinutes)
        .sort((a, b) => a.dist - b.dist || a.stopMin - b.stopMin);
      const topNearest = upcomingStopsByDist[0] || null;
      if (topNearest) {
        topNearest.walkingMin = Math.max(1, Math.round(topNearest.dist / TRAVEL_PROFILES.walking.speedMpm));
      }

      // 判定家門口最近班次是否已經開走
      const isLocalShiftMissed = Boolean(nearestAnyTime && (nearestAnyTime.isPassed || nearestAnyTime.stopMin < targetMinutes));

      let topFastest = null;
      let shiftState = 'LIVE'; // LIVE | INTERCEPT | NIGHT_CLOSED | DAY_PREVIEW

      // =========================================================================
      // 【1｜「最快」卡片：從車出發找站】
      // 1. 抓出現在所有正在出勤的車的實際 GPS 位置（垃圾車與回收車都要）。
      // 2. 每一台車只看它還沒經過的站 (!s.isPassed)。
      // 3. 每一站計算：車預估幾點到、客人從定位點出發幾點到。
      // 4. 只保留「客人能比車先到」的站 (s.canCatch: userArrivalMin <= truckEtaMin)。
      // 5. 從中選出客人最早完成倒垃圾 (truckEtaMin 最早，以「最早攔得到」為準)！
      // =========================================================================
      const liveTruckCandidates = [];
      const seenTruckRuns = new Set();
      if (liveTrucksCache) {
        Object.values(liveTrucksCache).forEach(t => {
          if (t && !isNaN(t.lat) && !isNaN(t.lon) && t.status !== "未執勤" && (t.speed > 0 || t.status === "執勤中")) {
            const runKey = t.run_id || t.car_no || t.name;
            if (!seenTruckRuns.has(runKey)) {
              seenTruckRuns.add(runKey);
              liveTruckCandidates.push(t);
            }
          }
        });
      }

      let bestFromTrucks = [];
      if (liveTruckCandidates.length > 0) {
        // 從所有出勤車輛的所有未過站點中，找出「客人能比車先到」的站
        allStops.forEach(s => {
          if (s.liveTruck && !s.isPassed && s.canCatch && s.totalTaskMinutes >= 0 && s.totalTaskMinutes <= 60) {
            bestFromTrucks.push(s);
          }
        });

        if (bestFromTrucks.length > 0) {
          // 以「最早攔得到（truckEtaMin 最小）」為準！若到站時間相同，選客人路程最近者
          bestFromTrucks.sort((a, b) => a.truckEtaMin - b.truckEtaMin || a.dist - b.dist);
          topFastest = bestFromTrucks[0];
          shiftState = isLocalShiftMissed ? 'INTERCEPT' : 'LIVE';
        }
      }

      // 若在線車輛均無可攔到站點，或處於離峰未發車時段，回退至未過站候選池中挑選
      if (!topFastest) {
        // 嚴格排除已過站 (!s.isPassed) 與防提早安全門禁 (!s.isEarlyWarning，不能當首選)
        const unpassedCatchable = allStops.filter(s => 
          !s.isPassed && 
          !s.isEarlyWarning && 
          s.canCatch && 
          s.totalTaskMinutes >= 0 && 
          s.totalTaskMinutes <= 60
        );

        if (unpassedCatchable.length > 0) {
          unpassedCatchable.sort((a, b) => (Math.floor(a.totalTaskMinutes / 3) - Math.floor(b.totalTaskMinutes / 3)) || (a.dist - b.dist));
          topFastest = unpassedCatchable[0];
          shiftState = isLocalShiftMissed ? 'INTERCEPT' : 'LIVE';
        } else {
          // 判定是否收工或白天離峰預報
          const allNightShiftsPast = allStops.length === 0 || allStops.every(s => s.isPassed || s.stopMin < targetMinutes);
          if (targetMinutes > maxStopMin || allNightShiftsPast) {
            shiftState = 'NIGHT_CLOSED';
          } else {
            // 白天或距離下一班超過 60 分鐘時段，顯示最近即將發車預報 (嚴格排除已過站)
            const earliestUpcoming = allStops
              .filter(s => !s.isPassed && !s.isEarlyWarning && s.stopMin >= targetMinutes)
              .sort((a, b) => a.stopMin - b.stopMin || a.dist - b.dist);
            topFastest = earliestUpcoming[0] || null;
            shiftState = topFastest ? 'DAY_PREVIEW' : 'NIGHT_CLOSED';
          }
        }
      }

      """

match = old_radar_calc_pattern.search(html)
if match:
    html = html[:match.start(1)] + new_radar_calc_block + html[match.end(1):]
    print("Replaced renderRadar core calculation block with Founder's Round 4 Deep Engine!")
else:
    print("ERROR: Could not find old_radar_calc_pattern in index.html!")

# -------------------------------------------------------------------------
# 5. 卡片 1 界面增強：顯示即時攔截鎖定與「車可能已提早經過」警示標籤
# -------------------------------------------------------------------------
# 檢查是否有 isEarlyWarning 提示與 matchedLiveTruck 提示
card1_early_warning_ui = """
              ${topFastest.isEarlyWarning ? `
                <div style="background: #FEF3C7; border: 1px solid #FCD34D; border-radius: 10px; padding: 6px 12px; margin-bottom: 10px; font-size: 12px; color: #92400E; font-weight: 700; display: flex; align-items: center; gap: 6px;">
                  <span>⚠️</span>
                  <span><strong>安全門禁提示：</strong> 此班表定在 15 分鐘內，清潔隊車輛常有大幅提早經過可能，建議從容前往後續班次！</span>
                </div>
              ` : ''}

              ${topFastest.liveTruck ? `
                <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 6px 12px; margin-bottom: 10px; font-size: 12px; color: #1E40AF; font-weight: 700; display: flex; align-items: center; gap: 6px;">
                  <span>🛰️</span>
                  <span>雷達已鎖定執勤車號：<strong>${topFastest.plate}</strong>（即時車距約 <strong>${haversine(currentLat, currentLon, topFastest.liveTruck.lat, topFastest.liveTruck.lon)}m</strong>，時速 ${Math.round(topFastest.liveTruck.speed || 0)} km/h）</span>
                </div>
              ` : ''}
"""

# 檢查 index.html 中是否需要替換卡片 1 頂部提示
if "${topFastest.isEarlyWarning ?" not in html:
    html = html.replace(
        "<!-- D 項：提早出門提醒 -->",
        card1_early_warning_ui + "\n              <!-- D 項：提早出門提醒 -->"
    )
    print("Injected isEarlyWarning and liveTruck banner to Card 1.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully written all updates to index.html!")
