# -*- coding: utf-8 -*-
"""
apply_founder_radar_rules.py
落實創辦人品碩親傳之兩大核心實戰規則：
1. 最快卡片：先抓離客人定位最近的實際 GPS 車輛，再判定其前方未過站點
2. 絕對不提供已過站（已清運/已駛離/時間已過）的站點給客人
"""

import re

INDEX_PATH = "05_Trash_Radar_Engine/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 尋找 renderRadar 中遍歷站點的區塊
# 我們要在遍歷站點時精準計算 isPassed
old_stop_push_block = """          const dist = haversine(currentLat, currentLon, stop.lat, stop.lon);
          const travelMin = Math.max(1, Math.round(dist / profile.speedMpm));
          const userArrivalMin = targetMinutes + travelMin;
          
          const canCatch = (userArrivalMin <= stopMin + 1);
          const totalTaskMinutes = Math.max(travelMin, stopMin - targetMinutes);
          const waitAtStopMin = Math.max(0, stopMin - userArrivalMin);

          allStops.push({
            routeId: route.route_id,
            runId: runId,
            routeName: route.route_name,
            plate: route.truck_plate,
            hasRecycling: stopHasRecyclingToday,
            recycleDay: stopRecycleDay,
            name: stop.name,
            lat: stop.lat,
            lon: stop.lon,
            time: stopTime,
            rawSeedTime: stop.time,
            isOffline: isOffline,
            officialEst: officialEst,
            stopMin: stopMin,
            dist: dist,
            travelMin: travelMin,
            userArrivalMin: userArrivalMin,
            canCatch: canCatch,
            totalTaskMinutes: totalTaskMinutes,
            waitAtStopMin: waitAtStopMin,
            notes: stop.notes
          });"""

new_stop_push_block = """          const dist = haversine(currentLat, currentLon, stop.lat, stop.lon);
          const travelMin = Math.max(1, Math.round(dist / profile.speedMpm));
          const userArrivalMin = targetMinutes + travelMin;

          // 核心規則 2【絕對過站硬性判定】：已清運、已駛離、或時間已過的站點，標記 isPassed=true 絕不提供給客人！
          let isPassed = false;
          if (officialEst === "已清運" || officialEst.includes("已駛離") || officialEst.includes("已離開")) {
            isPassed = true;
          }

          const normPlate = normalizePlate(route.truck_plate);
          const normRoute = normalizePlate(route.route_name);
          const truckObj = (liveTrucksCache && (liveTrucksCache[normPlate] || liveTrucksCache[normRoute] || liveTrucksCache[route.truck_plate])) || null;

          if (truckObj && truckObj.visitedStops) {
            const stopKey = makeStopKey(stop.lat, stop.lon);
            if (truckObj.visitedStops[stopKey] && haversine(truckObj.lat, truckObj.lon, stop.lat, stop.lon) > 400) {
              isPassed = true;
            }
          }

          // 若為離線模式或未出勤時段，若表定時間已過客人出發時間，視為已過站
          if (isOffline && stopMin < targetMinutes) {
            isPassed = true;
          }

          // 判定客人是否能趕上（必須未過站，且抵達時間及時）
          let canCatch = (!isPassed && userArrivalMin <= stopMin + 1);
          if (officialEst && officialEst.includes("分到")) {
            const estMinMatch = officialEst.match(/約(\d+)分到/);
            if (estMinMatch) {
              const liveMinArrival = targetMinutes + parseInt(estMinMatch[1], 10);
              canCatch = (!isPassed && userArrivalMin <= liveMinArrival + 1);
            }
          } else if (officialEst === "已抵達") {
            // 已在現場，客人必須出發時間剛好就在當下且步行極短 (1~2分鐘內)
            canCatch = (!isPassed && travelMin <= 2);
          }

          const totalTaskMinutes = Math.max(travelMin, stopMin - targetMinutes);
          const waitAtStopMin = Math.max(0, stopMin - userArrivalMin);

          allStops.push({
            routeId: route.route_id,
            runId: runId,
            routeName: route.route_name,
            plate: route.truck_plate,
            hasRecycling: stopHasRecyclingToday,
            recycleDay: stopRecycleDay,
            name: stop.name,
            lat: stop.lat,
            lon: stop.lon,
            time: stopTime,
            rawSeedTime: stop.time,
            isOffline: isOffline,
            officialEst: officialEst,
            isPassed: isPassed,
            stopMin: stopMin,
            dist: dist,
            travelMin: travelMin,
            userArrivalMin: userArrivalMin,
            canCatch: canCatch,
            totalTaskMinutes: totalTaskMinutes,
            waitAtStopMin: waitAtStopMin,
            notes: stop.notes
          });"""

