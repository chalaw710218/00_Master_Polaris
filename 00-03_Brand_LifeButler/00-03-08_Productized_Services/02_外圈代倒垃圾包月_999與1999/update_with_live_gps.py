# -*- coding: utf-8 -*-
import io
import os
import sys

INDEX_PATH = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-08_Productized_Services\02_外圈代倒垃圾包月_999與1999\05_Trash_Radar_Engine\index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# 1. 注入 JavaScript 引擎至 <script> 開頭
live_engine_definition = """
    // ==========================================
    // 🛰️ 即時車機 GPS ✕ 動態 ETA 計算引擎 (零新增按鈕)
    // ==========================================
    let liveTrucksCache = {}; // { [plate]: { lat, lon, speed, time, status, lastUpdate } }
    let lastLiveFetchTimestamp = 0;
    let isFetchingLiveGps = false;

    // 支援 CORS 之輕量代理端點矩陣 (自動故障轉移)
    const LIVE_GPS_PROXIES = [
      (target) => `https://api.allorigins.win/raw?url=${encodeURIComponent(target)}`,
      (target) => `https://corsproxy.io/?url=${encodeURIComponent(target)}`
    ];

    async function fetchLiveTruckLocations() {
      const now = Date.now();
      // 45 秒內不重複向公所伺服器發動請求 (防抖與保護公所頻寬)
      if (now - lastLiveFetchTimestamp < 45000 || isFetchingLiveGps) {
        return;
      }
      isFetchingLiveGps = true;

      const targetUrl = "https://www.bstruck.hinet.net/MIS/subsystem/XML/Appcarlocation.ashx?customer_id=22&key=1";

      for (let i = 0; i < LIVE_GPS_PROXIES.length; i++) {
        try {
          const proxyUrl = LIVE_GPS_PROXIES[i](targetUrl);
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 5000); // 5秒超時防呆
          
          const res = await fetch(proxyUrl, { signal: controller.signal });
          clearTimeout(timeoutId);

          if (!res.ok) continue;
          const xmlText = await res.text();
          if (!xmlText || !xmlText.includes("<Items>")) continue;

          // XML 解析
          const parser = new DOMParser();
          const xmlDoc = parser.parseFromString(xmlText, "text/xml");
          const carNodes = xmlDoc.getElementsByTagName("Car");

          const newCache = {};
          for (let c = 0; c < carNodes.length; c++) {
            const node = carNodes[c];
            const plate = node.getAttribute("car_no");
            const lat = parseFloat(node.getAttribute("lat"));
            const lon = parseFloat(node.getAttribute("lon"));
            const speed = parseFloat(node.getAttribute("speed") || "0");
            const time = node.getAttribute("time") || "";
            const status = node.getAttribute("car_status") || "執勤中";

            if (plate && !isNaN(lat) && !isNaN(lon)) {
              newCache[plate] = { lat, lon, speed, time, status, lastUpdate: now };
            }
          }

          liveTrucksCache = newCache;
          lastLiveFetchTimestamp = now;
          isFetchingLiveGps = false;

          // 抓到即時車況後，原地無感微刷新卡片（不閃爍）
          updateCardsWithLiveStatus();
          return;
        } catch (e) {
          console.warn(`Live GPS fetch proxy [${i}] error:`, e.message);
        }
      }

      isFetchingLiveGps = false;
      lastLiveFetchTimestamp = now; // 即使全部離線，也等 45 秒後再試
    }

    // 計算特定車輛對特定站點的即時動態 ETA
    function evaluateLiveTruckStatus(plate, stopLat, stopLon, stopMin) {
      if (!liveTrucksCache || !liveTrucksCache[plate]) {
        return {
          hasLive: false,
          badgeColor: '#64748B',
          badgeBg: '#F1F5F9',
          border: '#E2E8F0',
          dotColor: '#94A3B8',
          label: '⚪ 依官方表定時間',
          detail: '車機目前離峰或尚未出勤',
          delayMin: 0,
          isPassed: false
        };
      }

      const truck = liveTrucksCache[plate];
      const dist = haversine(truck.lat, truck.lon, stopLat, stopLon);
      // 市區垃圾車平均速度約 260 公尺/分鐘 (考量停等家戶投遞)
      const liveEtaMin = Math.max(1, Math.round(dist / 260));

      const now = new Date();
      const currentMin = now.getHours() * 60 + now.getMinutes();
      const estArrivalMin = currentMin + liveEtaMin;
      const delayMin = estArrivalMin - stopMin;

      // 1. 車輛已過站判定 (表定時間已過，且車輛與站點距離拉開 > 400m)
      if (currentMin > stopMin + 2 && dist > 400) {
        return {
          hasLive: true,
          badgeColor: '#9A3412',
          badgeBg: '#FFEDD5',
          border: '#FDBA74',
          dotColor: '#EA580C',
          label: '⚠️ 車輛已駛離本站',
          detail: `車輛已通過該路段（目前車速 ${truck.speed}km/h），已為您銜接下一班`,
          delayMin: delayMin,
          isPassed: true,
          dist: dist,
          liveEtaMin: liveEtaMin
        };
      }

      // 2. 現場收運中判定 (距離站點 120m 內且慢速/停等)
      if (dist <= 120 && truck.speed <= 8) {
        return {
          hasLive: true,
          badgeColor: '#065F46',
          badgeBg: '#D1FAE5',
          border: '#6EE7B7',
          dotColor: '#10B981',
          label: '🛑 垃圾車正在現場收運中！',
          detail: `垃圾車已在站點周邊（車速 ${truck.speed}km/h），請立即前往投遞！`,
          delayMin: delayMin,
          isPassed: false,
          dist: dist,
          liveEtaMin: 0
        };
      }

      // 3. 誤點情況判定 (比表定時間晚 4 分鐘以上)
      if (delayMin >= 4) {
        const estH = String(Math.floor(estArrivalMin / 60)).padStart(2, '0');
        const estM = String(estArrivalMin % 60).padStart(2, '0');
        return {
          hasLive: true,
          badgeColor: '#9A3412',
          badgeBg: '#FFF7ED',
          border: '#FED7AA',
          dotColor: '#F97316',
          label: `🔴 預估稍有延誤 (${delayMin} 分鐘)`,
          detail: `沿途清運量較大，目前距離此站 ${dist}m，預計約 ${estH}:${estM} 抵達 (請從容出發，不必在路口吹風)`,
          delayMin: delayMin,
          isPassed: false,
          dist: dist,
          liveEtaMin: liveEtaMin
        };
      }

      // 4. 正常行駛接近中
      return {
        hasLive: true,
        badgeColor: '#065F46',
        badgeBg: '#ECFDF5',
        border: '#A7F3D0',
        dotColor: '#10B981',
        label: `🟢 即時動態：垃圾車行駛中`,
        detail: `距離此站約 ${dist}m（車速 ${truck.speed}km/h），預估還有 ${liveEtaMin} 分鐘抵達`,
        delayMin: delayMin,
        isPassed: false,
        dist: dist,
        liveEtaMin: liveEtaMin
      };
    }

    // 當非同步取得即時車機後，僅微更新 DOM 中的即時徽章區塊 (零閃爍)
    function updateCardsWithLiveStatus() {
      const liveFastestEl = document.getElementById('liveFastestStatusBox');
      if (liveFastestEl && liveFastestEl.dataset.plate) {
        const p = liveFastestEl.dataset.plate;
        const lat = parseFloat(liveFastestEl.dataset.lat);
        const lon = parseFloat(liveFastestEl.dataset.lon);
        const sMin = parseInt(liveFastestEl.dataset.stopmin, 10);
        const status = evaluateLiveTruckStatus(p, lat, lon, sMin);

        liveFastestEl.innerHTML = `
          <div style="display: flex; align-items: center; gap: 6px; font-weight: 800; font-size: 13px; color: ${status.badgeColor};">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background-color: ${status.dotColor}; animation: pulse 1.5s infinite;"></span>
            <span>${status.label}</span>
          </div>
          <div style="font-size: 12px; color: ${status.badgeColor}; opacity: 0.95; line-height: 1.4; margin-top: 2px;">
            ${status.detail}
          </div>
        `;
        liveFastestEl.style.backgroundColor = status.badgeBg;
        liveFastestEl.style.borderColor = status.border;
      }
    }
"""

