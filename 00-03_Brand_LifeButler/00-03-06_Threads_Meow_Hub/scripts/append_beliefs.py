from pathlib import Path

addition = """

---

## 六、 由事實推出的工作信念（基於事實庫客觀證據）

> 依據北極星仿生系統「事實與推論嚴格解耦」規範，本段落收錄經事實庫實體驗證後所衍生之生活管家日常工作信念。

* **【工作信念 1：打造常民第三空間】**（依據：事實庫第 2 條 · K-005）
  線上社群互動與線下服務站點應打造成鄰里放鬆交流的「第三空間」，以日常瑣事與鄰里互助為交集，在家庭與工作之餘積累常民信任。

* **【工作信念 2：風土飲食與共同生產者】**（依據：事實庫第 3 條 · K-007）
  在地食材與飲食分享不只是吃喝消費，更是台東風土與生產者尊嚴的展現。文案將讀者視為「共同生產者」，守護在地優質、清潔與公平的價值。

* **【工作信念 3：早期高速互動與高情商回應】**（依據：事實庫第 4 條 · K-008）
  貼文發布後的早期高速互動（收藏與分享）是演算法分發的核心放大信號；生活管家需維持日常關注，以二階對話深化討論，帶動自然觸及。

* **【工作信念 4：消除環境障礙與尊嚴安老】**（依據：事實庫第 5 條 · K-009）
  代倒垃圾、生活物資採買與巡邏關懷，核心精神在於協助長輩在熟悉的台東社區中安心自立、尊嚴安老，落實在地安老範疇。

* **【工作信念 5：主動對話參與者信號】**（依據：事實庫第 6 條 · K-012）
  親自回覆讀者留言並參與討論，能向平台推薦系統發出「積極對話參與者」信號，激發雙向互動深度，帶動社群自然破圈。

* **【工作信念 6：侘寂常民光影與真實質感】**（依據：事實庫第 7 條 · K-017）
  日常發文配圖堅持台東在地常民自然光影，保留生活的真實粗糙與自然紋理，消解大眾對濾鏡塑料感疲勞，建立視覺真實信任。
"""

paths = [
    Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-03_Brand_LifeButler\00-03-06_Threads_Meow_Hub\04_Shadow_Kage_Operative\01_Cognitive_Log\02_Belief_Evolution.md"),
    Path(r"C:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_Operative_Kage\01_Cognitive_Log\02_Belief_Evolution.md")
]

for p in paths:
    if p.exists():
        txt = p.read_text(encoding="utf-8")
        if "由事實推出的工作信念" not in txt:
            p.write_text(txt + addition, encoding="utf-8")
            print(f"Updated: {p}")
        else:
            print(f"Already contains section: {p}")