if old_stop_push_block in content:
    content = content.replace(old_stop_push_block, new_stop_push_block)
    print("Injected isPassed and canCatch logic into stop iteration.")
else:
    print("WARNING: Could not find old_stop_push_block!")

# 尋找挑選候選站點與 topFastest / topNearest 的區塊
old_selection_block = """      // 第 5 項：卡片 2「離家最近」只從「表定時間 ≥ 出門時間」的站點裡挑最近的
      const upcomingStopsByDist = allStops
        .filter(s => s.stopMin >= targetMinutes)
        .sort((a, b) => a.dist - b.dist || a.stopMin - b.stopMin);
      const topNearest = upcomingStopsByDist[0] || null;
      if (topNearest) {
        topNearest.walkingMin = Math.max(1, Math.round(topNearest.dist / TRAVEL_PROFILES.walking.speedMpm));
      }

      // 判定家門口最近班次是否已經開走
      const isLocalShiftMissed = Boolean(nearestAnyTime && nearestAnyTime.stopMin < targetMinutes);

      let topFastest = null;
      let shiftState = 'LIVE'; // LIVE | INTERCEPT | NIGHT_CLOSED | DAY_PREVIEW

      // 嚴格篩選：客人出發後「交通工具趕得上」且在 60 分鐘內可完成任務的站點
      const catchableCandidates = allStops.filter(s => s.canCatch && s.totalTaskMinutes >= 0 && s.totalTaskMinutes <= 60);
      
      if (catchableCandidates.length > 0) {
        // 常民生活第一性原理：以 3 分鐘為時空等價區間，區間內離家近者絕對優先！
        catchableCandidates.sort((a, b) => (Math.floor(a.totalTaskMinutes / 3) - Math.floor(b.totalTaskMinutes / 3)) || (a.dist - b.dist));
        topFastest = catchableCandidates[0];
        shiftState = isLocalShiftMissed ? 'INTERCEPT' : 'LIVE';
      } else {
        // 第 3 項：門檻改為「今天有出勤路線的最晚站點時間 (maxStopMin)」
        const allNightShiftsPast = allStops.length === 0 || allStops.every(s => s.stopMin < targetMinutes);
        if (targetMinutes > maxStopMin || allNightShiftsPast) {
          shiftState = 'NIGHT_CLOSED';
        } else {
          // 白天或距離下一班超過 60 分鐘時段，顯示最近即將發車預報
          const earliestCandidates = [...allStops]
            .filter(s => s.stopMin >= targetMinutes)
            .sort((a, b) => a.stopMin - b.stopMin || a.dist - b.dist);
          topFastest = earliestCandidates[0] || allStopsByDist[0];
          shiftState = 'DAY_PREVIEW';
        }
      }"""

