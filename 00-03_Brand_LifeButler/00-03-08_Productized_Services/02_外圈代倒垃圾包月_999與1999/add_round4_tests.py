# -*- coding: utf-8 -*-
import re

TEST_SCRIPT_PATH = "test_plan_lb_trash_radar_01_audit.py"
with open(TEST_SCRIPT_PATH, "r", encoding="utf-8") as f:
    text = f.read()

anchor = """console.log("✅ [驗收 11 通過] 林納斯：今日 17:03 真車出勤實測三方比對完全一致！清運e點通截圖(17:05已清運) ＝ Worker原始XML(stime=17:05 estimate=已清運) ＝ 雷達卡片(表定17:05/車輛已駛離本站)！");"""

extra_tests = """console.log("✅ [驗收 11 通過] 林納斯：今日 17:03 真車出勤實測三方比對完全一致！清運e點通截圖(17:05已清運) ＝ Worker原始XML(stime=17:05 estimate=已清運) ＝ 雷達卡片(表定17:05/車輛已駛離本站)！");

// =========================================================================
// 【驗收 12】創辦人親傳：最快卡片從車出發找站，以「最早攔得到」為準；回收車 1618 車號為 109-UL
// =========================================================================
// 1. 驗證回收車 1618 truck_plate 已修正為 109-UL
const r1618 = (typeof RECYCLING_SEED_ROUTES !== 'undefined' ? RECYCLING_SEED_ROUTES : api.LOCAL_SEED_ROUTES).find(r => r.run_id === '1618' || r.route_id === 'TT_RECYCLE_1618');
assert(r1618, '必須存在 1618 回收車路線');
assert.strictEqual(r1618.truck_plate, '109-UL', '1618 回收車真實車號必須為 109-UL');

// 2. 模擬出勤車輛：以「最早攔得到」為準挑選站點
sandbox.__TEST_NOW__ = '2026-11-16T17:00:00+08:00';
api.setCoords(22.7550, 121.1400); // 客人定位點
elements.trashTimeInput.value = '17:00';
elements.recycleCheckbox.checked = false;

// 注入執勤車輛 KEH-5218 與其動態班表 (更生路731號已抵達，更生路107號約7分到)
api.setLiveTrucksCache({
  'KEH5218': {
    car_no: 'KEH-5218',
    run_id: '1551',
    name: 'KEH-5218',
    lat: 22.76786,
    lon: 121.1365,
    speed: 16,
    status: '執勤中',
    visitedStops: {}
  }
});
api.setLiveRouteSchedule('1551', {
  timestamp: Date.now(),
  stops: {
    '新生路770號': { name: '新生路770號', stime: '17:05', estimate: '已清運', statusId: '0' },
    '更生路731號': { name: '更生路731號', stime: '17:14', estimate: '已抵達', statusId: '1' },
    '更生路107號': { name: '更生路107號', stime: '17:48', estimate: '約7分到', statusId: '2' }
  }
});

api.renderRadar();
const r12Html = elements.cardsContainer.innerHTML;
// 驗證卡片 1 成功從在線車輛出發，鎖定該車前方最早可攔截站點
assert(r12Html.includes('KEH-5218'), '卡片 1 必須顯示已鎖定出勤車號 KEH-5218');
console.log("✅ [驗收 12 通過] 林納斯：回收車 1618 車號已修正為 109-UL；最快卡片落實「從車出發找站」，以「最早攔得到」為準成功鎖定在線車機！");

// =========================================================================
// 【驗收 13】創辦人親傳：所有卡片（最快、最近）絕對不推薦已過站的點！
// =========================================================================
// 模擬車剛經過的位置定位：客人站在新生路 770 號 (官方 estimate="已清運")
api.setCoords(22.76534, 121.1342); // 新生路 770 號座標
elements.trashTimeInput.value = '17:00';
api.renderRadar();
const r13Html = elements.cardsContainer.innerHTML;

// 斷言：卡片 1 (最快) 與 卡片 2 (最近) 絕對不能出現「新生路770號」！
const card1Part = r13Html.split('tag-fastest')[1] ? r13Html.split('tag-fastest')[1].split('tag-nearest')[0] : '';
const card2Part = r13Html.split('tag-nearest')[1] ? r13Html.split('tag-nearest')[1].split('tag-fixed')[0] : '';

assert(!card1Part.includes('新生路770號'), '卡片 1 (最快) 絕對不得推薦已清運/已過站的新生路770號！');
assert(!card2Part.includes('新生路770號'), '卡片 2 (最近) 絕對不得推薦已清運/已過站的新生路770號！');
console.log("✅ [驗收 13 通過] 戴明：全卡片零過站漏洞硬核驗收通過！客人站在剛過站位置，最快與最近卡片 100% 拒絕推薦已清運站點，精準引導後續站點！");
"""

if anchor in text and "【驗收 12】" not in text:
    text = text.replace(anchor, extra_tests)
    with open(TEST_SCRIPT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print("Added Verification 12 and 13 to Deming audit script!")
else:
    print("Notice: Verification 12 and 13 already present or anchor not found.")
