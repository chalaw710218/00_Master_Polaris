# -*- coding: utf-8 -*-
"""
執行 PLAN-LB-TRASH-RADAR-01 修補單 (全 10 項修補)
原則：只改邏輯與文案，不動 UI 版面、不新增按鈕。改前先備份 index.html。
"""
import os
import re
import json
import shutil
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE_DIR = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-08_Productized_Services\02_外圈代倒垃圾包月_999與1999"
ENGINE_DIR = os.path.join(BASE_DIR, "05_Trash_Radar_Engine")
INDEX_PATH = os.path.join(ENGINE_DIR, "index.html")
BACKUP_PATH = os.path.join(ENGINE_DIR, "index.html.bak")
SEED_JSON_PATH = os.path.join(ENGINE_DIR, "taitung_trash_routes_seed.json")

# 清理先前臨時檔案
for tmp_f in ["deploy_gcp_trash_proxy.py", "trash_proxy.php", "register_cf_subdomain.py"]:
    p = os.path.join(BASE_DIR, tmp_f)
    if os.path.exists(p):
        os.remove(p)

# 0. 備份 index.html
if not os.path.exists(BACKUP_PATH):
    shutil.copy2(INDEX_PATH, BACKUP_PATH)
    print(f"✅ 已建立備份檔案: {BACKUP_PATH}")
else:
    print(f"ℹ️ 備份檔案已存在: {BACKUP_PATH}")

# 1. 解析站點層 recycle_day (第 10 項：48 個站名寫有「(週X回收車)」，在站點層加 recycle_day 欄位)
def extract_stop_recycle_day(stop_name, route_recycle_day):
    # 匹配如 (週二.五回收車)、(週二、五回收車)、(週六(15:00)回收車)、（週六回收車）、(週二回收)
    m = re.search(r'[(\uff08]週([一二三四五六日\.、,，]+)(?:\([0-9:]+\))?回收', stop_name)
    if m:
        days_raw = m.group(1)
        days = []
        for ch in days_raw:
            if ch in "一二三四五六日" and ch not in days:
                days.append(ch)
        if days:
            return "星期" + "、".join(days)
    return route_recycle_day if route_recycle_day else "無"

with open(SEED_JSON_PATH, "r", encoding="utf-8") as f:
    seed_data = json.load(f)

count_48 = 0
js_routes_lines = ["    const LOCAL_SEED_ROUTES = ["]
for route in seed_data["routes"]:
    r_id = route["route_id"]
    r_name = route["route_name"]
    plate = route["truck_plate"]
    t_day = route["trash_day"]
    r_day = route.get("recycle_day", "無")
    has_rec = "true" if route.get("has_recycling") else "false"

    js_routes_lines.append("      {")
    js_routes_lines.append(f'        route_id: "{r_id}", route_name: "{r_name}", truck_plate: "{plate}",')
    js_routes_lines.append(f'        trash_day: "{t_day}", recycle_day: "{r_day}",')
    js_routes_lines.append(f'        has_recycling: {has_rec},')
    js_routes_lines.append("        stops: [")

    for stop in route["stops"]:
        s_name = stop["name"]
        s_lat = stop["lat"]
        s_lon = stop["lon"]
        s_time = stop.get("scheduled_time") or stop.get("time")
        stop_r_day = extract_stop_recycle_day(s_name, r_day)
        stop["recycle_day"] = stop_r_day
        if not route.get("has_recycling") and stop_r_day != "無":
            count_48 += 1
        js_routes_lines.append(
            f'          {{ name: {json.dumps(s_name, ensure_ascii=False)}, lat: {s_lat}, lon: {s_lon}, time: "{s_time}", recycle_day: "{stop_r_day}" }},'
        )

    js_routes_lines.append("        ]")
    js_routes_lines.append("      },")
js_routes_lines.append("    ];")
new_local_seed_routes_js = "\n".join(js_routes_lines)

print(f"✅ 站點層 recycle_day 轉換完成：在 has_recycling=false 路線中精準識別出 {count_48} 個獨立回收日站點")
assert count_48 == 48, f"Expected 48 stops, got {count_48}"

