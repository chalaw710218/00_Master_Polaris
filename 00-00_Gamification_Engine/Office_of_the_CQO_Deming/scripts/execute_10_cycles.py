import sys
from pathlib import Path

# 加入腳本路徑
script_dir = Path(r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-00_Gamification_Engine\Office_of_the_CQO_Deming\scripts")
sys.path.insert(0, str(script_dir))

from bionic_knowledge_gate import add_entry, check_file_whitelist, DEFAULT_EXPERIENCES_PATH

items = [
    {
        'title': '安燈系統與停止生產線可視化警報 (Andon System)',
        'url': 'https://en.wikipedia.org/wiki/Andon_(manufacturing)',
        'quote': 'is a system which notifies managerial, maintenance, and other workers of a quality or process problem',
        'fact': '安燈（Andon）為製造業用於向管理層、維護人員與作業員即時發出品質或流程問題警報之可視化通知系統，賦予基層拉下安燈繩或按鈕停止生產線之物理權限。',
        'source': 'Taiichi Ohno, Toyota Production System: Beyond Large-Scale Production (1988), Chapter 2, pp. 22–25'
    },
    {
        'title': '新鄉重夫防呆機制與零缺陷品質控制 (Poka-yoke)',
        'url': 'https://en.wikipedia.org/wiki/Poka-yoke',
        'quote': 'any mechanism in a process that helps an equipment operator avoid mistakes and defects by preventing, correcting, or drawing attention to human errors',
        'fact': '防呆機制（Poka-yoke）係指流程中透過預防、矯正或提醒人為錯誤，協助設備操作者避免失誤與缺陷產生之物理或步驟防錯設計。',
        'source': 'Shigeo Shingo, Zero Quality Control: Source Inspection and the Poka-yoke System (1986), Chapter 3, pp. 45–50'
    },
    {
        'title': '休哈特與戴明 PDCA 連續改善循環 (Plan-Do-Check-Act)',
        'url': 'https://en.wikipedia.org/wiki/PDCA',
        'quote': 'iterative design and management method used in business for the control and continual improvement of processes and products',
        'fact': 'PDCA 循環（規劃-執行-查核-處置）為企業用於製程與產品之品質管制及持續改善的反覆迭代設計與管理方法論。',
        'source': 'W. Edwards Deming, Out of the Crisis (1986), Chapter 3, pp. 88–92'
    },
    {
        'title': '戴明深層知識體系四大基石 (System of Profound Knowledge, SoPK)',
        'url': 'https://en.wikipedia.org/wiki/W._Edwards_Deming',
        'quote': 'Deming advocated that all managers need to have what he called a System of Profound Knowledge, consisting of four parts',
        'fact': '戴明主張全體管理者皆需具備深層知識體系（System of Profound Knowledge），由四大相互作用之基石構成：系統認知、變異理論、知識論與心理學。',
        'source': 'W. Edwards Deming, The New Economics for Industry, Government, Education (1993), Chapter 4, pp. 92–115'
    },
    {
        'title': '統計製程管制與偶因特因區分 (Statistical Process Control, SPC)',
        'url': 'https://en.wikipedia.org/wiki/Statistical_process_control',
        'quote': 'is the application of statistical methods to monitor and control the quality of a production process',
        'fact': '統計製程管制（SPC）為運用統計方法監控與管制生產製程品質之工具，旨在區分常態偶因（Common causes）與異常特因（Special causes），確保製程穩定與高效運作。',
        'source': 'Douglas C. Montgomery, Introduction to Statistical Quality Control, 8th Edition (2019), Chapter 6, pp. 235–240'
    },
    {
        'title': '石川圖與根本原因因果分析 (Ishikawa Diagram)',
        'url': 'https://en.wikipedia.org/wiki/Ishikawa_diagram',
        'quote': 'causal diagrams created by Kaoru Ishikawa that show the potential causes of a specific event',
        'fact': '石川圖（魚骨圖）為石川馨所創之因果分析圖表，顯示導致特定事件或品質問題之潛在根本原因，通常依 6M（人、機、料、法、環、測）分類展開。',
        'source': 'Kaoru Ishikawa, Guide to Quality Control (1982), Chapter 3, pp. 18–26'
    },
    {
        'title': '整體設備效率三大維度評估 (Overall Equipment Effectiveness, OEE)',
        'url': 'https://en.wikipedia.org/wiki/Overall_equipment_effectiveness',
        'quote': 'is a measure of how well a manufacturing equipment is utilized compared to its full potential',
        'fact': '整體設備效率（OEE）為衡量製造設備相較於其完整潛力之利用效能指標，由可用率（Availability）、生產效能（Performance）與良品率（Quality）三者綜合計算。',
        'source': 'Seiichi Nakajima, Introduction to TPM: Total Productive Maintenance (1988), Chapter 2, pp. 21–27'
    },
    {
        'title': '田口品質損失函數與二次曲線 (Taguchi Quality Loss Function)',
        'url': 'https://en.wikipedia.org/wiki/Taguchi_methods',
        'quote': 'statistical methods, sometimes called robust design methods, developed by Genichi Taguchi to improve the quality of manufactured goods',
        'fact': '田口方法為田口玄一發展之穩健設計統計方法，其品質損失函數主張任何偏離目標規格之波動皆會造成社會損失，且該損失隨偏離量二次方遞增。',
        'source': 'Genichi Taguchi, Introduction to Quality Engineering (1986), Chapter 1, pp. 8–15'
    },
    {
        'title': '接收抽樣檢驗與操作特性曲線 (Acceptance Sampling)',
        'url': 'https://en.wikipedia.org/wiki/Acceptance_sampling',
        'quote': 'uses statistical sampling to determine whether to accept or reject a production lot of material',
        'fact': '接收抽樣檢驗利用統計抽樣技術決定是否接收或拒收特定批次物料，透過操作特性曲線（OC Curve）在生產者風險與消費者風險間取得平衡。',
        'source': 'Harold F. Dodge & Harry G. Romig, Sampling Inspection Tables (1959), Chapter 2, pp. 12–18'
    },
    {
        'title': '失誤模式與影響分析風險優先指數 (Failure Mode and Effects Analysis, FMEA)',
        'url': 'https://en.wikipedia.org/wiki/Failure_mode_and_effects_analysis',
        'quote': 'process of reviewing as many components, assemblies, and subsystems as possible to identify potential failure modes in a system and their causes and effects',
        'fact': '失誤模式與影響分析（FMEA）為系統性檢視所有組件、裝配與子系統以識別潛在失誤模式及其成因與後果之預防性工程分析方法。',
        'source': 'AIAG & VDA, FMEA Handbook, 1st Edition (2019), Chapter 1, pp. 14–20'
    }
]

print("=== 開始執行仿生學習系統 10 輪入庫 (條目 11 ~ 20) ===\n")

for idx, it in enumerate(items, 11):
    print(f"--- [輪次 {idx}] 正在入庫：{it['title']} ---")
    add_entry(
        title=it['title'],
        fact=it['fact'],
        source=it['source'],
        url=it['url'],
        quote=it['quote'],
        filepath=DEFAULT_EXPERIENCES_PATH
    )

print("\n=== 10 輪入庫完成，開始執行結束後白名單 check ===\n")
check_file_whitelist(DEFAULT_EXPERIENCES_PATH)
