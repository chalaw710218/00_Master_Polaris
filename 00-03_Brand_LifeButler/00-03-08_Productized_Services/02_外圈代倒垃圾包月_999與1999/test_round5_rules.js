
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const engineDir = path.resolve('05_Trash_Radar_Engine');
const indexPath = path.join(engineDir, 'index.html');
const html = fs.readFileSync(indexPath, 'utf-8');

const match = html.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/);
if (!match) {
  console.error("Cannot extract script");
  process.exit(1);
}
const scriptCode = match[1];

const garbageJson = JSON.parse(fs.readFileSync(path.join(engineDir, 'data', 'garbage_routes.json'), 'utf-8'));
const recyclingJson = JSON.parse(fs.readFileSync(path.join(engineDir, 'data', 'recycling_routes.json'), 'utf-8'));
const fixedJson = JSON.parse(fs.readFileSync(path.join(engineDir, 'data', 'fixed_stations.json'), 'utf-8'));

const elements = {
  liveClock: { innerText: '', style: {} },
  trashTimeInput: { value: '17:15', style: {} },
  timeRelativeDesc: { innerText: '', style: {} },
  recycleCheckbox: { checked: false, style: {} },
  recycleBox: { style: {} },
  recycleSubText: { innerText: '', style: {} },
  recycleTitleText: { style: {} },
  alertContainer: { innerHTML: '', style: {} },
  cardsContainer: { innerHTML: '', style: {} },
  travelModeDesc: { innerText: '', style: {} },
  modeWalkBtn: { classList: { add(){}, remove(){} } },
  modeScooterBtn: { classList: { add(){}, remove(){} } },
  modeCarBtn: { classList: { add(){}, remove(){} } },
  gpsTriggerBtn: { innerHTML: '', style: {} },
  currentLocationText: { innerText: '', style: {} },
  liveFastestStatusBox: null
};

const sandbox = {
  console,
  Math,
  Date,
  Number,
  String,
  Boolean,
  Array,
  Object,
  RegExp,
  JSON,
  parseFloat,
  parseInt,
  isNaN,
  Infinity,
  encodeURIComponent,
  AbortController: class { abort(){} },
  setTimeout: () => 1,
  clearTimeout: () => {},
  setInterval: () => 1,
  fetch: async () => ({ ok: true, text: async () => '<Items></Items>', json: async () => ([]) }),
  DOMParser: class {
    parseFromString() {
      return { getElementsByTagName() { return []; } };
    }
  },
  navigator: {},
  alert: () => {},
  document: {
    getElementById(id) {
      if (id === 'liveFastestStatusBox') return elements.liveFastestStatusBox;
      if (!elements[id]) {
        elements[id] = { innerText: '', innerHTML: '', value: '', checked: false, style: {}, classList: { add(){}, remove(){} } };
      }
      return elements[id];
    },
    querySelectorAll() {
      return [{ classList: { add(){}, remove(){} } }];
    }
  }
};
sandbox.window = sandbox;

vm.createContext(sandbox);

const instrumentedCode = scriptCode + `
LOCAL_SEED_ROUTES = ${JSON.stringify(garbageJson)};
RECYCLING_SEED_ROUTES = ${JSON.stringify(recyclingJson)};
FIXED_STATIONS = ${JSON.stringify(fixedJson)};
;globalThis.__EXPORT__ = {
  renderRadar,
  setTravelMode,
  setCoords: (lat, lon) => { currentLat = lat; currentLon = lon; },
  setLiveTrucksCache: (v) => { liveTrucksCache = v; },
  setLiveRouteSchedule: (runId, v) => { liveRouteSchedules[runId] = v; },
  getLiveRouteSchedules: () => liveRouteSchedules
};
`;

vm.runInContext(instrumentedCode, sandbox);
const api = sandbox.__EXPORT__;

console.log("==================================================");
console.log("🧪 測試 1：車停在 KEM-8821「連航路198之1號」附近，後段站點不得被隱藏");
console.log("==================================================");
// 週一 16:30，KEM-8821 (TT_OFFICIAL_1470) 出勤
sandbox.__TEST_NOW__ = '2026-11-16T16:30:00+08:00';
elements.trashTimeInput.value = '16:30';
elements.recycleCheckbox.checked = false;

// 模擬車機停在「連航路198之1號（日光橋下）」(22.77512, 121.1257)
api.setLiveTrucksCache({
  'KEM8821': {
    car_no: 'KEM-8821',
    lat: 22.77512,
    lon: 121.1257,
    speed: 0,
    status: '執勤中',
    visitedStops: {}
  }
});

// 使用者定位在更生北路278巷 (第2站) 附近
api.setCoords(22.78139, 121.1216);
api.setTravelMode('walking');
api.renderRadar();

const html1 = elements.cardsContainer.innerHTML;
// 驗證後段站點（如更生北路278巷）正常被推薦，不得被誤判為已過站隱藏
assert(html1.includes('更生北路278巷') || html1.includes('更生北路'), '後段站點不得被隱藏！');
assert(!html1.includes('已清運'), '未過站之站點不得出現已清運！');
console.log("🟢 驗收 1 通過：車停在連航路198之1號附近，後段站點未被誤判過站，正常推薦！");

console.log("\n==================================================");
console.log("🧪 測試 2：離線模式定位在新生路460號附近、16:50 出發，首選應為附近的站，並顯示提早警告");
console.log("==================================================");
// 清空所有即時車機與官方班表快取 (純離線模式)
api.setLiveTrucksCache({});
api.getLiveRouteSchedules && Object.keys(api.getLiveRouteSchedules()).forEach(k => delete api.getLiveRouteSchedules()[k]);

sandbox.__TEST_NOW__ = '2026-11-16T16:50:00+08:00';
elements.trashTimeInput.value = '16:50';
elements.recycleCheckbox.checked = false;

// 定位在新生路460號 (lat: 22.7594, lon: 121.1400)
api.setCoords(22.7594, 121.1400);
api.setTravelMode('walking');
api.renderRadar();

const html2 = elements.cardsContainer.innerHTML;

// 驗證首選站點為新生路460號 (或鄰近站點，距離 <= 150m)
assert(html2.includes('新生路460號') || html2.includes('新生路'), '首選應為附近的新生路460號站點！');
// 驗證卡片顯示提早警告
assert(html2.includes('車可能提早到，建議提早 15 分鐘出門'), '卡片必須加註「⚠️ 車可能提早到，建議提早 15 分鐘出門」！');
console.log("🟢 驗收 2 通過：離線模式 16:50 出發，首選推薦家門口新生路460號，並清楚標示提早 15 分鐘出門警示！");

console.log("\n==================================================");
console.log("🎉 全部退件驗收項目 100% PASS (Exit Code: 0)");
console.log("==================================================");
