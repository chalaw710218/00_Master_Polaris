# 📋 生活管家儲備知識庫（31 條 K）物理真值反查表

> **審查日期**：2026-11-24  
> **檢驗工具**：`evidence_gate.py`（Python 標準庫 urllib 物理抓取 + `quote_in_page` 逐字驗算）  
> **狀態定義**：  
> - **【已驗證】**：網頁抓取成功，且找到逐字原文完全支持該 K 假說（數字無出處者已標註備註）。  
> - **【對不上】**：網頁抓取成功，但網頁內容與該 K 假說論點無關或相互矛盾。  
> - **【未驗證】**：網頁無法抓取（404/403/reCAPTCHA/動態渲染），或網頁正文未包含足以支持假說之句子。  

| K 編號 | 標題 | 網址 | 狀態 | 原文摘句 | 備註 |
| :--- | :--- | :--- | :---: | :--- | :--- |
| K-001 | Threads 演算法會話信號與抑制釣魚誘餌 | [https://www.standard.co.uk/news/tec...](https://www.standard.co.uk/news/tech/threads-app-feed-meta-engagement-bait-spam-adam-mosseri-b1158482.html) | 【對不上】 | 無（網頁轉向英超曼城足球新聞） | 網頁重導向至《The Standard》體育報導（Pep Guardiola predicts what will happen to Man City against West Ham），查無 Threads 演算法與 engagement bait 內容。 |
| K-002 | 遞歸模型崩潰與數據分佈長尾消失 | [https://arxiv.org/abs/2305.17493...](https://arxiv.org/abs/2305.17493) | 【已驗證】 | We find that use of model-generated content in training causes irreversible defects in the resulting models, where tails of the original content distribution disappear. We refer to this effect as Model Collapse and show that it can occur in Variational Autoencoders, Gaussian Mixture Models and LLMs. | 經 evidence_gate.quote_in_page 逐字驗收通過，arXiv 論文摘要原文與假說完全吻合。 |
| K-003 | 柳宗悅民藝用之美與無名工匠哲學 | [https://traversingtradition.com/202...](https://traversingtradition.com/2021/04/19/the-beauty-of-everyday-things-soetsu-yanagi/) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-004 | 行動端人因排版工學 | [https://developerux.com/mobile-typo...](https://developerux.com/mobile-typography-ux-guide/) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-005 | 第三空間與社區弱連結信任 | [https://www.brookings.edu/articles/...](https://www.brookings.edu/articles/third-places-as-community-builders/) | 【已驗證】 | Third places is a term coined by sociologist Ray Oldenburg and refers to places where people spend time between home ('first' place) and work ('second' place). | 經 evidence_gate.quote_in_page 逐字驗收通過，支持第三空間與社區向心力定義。 |
| K-006 | Anthropic 去 AI 腔提示詞工程 | [https://docs.anthropic.com/en/docs/...](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) | 【未驗證】 | 無 | 網頁抓取成功，但內容為 Anthropic 官方提示詞工程總覽導航目錄，查無「使用主動動詞消除 AI 腔」之支持原文。 |
| K-007 | 國際慢食哲學（優質/清潔/公平） | [https://www.slowfood.com/about-us/o...](https://www.slowfood.com/about-us/our-philosophy/) | 【已驗證】 | Slow Food is a global movement of local groups and activists united by the common goal of ensuring everyone has access to good, clean and fair food. | 經 evidence_gate.quote_in_page 逐字驗收通過，支持國際慢食核心三原則（Good/Clean/Fair）。 |
| K-008 | 社群會話速度與互動時效 | [https://sproutsocial.com/insights/s...](https://sproutsocial.com/insights/social-media-algorithms/) | 【已驗證】 | Social media algorithms act as primary distribution filters. They heavily amplify content that captures early, high-velocity engagement like saves and shares, while actively burying passive, low-effort content beneath more competitive signals. | 經 evidence_gate.quote_in_page 逐字驗收通過。概念吻合高初速互動（high-velocity engagement），但原摘要之「30至60分鐘」時間數字在原文中無出處。 |
| K-009 | WHO 高齡友善環境與在地安老八大面向 | [https://extranet.who.int/agefriendl...](https://extranet.who.int/agefriendlyworld/) | 【已驗證】 | The city of Oldenburg has pursued a systematic strategy to promote age-friendliness since 2012, guided by the eight domains of the WHO “Age-Friendly Cities” framework. | 經 evidence_gate.quote_in_page 逐字驗收通過，確認 WHO 八大高齡友善範疇（eight domains of the WHO Age-Friendly Cities framework）。 |
| K-010 | 常民生活攝影之真實感信任與反塑料化 | [https://fstoppers.com/originals/why...](https://fstoppers.com/originals/why-authenticity-photography-matters-more-ever-634912) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-011 | Threads 演算法冷啟動與前千粉積累路徑 | [https://socialk.it/blog/how-to-grow...](https://socialk.it/blog/how-to-grow-on-threads) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-012 | Threads 推薦系統二階會話與主動互動權重 | [https://buffer.com/resources/thread...](https://buffer.com/resources/threads-algorithm/) | 【已驗證】 | The Threads algorithm prioritizes signals that show genuine interest, such as replies, profile visits, time spent engaging with a post, and repeat interactions with an author. | 經 evidence_gate.quote_in_page 逐字驗收通過，支持 Threads 推薦系統主動互動與回覆權重高於被動滑動之論述。 |
| K-013 | 店貓人設情緒降噪與準社會互動信任機制 | [https://www.ncbi.nlm.nih.gov/pmc/ar...](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9317584/) | 【未驗證】 | 無 | 網頁抓不到（遭 reCAPTCHA 防火牆攔截，無法讀取論文正文）。 |
| K-014 | 常民生活文案具身認知與微小感官描摹 | [https://medium.com/@storytelling_ne...](https://medium.com/@storytelling_neuroscience/sensory-language-in-copywriting) | 【未驗證】 | 無 | 網頁抓不到（Medium 登入/轉址攔截，長度僅 424 字元查無正文）。 |
| K-015 | 微型社區服務與無負擔敲門磚鄰里互助信任 | [https://www.air.org/resource/spotli...](https://www.air.org/resource/spotlight/aging-place-mutual-aid-and-community-support) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-016 | 跨世代資訊接觸與青銀共創實體信任 | [https://www.ncbi.nlm.nih.gov/pmc/ar...](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8305882/) | 【對不上】 | Articles from Journal of Fungi are provided here courtesy of Multidisciplinary Digital Publishing Institute (MDPI) | 網頁抓取成功，但該論文發表於真菌學期刊《Journal of Fungi》（真菌生物學研究），與跨世代資訊接觸及青銀信任完全無關。 |
| K-017 | 侘寂美學與自然光常民生活攝影視覺信任 | [https://www.wearejustlooking.org/wa...](https://www.wearejustlooking.org/wabi-sabi-photography) | 【已驗證】 | The underlying idea became that things are more beautiful for bearing imperfections. | 經 evidence_gate.quote_in_page 逐字驗收通過，支持侘寂美學與真實粗糙感光影。 |
| K-018 | 社群平台推薦流降權避坑與非機器人信任累積 | [https://postory.io/blog/threads-sha...](https://postory.io/blog/threads-shadowban-guide) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-019 | 地方風土慢生活與超在地社群共同體認同 | [https://www.researchgate.net/public...](https://www.researchgate.net/publication/344211116_Hyperlocal_Social_Media_and_Sense_of_Place) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 403: Forbidden，ResearchGate 權限阻擋）。 |
| K-020 | 從線上社群到線下實體信任轉化漏斗 | [https://www.forbes.com/councils/for...](https://www.forbes.com/councils/forbesagencycouncil/converting-social-media-followers-to-offline-customers/) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-021 | Threads 單一主題標籤與利基推薦索引機制 | [https://socialbee.com/blog/threads-...](https://socialbee.com/blog/threads-algorithm/) | 【未驗證】 | 無 | 網頁抓取結果為圖片二進位檔（WEBP），查無正文文字。 |
| K-022 | 社群高情商神回覆與圈內互動留存力學 | [https://wearesculpt.com/blog/commun...](https://wearesculpt.com/blog/community-management-brand-voice-banter/) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-023 | 雙主角敘事節奏交替與抗疲勞張弛互補 | [https://creativescreenwriting.com/d...](https://creativescreenwriting.com/dual-protagonist-narrative-cadence/) | 【未驗證】 | 無 | 網頁為客戶端動態渲染頁面（僅有 Loading 字樣），查無正文。 |
| K-024 | 常民生活晝夜生理節律與社群共時發文動能 | [https://trendsuite.ai/blog/circadia...](https://trendsuite.ai/blog/circadian-rhythm-social-media-posting/) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-025 | 哈佛營運透明度與服務代勞努力啟發式信任 | [https://www.hbs.edu/faculty/Pages/i...](https://www.hbs.edu/faculty/Pages/item.aspx?num=47854) | 【對不上】 | What is Facebook, Really? - Article - Faculty & Research - Harvard Business School | 網頁抓取成功，但該編號對應之文章為哈佛商學院 John Deighton 關於臉書商業模式之論文《What is Facebook, Really?》，與營運透明度（Operational Transparency）或努力啟發式無關。 |
| K-026 | 多模態內容切換與抗演算法疲勞生態 | [https://www.semrush.com/blog/multim...](https://www.semrush.com/blog/multimodal-content-strategy/) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-027 | 地方小店生態聯動與草根信任轉移效應 | [https://castopia.ai/blog/cross-prom...](https://castopia.ai/blog/cross-promotion-small-business-trust-transfer/) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-028 | 主頁簡介排版優化與置頂精華低阻力追蹤轉化 | [https://momentumhive.app/blog/threa...](https://momentumhive.app/blog/threads-profile-bio-optimization-conversion/) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-029 | 社群負面爭議柔性公關降溫與高情商化解話術 | [https://www.talaera.com/blog/handli...](https://www.talaera.com/blog/handling-customer-complaints-deescalation/) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 404: Not Found）。 |
| K-030 | 敘事傳遞理論與常民生活共鳴品牌忠誠 | [https://www.researchgate.net/public...](https://www.researchgate.net/publication/228224538_Narrative_Processing_Building_Consumer_Connections_to_Brands) | 【未驗證】 | 無 | 網頁抓不到（HTTP Error 403: Forbidden，ResearchGate 權限阻擋）。 |
| K-031 | 未來服務需求前置探測與互動徵詢假說 | [https://steveblank.com/category/cus...](https://steveblank.com/category/customer-development/) | 【未驗證】 | 無 | 網頁抓取成功，但內容為 Steve Blank 部落格彙整頁，查無關於「前置意圖探測（Pre-announcement）」之原文支持句。 |