# 檢查是否已插入 live_engine_definition
if "let liveTrucksCache =" not in text:
    script_target = "  <script>\n    // 預設台東座標 (鐵花/轉運站)"
    script_replacement = f"  <script>\n{live_engine_definition}\n    // 預設台東座標 (鐵花/轉運站)"
    assert script_target in text, "Could not find script target anchor"
    text = text.replace(script_target, script_replacement, 1)

# 2. 在 renderRadar() 開頭加入靜音非同步擷取呼叫
radar_target = "    function renderRadar() {\n      const now = new Date();"
radar_replacement = "    function renderRadar() {\n      fetchLiveTruckLocations(); // 靜音非同步查詢即時車機\n      const now = new Date();"
if "fetchLiveTruckLocations(); // 靜音非同步查詢即時車機" not in text:
    assert radar_target in text, "Could not find renderRadar target anchor"
    text = text.replace(radar_target, radar_replacement, 1)

# 3. 在 topFastest 卡片內容中置入即時狀態徽章
card_content_target = """              <div class="card-title-row">
                <div>
                  <div style="font-size: 11px; color: #DC2626; font-weight: 800; letter-spacing: 0.5px;">${isIntercept ? '🔥 火速攔截點' : '首選攔截點'}</div>
                  <div class="stop-name" style="font-size: 21px;">${topFastest.name}</div>
                </div>
                <div style="text-align: right; background: #FFF5F5; padding: 6px 12px; border-radius: 12px; border: 1px solid #FECACA;">
                  <div style="font-size: 11px; color: #991B1B; font-weight: 700;">車次表定</div>
                  <div style="font-size: 20px; font-weight: 900; color: #DC2626; line-height: 1.1;">${topFastest.time}</div>
                </div>
              </div>"""

