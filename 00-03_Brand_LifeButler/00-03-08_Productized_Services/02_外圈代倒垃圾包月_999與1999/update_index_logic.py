import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(SCRIPT_DIR, "05_Trash_Radar_Engine")
HTML_PATH = os.path.join(ENGINE_DIR, "index.html")
SEED_PATH = os.path.join(ENGINE_DIR, "taitung_trash_routes_seed.json")

# 1. 讀取種子路線
with open(SEED_PATH, "r", encoding="utf-8") as f:
    seed_data = json.load(f)

routes_js_lines = ["    const LOCAL_SEED_ROUTES = ["]
for r in seed_data["routes"]:
    routes_js_lines.append("      {")
    routes_js_lines.append(f'        route_name: "{r["route_name"]}", truck_plate: "{r["truck_plate"]}", has_recycling: {str(r["has_recycling"]).lower()},')
    routes_js_lines.append("        stops: [")
    for s in r["stops"]:
        time_val = s.get("scheduled_time") or s.get("time")
        note_val = s.get("notes", "")
        routes_js_lines.append(f'          {{ name: "{s["name"]}", lat: {s["lat"]}, lon: {s["lon"]}, time: "{time_val}", notes: "{note_val}" }},')
    routes_js_lines.append("        ]")
    routes_js_lines.append("      },")
routes_js_lines.append("    ];")
new_routes_js = "\n".join(routes_js_lines)

