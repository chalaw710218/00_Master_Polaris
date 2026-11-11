# -*- coding: utf-8 -*-
with open('05_Trash_Radar_Engine/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = '''      const DAY_NAMES = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
      const currentDayName = DAY_NAMES[day];

      LOCAL_SEED_ROUTES.forEach(route => {
        // 1. 星期出勤防呆：該車次今日若無排班則略過
        if (route.trash_day && !route.trash_day.includes(currentDayName) && !isOffDay) {
          return;
        }
        // 2. 資源回收過濾：若勾選資源回收，檢查今日該車次是否有回收
        if (wantRecycle) {
          if (!route.has_recycling || (route.recycle_day && !route.recycle_day.includes(currentDayName) && !isOffDay)) {
            return;
          }
        }'''

replacement = '''      const DAY_CHARS = ["日", "一", "二", "三", "四", "五", "六"];
      const currentDayChar = DAY_CHARS[day];

      LOCAL_SEED_ROUTES.forEach(route => {
        // 1. 星期出勤防呆：該車次今日若無排班則略過 (台東公所格式：星期一、二、四、五、六)
        if (route.trash_day && !route.trash_day.includes(currentDayChar) && !isOffDay) {
          return;
        }
        // 2. 資源回收過濾：若勾選資源回收，檢查今日該車次是否有回收
        if (wantRecycle) {
          if (!route.has_recycling || (route.recycle_day && !route.recycle_day.includes(currentDayChar) && !isOffDay)) {
            return;
          }
        }'''

assert target in c, "Target not found in index.html"
c = c.replace(target, replacement)

with open('05_Trash_Radar_Engine/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully fixed DAY_CHARS in index.html!")