card_content_replacement = """              <div class="card-title-row">
                <div>
                  <div style="font-size: 11px; color: #DC2626; font-weight: 800; letter-spacing: 0.5px;">${isIntercept ? '🔥 火速攔截點' : '首選攔截點'}</div>
                  <div class="stop-name" style="font-size: 21px;">${topFastest.name}</div>
                </div>
                <div style="text-align: right; background: #FFF5F5; padding: 6px 12px; border-radius: 12px; border: 1px solid #FECACA;">
                  <div style="font-size: 11px; color: #991B1B; font-weight: 700;">車次表定</div>
                  <div style="font-size: 20px; font-weight: 900; color: #DC2626; line-height: 1.1;">${topFastest.time}</div>
                </div>
              </div>

              <!-- 🛰️ 即時車機動態微狀態 (零新增按鈕・原地呼吸燈更新) -->
              <div id="liveFastestStatusBox" data-plate="${topFastest.plate}" data-lat="${topFastest.lat}" data-lon="${topFastest.lon}" data-stopmin="${topFastest.stopMin}" style="background: ${evaluateLiveTruckStatus(topFastest.plate, topFastest.lat, topFastest.lon, topFastest.stopMin).badgeBg}; border: 1px solid ${evaluateLiveTruckStatus(topFastest.plate, topFastest.lat, topFastest.lon, topFastest.stopMin).border}; border-radius: 12px; padding: 8px 12px; transition: all 0.3s ease;">
                <div style="display: flex; align-items: center; gap: 6px; font-weight: 800; font-size: 13px; color: ${evaluateLiveTruckStatus(topFastest.plate, topFastest.lat, topFastest.lon, topFastest.stopMin).badgeColor};">
                  <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background-color: ${evaluateLiveTruckStatus(topFastest.plate, topFastest.lat, topFastest.lon, topFastest.stopMin).dotColor}; animation: pulse 1.5s infinite;"></span>
                  <span>${evaluateLiveTruckStatus(topFastest.plate, topFastest.lat, topFastest.lon, topFastest.stopMin).label}</span>
                </div>
                <div style="font-size: 12px; color: ${evaluateLiveTruckStatus(topFastest.plate, topFastest.lat, topFastest.lon, topFastest.stopMin).badgeColor}; opacity: 0.95; line-height: 1.4; margin-top: 2px;">
                  ${evaluateLiveTruckStatus(topFastest.plate, topFastest.lat, topFastest.lon, topFastest.stopMin).detail}
                </div>
              </div>"""

if "id=\"liveFastestStatusBox\"" not in text:
    assert card_content_target in text, "Could not find card content target"
    text = text.replace(card_content_target, card_content_replacement, 1)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Successfully updated {INDEX_PATH} with Live GPS Engine!")
