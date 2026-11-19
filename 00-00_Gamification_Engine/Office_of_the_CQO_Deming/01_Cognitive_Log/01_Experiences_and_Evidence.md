# 📘 戴明認知存摺 01：客觀事實庫 (CQO_Deming)

> 記錄 CQO_Deming 在真實審計與文獻考證中所獲取之客觀事實、文獻依據與物理限制。  
> **整理狀態**：2026-11-19 完成整肅。未驗證之 51 條已全數移至 `_未驗證封存` 資料夾；本文件僅保留具備文獻出處之 9 條核心概念，並已校正數字與剔除無依據虛構數字。

---

### [2026-11-19 校正整理] 經文獻考證之核心事實條目 (共 9 條)

1. **戴明漏斗實驗變異數與標準差**：
   - **核心事實**：對受控系統中的常態隨機波動進行補償調整（規則 2：依前一次落點誤差反向補償），系統的變異數 (Variance) 是不調整（規則 1）的 2 倍，標準差擴大為 $\sqrt{2} \approx 1.41$ 倍；若對原始目標過度反應（規則 3 與規則 4），系統變異將發散至無窮大。過度調整（Tampering）只會增加變異。
   - **出處**：W. Edwards Deming, *Out of the Crisis* (1986), Chapter 11 "The Funnel Experiment", pp. 327–332.

2. **94/6 系統責任原則**：
   - **核心事實**：94% 屬於系統（管理層責任），6% 屬於特殊原因。生產與服務系統中的問題與變異，絕大部分源於系統與流程，管理者的職責在於改造系統流程與器具防呆，而非怪罪基層作業人員。
   - **出處**：W. Edwards Deming, *Out of the Crisis* (1986), Chapter 11, p. 315.

3. **製程能力指數 (Cpk) 治理標準**：
   - **核心事實**：以統計製程能力指數 $C_{pk}$ 作為製程品質能力的衡量標準，評估製程平均值偏移與規格界限之距離。製程能力分析的前提為系統必須處於統計受控狀態，且數據符合常態分佈。
   - **出處**：Douglas C. Montgomery, *Introduction to Statistical Quality Control*, 8th Edition (2019), Chapter 8 "Process Capability Analysis".

