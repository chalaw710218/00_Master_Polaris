# -*- coding: utf-8 -*-
import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(SCRIPT_DIR, "05_Trash_Radar_Engine")
HTML_PATH = os.path.join(ENGINE_DIR, "index.html")
SEED_PATH = os.path.join(ENGINE_DIR, "taitung_trash_routes_seed.json")

# 1. 更新 taitung_trash_routes_seed.json，加入 TT_ROUTE_11 (KEH-5109)
with open(SEED_PATH, "r", encoding="utf-8") as f:
    seed_data = json.load(f)

# 檢查是否已存在 TT_ROUTE_11
existing_ids = [r["route_id"] for r in seed_data["routes"]]
if "TT_ROUTE_11" not in existing_ids:
    new_route_11 = {
        "route_id": "TT_ROUTE_11",
        "route_name": "中興新站/馬蘭先鋒線",
        "truck_plate": "KEH-5109",
        "area": "中興三段/新站特區",
        "has_recycling": True,
        "stops": [
            { "stop_id": "S11_01", "name": "中興路三段20號前", "lat": 22.7718, "lon": 121.1215, "scheduled_time": "16:20", "notes": "近志航路一段口/台東專校，16:20 先鋒車次 (創辦人實證點)" },
            { "stop_id": "S11_02", "name": "中興路三段與志航路一段路口", "lat": 22.7745, "lon": 121.1220, "scheduled_time": "16:35", "notes": "新站南向咽喉路段" },
            { "stop_id": "S11_03", "name": "志航路一段與新興路口（九間座北側）", "lat": 22.7790, "lon": 121.1225, "scheduled_time": "16:45", "notes": "志航路大動脈" },
            { "stop_id": "S11_04", "name": "志航路一段與興安路口（台東新站前）", "lat": 22.7930, "lon": 121.1225, "scheduled_time": "17:10", "notes": "火車站站前廣場" },
            { "stop_id": "S11_05", "name": "文昌路與文安街口", "lat": 22.7960, "lon": 121.1235, "scheduled_time": "17:30", "notes": "新站北側住宅區" }
        ]
    }
    seed_data["routes"].append(new_route_11)
    with open(SEED_PATH, "w", encoding="utf-8") as f:
        json.dump(seed_data, f, ensure_ascii=False, indent=2)
    print("Added TT_ROUTE_11 to taitung_trash_routes_seed.json")

# 2. 生成 JavaScript 的 LOCAL_SEED_ROUTES 字串
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

# 3. 讀取 index.html
with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 替換 LOCAL_SEED_ROUTES
routes_pattern = re.compile(r'const LOCAL_SEED_ROUTES = \[.*?\];', re.DOTALL)
assert routes_pattern.search(content), "Cannot find LOCAL_SEED_ROUTES pattern"
content = routes_pattern.sub(new_routes_js.strip(), content)

# 替換 TAITUNG_GEO_DICT 增加中興路三段20號
if '"中興路三段20號"' not in content:
    content = content.replace(
        '"興航街": { lat: 22.7932, lon: 121.1218, name: "台東新站／興航街特區" },',
        '"興航街": { lat: 22.7932, lon: 121.1218, name: "台東新站／興航街特區" },\n      "中興路三段20號": { lat: 22.7718, lon: 121.1215, name: "台東市中興路三段20號 (近志航路口)" },\n      "中興路三段": { lat: 22.7718, lon: 121.1215, name: "台東市中興路三段 (近馬蘭榮家/台東專校)" },'
    )

# 4. 升級卡片 2 渲染邏輯，連動交通工具動力學並加上等待提示
card2_old = '''      // 5. 渲染 卡片 2：步行最近（戴明安燈三級防線）
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
      }'''

card2_new = '''      // 5. 渲染 卡片 2：離家最近（連動交通工具動力學 ✕ 戴明安燈防呆）
      if (topNearest) {
        topNearest.travelMin = Math.max(1, Math.round(topNearest.dist / profile.speedMpm));
        topNearest.walkingMin = Math.max(1, Math.round(topNearest.dist / TRAVEL_PROFILES.walking.speedMpm));

        let badgeHtml = '';
        let distanceNoticeHtml = '';
        let waitHomeNoticeHtml = '';

        // 判定離家門口表定時間是否還很久 (> 20 分鐘)
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
          // 機車或開車模式
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
      }'''

assert card2_old in content, "Cannot find card2_old block in index.html"
content = content.replace(card2_old, card2_new)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated index.html with KEH-5109 and enhanced Card 2!")