with open(SEED_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(seed_data, f, ensure_ascii=False, indent=2)

# 2. 讀取 index.html 並替換 <script> 主邏輯區塊（完全保留 HTML 與 CSS 版面，不新增按鈕）
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html_content = f.read()

script_start_marker = "  <script>\n"
script_end_marker = "  </script>\n</body>"
assert script_start_marker in html_content and script_end_marker in html_content, "Script markers not found"

prefix_html = html_content.split(script_start_marker)[0]
suffix_html = html_content.split(script_end_marker)[1]

new_main_script = """  <script>
    // ==========================================
    // 🛰️ 即時車機 GPS ✕ 動態 ETA 計算引擎 (PLAN-LB-TRASH-RADAR-01 修補版)
    // ==========================================
    let liveTrucksCache = {}; // { [normKey]: { car_no, name, run_id, lat, lon, speed, time, status, lastUpdate, visitedStops: {} } }
    let lastLiveFetchTimestamp = 0;
    let isFetchingLiveGps = false;

    // 第 8 項：統一車號格式（去掉括號備註、去掉「-」與空白、轉大寫）
    function normalizePlate(plateStr) {
      if (!plateStr) return "";
      return String(plateStr)
        .replace(/\\(.*?\\)/g, "")
        .replace(/（.*?）/g, "")
        .replace(/^回/, "")
        .replace(/[-\\s]/g, "")
        .toUpperCase();
    }

    function makeStopKey(lat, lon) {
      return `${Number(lat).toFixed(5)},${Number(lon).toFixed(5)}`;
    }

    // 第 6 項：改用自家 Cloudflare Worker 為第一順位，公共代理保留為備援
    const CF_WORKER_URL = "https://taitung-trash-proxy.chalaw710218.workers.dev";
    const LIVE_GPS_PROXIES = [
      (target) => `${CF_WORKER_URL}/?url=${encodeURIComponent(target)}`,
      (target) => `https://api.allorigins.win/raw?url=${encodeURIComponent(target)}`,
      (target) => `https://corsproxy.io/?url=${encodeURIComponent(target)}`
    ];

    async function fetchLiveTruckLocations(forceByInterval = false) {
      const now = Date.now();
      // 45 秒防抖保護 (若為每 45 秒定時器觸發則允許執行)
      if ((!forceByInterval && now - lastLiveFetchTimestamp < 45000) || isFetchingLiveGps) {
        return;
      }
      isFetchingLiveGps = true;

      const targetUrl = "https://www.bstruck.hinet.net/MIS/subsystem/XML/Appcarlocation.ashx?customer_id=22&key=1";

      for (let i = 0; i < LIVE_GPS_PROXIES.length; i++) {
        try {
          const proxyUrl = LIVE_GPS_PROXIES[i](targetUrl);
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 6000);

          const res = await fetch(proxyUrl, { signal: controller.signal });
          clearTimeout(timeoutId);

          if (!res.ok) continue;
          const xmlText = await res.text();
          if (!xmlText || (!xmlText.includes("<Items>") && !xmlText.includes("<Items/>") && !xmlText.includes("<Items />"))) continue;

          // XML 解析
          const parser = new DOMParser();
          const xmlDoc = parser.parseFromString(xmlText, "text/xml");
          const carNodes = xmlDoc.getElementsByTagName("Car");

          const nextCache = { ...liveTrucksCache };
          for (let c = 0; c < carNodes.length; c++) {
            const node = carNodes[c];
            const rawCarNo = node.getAttribute("car_no") || "";
            const rawRouteName = node.getAttribute("name") || "";
            const runId = node.getAttribute("run_id") || "";
            const lat = parseFloat(node.getAttribute("lat"));
            const lon = parseFloat(node.getAttribute("lon"));
            const hasSpeedAttr = node.hasAttribute("speed");
            const status = node.getAttribute("car_status") || "執勤中";
            const speed = hasSpeedAttr ? parseFloat(node.getAttribute("speed") || "0") : (status === "執勤中" ? 15 : 0);
            const time = node.getAttribute("time") || "";

            if ((rawCarNo || rawRouteName) && !isNaN(lat) && !isNaN(lon)) {
              const normCar = normalizePlate(rawCarNo);
              const normRoute = normalizePlate(rawRouteName);
              const prevEntry = nextCache[normCar] || nextCache[normRoute] || nextCache[rawCarNo] || {};
              const visitedStops = { ...(prevEntry.visitedStops || {}) };

              // 第 1 項：檢查該車目前位置是否進入任何站點 120m 內，記錄於歷史欄位 visitedStops
              if (typeof LOCAL_SEED_ROUTES !== "undefined" && status !== "未執勤") {
                LOCAL_SEED_ROUTES.forEach(r => {
                  if (normalizePlate(r.truck_plate) === normCar || normalizePlate(r.route_name) === normRoute || (runId && r.route_id === `TT_OFFICIAL_${runId}`)) {
                    r.stops.forEach(st => {
                      if (haversine(lat, lon, st.lat, st.lon) <= 120) {
                        visitedStops[makeStopKey(st.lat, st.lon)] = true;
                      }
                    });
                  }
                });
              }

              const record = {
                car_no: rawCarNo,
                name: rawRouteName,
                run_id: runId,
                lat,
                lon,
                speed,
                time,
                status,
                lastUpdate: now,
                visitedStops
              };

              if (normCar) nextCache[normCar] = record;
              if (normRoute) nextCache[normRoute] = record;
              if (rawCarNo) nextCache[rawCarNo] = record;
              if (rawRouteName) nextCache[rawRouteName] = record;
            }
          }

          liveTrucksCache = nextCache;
          lastLiveFetchTimestamp = now;
          isFetchingLiveGps = false;

          // 第 7 項：抓到即時車況後，只微更新徽章（不重繪整頁）
          updateCardsWithLiveStatus();
          return;
        } catch (e) {
          console.warn(`Live GPS fetch proxy [${i}] error:`, e.message);
        }
      }

      isFetchingLiveGps = false;
      lastLiveFetchTimestamp = now;
    }

    // 第 1 項 & 第 8 項：計算特定車輛對特定站點的即時動態 ETA
    function evaluateLiveTruckStatus(plate, stopLat, stopLon, stopMin) {
      const normKey = normalizePlate(plate);
      const truck = (liveTrucksCache && (liveTrucksCache[normKey] || liveTrucksCache[plate])) || null;

      if (!truck || truck.status === "未執勤") {
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

      if (!truck.visitedStops) {
        truck.visitedStops = {};
      }

      const stopKey = makeStopKey(stopLat, stopLon);
      const dist = haversine(truck.lat, truck.lon, stopLat, stopLon);

      // 只要進入該站 120m 內，即寫入 visitedStops 歷史紀錄
      if (dist <= 120) {
        truck.visitedStops[stopKey] = true;
      }

      const hasVisited = Boolean(
        truck.visitedStops[stopKey] ||
        truck.visitedStops[`${stopLat},${stopLon}`]
      );

      // 市區垃圾車平均速度約 260 公尺/分鐘 (考量停等家戶投遞)
      const liveEtaMin = Math.max(1, Math.round(dist / 260));

      const now = (typeof window !== 'undefined' && window.__TEST_NOW__) ? new Date(window.__TEST_NOW__) : new Date();
      const currentMin = now.getHours() * 60 + now.getMinutes();
      const estArrivalMin = currentMin + liveEtaMin;
      const delayMin = estArrivalMin - stopMin;

      // 1. 車輛已過站判定：只有「曾到過該站 120m 內 (hasVisited) 且已離開 > 400m」才判已駛離！
      if (hasVisited && dist > 400) {
        return {
          hasLive: true,
          badgeColor: '#9A3412',
          badgeBg: '#FFEDD5',
          border: '#FDBA74',
          dotColor: '#EA580C',
          label: '⚠️ 車輛已駛離本站',
          detail: `車輛已通過該路段（目前距離 ${dist}m）`,
          delayMin: delayMin,
          isPassed: true,
          dist: dist,
          liveEtaMin: liveEtaMin
        };
      }

      // 若時間已過表定 > 2 分鐘且車距 > 400m，但「從未記錄到進入本站 120m 內 (!hasVisited)」
      // 無法確定是否已過站或晚到，一律顯示「依官方表定時間」
      if (currentMin > stopMin + 2 && dist > 400 && !hasVisited) {
        return {
          hasLive: false,
          badgeColor: '#64748B',
          badgeBg: '#F1F5F9',
          border: '#E2E8F0',
          dotColor: '#94A3B8',
          label: '⚪ 依官方表定時間',
          detail: '依官方班表時間為準',
          delayMin: delayMin,
          isPassed: false,
          dist: dist,
          liveEtaMin: liveEtaMin
        };
      }

      // 2. 現場收運中判定 (距離站點 120m 內且慢速/停等)
      if (dist <= 120 && (truck.speed === undefined || truck.speed <= 8)) {
        return {
          hasLive: true,
          badgeColor: '#065F46',
          badgeBg: '#D1FAE5',
          border: '#6EE7B7',
          dotColor: '#10B981',
          label: '🛑 垃圾車正在現場收運中！',
          detail: `垃圾車已在站點周邊（距此站 ${dist}m），請立即前往投遞！`,
          delayMin: delayMin,
          isPassed: false,
          dist: dist,
          liveEtaMin: 0
        };
      }

      // 3. 誤點情況判定 (比表定時間晚 4 分鐘以上)
      if (delayMin >= 4) {
        const estH = String(Math.floor(estArrivalMin / 60) % 24).padStart(2, '0');
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
        detail: `距離此站約 ${dist}m，預估還有 ${liveEtaMin} 分鐘抵達`,
        delayMin: delayMin,
        isPassed: false,
        dist: dist,
        liveEtaMin: liveEtaMin
      };
    }

    // 第 7 項：當非同步取得即時車機後，僅微更新 DOM 中的即時徽章區塊 (零閃爍)
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

    // 第 4 項：計算定點收運站（只開週一、二、四、五 07:30-08:30）下一個開放日資訊
    function getNextFixedStationOpenInfo(currentDay) {
      const OPEN_DAYS = [1, 2, 4, 5];
      const DAY_NAMES = ["週日", "週一", "週二", "週三", "週四", "週五", "週六"];
      const tomorrow = (currentDay + 1) % 7;
      if (OPEN_DAYS.includes(tomorrow)) {
        return {
          isTomorrowOpen: true,
          nextDayName: DAY_NAMES[tomorrow],
          pillText: "明早 07:30 救急",
          cardTitlePrefix: "明日早晨救急首選・定點收運站",
          rightBoxLabel: "明日早晨開放",
          rightBoxValue: "07:30",
          navBtnText: (stationName) => `🧭 一鍵導航至明早定點站 (${stationName})`,
          noticeHtml: ""
        };
      }
      // 隔天不開（例如週二晚上、週五晚上、週六晚上），往後找下一個開放日
      let offset = 2;
      while (offset <= 7) {
        const candidateDay = (currentDay + offset) % 7;
        if (OPEN_DAYS.includes(candidateDay)) {
          const nextName = DAY_NAMES[candidateDay];
          return {
            isTomorrowOpen: false,
            nextDayName: nextName,
            pillText: `下一個開放日 ${nextName} 07:30`,
            cardTitlePrefix: `定點站隔日停開・下一個開放日 ${nextName} 07:30`,
            rightBoxLabel: "下一個開放日",
            rightBoxValue: `${nextName} 07:30`,
            navBtnText: (stationName) => `🧭 查看定點站位置 (${stationName}・${nextName} 07:30 開放)`,
            noticeHtml: `
              <div style="background: #FFF7ED; border: 1px solid #FED7AA; border-radius: 12px; padding: 10px 14px; margin-bottom: 10px; font-size: 13px; color: #9A3412; line-height: 1.5;">
                <strong>⚠️ 定點站開放日提醒：</strong> 定點收運站僅每週一、二、四、五 07:30-08:30 開放，<strong>下一個開放日為 ${nextName} 07:30</strong>。<br>
                不想把垃圾堆在家裡苦等？歡迎直接預約下方【生活管家 999 包月到府代倒】！
              </div>
            `
          };
        }
        offset++;
      }
    }

    // 預設台東座標 (鐵花/轉運站)
    let currentLat = 22.7518;
    let currentLon = 121.1475;
    let currentAreaName = "鐵花村 / 轉運站周邊";
    let currentLocMode = 'gps'; // 'gps' 或 'manual'
    let currentTravelMode = 'scooter'; // 創辦人指引：預設台東常民生活首選【🛵 騎機車】！

    // 交通工具動力模型：速度 (公尺/分)、圖示與 Google Maps 導航協議
    const TRAVEL_PROFILES = {
      walking: { name: "步行", speedMpm: 75, icon: "🚶", gmapMode: "walking", desc: "(步行約 4.5km/h)" },
      scooter: { name: "騎車", speedMpm: 500, icon: "🛵", gmapMode: "two-wheeler", desc: "(騎機車約 30km/h)" },
      car:     { name: "開車", speedMpm: 400, icon: "🚗", gmapMode: "driving", desc: "(開車市區含臨停約 24km/h)" }
    };

    function setTravelMode(mode) {
      currentTravelMode = mode;
      document.querySelectorAll('#modeWalkBtn, #modeScooterBtn, #modeCarBtn').forEach(b => b.classList.remove('active'));
      const desc = document.getElementById('travelModeDesc');
      if (mode === 'walking') {
        document.getElementById('modeWalkBtn').classList.add('active');
        desc.innerText = TRAVEL_PROFILES.walking.desc;
      } else if (mode === 'scooter') {
        document.getElementById('modeScooterBtn').classList.add('active');
        desc.innerText = TRAVEL_PROFILES.scooter.desc;
      } else if (mode === 'car') {
        document.getElementById('modeCarBtn').classList.add('active');
        desc.innerText = TRAVEL_PROFILES.car.desc;
      }
      renderRadar();
    }

    // 台東市區主要地標與路段地理詞庫 (包含新站特區、外環聚落與創辦人實測路段)
    const TAITUNG_GEO_DICT = [
      { keywords: ["興航", "興航街", "興安路一段", "興安", "新站特區"], name: "台東市新站特區/興航街", lat: 22.7932, lon: 121.1218 },
      { keywords: ["台東新站", "台東車站", "火車站", "志航路一段", "文昌路"], name: "台東新站/志航路前站", lat: 22.7930, lon: 121.1225 },
      { keywords: ["正氣", "基督教醫院", "夜市", "正氣路"], name: "台東市正氣路商圈", lat: 22.7535, lon: 121.1512 },
      { keywords: ["鐵花", "轉運站", "秀泰", "新生路", "鐵花村"], name: "台東市鐵花村/轉運站", lat: 22.7518, lon: 121.1475 },
      { keywords: ["寶桑", "精誠", "寶桑路"], name: "台東市寶桑路老街", lat: 22.7588, lon: 121.1522 },
      { keywords: ["四維", "強國", "四維路"], name: "台東市四維路一段", lat: 22.7610, lon: 121.1505 },
      { keywords: ["更生", "馬偕", "馬偕醫院", "更生路"], name: "台東市更生路/馬偕醫院", lat: 22.7560, lon: 121.1440 },
      { keywords: ["傳廣", "傳廣路"], name: "台東市傳廣路段", lat: 22.7582, lon: 121.1395 },
      { keywords: ["東海", "漢陽", "中華路二段", "東海運動公園"], name: "台東市中華路二段/東海", lat: 22.7420, lon: 121.1390 },
      { keywords: ["豐榮", "漢中", "豐榮路"], name: "台東市豐榮路/漢中街", lat: 22.7405, lon: 121.1352 },
      { keywords: ["豐年", "康樂", "中興路二段", "中興路三段", "機場"], name: "台東市豐年/康樂機場特區", lat: 22.7630, lon: 121.1180 },
      { keywords: ["大豐", "豐里", "中華路三段", "中華路四段"], name: "台東市大豐/豐里生活圈", lat: 22.7230, lon: 121.1380 },
      { keywords: ["知本", "建興", "青海路", "大學路", "知本車站"], name: "台東市知本/建興生活圈", lat: 22.7050, lon: 121.0580 },
      { keywords: ["富岡", "石川", "松江路", "漁港"], name: "台東市富岡漁港/海線圈", lat: 22.7920, lon: 121.1920 },
      { keywords: ["南王", "卑南", "更生北路", "綠色隧道"], name: "台東市南王/卑南文化區", lat: 22.7820, lon: 121.1180 }
    ];

    function switchLocMode(mode) {
      currentLocMode = mode;
      const tabGps = document.getElementById('tabGpsBtn');
      const tabManual = document.getElementById('tabManualBtn');
      const gpsView = document.getElementById('gpsView');
      const manualView = document.getElementById('manualView');

      if (mode === 'gps') {
        tabGps.classList.add('active');
        tabManual.classList.remove('active');
        gpsView.style.display = 'flex';
        manualView.style.display = 'none';
        requestLocation();
      } else {
        tabManual.classList.add('active');
        tabGps.classList.remove('active');
        gpsView.style.display = 'none';
        manualView.style.display = 'flex';
        const inp = document.getElementById('manualAddressInput');
        inp.focus();
      }
    }

    async function searchManualAddress() {
      const q = document.getElementById('manualAddressInput').value.trim();
      const notice = document.getElementById('manualSearchNotice');
      if (!q) {
        notice.innerText = "⚠️ 請輸入路名或門牌地址！";
        notice.style.color = "#DC2626";
        return;
      }

      notice.innerText = "🔍 正在精準定位中...";
      notice.style.color = "#0284C7";

      let match = TAITUNG_GEO_DICT.find(item => 
        item.keywords.some(kw => q.includes(kw) || kw.includes(q))
      );

      if (match) {
        currentLat = match.lat;
        currentLon = match.lon;
        currentAreaName = match.name;
        notice.innerText = `✅ 已精準定位至【${match.name}】！`;
        notice.style.color = "#059669";
        renderRadar();
        return;
      }

      try {
        const query = q.includes("台東") ? q : `台東縣台東市 ${q}`;
        const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=1&countrycodes=tw`;
        const res = await fetch(url, { headers: { 'Accept-Language': 'zh-TW' } });
        const data = await res.json();
        if (data && data.length > 0) {
          currentLat = parseFloat(data[0].lat);
          currentLon = parseFloat(data[0].lon);
          currentAreaName = q;
          notice.innerText = `✅ 已成功定位至【${q}】！(${currentLat.toFixed(4)}, ${currentLon.toFixed(4)})`;
          notice.style.color = "#059669";
          renderRadar();
          return;
        }
      } catch (e) {
        console.warn("Geocoding fetch error:", e);
      }

      notice.innerText = `⚠️ 找不到「${q}」的確切位置！請確認路名（如：興航街、正氣路），或改點上方【🎯 手機自動定位】`;
      notice.style.color = "#DC2626";
    }

    function initTimeInput() {
      const now = (typeof window !== 'undefined' && window.__TEST_NOW__) ? new Date(window.__TEST_NOW__) : new Date();
      const currentH = now.getHours();
      const currentM = now.getMinutes();
      const timeInput = document.getElementById('trashTimeInput');
      const timeDesc = document.getElementById('timeRelativeDesc');

      if (currentH < 15 || currentH >= 21) {
        timeInput.value = "17:15";
        timeDesc.innerText = "(推薦 17:15 清運時段)";
      } else {
        const hh = String(currentH).padStart(2, '0');
        const mm = String(currentM).padStart(2, '0');
        timeInput.value = `${hh}:${mm}`;
        timeDesc.innerText = "(目前手機時間)";
      }
    }

    function onTimeInputChange() {
      const val = document.getElementById('trashTimeInput').value;
      if (val) {
        document.getElementById('timeRelativeDesc').innerText = `(預計 ${val} 出發)`;
        renderRadar();
      }
    }

    function setNowTime() {
      const now = (typeof window !== 'undefined' && window.__TEST_NOW__) ? new Date(window.__TEST_NOW__) : new Date();
      const hh = String(now.getHours()).padStart(2, '0');
      const mm = String(now.getMinutes()).padStart(2, '0');
      document.getElementById('trashTimeInput').value = `${hh}:${mm}`;
      document.getElementById('timeRelativeDesc').innerText = `(現在 ${hh}:${mm})`;
      renderRadar();
    }

    function quickSetTime(tStr) {
      document.getElementById('trashTimeInput').value = tStr;
      document.getElementById('timeRelativeDesc').innerText = `(指定 ${tStr} 出發)`;
      renderRadar();
    }

    function toggleRecycle(e) {
      if (e.target.id !== 'recycleCheckbox') {
        const cb = document.getElementById('recycleCheckbox');
        cb.checked = !cb.checked;
        onRecycleChange();
      }
    }

    function onRecycleChange() {
      const cb = document.getElementById('recycleCheckbox');
      const box = document.getElementById('recycleBox');
      const sub = document.getElementById('recycleSubText');
      const title = document.getElementById('recycleTitleText');
      if (cb.checked) {
        box.style.borderColor = '#059669';
        box.style.backgroundColor = '#ECFDF5';
        title.style.color = '#065F46';
        sub.innerText = '✅ 已勾選：僅為您篩選【一般垃圾 ＋ 資源回收車】雙收班次！';
      } else {
        box.style.borderColor = '#E2E8F0';
        box.style.backgroundColor = '#F8FAFC';
        title.style.color = 'var(--text-main)';
        sub.innerText = '未勾選默認只倒垃圾；勾選後只顯示【垃圾+回收雙收】車次';
      }
      renderRadar();
    }

    // 本地內建台東站點快取 (含第 10 項站點層 recycle_day 欄位)
__LOCAL_SEED_ROUTES_PLACEHOLDER__

    // 台東常態三大早晨定點收運站
    const FIXED_STATIONS = [
      { name: "南京路與正氣路口廣場", lat: 22.75382, lon: 121.14925, time: "每週一二四五 07:30-08:30" },
      { name: "臺東縣立體育場大門前", lat: 22.75231, lon: 121.14083, time: "每週一二四五 07:30-08:30" },
      { name: "東海運動公園停車場", lat: 22.74125, lon: 121.13952, time: "每週一二四五 07:30-08:30" }
    ];

    function updateLiveClock() {
      const now = (typeof window !== 'undefined' && window.__TEST_NOW__) ? new Date(window.__TEST_NOW__) : new Date();
      const h = String(now.getHours()).padStart(2, '0');
      const m = String(now.getMinutes()).padStart(2, '0');
      const el = document.getElementById('liveClock');
      if (el) el.innerText = `${h}:${m}`;
    }
    setInterval(updateLiveClock, 1000);
    updateLiveClock();

    function haversine(lat1, lon1, lat2, lon2) {
      const R = 6371000;
      const dLat = (lat2 - lat1) * Math.PI / 180;
      const dLon = (lon2 - lon1) * Math.PI / 180;
      const a = Math.sin(dLat / 2) ** 2 +
                Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                Math.sin(dLon / 2) ** 2;
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      return Math.round(R * c * 1.25); // 路網折算係數
    }

    function requestLocation() {
      const btn = document.getElementById('gpsTriggerBtn');
      const locText = document.getElementById('currentLocationText');
      btn.innerHTML = "<span>⏳ 定位中...</span>";
      
      if (!navigator.geolocation) {
        alert("您的瀏覽器未開啟定位授權，為您使用預設生活圈。");
        btn.innerHTML = "<span>🎯 GPS 定位</span>";
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (pos) => {
          currentLat = pos.coords.latitude;
          currentLon = pos.coords.longitude;
          btn.innerHTML = "<span>✅ 定位成功</span>";
          locText.innerText = `GPS 定位 (${currentLat.toFixed(4)}, ${currentLon.toFixed(4)})`;
          document.querySelectorAll('.area-chip').forEach(c => c.classList.remove('active'));
          renderRadar();
        },
        (err) => {
          console.warn("GPS error:", err);
          btn.innerHTML = "<span>⚠️ 請手選生活圈</span>";
          renderRadar();
        },
        { timeout: 5000, enableHighAccuracy: true }
      );
    }

    function formatMinToTimeStr(m) {
      const hh = String(Math.floor(m / 60)).padStart(2, '0');
      const mm = String(m % 60).padStart(2, '0');
      return `${hh}:${mm}`;
    }

    function renderRadar() {
      fetchLiveTruckLocations(); // 靜音非同步查詢即時車機
      const now = (typeof window !== 'undefined' && window.__TEST_NOW__) ? new Date(window.__TEST_NOW__) : new Date();
      const day = now.getDay(); // 0 is Sunday, 3 is Wednesday
      const isOffDay = (day === 0 || day === 3); // 台東在地：週日與週三例休！

      const alertContainer = document.getElementById('alertContainer');
      const cardsContainer = document.getElementById('cardsContainer');
      cardsContainer.innerHTML = '';
      alertContainer.innerHTML = '';

      const timeInput = document.getElementById('trashTimeInput');
      const targetTimeStr = (timeInput && timeInput.value) ? timeInput.value : "17:15";
      const [th, tm] = targetTimeStr.split(':').map(Number);
      const targetMinutes = th * 60 + tm;
      const wantRecycle = document.getElementById('recycleCheckbox') ? document.getElementById('recycleCheckbox').checked : false;
      const profile = TRAVEL_PROFILES[currentTravelMode] || TRAVEL_PROFILES.scooter;

      // 定點收運站 (早晨救急) 與隔天開放日判斷 (第 4 項)
      const fixedStationsWithDist = FIXED_STATIONS.map(f => ({
        ...f,
        dist: haversine(currentLat, currentLon, f.lat, f.lon),
        travelMin: Math.max(1, Math.round(haversine(currentLat, currentLon, f.lat, f.lon) / profile.speedMpm))
      })).sort((a, b) => a.dist - b.dist);
      const topFixed = fixedStationsWithDist[0];
      const fixedOpenInfo = getNextFixedStationOpenInfo(day);

      // 第 2 項：停收日 (週三、週日) 跳過站點計算，只顯示停收橫幅、定點站卡、代倒入口
      if (isOffDay) {
        alertContainer.innerHTML = `
          <div class="alert-banner alert-danger">
            <span style="font-size: 20px;">🚫</span>
            <div>
              <strong>今日台東市清潔隊例行停收！</strong><br>
              台東固定每週三與週日全縣停收垃圾。今日無夜間清運車次，請勿將垃圾堆置門外以免受罰！
            </div>
          </div>
        `;

        if (topFixed) {
          cardsContainer.innerHTML += `
            <div class="card">
              <div class="card-tag tag-fixed">🥉 停收日救急・${fixedOpenInfo.pillText}</div>
              <div class="card-title-row">
                <div class="stop-name">${topFixed.name}</div>
              </div>
              ${fixedOpenInfo.noticeHtml}
              <div class="card-meta-grid">
                <div class="meta-item">
                  <span class="meta-label">${fixedOpenInfo.rightBoxLabel}</span>
                  <span class="meta-val" style="color: #D97706;">${fixedOpenInfo.isTomorrowOpen ? '明早 07:30 - 08:30' : fixedOpenInfo.rightBoxValue + ' - 08:30'}</span>
                </div>
                <div class="meta-item">
                  <span class="meta-label">距離目前位置</span>
                  <span class="meta-val">${topFixed.dist} 公尺 (${profile.name}約 ${topFixed.travelMin} 分鐘)</span>
                </div>
              </div>
              <a class="nav-btn secondary" href="https://www.google.com/maps/dir/?api=1&destination=${topFixed.lat},${topFixed.lon}&travelmode=${profile.gmapMode}" target="_blank">
                ${fixedOpenInfo.navBtnText(topFixed.name)}
              </a>
              <a class="nav-btn" style="background: #FFF7ED; color: #9A3412; border: 1.5px solid #FDBA74;" href="#upsellCard">
                🛋️ 停收日不想囤垃圾？預約生活管家 999 包月到府代倒
              </a>
            </div>
          `;
        }
        return;
      }

      // 2. 非停收日空間演算計算：依據客人輸入的倒垃圾目標時間、站點層資源回收需求與出門交通工具
      let allStops = [];
      let todayAllRouteMinStop = Infinity;
      let todayAllRouteMaxStop = -Infinity;
      const DAY_CHARS = ["日", "一", "二", "三", "四", "五", "六"];
      const currentDayChar = DAY_CHARS[day];

      LOCAL_SEED_ROUTES.forEach(route => {
        // 星期出勤防呆：該車次今日若無排班則略過
        if (route.trash_day && !route.trash_day.includes(currentDayChar)) {
          return;
        }

        route.stops.forEach(stop => {
          const [sh, sm] = stop.time.split(':').map(Number);
          const stopMin = sh * 60 + sm;
          if (stopMin < todayAllRouteMinStop) todayAllRouteMinStop = stopMin;
          if (stopMin > todayAllRouteMaxStop) todayAllRouteMaxStop = stopMin;

          // 第 10 項：以站點層 recycle_day 判斷今日是否有資源回收
          const stopRecycleDay = stop.recycle_day || route.recycle_day || "無";
          const stopHasRecyclingToday = (stopRecycleDay !== "無" && stopRecycleDay.includes(currentDayChar));
          if (wantRecycle && !stopHasRecyclingToday) {
            return;
          }

          const dist = haversine(currentLat, currentLon, stop.lat, stop.lon);
          const travelMin = Math.max(1, Math.round(dist / profile.speedMpm));
          const userArrivalMin = targetMinutes + travelMin;
          
          const canCatch = (userArrivalMin <= stopMin + 1);
          const totalTaskMinutes = Math.max(travelMin, stopMin - targetMinutes);
          const waitAtStopMin = Math.max(0, stopMin - userArrivalMin);

          allStops.push({
            routeName: route.route_name,
            plate: route.truck_plate,
            hasRecycling: stopHasRecyclingToday,
            recycleDay: stopRecycleDay,
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

      // 第 3 項：動態計算今日有出勤路線的最早與最晚站點時間
      const minStopMin = allStops.length > 0 ? Math.min(...allStops.map(s => s.stopMin)) : (todayAllRouteMinStop !== Infinity ? todayAllRouteMinStop : 930);
      const maxStopMin = allStops.length > 0 ? Math.max(...allStops.map(s => s.stopMin)) : (todayAllRouteMaxStop !== -Infinity ? todayAllRouteMaxStop : 1280);
      const earliestTimeStr = formatMinToTimeStr(minStopMin);
      const latestTimeStr = formatMinToTimeStr(maxStopMin);

      // 全日離家最近站點 (僅用於判定家門口原班次是否已過)
      const allStopsByDist = [...allStops].sort((a, b) => a.dist - b.dist || a.stopMin - b.stopMin);
      const nearestAnyTime = allStopsByDist[0] || null;

      // 第 5 項：卡片 2「離家最近」只從「表定時間 ≥ 出門時間」的站點裡挑最近的
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
      }

      // 4. 渲染 卡片 1：最快抵達 / 時空救急安全梯
      if (shiftState === 'NIGHT_CLOSED') {
        cardsContainer.innerHTML += `
          <div class="card card-fastest" style="border-color: #6366F1; background: linear-gradient(180deg, #EEF2FF 0%, #FFFFFF 100%);">
            <div class="card-fastest-banner" style="background: linear-gradient(135deg, #4F46E5 0%, #3730A3 100%);">
              <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 16px;">🌙</span>
                <span class="card-tag tag-fastest" style="background: transparent; padding: 0; box-shadow: none; font-size: 13px; font-weight: 900;">今晚台東夜間垃圾車已全數收工</span>
              </div>
              <div class="countdown-pill" style="background: rgba(0,0,0,0.22); border: 1px solid rgba(255,255,255,0.35); font-size: 12px;">${fixedOpenInfo.pillText}</div>
            </div>

            <div class="card-fastest-content">
              <div style="background: #E0E7FF; border: 1px solid #C7D2FE; border-radius: 12px; padding: 12px; margin-bottom: 12px; font-size: 13px; color: #3730A3; line-height: 1.5;">
                <strong>🚨 今晚夜間清運已全線結束！</strong><br>
                台東市今日垃圾車約於 ${earliestTimeStr} ~ ${latestTimeStr} 出勤。您預計出門時間（${targetTimeStr}）已無夜間車次。<br>
                <strong>別擔心！您有以下救急解法：</strong>
              </div>

              ${fixedOpenInfo.noticeHtml}

              <div class="card-title-row">
                <div>
                  <div style="font-size: 11px; color: #4338CA; font-weight: 800;">${fixedOpenInfo.cardTitlePrefix}</div>
                  <div class="stop-name" style="font-size: 20px;">${topFixed.name}</div>
                </div>
                <div style="text-align: right; background: #EEF2FF; padding: 6px 12px; border-radius: 12px; border: 1px solid #C7D2FE;">
                  <div style="font-size: 11px; color: #4338CA; font-weight: 700;">${fixedOpenInfo.rightBoxLabel}</div>
                  <div style="font-size: 18px; font-weight: 900; color: #3730A3;">${fixedOpenInfo.rightBoxValue}</div>
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
                ${fixedOpenInfo.navBtnText(topFixed.name)}
              </a>

              <a class="nav-btn" style="background: #F8FAFC; color: #0F172A; border: 1.5px solid #CBD5E1;" href="#upsellCard">
                🛋️ 不想追車或囤垃圾？預約生活管家 999 包月到府代倒
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

        // 第 9 項：evaluateLiveTruckStatus 只算一次存成變數 fastestLive
        const fastestLive = evaluateLiveTruckStatus(topFastest.plate, topFastest.lat, topFastest.lon, topFastest.stopMin);

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
                  <strong>⚠️ 救急通報：</strong> 您住家附近較早班次（表定 ${nearestAnyTime ? nearestAnyTime.time : '先前'}）已過！<br>
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

              <!-- 🛰️ 即時車機動態微狀態 (第 9 項：單次計算變數渲染) -->
              <div id="liveFastestStatusBox" data-plate="${topFastest.plate}" data-lat="${topFastest.lat}" data-lon="${topFastest.lon}" data-stopmin="${topFastest.stopMin}" style="background: ${fastestLive.badgeBg}; border: 1px solid ${fastestLive.border}; border-radius: 12px; padding: 8px 12px; transition: all 0.3s ease;">
                <div style="display: flex; align-items: center; gap: 6px; font-weight: 800; font-size: 13px; color: ${fastestLive.badgeColor};">
                  <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background-color: ${fastestLive.dotColor}; animation: pulse 1.5s infinite;"></span>
                  <span>${fastestLive.label}</span>
                </div>
                <div style="font-size: 12px; color: ${fastestLive.badgeColor}; opacity: 0.95; line-height: 1.4; margin-top: 2px;">
                  ${fastestLive.detail}
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
              台東市今日垃圾車約於 ${earliestTimeStr} ~ ${latestTimeStr} 陸續出勤。您預計的時間若不在傍晚，週一二四五早晨（07:30~08:30）可至定點收運站倒垃圾！
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

      // 5. 渲染 卡片 2：離家最近（第 5 項：只從表定時間 ≥ 出門時間挑最近；全部都過了就顯示「今日最近班次已過」；導航改用 profile.gmapMode）
      if (topNearest) {
        topNearest.travelMin = Math.max(1, Math.round(topNearest.dist / profile.speedMpm));
        topNearest.walkingMin = Math.max(1, Math.round(topNearest.dist / TRAVEL_PROFILES.walking.speedMpm));

        let badgeHtml = '';
        let distanceNoticeHtml = '';
        let waitHomeNoticeHtml = '';

        const waitMinutesAtHome = topNearest.stopMin - targetMinutes;
        if (waitMinutesAtHome > 20) {
          waitHomeNoticeHtml = `
            <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 12px; padding: 10px 14px; margin-bottom: 12px; font-size: 13px; color: #166534; line-height: 1.5;">
              🏠 <strong>離家最近班次提示：</strong> 此班車離家僅 <strong>${topNearest.dist}m</strong>，表定 <strong>${topNearest.time}</strong> 抵達。<br>
              距您預計時間還需等候約 <strong>${waitMinutesAtHome} 分鐘</strong>。若您想現在立刻搞定，請參考上方【最快完成】先鋒車次！
            </div>
          `;
        }

        if (currentTravelMode === 'walking') {
          if (topNearest.dist <= 400) {
            badgeHtml = `<div class="card-tag tag-nearest">🥈 步行最近・從容走去</div>`;
            distanceNoticeHtml = `<div style="font-size: 14px; font-weight: 700; color: #0284C7;">離家僅 ${topNearest.dist}m (${topNearest.walkingMin} 分鐘)</div>`;
          } else if (topNearest.dist <= 700) {
            badgeHtml = `<div class="card-tag tag-nearest" style="background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD;">🥈 步行可達・快步前往</div>`;
            distanceNoticeHtml = `<div style="font-size: 14px; font-weight: 700; color: #D97706;">離家 ${topNearest.dist}m (${topNearest.walkingMin} 分鐘)</div>`;
          } else {
            badgeHtml = `<div class="card-tag" style="background: #FEF3C7; color: #B45309; border: 1px solid #FDE68A;">⚠️ 步行距離過遠・手提沉重</div>`;
            distanceNoticeHtml = `<div style="font-size: 14px; font-weight: 700; color: #DC2626;">離家約 ${topNearest.dist}m (${topNearest.walkingMin} 分鐘)</div>`;
          }
        } else {
          badgeHtml = `<div class="card-tag tag-nearest">🥈 離家最近・${profile.name}直達</div>`;
          distanceNoticeHtml = `<div style="font-size: 14px; font-weight: 700; color: #0284C7;">離家 ${topNearest.dist}m (${profile.name}約 ${topNearest.travelMin} 分鐘)</div>`;
        }

        cardsContainer.innerHTML += `
          <div class="card" ${currentTravelMode === 'walking' && topNearest.dist > 700 ? 'style="border-color: #FCD34D;"' : ''}>
            ${badgeHtml}
            <div class="card-title-row">
              <div class="stop-name">${topNearest.name}</div>
              ${distanceNoticeHtml}
            </div>

            ${waitHomeNoticeHtml}
            
            ${currentTravelMode === 'walking' && topNearest.dist > 700 ? `
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
                <span class="meta-label">${profile.name}距離</span>
                <span class="meta-val">${topNearest.dist}m (${topNearest.travelMin}分)</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">車次/路線</span>
                <span class="meta-val">${topNearest.plate}</span>
              </div>
            </div>
            <a class="nav-btn secondary" href="https://www.google.com/maps/dir/?api=1&destination=${topNearest.lat},${topNearest.lon}&travelmode=${profile.gmapMode}" target="_blank">
              ${profile.icon} ${profile.name}導航 (${topNearest.travelMin} 分鐘)
            </a>
          </div>
        `;
      } else {
        // 第 5 項：全部都過了就顯示「今日最近班次已過」
        cardsContainer.innerHTML += `
          <div class="card" style="border-color: #CBD5E1;">
            <div class="card-tag tag-nearest" style="background: #64748B;">🥈 今日最近班次已過</div>
            <div class="card-title-row">
              <div class="stop-name">今日最近班次已過</div>
            </div>
            <div style="font-size: 13px; color: var(--text-sub); line-height: 1.5;">
              您預計出門時間（${targetTimeStr}）之後，今日已無後續停靠班次。建議查看定點收運站資訊，或直接預約下方【生活管家 999 包月到府代倒】由專人到府收運！
            </div>
          </div>
        `;
      }

      // 6. 渲染 卡片 3：早晨定點收運 (第 4 項：檢查隔天星期，若隔天不開顯示「下一個開放日 X 07:30」並導流 999 代倒)
      if (topFixed && shiftState !== 'NIGHT_CLOSED') {
        cardsContainer.innerHTML += `
          <div class="card">
            <div class="card-tag tag-fixed">🥉 錯過夜間車救急・${fixedOpenInfo.pillText}</div>
            <div class="card-title-row">
              <div class="stop-name">${topFixed.name}</div>
            </div>
            ${fixedOpenInfo.noticeHtml}
            <div class="card-meta-grid">
              <div class="meta-item">
                <span class="meta-label">${fixedOpenInfo.rightBoxLabel}</span>
                <span class="meta-val" style="color: #D97706;">${fixedOpenInfo.isTomorrowOpen ? '07:30 - 08:30' : fixedOpenInfo.rightBoxValue + ' - 08:30'}</span>
              </div>
              <div class="meta-item">
                <span class="meta-label">距離目前位置</span>
                <span class="meta-val">${topFixed.dist} 公尺 (${profile.name}約 ${topFixed.travelMin} 分鐘)</span>
              </div>
            </div>
            <a class="nav-btn secondary" href="https://www.google.com/maps/dir/?api=1&destination=${topFixed.lat},${topFixed.lon}&travelmode=${profile.gmapMode}" target="_blank">
              ${fixedOpenInfo.navBtnText(topFixed.name)}
            </a>
          </div>
        `;
      }
    }

    // LINE LIFF 雙模引擎 (生活管家專屬 LIFF ID: 2012513387-UT7yDt1M)
    const LIFF_ID = "2012513387-UT7yDt1M";
    let liffProfile = null;

    async function initLiff() {
      if (typeof liff === 'undefined') return;
      try {
        await liff.init({ liffId: LIFF_ID });
        if (liff.isLoggedIn()) {
          liffProfile = await liff.getProfile();
          const nameEl = document.getElementById('userDisplayName');
          if (nameEl && liffProfile.displayName) {
            nameEl.innerText = `👋 您好，${liffProfile.displayName}！`;
            nameEl.style.display = 'inline-block';
          }
        }
      } catch (err) {
        console.warn("LIFF init skipped or fallback to web:", err);
      }
    }

    async function shareToLine(name, time, waitMin, dist) {
      const shareUrl = `https://liff.line.me/${LIFF_ID}`;
      const msg = `🚨【生活管家・台東倒垃圾快報】\\n今晚最快班次：${name}\\n⏰ 表定抵達：${time}\\n📍 距離目前約 ${dist}m (現場等約 ${waitMin} 分鐘)\\n\\n👉 點此查看即時清運雷達：\\n${shareUrl}`;
      if (typeof liff !== 'undefined' && liff.isApiAvailable && liff.isApiAvailable('shareTargetPicker')) {
        try {
          await liff.shareTargetPicker([{ type: 'text', text: msg }]);
        } catch (e) {
          console.warn("share error:", e);
        }
      } else {
        if (navigator.clipboard) {
          navigator.clipboard.writeText(msg).then(() => {
            alert("已為您複製這班垃圾車資訊！可直接貼在 LINE 傳給家人。");
          });
        } else {
          alert(`請手動複製給家人：\\n${msg}`);
        }
      }
    }

    // 第 7 項：每 45 秒自動抓一次即時位置，抓到後只更新徽章
    setInterval(() => {
      fetchLiveTruckLocations(true);
    }, 45000);

    // 初始化流程：先設置預設時間、渲染初始卡片，隨後自動嘗試手機 GPS 定位與 LIFF
    initTimeInput();
    renderRadar();
    if (navigator.geolocation) {
      requestLocation();
    }
    initLiff();
  </script>
</body>"""

new_main_script = new_main_script.replace("__LOCAL_SEED_ROUTES_PLACEHOLDER__", new_local_seed_routes_js)
final_html = prefix_html + new_main_script + suffix_html

# 同時確保 upsell-card 有 id="upsellCard" 供錨點平滑跳轉
final_html = final_html.replace('<section class="upsell-card">', '<section class="upsell-card" id="upsellCard">', 1)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"✅ 已完成 {INDEX_PATH} 全數 10 項修補！")