# 2. 定義升級版 renderRadar 函式
new_render_radar_js = '''    function renderRadar() {
      const now = new Date();
      const day = now.getDay(); // 0 is Sunday, 3 is Wednesday
      const isOffDay = (day === 0 || day === 3); // 台東在地：週日與週三例休！

      const alertContainer = document.getElementById('alertContainer');
      const cardsContainer = document.getElementById('cardsContainer');
      cardsContainer.innerHTML = '';
      alertContainer.innerHTML = '';

      // 1. 戴明安燈防呆：台東在地週三與週日停收通知
      if (isOffDay) {
        alertContainer.innerHTML = `
          <div class="alert-banner alert-danger">
            <span style="font-size: 20px;">🚫</span>
            <div>
              <strong>今日台東市清潔隊例行停收！</strong><br>
              台東固定每週三與週日全縣停收垃圾。今晚無夜間垃圾車，請勿將垃圾堆置門外以免受罰！
            </div>
          </div>
        `;
      }

      // 2. 空間演算計算：依據客人輸入的倒垃圾目標時間、資源回收需求與出門交通工具
      const timeInput = document.getElementById('trashTimeInput');
      const targetTimeStr = (timeInput && timeInput.value) ? timeInput.value : "17:15";
      const [th, tm] = targetTimeStr.split(':').map(Number);
      const targetMinutes = th * 60 + tm;
      const wantRecycle = document.getElementById('recycleCheckbox') ? document.getElementById('recycleCheckbox').checked : false;
      const profile = TRAVEL_PROFILES[currentTravelMode] || TRAVEL_PROFILES.scooter;

      let allStops = [];
      LOCAL_SEED_ROUTES.forEach(route => {
        // 創辦人指示：若勾選「資源回收」，強制只挑選具備【垃圾+回收雙收】的車次！
        if (wantRecycle && !route.has_recycling) {
          return;
        }
        route.stops.forEach(stop => {
          const dist = haversine(currentLat, currentLon, stop.lat, stop.lon);
          const [sh, sm] = stop.time.split(':').map(Number);
          const stopMin = sh * 60 + sm;
          // 依交通工具動力學計算行車/步行所需時間 (機車 500m/分, 汽車 400m/分, 步行 75m/分)
          const travelMin = Math.max(1, Math.round(dist / profile.speedMpm));
          const userArrivalMin = targetMinutes + travelMin;     // 客人抵達站點的時刻
          
          // 物理可行性約束 (客人出門抵達，必須在垃圾車離開前趕到！)
          const canCatch = (userArrivalMin <= stopMin + 1);
          // 完成任務總耗時 (從出門到垃圾投入車斗的總分鐘數，不小於行進時間)
          const totalTaskMinutes = Math.max(travelMin, stopMin - targetMinutes);
          // 客人到站後在現場等待垃圾車抵達的分鐘數
          const waitAtStopMin = Math.max(0, stopMin - userArrivalMin);

          allStops.push({
            routeName: route.route_name,
            plate: route.truck_plate,
            hasRecycling: route.has_recycling,
            name: stop.name,
            lat: stop.lat,
            lon: stop.lon,
            time: stop.time,
            stopMin: stopMin,
            dist: dist,
            travelMin: travelMin,
            userArrivalMin: userArrivalMin,
            canCatch: canCatch,
            totalTaskMinutes: totalTaskMinutes,
            waitAtStopMin: waitAtStopMin,
            notes: stop.notes
          });
        });
      });

      // 依距離排序全站點
      allStops.sort((a, b) => a.dist - b.dist);
      const topNearest = allStops[0];
      if (topNearest) {
        topNearest.walkingMin = Math.max(1, Math.round(topNearest.dist / TRAVEL_PROFILES.walking.speedMpm));
      }

      // 定點收運站 (早晨救急)
      const fixedStationsWithDist = FIXED_STATIONS.map(f => ({
        ...f,
        dist: haversine(currentLat, currentLon, f.lat, f.lon),
        travelMin: Math.max(1, Math.round(haversine(currentLat, currentLon, f.lat, f.lon) / profile.speedMpm))
      })).sort((a, b) => a.dist - b.dist);
      const topFixed = fixedStationsWithDist[0];

      // 3. 創辦人四階時空救急安全梯 (Missed-Shift Ladder)
      // 判定家門口最近班次是否已經開走
      const isLocalShiftMissed = (topNearest && topNearest.stopMin < targetMinutes);

      let topFastest = null;
      let shiftState = 'LIVE'; // LIVE | INTERCEPT | NIGHT_CLOSED | DAY_PREVIEW

      if (!isOffDay) {
        // 嚴格篩選：客人出發後「交通工具趕得上」且在 60 分鐘內可完成任務的站點
        const catchableCandidates = allStops.filter(s => s.canCatch && s.totalTaskMinutes >= 0 && s.totalTaskMinutes <= 60);
        
        if (catchableCandidates.length > 0) {
          // 以【最快完成任務總耗時】為第一優先排序，耗時相同則選距離最近的
          catchableCandidates.sort((a, b) => a.totalTaskMinutes - b.totalTaskMinutes || a.dist - b.dist);
          topFastest = catchableCandidates[0];
          shiftState = isLocalShiftMissed ? 'INTERCEPT' : 'LIVE';
        } else {
          // 趕不上任何夜間車：判定是否夜間已全收工 (> 19:30 或全數過去)
          const allNightShiftsPast = allStops.every(s => s.stopMin < targetMinutes);
          if (targetMinutes >= 1170 || allNightShiftsPast) { // 19:30 以後或全部已過
            shiftState = 'NIGHT_CLOSED';
          } else {
            // 白天或非夜間時段，顯示首班車預報
            const earliestCandidates = [...allStops].sort((a, b) => a.stopMin - b.stopMin || a.dist - b.dist);
            topFastest = earliestCandidates[0];
            shiftState = 'DAY_PREVIEW';
          }
        }
      }

      // 4. 渲染 卡片 1：最快抵達 / 時空救急安全梯
      if (shiftState === 'NIGHT_CLOSED') {
        // 時空救急第四階：夜間已全數收工，直接展示明日早晨救急卡
        cardsContainer.innerHTML += `
          <div class="card card-fastest" style="border-color: #6366F1; background: linear-gradient(180deg, #EEF2FF 0%, #FFFFFF 100%);">
            <div class="card-fastest-banner" style="background: linear-gradient(135deg, #4F46E5 0%, #3730A3 100%);">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 16px;">🌙</span>
                <span class="card-tag tag-fastest" style="background: transparent; padding: 0; box-shadow: none; font-size: 13px; font-weight: 900;">今晚台東夜間垃圾車已全數收工</span>
              </div>
              <div class="countdown-pill" style="background: rgba(0,0,0,0.22); border: 1px solid rgba(255,255,255,0.35); font-size: 12px;">明早 07:30 救急</div>
            </div>

            <div class="card-fastest-content">
              <div style="background: #E0E7FF; border: 1px solid #C7D2FE; border-radius: 12px; padding: 12px; margin-bottom: 12px; font-size: 13px; color: #3730A3; line-height: 1.5;">
                <strong>🚨 今晚夜間清運已全線結束！</strong><br>
                台東市夜間垃圾車每日約於 16:30 ~ 19:30 出勤。您預計出門時間（${targetTimeStr}）已無夜間車次。<br>
                <strong>別擔心！您有兩個救急解法：</strong>
              </div>

              <div class="card-title-row">
                <div>
                  <div style="font-size: 11px; color: #4338CA; font-weight: 800;">明日早晨救急首選・定點收運站</div>
                  <div class="stop-name" style="font-size: 20px;">${topFixed.name}</div>
                </div>
                <div style="text-align: right; background: #EEF2FF; padding: 6px 12px; border-radius: 12px; border: 1px solid #C7D2FE;">
                  <div style="font-size: 11px; color: #4338CA; font-weight: 700;">明日早晨開放</div>
                  <div style="font-size: 18px; font-weight: 900; color: #3730A3;">07:30</div>
                </div>
              </div>

              <div class="card-meta-grid">
                <div class="meta-item">
                  <span class="meta-label">開放時段</span>
                  <span class="meta-val" style="color: #4338CA;">每週一二四五 07:30-08:30</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">離家距離</span>
                  <span class="meta-val">${topFixed.dist} 公尺 (${profile.name}約 ${topFixed.travelMin} 分鐘)</span>
                </div>
              </div>

              <a class="nav-btn" style="background: linear-gradient(135deg, #4F46E5 0%, #3730A3 100%); color: #FFF; margin-bottom: 8px;" href="https://www.google.com/maps/dir/?api=1&destination=${topFixed.lat},${topFixed.lon}&travelmode=${profile.gmapMode}" target="_blank">
                🧭 一鍵導航至明早定點站 (${topFixed.name})
              </a>

              <a class="nav-btn" style="background: #F8FAFC; color: #0F172A; border: 1.5px solid #CBD5E1;" href="#upsellCard">
                🛋️ 不想起早追車？預約生活管家 999 包月到府代倒
              </a>
            </div>
          </div>
        `;
      } else if (topFastest && (shiftState === 'LIVE' || shiftState === 'INTERCEPT')) {
        const isIntercept = (shiftState === 'INTERCEPT');
        const titleTag = isIntercept 
          ? `🚨 家門口班次已過・火速跨區攔截！` 
          : (wantRecycle ? `🥇 ${targetTimeStr} 出發・【雙收】最快搞定` : `🥇 ${targetTimeStr} 出發・最快完成倒垃圾`);
        
        const arrH = Math.floor(topFastest.userArrivalMin / 60);
        const arrM = topFastest.userArrivalMin % 60;
        const userArrivalStr = `${String(arrH).padStart(2, '0')}:${String(arrM).padStart(2, '0')}`;

        cardsContainer.innerHTML += `
          <div class="card card-fastest" ${isIntercept ? 'style="border-color: #EA580C;"' : ''}>
            <div class="card-fastest-banner" ${isIntercept ? 'style="background: linear-gradient(135deg, #C2410C 0%, #9A3412 100%);"' : ''}>
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 16px; animation: pulse 1s infinite;">${isIntercept ? '⚡' : '🔥'}</span>
                <span class="card-tag tag-fastest" style="background: transparent; padding: 0; box-shadow: none; font-size: 13px; font-weight: 900;">${titleTag}</span>
              </div>
              <div class="countdown-pill" style="background: rgba(0,0,0,0.22); border: 1px solid rgba(255,255,255,0.35); box-shadow: none; font-size: 12px;">⚡ 出門 ${topFastest.totalTaskMinutes} 分鐘搞定！</div>
            </div>

            <div class="card-fastest-content">
              ${isIntercept ? `
                <div style="background: #FFF7ED; border: 1px solid #FFEDD5; border-radius: 12px; padding: 10px 14px; margin-bottom: 12px; font-size: 13px; color: #9A3412; line-height: 1.5;">
                  <strong>⚠️ 救急通報：</strong> 您住家附近原定班次（表定 ${topNearest ? topNearest.time : '先前'}）已駛離！<br>
                  生活管家雷達已自動為您鎖定<strong>鄰近生活圈趕得上</strong>的火速攔截點！<br>
                  ${currentTravelMode === 'walking' && topFastest.dist > 500 ? '🛵 <strong>強烈建議切換上方【騎機車】</strong>，出門只需數分鐘即可趕上！' : '請準時出發以防再次錯過！'}
                </div>
              ` : ''}

              <div class="card-title-row">
                <div>
                  <div style="font-size: 11px; color: #DC2626; font-weight: 800; letter-spacing: 0.5px;">${isIntercept ? '🔥 火速攔截點' : '首選攔截點'}</div>
                  <div class="stop-name" style="font-size: 21px;">${topFastest.name}</div>
                </div>
                <div style="text-align: right; background: #FFF5F5; padding: 6px 12px; border-radius: 12px; border: 1px solid #FECACA;">
                  <div style="font-size: 11px; color: #991B1B; font-weight: 700;">車次表定</div>
                  <div style="font-size: 20px; font-weight: 900; color: #DC2626; line-height: 1.1;">${topFastest.time}</div>
                </div>
              </div>

              <!-- 任務完成時間節奏條 -->
              <div class="stepper-container">
                <div class="stepper-node">
                  <span class="stepper-time">${targetTimeStr}</span>
                  <span class="stepper-label">您出門出發</span>
                </div>
                <div class="stepper-arrow">
                  <span style="background: #FEE2E2; padding: 1px 6px; border-radius: 6px;">${profile.icon} ${topFastest.travelMin}分</span>
                  <span style="font-size: 13px;">➔</span>
                </div>
                <div class="stepper-node">
                  <span class="stepper-time">${userArrivalStr}</span>
                  <span class="stepper-label">到場 (等${topFastest.waitAtStopMin}分)</span>
                </div>
                <div class="stepper-arrow">
                  <span style="color: #BE123C;">投遞</span>
                  <span style="font-size: 13px;">➔</span>
                </div>
                <div class="stepper-node">
                  <span class="stepper-time" style="color: #BE123C; font-size: 17px; font-weight: 900;">${topFastest.time}</span>
                  <span class="stepper-label" style="color: #9F1239; font-weight: 900;">車到搞定</span>
                </div>
              </div>

              <div class="card-meta-grid">
                <div class="meta-item">
                  <span class="meta-label">服務項目</span>
                  <span class="meta-val" style="color: ${topFastest.hasRecycling ? '#059669' : '#64748B'};">${topFastest.hasRecycling ? '♻️ 垃圾+回收雙收' : '🗑️ 純一般垃圾'}</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">${profile.name}作戰距離</span>
                  <span class="meta-val">${topFastest.dist} 公尺 (${topFastest.travelMin} 分鐘)</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">出勤車號</span>
                  <span class="meta-val">${topFastest.plate}</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">路線生活圈</span>
                  <span class="meta-val" style="font-size: 13px; color: #475569;">${topFastest.routeName}</span>
                </div>
              </div>
              <a class="nav-btn nav-btn-fastest" href="https://www.google.com/maps/dir/?api=1&destination=${topFastest.lat},${topFastest.lon}&travelmode=${profile.gmapMode}" target="_blank">
                ${profile.icon} 一鍵開啟 Google Maps ${profile.name}導航
              </a>
              <button onclick="shareToLine('${topFastest.name}', '${topFastest.time}', ${topFastest.waitAtStopMin}, ${topFastest.dist})" style="width: 100%; background: #F8FAFC; color: #1E293B; border: 1.5px solid #CBD5E1; padding: 12px; border-radius: 14px; font-size: 14px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; min-height: 46px;">
                📲 一鍵把這班車分享給家人 (LINE)
              </button>
            </div>
          </div>
        `;
      } else if (topFastest && shiftState === 'DAY_PREVIEW') {
        cardsContainer.innerHTML += `
          <div class="card card-fastest" style="border-color: #EF4444;">
            <div class="card-tag tag-fastest">🥇 白天離峰時段・傍晚首班出勤預報</div>
            <div class="card-title-row">
              <div class="stop-name">${topFastest.name}</div>
              <div style="background: #FEE2E2; color: #DC2626; font-size: 13px; font-weight: 700; padding: 4px 10px; border-radius: 999px;">
                傍晚 ${topFastest.time} 起跑
              </div>
            </div>
            <div style="font-size: 13px; color: var(--text-sub); line-height: 1.4;">
              台東夜間垃圾車於傍晚 16:30 ~ 19:30 陸續出勤。您預計的時間若不在傍晚，早晨（07:30~08:30）可至定點收運站倒垃圾！
            </div>
            <div class="card-meta-grid">
              <div class="meta-item">
                <span class="meta-label">傍晚首班車號</span>
                <span class="meta-val">${topFastest.plate}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">服務項目</span>
                <span class="meta-val">${topFastest.hasRecycling ? '♻️ 垃圾+回收雙收' : '🗑️ 純一般垃圾'}</span>
              </div>
            </div>
            <a class="nav-btn nav-btn-fastest" href="https://www.google.com/maps/dir/?api=1&destination=${topFastest.lat},${topFastest.lon}&travelmode=${profile.gmapMode}" target="_blank">
              📍 預先查看站點地圖位置
            </a>
          </div>
        `;
      }

      // 5. 渲染 卡片 2：步行最近（戴明安燈三級防線）
      if (topNearest) {
        let badgeHtml = '';
        let distanceNoticeHtml = '';
        
        if (topNearest.dist <= 400) {
          // 第一級：400m 內，從容走去
          badgeHtml = `<div class="card-tag tag-nearest">🥈 步行最近・從容走去</div>`;
          distanceNoticeHtml = `
            <div style="font-size: 14px; font-weight: 700; color: #0284C7;">離家僅 ${topNearest.dist}m (${topNearest.walkingMin} 分鐘)</div>
          `;
        } else if (topNearest.dist <= 700) {
          // 第二級：400~700m，快步前往
          badgeHtml = `<div class="card-tag tag-nearest" style="background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD;">🥈 步行可達・快步前往</div>`;
          distanceNoticeHtml = `
            <div style="font-size: 14px; font-weight: 700; color: #D97706;">離家 ${topNearest.dist}m (${topNearest.walkingMin} 分鐘)</div>
          `;
        } else {
          // 第三級：超過 700m，嚴禁欺騙「從容走去」，顯示安燈警示與替代方案
          badgeHtml = `<div class="card-tag" style="background: #FEF3C7; color: #B45309; border: 1px solid #FDE68A;">⚠️ 步行距離過遠・手提沉重</div>`;
          distanceNoticeHtml = `
            <div style="font-size: 14px; font-weight: 700; color: #DC2626;">離家約 ${topNearest.dist}m (${topNearest.walkingMin} 分鐘)</div>
          `;
        }

        cardsContainer.innerHTML += `
          <div class="card" ${topNearest.dist > 700 ? 'style="border-color: #FCD34D;"' : ''}>
            ${badgeHtml}
            <div class="card-title-row">
              <div class="stop-name">${topNearest.name}</div>
              ${distanceNoticeHtml}
            </div>
            
            ${topNearest.dist > 700 ? `
              <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 12px; padding: 10px 14px; margin-bottom: 12px; font-size: 13px; color: #92400E; line-height: 1.5;">
                <strong>💡 生活管家貼心提醒：</strong><br>
                最近站點步行需 <strong>${topNearest.walkingMin} 分鐘</strong>，提重物走路非常吃力！<br>
                建議切換上方為【🛵 騎機車】（約 <strong>${Math.max(1, Math.round(topNearest.dist / TRAVEL_PROFILES.scooter.speedMpm))} 分鐘</strong> 抵達），或直接預約下方【生活管家 999 包月到府代倒】。
              </div>
            ` : ''}

            <div class="card-meta-grid">
              <div class="meta-item">
                <span class="meta-label">表定清運時間</span>
                <span class="meta-val">${topNearest.time}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">清運服務</span>
                <span class="meta-val" style="color: ${topNearest.hasRecycling ? '#059669' : '#64748B'};">${topNearest.hasRecycling ? '♻️ 垃圾+回收' : '🗑️ 僅垃圾'}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">步行距離</span>
                <span class="meta-val">${topNearest.dist}m (${topNearest.walkingMin}分)</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">車次/路線</span>
                <span class="meta-val">${topNearest.plate}</span>
              </div>
            </div>
            <a class="nav-btn secondary" href="https://www.google.com/maps/dir/?api=1&destination=${topNearest.lat},${topNearest.lon}&travelmode=walking" target="_blank">
              📍 步行導航 (${topNearest.walkingMin} 分鐘)
            </a>
          </div>
        `;
      }

      // 6. 渲染 卡片 3：早晨定點收運 (救急首選)
      if (topFixed && shiftState !== 'NIGHT_CLOSED') {
        cardsContainer.innerHTML += `
          <div class="card">
            <div class="card-tag tag-fixed">🥉 錯過夜間車救急・早晨定點站</div>
            <div class="card-title-row">
              <div class="stop-name">${topFixed.name}</div>
            </div>
            <div class="card-meta-grid">
              <div class="meta-item">
                <span class="meta-label">開放時段</span>
                <span class="meta-val" style="color: #D97706;">07:30 - 08:30</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">距離目前位置</span>
                <span class="meta-val">${topFixed.dist} 公尺 (${profile.name}約 ${topFixed.travelMin} 分鐘)</span>
              </div>
            </div>
            <a class="nav-btn secondary" href="https://www.google.com/maps/dir/?api=1&destination=${topFixed.lat},${topFixed.lon}&travelmode=${profile.gmapMode}" target="_blank">
              🧭 導航至定點收運廣場
            </a>
          </div>
        `;
      }
    }'''

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 替換 LOCAL_SEED_ROUTES
routes_pattern = re.compile(r'const LOCAL_SEED_ROUTES = \[.*?\];', re.DOTALL)
assert routes_pattern.search(content), "Cannot find LOCAL_SEED_ROUTES pattern"
content = routes_pattern.sub(new_routes_js.strip(), content)

# 替換 renderRadar
radar_pattern = re.compile(r'function renderRadar\(\) \{.*?\n    \}\n\n    // LINE LIFF 雙模引擎', re.DOTALL)
assert radar_pattern.search(content), "Cannot find renderRadar pattern"
content = radar_pattern.sub(new_render_radar_js + "\n\n    // LINE LIFF 雙模引擎", content)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully updated {HTML_PATH}")
