# -*- coding: utf-8 -*-
import os

slides_data = [
    {
        "tag": "生活管家 · 2026 秋季實戰家教班",
        "title": "告別手動複製貼上！把社群發射台交給 AI",
        "subtitle": "第 2 講：Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads)",
        "content": """
        <div style="text-align:center; padding: 30px 20px;">
          <h1 style="font-size: 38px; color: #ffffff; margin-bottom: 20px; line-height: 1.3;">
            告別手動複製貼上！<br><span style="color:#38bdf8;">把社群發射台交給 AI</span>
          </h1>
          <p style="font-size: 20px; color: #f59e0b; margin-bottom: 30px; font-weight: 600;">
            Antigravity 操作 ✕ Meta 官方自動發文串接 (FB / Threads)
          </p>
          <div style="background: rgba(15,23,42,0.85); border: 1px solid rgba(56,189,248,0.3); border-radius: 12px; padding: 24px; max-width: 750px; margin: 0 auto; text-align: left; line-height: 1.8;">
            <p style="color:#f8fafc; font-size: 16px; margin:0;">
              📍 <strong>上課地點</strong>：台東市正氣北路166巷90號（生活管家·家宅總部）<br>
              ⏰ <strong>上課時間</strong>：2026-11-18 (週三) 14:00 - 16:00 (13:50 開放入席)<br>
              🎯 <strong>核心目標</strong>：下課前，每位夥伴的筆電上都親手裝上一台「專屬自動發射台」，把每天被社群綁架的時間徹底買回來！
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "溫故知新 · 邏輯承接",
        "title": "上週我們做出了故事海報與文案，但……然後呢？",
        "subtitle": "好內容已經誕生，為什麼我們依然感覺每天被社群折磨？",
        "content": """
        <div style="display:flex; gap:24px;">
          <div style="flex:1; background:rgba(16,185,129,0.08); border-left:4px solid #10b981; border-radius:8px; padding:20px;">
            <h3 style="color:#10b981; margin-bottom:12px;">🎉【上週的驕傲戰果】</h3>
            <p style="color:#cbd5e1; line-height:1.7;">
              • 我們每個人帶著手邊最真實的筆記、老照片與故事。<br>
              • 透過 NotebookLM 深度消化，提煉出專屬結構。<br>
              • <strong>親手產出了：專屬故事海報 ＋ 精采文案 ＋ 簡報架構！</strong><br><br>
              💡 <strong>智囊大腦已經就位</strong>：我們證明了只要工具用對，每個人都能產出高品質內容！
            </p>
          </div>
          <div style="flex:1; background:rgba(244,63,94,0.08); border-left:4px solid #f43f5e; border-radius:8px; padding:20px;">
            <h3 style="color:#f43f5e; margin-bottom:12px;">⚠️【今天面臨的現實卡點】</h3>
            <p style="color:#cbd5e1; line-height:1.7;">
              • <strong>海報做好了，但躺在電腦裡不會自己飛出去！</strong><br>
              • 開店忙備料、招呼客人，哪有時間天天開手機複製貼上？<br>
              • 每天手動搬運排版，一旦漏發，流量就斷了！<br><br>
              🚀 <strong>今天的終極使命</strong>：替內容裝上「全自動發射引擎」，一鍵飛上社群！
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "心制定錨 · 核心心法",
        "title": "AI 的應用取決於認知，學好 AI 唯有靠熟練度",
        "subtitle": "工具沒有極限，限制我們的是想像力；唯有親手實作，技術才會長在自己身上！",
        "content": """
        <div style="display:flex; gap:24px;">
          <div style="flex:1; background:rgba(245,158,11,0.08); border-left:4px solid #f59e0b; border-radius:8px; padding:24px;">
            <h3 style="color:#f59e0b; margin-bottom:14px; font-size:20px;">🧠【認知決定高度：你把 AI 當什麼？】</h3>
            <p style="color:#cbd5e1; line-height:1.8; font-size:15px;">
              • <strong>淺層認知</strong>：只把它當成聊天打字的玩具或搜尋引擎（只發揮了 5% 潛力）。<br><br>
              • <strong>高階認知</strong>：它是能看懂電腦檔案、能跑代碼、能直連 Meta 官方幫你天天推播的<strong>「24 小時數位副駕駛」</strong>！<br><br>
              🔥 <em>「你對 AI 的認知有多寬廣，AI 替你換回的自由就有多大！」</em>
            </p>
          </div>
          <div style="flex:1; background:rgba(56,189,248,0.08); border-left:4px solid #38bdf8; border-radius:8px; padding:24px;">
            <h3 style="color:#38bdf8; margin-bottom:14px; font-size:20px;">💪【熟練鍛造直覺：為什麼堅持純實體？】</h3>
            <p style="color:#cbd5e1; line-height:1.8; font-size:15px;">
              • <strong>AI 不是看書看影片就能學會的</strong>，它像煎蛋餅、學騎車一樣，是一門「肉身手感工藝」。<br><br>
              • <strong>想要學好 AI，唯一途徑就是天天摸它、跟它對話、親手踩坑排錯</strong>！熟練度到了，它就是你的第二大腦。<br><br>
              🤝 <em>這就是為什麼今天我們要坐在你身邊，親手幫你在筆電上跑通發射台！</em>
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "核心概念 · 定位解密",
        "title": "Antigravity 究竟是什麼？",
        "subtitle": "它不是一般的聊天網頁，它是住在你筆電裡的「24 小時數位發射台員工」",
        "content": """
        <div style="display:flex; gap:20px;">
          <div style="flex:1; background:rgba(244,63,94,0.08); border:1px solid rgba(244,63,94,0.2); border-radius:8px; padding:20px;">
            <h3 style="color:#f43f5e; margin-bottom:10px;">❌ 傳統網頁 AI</h3>
            <p style="color:#94a3b8; line-height:1.7;">
              • 關在瀏覽器小框框裡<br>
              • 看不到你電腦裡的資料夾<br>
              • 無法替你執行發布指令<br>
              • 每次都要你手動複製貼上
            </p>
          </div>
          <div style="flex:1; background:rgba(56,189,248,0.08); border:1px solid rgba(56,189,248,0.3); border-radius:8px; padding:20px;">
            <h3 style="color:#38bdf8; margin-bottom:10px;">⚡ Antigravity 核心能力</h3>
            <p style="color:#f8fafc; line-height:1.7;">
              • <strong>長住在你的本機電腦中</strong><br>
              • <strong>能直接讀取海報與文案</strong><br>
              • <strong>自帶執行手腳</strong>（跑 Python 腳本）<br>
              • <strong>直連 Meta 官方發布貼文</strong>
            </p>
          </div>
          <div style="flex:1; background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.3); border-radius:8px; padding:20px;">
            <h3 style="color:#f59e0b; margin-bottom:10px;">🎯 你的實體發射台</h3>
            <p style="color:#94a3b8; line-height:1.7;">
              • 就像店裡請了一位專職發射員<br>
              • 你把好料（照片文案）丟進資料夾<br>
              • 它負責打包、定時、推上時間軸！
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "現場表演 · 震撼見證",
        "title": "現場實機演示：倒數 3 秒，全自動發射！",
        "subtitle": "請大家拿出手機，打開我們的 Facebook 粉絲專頁與 Threads……",
        "content": """
        <div style="display:flex; gap:24px;">
          <div style="flex:1; background:rgba(15,23,42,0.8); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:20px;">
            <h3 style="color:#38bdf8; margin-bottom:12px;">🎬【現場實機演示流程】</h3>
            <p style="color:#cbd5e1; line-height:1.8;">
              1. 講師電腦資料夾內只有一張照片 + 一段文字<br>
              2. 講師完全不打開 FB 或 Threads 網頁<br>
              3. 終端機按下一行指令：<br>
              <code style="background:#000; color:#38bdf8; padding:4px 10px; border-radius:4px; display:inline-block; margin:6px 0;">python launch_post.py</code><br>
              4. 3秒完成：上傳圖片 ➡️ 發布貼文 ➡️ 掛載留言！
            </p>
          </div>
          <div style="flex:1; background:rgba(16,185,129,0.08); border-left:4px solid #10b981; border-radius:8px; padding:20px;">
            <h3 style="color:#10b981; margin-bottom:12px;">📱【請大家看手機驗收】</h3>
            <p style="color:#cbd5e1; line-height:1.8;">
              • <strong>Facebook 粉專</strong>：新貼文秒級上線，排版完美！<br>
              • <strong>Threads</strong>：同步推播，觸及在地演算法！<br>
              • <strong>第一則留言</strong>：自動附帶購買連結（防降權）！<br><br>
              ✨ <em>「原來每天半小時的痛苦，電腦 3 秒就能做完！」</em>
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "安全第一 · 法規護城河",
        "title": "為什麼絕對不用外掛？Meta 官方 API 才是唯一合法保險",
        "subtitle": "做生意粉專是命根子！我們要走正道，絕不拿商業資產冒險",
        "content": """
        <div style="display:flex; gap:24px;">
          <div style="flex:1; background:rgba(244,63,94,0.08); border-left:4px solid #f43f5e; border-radius:8px; padding:20px;">
            <h3 style="color:#f43f5e; margin-bottom:12px;">❌ 坊間黑心爬蟲 / 自動按鍵外掛</h3>
            <p style="color:#cbd5e1; line-height:1.8;">
              • <strong>模擬真人點擊</strong>：Meta 演算法天天抓異常連線。<br>
              • <strong>封號風險極高</strong>：辛苦經營的粉專一夕被鎖。<br>
              • <strong>密碼外洩危機</strong>：把帳密交給不知名外掛，隨時被盜刷或綁架。
            </p>
          </div>
          <div style="flex:1; background:rgba(16,185,129,0.08); border-left:4px solid #10b981; border-radius:8px; padding:20px;">
            <h3 style="color:#10b981; margin-bottom:12px;">⭕ Meta 官方 Graph API 直連</h3>
            <p style="color:#cbd5e1; line-height:1.8;">
              • <strong>官方合法發放執照</strong>：官方給予的開發者安全憑證。<br>
              • <strong>永不封號</strong>：走合法通道推播，受 Meta 官方正式保障。<br>
              • <strong>極星資安鐵律</strong>：敏感金鑰鎖在本地 .secrets.env，絕不上傳公網，100% 保障粉專主權！
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "通行證步驟 1 / 5",
        "title": "第 1 步：進入 Meta 開發者後台，建立 App",
        "subtitle": "developers.facebook.com ➡️ 點右上角【建立應用程式】",
        "content": """
        <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:24px; line-height:1.9; font-size:16px;">
          1. 打開瀏覽器，前往：<code style="color:#f59e0b;">developers.facebook.com</code><br>
          2. 登入自己的 Facebook 帳號，點右上角<strong>【建立應用程式 (Create App)】</strong>。<br>
          3. <strong>【關鍵選擇】</strong>：用途請選<strong>「其他 (Other)」 ➡️ 「企業商家 (Business)」</strong>！<br>
          4. 命名應用程式（例如：<code>佩真早餐發射台</code>），按下建立。<br><br>
          ⚠️ <strong>避坑提醒</strong>：為什麼一定要選 Business？因為只有這個類型，Meta 才會開放「管理粉絲專頁貼文」的完整 API 權限！
        </div>
        """
    },
    {
        "tag": "通行證步驟 2 / 5",
        "title": "第 2 步：打開「圖形 API 測試工具」金鑰工廠",
        "subtitle": "點擊頂部【工具】 ➡️ 【圖形 API 測試工具 (Graph API Explorer)】",
        "content": """
        <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:24px; line-height:1.9; font-size:16px;">
          1. 點擊頂部導覽列<strong>【工具 (Tools)】</strong> ➡️ <strong>【圖形 API 測試工具】</strong>。<br>
          2. 右側面板頂部確認：<br>
          &nbsp;&nbsp;• <strong>Meta 應用程式</strong>：選取剛才建立的 App。<br>
          &nbsp;&nbsp;• <strong>用戶或粉絲專頁</strong>：先維持預設的 User Token。<br><br>
          💡 <strong>這是在做什麼？</strong> 這裡就是 Meta 的「鑰匙打製工廠」！我們要向 Meta 申請發文權限，並把剛打好的鑰匙領回電腦裡。
        </div>
        """
    },
    {
        "tag": "通行證步驟 3 / 5",
        "title": "第 3 步：破解權限陷阱，新增發文通行證",
        "subtitle": "在右側 Permissions 下拉選單中勾選兩大發文必備權限",
        "content": """
        <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:24px; line-height:1.9; font-size:16px;">
          1. 在右側 <strong>Permissions (權限)</strong> 下拉選單中，加入以下兩項：<br>
          &nbsp;&nbsp;✅ <strong style="color:#10b981;">pages_manage_posts</strong>（允許替粉專發布貼文）<br>
          &nbsp;&nbsp;✅ <strong style="color:#10b981;">pages_read_engagement</strong>（允許讀取留言）<br>
          2. 點擊藍色按鈕<strong>【Generate Access Token (產生存取權杖)】</strong>。<br>
          3. ⚠️ <strong>授權彈窗重點</strong>：在跳出的 Facebook 授權畫面中，<strong>務必勾選您要發文的「粉絲專頁」</strong>，並一路點選「繼續」與「完成」！
        </div>
        """
    },
    {
        "tag": "通行證步驟 4 / 5",
        "title": "第 4 步：致命關鍵！切換為「Page Token」",
        "subtitle": "全場最關鍵步驟！90% 的新手失敗，都是因為拿個人 Token 發文！",
        "content": """
        <div style="display:flex; gap:20px;">
          <div style="flex:1; background:rgba(244,63,94,0.08); border-left:4px solid #f43f5e; border-radius:8px; padding:20px;">
            <h3 style="color:#f43f5e; margin-bottom:10px;">❌ 新手最常犯的錯誤</h3>
            <p style="color:#cbd5e1; line-height:1.7;">
              • 剛才產生的代碼是「用戶個人權杖 (User Token)」。<br>
              • 拿個人權杖發粉專，Meta 會無情報錯：<code>(#200) Insufficient permission</code>！
            </p>
          </div>
          <div style="flex:1; background:rgba(16,185,129,0.08); border-left:4px solid #10b981; border-radius:8px; padding:20px;">
            <h3 style="color:#10b981; margin-bottom:10px;">⭕ 唯一正確解法（黃金動作）</h3>
            <p style="color:#cbd5e1; line-height:1.7;">
              1. 點開【User or Page】下拉選單。<br>
              2. <strong>點選您的「粉絲專頁名稱」！</strong><br>
              3. 上方的 Access Token 欄位會瞬間刷新成一串全新字串！<br>
              4. <strong>這串新代碼，才是真正能替粉專發文的「Page Token」！</strong>
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "通行證步驟 5 / 5",
        "title": "第 5 步：一鍵升級為「60 天無敵長效金鑰」",
        "subtitle": "點擊 Token 旁藍色 (i) 驚嘆號圖示 ➡️ 一鍵延長為 60 天！",
        "content": """
        <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:24px; line-height:1.9; font-size:16px;">
          1. 點擊 Access Token 欄位旁邊的<strong>藍色圓形 <code>ⓘ</code> 圖示</strong>。<br>
          2. 點擊<strong>【在存取權杖工具中開啟】</strong>。<br>
          3. 滑到最下方，點擊藍色按鈕<strong>【Extend Access Token (延長存取權杖)】</strong>！<br>
          4. 複製這串代碼，貼入桌面的 <code>.secrets.env</code> 保險箱中：<br>
          <div style="background:#000; color:#38bdf8; padding:10px 14px; border-radius:6px; margin:10px 0; font-family:monospace;">
            FB_PAGE_ID=你的粉專數字ID<br>
            FB_PAGE_ACCESS_TOKEN=EAA...（60天長效金鑰）
          </div>
          🎉 從此你的電腦就擁有了 60 天不中斷的合法發射權限！
        </div>
        """
    },
    {
        "tag": "發射原理 · 核心機制",
        "title": "為什麼發文要分兩段？社群 API 的行李托運定律",
        "subtitle": "生活比喻：出國託運行李，不能把行李箱直接塞進登機證！",
        "content": """
        <div style="display:flex; gap:24px;">
          <div style="flex:1; background:rgba(245,158,11,0.08); border-left:4px solid #f59e0b; border-radius:8px; padding:20px;">
            <h3 style="color:#f59e0b; margin-bottom:12px;">🧳 生活比喻：出國機場託運行李</h3>
            <p style="color:#cbd5e1; line-height:1.8;">
              • 你去搭飛機，不能直接把 28 吋大行李箱塞進登機證裡。<br>
              • 流程一定是：<br>
              &nbsp;&nbsp;1. 先去櫃檯把行李放上輸送帶 ➡️ 領取一張<strong>「行李吊牌號碼」</strong>。<br>
              &nbsp;&nbsp;2. 接著拿著你的護照、機票 ＋ 行李吊牌，一起登機出發！
            </p>
          </div>
          <div style="flex:1; background:rgba(56,189,248,0.08); border-left:4px solid #38bdf8; border-radius:8px; padding:20px;">
            <h3 style="color:#38bdf8; margin-bottom:12px;">🌐 Meta 伺服器的嚴格規定</h3>
            <p style="color:#cbd5e1; line-height:1.8;">
              • 圖片檔案通常幾 MB，文案文字只有幾百個字。<br>
              • <strong>第一步</strong>：電腦先把照片送上傳送帶，取得一組官方吊牌 <code>media_id</code>。<br>
              • <strong>第二步</strong>：把文案與這組 <code>media_id</code> 合體，正式向時間軸發射！
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "發射原理 · 第一階段",
        "title": "第一階段：上傳圖片取得行李吊牌 (Media ID)",
        "subtitle": "照片先上傳，但「先不要公開」，拿到號碼牌才算數",
        "content": """
        <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:24px; line-height:1.9; font-size:16px;">
          <strong>📡 電腦在後台做的事情：</strong><br>
          程式讀取你準備好的照片檔案，發送給 Meta 伺服器：<br>
          <div style="background:#000; color:#38bdf8; padding:10px 14px; border-radius:6px; margin:10px 0; font-family:monospace;">
            POST https://graph.facebook.com/v20.0/{PAGE_ID}/photos<br>
            檔案: photo.jpg ｜ 參數: published=false（暗號：先別公開！）
          </div>
          <strong>🎫 Meta 伺服器回傳號碼牌：</strong><br>
          <div style="background:#000; color:#10b981; padding:10px 14px; border-radius:6px; margin:10px 0; font-family:monospace;">
            { "id": "1164717469570488" }
          </div>
          這組數字就是照片在 Meta 雲端的代號！有了它，我們就能進行下一步的正式發布。
        </div>
        """
    },
    {
        "tag": "發射原理 · 第二階段",
        "title": "第二階段：文案與號碼牌合體推播 (Feed Publish)",
        "subtitle": "把上週寫好的故事文案，掛上號碼牌，瞬間打進時間軸",
        "content": """
        <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:24px; line-height:1.9; font-size:16px;">
          <strong>🚀 發射指令打包：</strong><br>
          程式將你的文字文案與剛才拿到的號碼牌打包成包裹：<br>
          <div style="background:#000; color:#38bdf8; padding:10px 14px; border-radius:6px; margin:10px 0; font-family:monospace;">
            POST https://graph.facebook.com/v20.0/{PAGE_ID}/feed<br>
            message: "上週我們用 NotebookLM 整理的故事..."<br>
            attached_media: [ {"media_fbid": "1164717469570488"} ]
          </div>
          🎉 <strong>貼文秒級出現在全世界面前！</strong><br>
          點擊送出後 0.5 秒，Meta 伺服器確認入庫，打開手機粉專，貼文已經穩穩掛在第一篇！
        </div>
        """
    },
    {
        "tag": "行銷絕技 · 自動暗樁",
        "title": "第三階段：自動暗樁！第一則留言防降權引流",
        "subtitle": "為什麼高手都不在主文放外部連結？用程式幫你秒回第一則留言",
        "content": """
        <div style="display:flex; gap:24px;">
          <div style="flex:1; background:rgba(244,63,94,0.08); border-left:4px solid #f43f5e; border-radius:8px; padding:20px;">
            <h3 style="color:#f43f5e; margin-bottom:12px;">❌ 主文放連結：被砍 50% 觸及</h3>
            <p style="color:#cbd5e1; line-height:1.7;">
              • Meta 最痛恨貼文把用戶帶離臉書（例如外部購買網址、Google表單、LINE連結）。<br>
              • <strong>一旦主文含有網址，演算法直接砍你觸及率！</strong>
            </p>
          </div>
          <div style="flex:1; background:rgba(16,185,129,0.08); border-left:4px solid #10b981; border-radius:8px; padding:20px;">
            <h3 style="color:#10b981; margin-bottom:12px;">⭕ 自動暗樁：主文講故事、留言引流</h3>
            <p style="color:#cbd5e1; line-height:1.7;">
              • 主文乾乾淨淨，專注講好動人的故事（觸及率 100% 滿載）。<br>
              • <strong>貼文發出後 1 秒，程式自動在下方發布第一則留言</strong>：<br>
              <code style="background:#000; color:#38bdf8; padding:4px 8px; border-radius:4px; display:inline-block; margin-top:6px;">💬「想了解更多或填表報名，請點留言連結...」</code>
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "高維進化 · 人機協同",
        "title": "步驟太多記不住？讓 AI Agent 變成你的「隨身教練」！",
        "subtitle": "你動嘴、AI 跑腿：今天不用背指令，打開對話框，Agent 一步一步帶著你做",
        "content": """
        <div style="display:flex; gap:24px;">
          <div style="flex:1; background:rgba(168,85,247,0.08); border-left:4px solid #a855f7; border-radius:8px; padding:20px;">
            <h3 style="color:#a855f7; margin-bottom:12px;">💡 傳統教學 vs Agentic 新時代</h3>
            <p style="color:#cbd5e1; line-height:1.8;">
              • <strong>過去的做法</strong>：背指令、記路徑、開黑色終端機（非工程師頭皮發麻）。<br><br>
              • <strong>Antigravity 的降維打擊</strong>：<br>
              &nbsp;&nbsp;👉 你的筆電裡坐著一位極有耐心的專屬助教！<br>
              &nbsp;&nbsp;👉 它看得到你的電腦、會替你建保險箱、會替你檢查照片。<br>
              &nbsp;&nbsp;👉 你只要跟它像朋友一樣打字對話，它就一步一步指引你完成！
            </p>
          </div>
          <div style="flex:1; background:rgba(56,189,248,0.08); border-left:4px solid #38bdf8; border-radius:8px; padding:20px;">
            <h3 style="color:#38bdf8; margin-bottom:12px;">🤖 專屬教練的 4 大主動能力</h3>
            <p style="color:#cbd5e1; line-height:1.8;">
              1. <strong>主動指引</strong>：手把手問你「建好 App 了嗎？拿到 Token 了嗎？」。<br>
              2. <strong>物理操作</strong>：你把金鑰貼給它，它自動幫你寫入 <code>.secrets.env</code>。<br>
              3. <strong>素材審查</strong>：自動看桌面有沒有照片，幫你排版文案。<br>
              4. <strong>一鍵發射</strong>：你說一聲「確認發射」，它立刻調用官方 API 直送時間軸！
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "對話實戰 · 狀態機流程",
        "title": "4 句對話，發射台全自動通關！",
        "subtitle": "學員視角：看看你如何像主管交代助理一樣，輕鬆完成發布",
        "content": """
        <div style="display:flex; gap:24px;">
          <div style="flex:1; background:rgba(15,23,42,0.8); border:1px solid rgba(56,189,248,0.25); border-radius:8px; padding:20px;">
            <h4 style="color:#38bdf8; margin-bottom:8px;">💬 對話 1：啟動發射教練</h4>
            <p style="color:#cbd5e1; line-height:1.6; font-size:14px; margin-bottom:16px;">
              學員：「我上週的海報文案準備好了，請一步一步帶我打造發射台！」<br>
              <span style="color:#38bdf8;">Agent：「沒問題！請打開 developers.facebook.com...」</span>
            </p>
            <h4 style="color:#10b981; margin-bottom:8px;">💬 對話 2：自動保管金鑰</h4>
            <p style="color:#cbd5e1; line-height:1.6; font-size:14px;">
              學員：「這是我的 Page Token：EAA...」<br>
              <span style="color:#10b981;">Agent：「已收到！我已幫您安全鎖入 .secrets.env 保險箱！」</span>
            </p>
          </div>
          <div style="flex:1; background:rgba(15,23,42,0.8); border:1px solid rgba(245,158,11,0.25); border-radius:8px; padding:20px;">
            <h4 style="color:#f59e0b; margin-bottom:8px;">💬 對話 3：素材排版確認</h4>
            <p style="color:#cbd5e1; line-height:1.6; font-size:14px; margin-bottom:16px;">
              學員：「照片在桌上了，文案我想寫：用手作溫度開啟...」<br>
              <span style="color:#f59e0b;">Agent：「已偵測到 photo.jpg！文案排版如上，請確認！」</span>
            </p>
            <h4 style="color:#a855f7; margin-bottom:8px;">💬 對話 4：秒級推播與回報</h4>
            <p style="color:#cbd5e1; line-height:1.6; font-size:14px;">
              學員：「確認，發射！」<br>
              <span style="color:#a855f7;">Agent：「🎉 貼文秒級上線！第一則留言已掛載，快看手機！」</span>
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "現場實作 · 全程常駐看板",
        "title": "【實機開練】跟著你的 AI 隨身助教，三步跑通發射台！",
        "subtitle": "打開 Antigravity，輸入第一句話，助教坐在你電腦裡帶著你做！",
        "content": """
        <div style="display:flex; gap:20px;">
          <div style="flex:1; background:rgba(245,158,11,0.08); border-top:4px solid #f59e0b; border-radius:8px; padding:20px;">
            <div style="font-size:32px; font-weight:bold; color:#f59e0b; margin-bottom:8px;">01</div>
            <h3 style="color:#ffffff; margin-bottom:8px;">輸入通關密語</h3>
            <p style="color:#cbd5e1; line-height:1.7;">
              在 Antigravity 對話框輸入：<br>
              <strong style="color:#f59e0b;">「請一步一步帶我打造社群發射台」</strong><br>
              教練 Agent 立刻啟動專屬引導！
            </p>
          </div>
          <div style="flex:1; background:rgba(56,189,248,0.08); border-top:4px solid #38bdf8; border-radius:8px; padding:20px;">
            <div style="font-size:32px; font-weight:bold; color:#38bdf8; margin-bottom:8px;">02</div>
            <h3 style="color:#ffffff; margin-bottom:8px;">依序對話通關</h3>
            <p style="color:#cbd5e1; line-height:1.7;">
              • 根據教練提示提供 Token<br>
              • 教練自動建立 .secrets.env<br>
              • 把照片與文案交代給教練
            </p>
          </div>
          <div style="flex:1; background:rgba(16,185,129,0.08); border-top:4px solid #10b981; border-radius:8px; padding:20px;">
            <div style="font-size:32px; font-weight:bold; color:#10b981; margin-bottom:8px;">03</div>
            <h3 style="color:#ffffff; margin-bottom:8px;">對話一鍵發射</h3>
            <p style="color:#cbd5e1; line-height:1.7;">
              對教練說：<strong>「確認發射！」</strong><br>
              • 觀察後台秒級推播 ➡️ 自動留言<br>
              • 拿出手機，親眼見證貼文出現在粉專！
            </p>
          </div>
        </div>
        """
    },
    {
        "tag": "總結與帶走資產 · 下週預告",
        "title": "今天帶走的不是一張證書，而是一套自轉系統！",
        "subtitle": "恭喜大家跨過數位轉型最高的一道門檻！",
        "content": """
        <div style="display:flex; gap:24px;">
          <div style="flex:1; background:rgba(16,185,129,0.08); border-left:4px solid #10b981; border-radius:8px; padding:20px;">
            <h3 style="color:#10b981; margin-bottom:12px;">🎁【今天你帶回家的 3 大數位資產】</h3>
            <p style="color:#cbd5e1; line-height:1.8;">
              1. <strong>實體自動發射台工具包</strong>：回家只要把新照片和新文字丟進去，點一下就自動發文！<br>
              2. <strong>Meta 官方 60 天合法長效通行證</strong>：合規穩定，再也不怕被封號。<br>
              3. <strong>把時間買回來的主權</strong>：從此告別每天手動複製貼上，省下時間專心顧店與生活！
            </p>
          </div>
          <div style="flex:1; background:rgba(245,158,11,0.08); border-left:4px solid #f59e0b; border-radius:8px; padding:20px;">
            <h3 style="color:#f59e0b; margin-bottom:12px;">🔮【下週預告 · 第 3 講】</h3>
            <p style="color:#cbd5e1; line-height:1.8;">
              <strong>《數據架構 ✕ 品牌人設工程：打造專屬語氣的 AI 管家》</strong><br><br>
              • 自動發文跑通了，但文案怎麼越寫越像你？<br>
              • 怎麼讓 AI 像「闆娘親自說話」一樣親切接地氣？<br>
              • 下週三下午 14:00，正氣北路家宅總部見！
            </p>
          </div>
        </div>
        """
    }
]

html_template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <title>2026 秋季 AI 家教實戰系列班 · 第 2 講教學簡報</title>
  <style>
    body {{
      background-color: #0a0f1d;
      color: #f8fafc;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans TC", "Microsoft JhengHei", sans-serif;
      margin: 0;
      padding: 40px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .slide-card {{
      background: #121a2f;
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: 16px;
      width: 100%;
      max-width: 1050px;
      margin-bottom: 40px;
      padding: 36px 40px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      position: relative;
    }}
    .slide-tag {{
      display: inline-block;
      font-size: 13px;
      font-weight: bold;
      color: #38bdf8;
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 4px 12px;
      border-radius: 20px;
      margin-bottom: 12px;
    }}
    .slide-num {{
      position: absolute;
      top: 36px;
      right: 40px;
      font-size: 14px;
      color: #64748b;
      font-weight: bold;
    }}
    .slide-title {{
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
      margin: 0 0 8px 0;
    }}
    .slide-subtitle {{
      font-size: 15px;
      color: #94a3b8;
      margin: 0 0 24px 0;
    }}
    code {{
      font-family: Consolas, Monaco, monospace;
    }}
  </style>
</head>
<body>

  {slides_html}

</body>
</html>
"""

cards_html = []
for idx, s in enumerate(slides_data):
    card = f"""
    <div class="slide-card" id="slide-{idx+1}">
      <span class="slide-tag">{s['tag']}</span>
      <span class="slide-num">{idx+1:02d} / {len(slides_data):02d}</span>
      <h2 class="slide-title">{s['title']}</h2>
      <p class="slide-subtitle">{s['subtitle']}</p>
      <div class="slide-body">
        {s['content']}
      </div>
    </div>
    """
    cards_html.append(card)

full_html = html_template.format(slides_html="\n".join(cards_html))

# Write to Workspace
workspace_file = r"c:\Users\lenovo\我的雲端硬碟\00_Master_Polaris\00-05_AI_Education\2026_Autumn_AI_Tutoring_Series\Lesson_02_Antigravity_Meta_Automation\slides.html"
with open(workspace_file, "w", encoding="utf-8-sig") as f:
    f.write(full_html)

# Write to Desktop
desktop_file = r"C:\Users\lenovo\Desktop\第2講教學簡報.html"
with open(desktop_file, "w", encoding="utf-8-sig") as f:
    f.write(full_html)

print("Bulletproof HTML slides successfully generated!")