new_selection_block = """      // 核心規則 2：卡片 2「離家最近」嚴格排除已過站 (!s.isPassed)，只從「尚未過站且表定時間 ≥ 出門時間」挑最近的
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

      // 核心規則 1【以實際 GPS 垃圾車距離為核心導向的最快推薦】：
      // 先找出目前在路上跑、距離客人最近的執勤中垃圾車，再判定該車前方客人趕得上的停靠點！
      const liveTruckList = [];
      const seenTruckKeys = new Set();
      if (liveTrucksCache) {
        Object.values(liveTrucksCache).forEach(t => {
          if (t && !isNaN(t.lat) && !isNaN(t.lon) && t.status !== "未執勤" && (t.speed > 0 || t.status === "執勤中")) {
            const k = normalizePlate(t.car_no || t.name);
            if (!seenTruckKeys.has(k)) {
              seenTruckKeys.add(k);
              const distToUser = haversine(currentLat, currentLon, t.lat, t.lon);
              liveTruckList.push({
                ...t,
                normKey: k,
                distToUser
              });
            }
          }
        });
      }
      liveTruckList.sort((a, b) => a.distToUser - b.distToUser);

      // 優先從距離客人最近的在線垃圾車路線中，挑選其前方未過站點
      if (liveTruckList.length > 0) {
        for (const truck of liveTruckList) {
          const candidateStopsOfTruck = allStops.filter(s => 
            !s.isPassed && 
            s.canCatch && 
            (normalizePlate(s.plate) === truck.normKey || normalizePlate(s.routeName) === truck.normKey || (s.runId && s.runId === truck.run_id))
          );
          
          if (candidateStopsOfTruck.length > 0) {
            // 從這台最近垃圾車的前方站點中，挑選客人完成任務最快/離客人最近的站點
            candidateStopsOfTruck.sort((a, b) => a.totalTaskMinutes - b.totalTaskMinutes || a.dist - b.dist);
            topFastest = candidateStopsOfTruck[0];
            topFastest.matchedLiveTruck = truck; // 綁定最近車機資訊
            shiftState = isLocalShiftMissed ? 'INTERCEPT' : 'LIVE';
            break;
          }
        }
      }

      // 若在線車輛均無可趕上之前方站點，或處於離峰未發車時段，回退至全體未過站點候選
      if (!topFastest) {
        // 嚴格過濾：必須未過站 (!s.isPassed) 且客人交通工具趕得上 (s.canCatch)
        const unpassedCatchable = allStops.filter(s => !s.isPassed && s.canCatch && s.totalTaskMinutes >= 0 && s.totalTaskMinutes <= 60);
        
        if (unpassedCatchable.length > 0) {
          unpassedCatchable.sort((a, b) => (Math.floor(a.totalTaskMinutes / 3) - Math.floor(b.totalTaskMinutes / 3)) || (a.dist - b.dist));
          topFastest = unpassedCatchable[0];
          shiftState = isLocalShiftMissed ? 'INTERCEPT' : 'LIVE';
        } else {
          // 第 3 項：門檻改為「今天有出勤路線的最晚站點時間 (maxStopMin)」
          const allNightShiftsPast = allStops.length === 0 || allStops.every(s => s.isPassed || s.stopMin < targetMinutes);
          if (targetMinutes > maxStopMin || allNightShiftsPast) {
            shiftState = 'NIGHT_CLOSED';
          } else {
            // 白天或距離下一班超過 60 分鐘時段，顯示最近即將發車預報 (嚴格排除已過站)
            const earliestUpcoming = allStops
              .filter(s => !s.isPassed && s.stopMin >= targetMinutes)
              .sort((a, b) => a.stopMin - b.stopMin || a.dist - b.dist);
            topFastest = earliestUpcoming[0] || null;
            shiftState = topFastest ? 'DAY_PREVIEW' : 'NIGHT_CLOSED';
          }
        }
      }"""

if old_selection_block in content:
    content = content.replace(old_selection_block, new_selection_block)
    print("Injected Founder's GPS-First and Anti-Passed-Stop selection logic.")
else:
    print("WARNING: Could not find old_selection_block!")

# 注入卡片 1 上顯示鎖定實際 GPS 車輛的微動態標籤
card1_target_anchor = """              <!-- D 項：提早出門提醒 -->
              <div style="background: #FFFBEB; border: 1px solid #FCD34D; border-radius: 10px; padding: 6px 12px; margin-bottom: 10px; font-size: 12px; color: #92400E; font-weight: 700; display: flex; align-items: center; gap: 6px;">
                <span>⚠️</span>
                <span>垃圾車常因路況提早 3~5 分鐘抵達，強烈建議提早前往候車！</span>
              </div>"""

card1_replacement = """              ${topFastest.matchedLiveTruck ? `
                <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 10px; padding: 6px 12px; margin-bottom: 10px; font-size: 12px; color: #1E40AF; font-weight: 700; display: flex; align-items: center; gap: 6px;">
                  <span>🛰️</span>
                  <span>雷達已鎖定離您最近垃圾車：<strong>${topFastest.plate}</strong>（目前距您約 <strong>${topFastest.matchedLiveTruck.distToUser}m</strong>，時速 ${Math.round(topFastest.matchedLiveTruck.speed || 0)} km/h）</span>
                </div>
              ` : ''}

              <!-- D 項：提早出門提醒 -->
              <div style="background: #FFFBEB; border: 1px solid #FCD34D; border-radius: 10px; padding: 6px 12px; margin-bottom: 10px; font-size: 12px; color: #92400E; font-weight: 700; display: flex; align-items: center; gap: 6px;">
                <span>⚠️</span>
                <span>垃圾車常因路況提早 3~5 分鐘抵達，強烈建議提早前往候車！</span>
              </div>"""

if card1_target_anchor in content:
    content = content.replace(card1_target_anchor, card1_replacement, 1)
    print("Injected matchedLiveTruck radar banner in Card 1.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated index.html with Founder's Round 4 rules!")
