---
name: pack-qu-guang-guang
description: 🚶‍♂️【去逛逛 · 全自動社群漫遊技能組】。當創辦人說「去逛逛」、「去巡邏」、「到街上走走」或「社交一下」時觸發。由執行長雪 (Yuki) 總控，組裝 5 大萬用原子（話題雷達 ✕ 店貓破防 ✕ 管家端茶 ✕ 戴明安燈 ✕ 確定性傳輸），全自動完成高情商漫遊、借光端茶與真實增粉閉環。
---

# 🚶‍♂️ pack-qu-guang-guang · 去逛逛 · 全自動社群漫遊技能組

> **最高總舵**：創辦人 陳品碩（闆仔）  
> **專案總控**：執行長 雪 (Yuki · CEO)  
> **雙主角掌舵**：生活管家 影 (Kage) ✕ 店貓 喵編 (Meow Editor)  
> **品質安燈**：首席品質長 戴明博士 (Dr. Deming · CQO)  
> **技術監製**：CTO 林納斯 (Linus)  
> **口語觸發指令**：「去逛逛」、「去巡邏」、「到街上走走」、「社交一下」  

---

## 🧩 萬用原子積木組裝拓撲 (Atomic Composition Topology)

本技能組由 5 大深層獨立的萬用原子組裝而成，各司其職、低耦合高內聚：

```mermaid
flowchart LR
    Trigger["創辦人指令：『去逛逛』"] --> Yuki["執行長雪：漫遊排程調度"]
    Yuki --> A1["【atom-trend-scout】<br/>全網熱點嗅探與常民降維"]
    A1 --> Switch{"角色與情境路由"}
    Switch -->|傲嬌破防/打工吐槽| A2["【atom-meow-voice】<br/>五態貓科行為接梗"]
    Switch -->|溫暖接住/友店端茶| A3["【atom-kage-clout-tea】<br/>四階生活管家客廳話術"]
    A2 --> A5["【atom-growth-quality-gate】<br/>戴明五維品質安燈質檢"]
    A3 --> A5
    A5 -->|安燈綠燈 PASS (>=90)| A4["【atom-threads-engine】<br/>確定性兩段式傳輸/離線隊列"]
    A5 -->|安燈紅燈 FAIL| Yuki
```

---

## 🚀 執行流程五部曲 (Five-Step Execution Pipeline)

1. **第一步 · 嗅探時空地氣**：呼叫 `atom-trend-scout`，取得即時熱點並自動降維轉譯為柴米油鹽或打工人心電圖。
2. **第二步 · 雙主角情境生成**：
   * 若為店貓視角：呼叫 `atom-meow-voice`，注入真貓生態動作與微對白。
   * 若為管家端茶：呼叫 `atom-kage-clout-tea`，遞上 30~50 字無行銷感的一杯溫茶。
3. **第三步 · 戴明安燈審查**：呼叫 `atom-growth-quality-gate`，五維客觀質檢，若含有內部代號「極星」或 AI 塑料套話，硬性攔截退出。
4. **第四步 · 確定性送達**：呼叫 `atom-threads-engine`，執行兩段式發布或安全存入本地離線 WAL 隊列。
5. **第五步 · 戰報總結呈報**：交付精確繁中戰報予創辦人。

---

## 💻 一鍵執行介面 (One-Command Invocation)

```bash
# 創辦人一聲令下即可執行漫遊
python scripts/pack_qu_guang_guang.py --dry-run
```