4. **利特爾法則 (Little's Law) 與在製品流動**：
   - **核心事實**：在穩定系統（平衡狀態）中，系統內的平均在製品數量 ($L$) 等於平均到達率（吞吐量 $\lambda$）乘以平均前置時間 ($W$)，公式為 $L = \lambda W$。限制排程中的在製品數量 (WIP) 是縮短前置時間、消除擁塞的數學基礎。
   - **出處**：John D. C. Little, "A Proof for the Queuing Formula: $L = \lambda W$", *Operations Research*, 9(3), 1961, pp. 383–387.

5. **休哈特管制圖與韋斯頓電氣四規則 (Western Electric Rules)**：
   - **核心事實**：在管制界限（3-Sigma）內劃分 Zone A ($2\sigma \sim 3\sigma$)、Zone B ($1\sigma \sim 2\sigma$) 與 Zone C ($0 \sim 1\sigma$)，利用非隨機排列規則（如單點落於 3-Sigma 外、連續點落在特定區域或中心線同側）提前辨識非隨機之特殊原因變異信號。
   - **出處**：Western Electric Company, *Statistical Quality Control Handbook* (1956), Part II, Section 1, pp. 25–28.

6. **卡諾滿意度模型 (Kano Model) 品質分類**：
   - **核心事實**：產品與服務品質屬性可劃分為必備品質（Must-be，未滿足引發強烈不滿，滿足則視為理所當然）、一維品質（One-dimensional，滿足度與滿意度呈線性關係）與魅力品質（Attractive，未提供不引起不滿，提供則帶來驚喜與高度滿意）。
   - **出處**：Noriaki Kano et al., "Attractive Quality and Must-be Quality", *Journal of the Japanese Society for Quality Control* (1984), 14(2), pp. 147–156.

7. **默克爾樹 (Merkle Tree) 雜湊校驗架構**：
   - **核心事實**：利用樹狀密碼學雜湊結構，將底層數據塊進行成對雜湊並遞歸匯總為單一根雜湊 (Merkle Root)，實現大規模數據完整性的對數級複雜度驗證與防偽防篡改。
   - **出處**：Ralph C. Merkle, "A Certified Digital Signature", *Advances in Cryptology – CRYPTO '89*, pp. 218–238.

8. **塔揚演算法 (Tarjan's Algorithm) 與有向圖無環排程**：
   - **核心事實**：利用深度優先搜尋 (DFS) 與搜尋時間戳、追蹤低點值 (low-link)，在線性時間 $\mathcal{O}(V+E)$ 內求解有向圖中的所有強連通分量 (SCC)，可用於工作流循環依賴與死鎖之靜態檢測。
   - **出處**：Robert E. Tarjan, "Depth-First Search and Linear Graph Algorithms", *SIAM Journal on Computing*, 1(2), 1972, pp. 146–160.

9. **持續微小改善的複利效應原理**：
   - **核心事實**：微小習慣與流程優化具備複利效應，長期持續的邊際改善會隨時間呈現指數級累積。
   - **出處**：James Clear, *Atomic Habits* (2018), Chapter 1.


10. **休哈特管制圖與韋斯頓電氣四規則 (Western Electric Rules)（網頁佐證）**：
   - **核心事實**：韋斯頓電氣規則為統計製程管制中用於管制圖上辨識非隨機模式與特殊原因之判定決策規則。
   - **出處**：Western Electric Company, Statistical Quality Control Handbook (1956), pp. 25–28
   - **證據網址**：https://en.wikipedia.org/wiki/Western_Electric_rules
   - **原文摘句**：decision rules in statistical process control

11. **安燈系統與停止生產線可視化警報 (Andon System)**：
   - **核心事實**：安燈（Andon）為製造業用於向管理層、維護人員與作業員即時發出品質或流程問題警報之可視化通知系統，賦予基層拉下安燈繩或按鈕停止生產線之物理權限。
   - **出處**：https://en.wikipedia.org/wiki/Andon_(manufacturing)
   - **證據網址**：https://en.wikipedia.org/wiki/Andon_(manufacturing)
   - **原文摘句**：is a system which notifies managerial, maintenance, and other workers of a quality or process problem

12. **新鄉重夫防呆機制與零缺陷品質控制 (Poka-yoke)**：
   - **核心事實**：防呆機制（Poka-yoke）係指流程中透過預防、矯正或提醒人為錯誤，協助設備操作者避免失誤與缺陷產生之物理或步驟防錯設計。
   - **出處**：https://en.wikipedia.org/wiki/Poka-yoke
   - **證據網址**：https://en.wikipedia.org/wiki/Poka-yoke
   - **原文摘句**：any mechanism in a process that helps an equipment operator avoid mistakes and defects by preventing, correcting, or drawing attention to human errors

13. **休哈特與戴明 PDCA 連續改善循環 (Plan-Do-Check-Act)**：
   - **核心事實**：PDCA 循環（規劃-執行-查核-處置）為企業用於製程與產品之品質管制及持續改善的反覆迭代設計與管理方法論。
   - **出處**：https://en.wikipedia.org/wiki/PDCA
   - **證據網址**：https://en.wikipedia.org/wiki/PDCA
   - **原文摘句**：iterative design and management method used in business for the control and continual improvement of processes and products

14. **戴明深層知識體系四大基石 (System of Profound Knowledge, SoPK)**：
   - **核心事實**：戴明主張全體管理者皆需具備深層知識體系（System of Profound Knowledge），由四大相互作用之基石構成：系統認知、變異理論、知識論與心理學。
   - **出處**：https://en.wikipedia.org/wiki/W._Edwards_Deming
   - **證據網址**：https://en.wikipedia.org/wiki/W._Edwards_Deming
   - **原文摘句**：Deming advocated that all managers need to have what he called a System of Profound Knowledge, consisting of four parts

15. **統計製程管制與偶因特因區分 (Statistical Process Control, SPC)**：
   - **核心事實**：統計製程管制（SPC）為運用統計方法監控與管制生產製程品質之工具，旨在區分常態偶因（Common causes）與異常特因（Special causes），確保製程穩定與高效運作。
   - **出處**：https://en.wikipedia.org/wiki/Statistical_process_control
   - **證據網址**：https://en.wikipedia.org/wiki/Statistical_process_control
   - **原文摘句**：is the application of statistical methods to monitor and control the quality of a production process

16. **石川圖與根本原因因果分析 (Ishikawa Diagram)**：
   - **核心事實**：石川圖（魚骨圖）為石川馨所創之因果分析圖表，顯示導致特定事件或品質問題之潛在根本原因，通常依 6M（人、機、料、法、環、測）分類展開。
   - **出處**：https://en.wikipedia.org/wiki/Ishikawa_diagram
   - **證據網址**：https://en.wikipedia.org/wiki/Ishikawa_diagram
   - **原文摘句**：causal diagrams created by Kaoru Ishikawa that show the potential causes of a specific event

17. **整體設備效率三大維度評估 (Overall Equipment Effectiveness, OEE)**：
   - **核心事實**：整體設備效率（OEE）為衡量製造設備相較於其完整潛力之利用效能指標，由可用率（Availability）、生產效能（Performance）與良品率（Quality）三者綜合計算。
   - **出處**：https://en.wikipedia.org/wiki/Overall_equipment_effectiveness
   - **證據網址**：https://en.wikipedia.org/wiki/Overall_equipment_effectiveness
   - **原文摘句**：is a measure of how well a manufacturing equipment is utilized compared to its full potential

18. **田口品質損失函數與二次曲線 (Taguchi Quality Loss Function)**：
   - **核心事實**：田口方法為田口玄一發展之穩健設計統計方法，其品質損失函數主張任何偏離目標規格之波動皆會造成社會損失，且該損失隨偏離量二次方遞增。
   - **出處**：https://en.wikipedia.org/wiki/Taguchi_methods
   - **證據網址**：https://en.wikipedia.org/wiki/Taguchi_methods
   - **原文摘句**：statistical methods, sometimes called robust design methods, developed by Genichi Taguchi to improve the quality of manufactured goods

19. **接收抽樣檢驗與操作特性曲線 (Acceptance Sampling)**：
   - **核心事實**：接收抽樣檢驗利用統計抽樣技術決定是否接收或拒收特定批次物料，透過操作特性曲線（OC Curve）在生產者風險與消費者風險間取得平衡。
   - **出處**：https://en.wikipedia.org/wiki/Acceptance_sampling
   - **證據網址**：https://en.wikipedia.org/wiki/Acceptance_sampling
   - **原文摘句**：uses statistical sampling to determine whether to accept or reject a production lot of material

20. **失誤模式與影響分析風險優先指數 (Failure Mode and Effects Analysis, FMEA)**：
   - **核心事實**：失誤模式與影響分析（FMEA）為系統性檢視所有組件、裝配與子系統以識別潛在失誤模式及其成因與後果之預防性工程分析方法。
   - **出處**：https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis
   - **證據網址**：https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis
   - **原文摘句**：process of reviewing as many components, assemblies, and subsystems as possible to identify potential failure modes in a system and their causes and effects

21. **班佛定律與首位數字舞弊鑑識 (Benford's Law)**：
   - **核心事實**：班佛定律（首位數字定律）指出在自然產生的數值數據集中，首位數字為 1 的機率約為 30.1%，數字越大概率遞減；審計人員常以此統計規律檢驗財務數字是否經過人為編造或捏造。
   - **出處**：https://en.wikipedia.org/wiki/Benford%27s_law
   - **證據網址**：https://en.wikipedia.org/wiki/Benford%27s_law
   - **原文摘句**：the leading digit is likely to be small

22. **會計對帳與跨帳戶一致性校驗 (Accounting Reconciliation)**：
   - **核心事實**：會計對帳（Reconciliation）為確保兩套獨立紀錄（例如企業銀行存款日記帳與銀行對帳單）之帳面餘額相互一致的核對程序，用以查明跨期未達帳與記帳錯誤。
   - **出處**：https://en.wikipedia.org/wiki/Reconciliation_(accounting)
   - **證據網址**：https://en.wikipedia.org/wiki/Reconciliation_(accounting)
   - **原文摘句**：process of ensuring that two sets of records

23. **複式簿記與借貸平衡原則 (Double-entry Bookkeeping)**：
   - **核心事實**：複式簿記為每筆交易均以相等且相反的借方（Debits）與貸方（Credits）分錄同時記錄之記帳方法，確保會計恆等式（資產 = 負債 + 業主權益）恆常平衡。
   - **出處**：https://en.wikipedia.org/wiki/Double-entry_bookkeeping
   - **證據網址**：https://en.wikipedia.org/wiki/Double-entry_bookkeeping
   - **原文摘句**：recorded with equal and opposite entries

24. **試算表借貸相等性驗算 (Trial Balance)**：
   - **核心事實**：試算表（Trial Balance）為內部財務編制表，彙總列出總分類帳中所有借方與貸方帳戶之期末餘額，透過「借方總額 = 貸方總額」之數學一致性檢驗數學加總與過帳差錯。
   - **出處**：https://en.wikipedia.org/wiki/Trial_balance
   - **證據網址**：https://en.wikipedia.org/wiki/Trial_balance
   - **原文摘句**：lists the adjusted closing balances of all the general ledger accounts

25. **現金流量表三大活動現金流分解 (Cash Flow Statement)**：
   - **核心事實**：現金流量表展示資產負債表科目變動與損益表利潤如何影響現金及約當現金，將現金流嚴格劃分為營業活動、投資活動與籌資活動三大板塊進行動態勾稽。
   - **出處**：https://en.wikipedia.org/wiki/Cash_flow_statement
   - **證據網址**：https://en.wikipedia.org/wiki/Cash_flow_statement
   - **原文摘句**：how changes in balance sheet accounts and income affect cash

26. **資產負債表財務狀況摘要 (Balance Sheet)**：
   - **核心事實**：資產負債表（財務狀況表）為企業在特定時點之財務餘額靜態摘要，揭示企業所擁有的經濟資源（資產）、承擔的債務義務（負債）與所有者淨權益。
   - **出處**：https://en.wikipedia.org/wiki/Balance_sheet
   - **證據網址**：https://en.wikipedia.org/wiki/Balance_sheet
   - **原文摘句**：summary of the financial balances of an individual or organization

27. **損益表營收費用與淨利潤轉結 (Income Statement)**：
   - **核心事實**：損益表（利潤表）反映企業在特定會計期間之收入與各項費用成本，其最終結算之淨利潤（Net Income）直接轉結至資產負債表之保留盈餘與現金流量表營業活動起點。
   - **出處**：https://en.wikipedia.org/wiki/Income_statement
   - **證據網址**：https://en.wikipedia.org/wiki/Income_statement
   - **原文摘句**：shows the company's revenues and expenses during a particular period

28. **財務報表結構與三表跨表勾稽 (Financial Statements)**：
   - **核心事實**：財務報表為實體財務活動與財務狀況之正式紀錄，資產負債表、損益表與現金流量表三者透過保留盈餘與期末現金餘額形成閉環數學勾稽，單表造假必然導致跨表失衡。
   - **出處**：https://en.wikipedia.org/wiki/Financial_statement
   - **證據網址**：https://en.wikipedia.org/wiki/Financial_statement
   - **原文摘句**：formal records of the financial activities and position

29. **鑑識會計與財務舞弊調查 (Forensic Accounting)**：
   - **核心事實**：鑑識會計（Forensic Accounting）為結合會計學、審計學與調查技術之專業領域，專門調查企業是否存在財務報告舞弊、虛假交易或數字編造，產出可用於法律訴訟之實質證據。
   - **出處**：https://en.wikipedia.org/wiki/Forensic_accounting
   - **證據網址**：https://en.wikipedia.org/wiki/Forensic_accounting
   - **原文摘句**：specialty practice area of accounting that investigates

30. **內部控制流程與目標保障 (Internal Control)**：
   - **核心事實**：內部控制為組織確保營運效能與效率、財務報告可靠性及法規合規性的系統性流程防禦機制，透過職能分離與授權審批防止未授權操作與虛報平帳。
   - **出處**：https://en.wikipedia.org/wiki/Internal_control
   - **證據網址**：https://en.wikipedia.org/wiki/Internal_control
   - **原文摘句**：process for assuring of an organization's objectives in operational effectiveness