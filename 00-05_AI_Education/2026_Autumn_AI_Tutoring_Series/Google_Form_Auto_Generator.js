function createPolarisRegistrationForm() {
  var form = FormApp.create('2026 秋季 AI 家教實戰系列班 · 第 1 講【實體入席申請表】');
  
  form.setDescription(
    '【限額 10 席 · 純實體現場教學 · 解決真實生意難題】\n\n' +
    '各位好朋友、老夥伴您好：\n' +
    '歡迎申請由生活管家創辦人 陳品碩（闆仔）親自授權主講之「AI 家教實戰系列班 · 第 1 講」。\n\n' +
    '⚠️【入席重要須知】\n' +
    '1. 本課程堅持 100% 純實體現場教學，絕無線上同步！導師極度嚴厲，現場手把手巡桌排錯，保證做出專屬成果。\n' +
    '2. 為了確保「每人一台螢幕個別指導」的最高教學品質，現場嚴格限額 10 席，多一張椅子都不加。\n' +
    '3. 若申請人數超過 10 名，將依「硬體準備完整度」與「業務情境契合度」進行審查分流；未排入本梯次之夥伴，將優先為您保留至【第二梯次加開場】，敬請理解與體諒。\n\n' +
    '📍 上課地點：生活管家·家宅總部（台東市正氣北路166巷90號）\n' +
    '⏰ 上課時間：每週三下午 14:00 - 16:00\n' +
    '💰 學費政策：老學員免收學費（0元免單回娘家特權）｜ 全新夥伴單堂實戰 NT$ 500 元（審查通過後通知付款）\n' +
    '💬 官方諮詢 LINE：https://lin.ee/z83YSq6 （加入後可直接私訊管家）'
  );

  form.setConfirmationMessage(
    '🎉 感謝您的填寫！我們已成功收到您的入席申請。\n\n' +
    '闆仔與教學團隊將於 24 小時內完成硬體與情境審查，並透過官方 LINE / 簡訊向您發送【正取確認通知】或【加開場優先保留通知】。\n\n' +
    '📍 上課地點：台東市正氣北路166巷90號（生活管家總部）\n' +
    '💬 官方 LINE 諮詢：https://lin.ee/z83YSq6\n\n' +
    '生活管家 敬上'
  );

  // 區塊一：基本資料
  form.addSectionHeaderItem().setTitle('📋 第一部分：基本資料與身分確認');
  
  var nameItem = form.addTextItem().setTitle('1. 您的真實姓名').setRequired(true);
  var phoneItem = form.addTextItem().setTitle('2. 您的聯絡電話 / 手機號碼').setHelpText('用於審查通過後發送正取報到通知簡訊').setRequired(true);
  var lineItem = form.addTextItem().setTitle('3. 您的 LINE ID 或 稱呼').setHelpText('便於教學團隊個別聯繫與行前提醒（亦可直接加入官方 LINE：https://lin.ee/z83YSq6 私訊我們）').setRequired(true);
  
  var identityItem = form.addMultipleChoiceItem();
  identityItem.setTitle('4. 您的學員身分')
    .setChoiceValues([
      '👑 生活管家老學員（享有回娘家 0 元免收學費特權）',
      '🌟 全新夥伴（單堂實戰 NT$ 500 元，通過審查後提供付款資訊）'
    ])
    .setRequired(true);

  // 區塊二：硬體與軟體環境自檢
  form.addSectionHeaderItem().setTitle('💻 第二部分：設備與帳號自檢（確保現場實作零阻礙）');

  var deviceItem = form.addMultipleChoiceItem();
  deviceItem.setTitle('5. 上課當天您預計攜帶的設備')
    .setChoiceValues([
      '筆記型電腦 (Windows 系統)',
      '筆記型電腦 (Mac / Apple 系統)',
      '⚠️ 平板電腦 (iPad / Android 平板) —— 建議自備外接鍵盤以利檔案操作'
    ])
    .setRequired(true);

  var checkItem = form.addCheckboxItem();
  checkItem.setTitle('6. 軟體環境與前置準備勾選（請全數確認）')
    .setChoiceValues([
      '已確認電腦安裝有 Google Chrome 瀏覽器',
      '確定記得自己的 Google 帳號與密碼（現場需登入 NotebookLM 實作）',
      '筆電可正常連接 Wi-Fi 無線網路',
      '確定當天會攜帶筆電原廠充電器 / 電源線'
    ])
    .setRequired(true);

  // 區塊三：業務情境與需求
  form.addSectionHeaderItem().setTitle('🎯 第三部分：業務痛點與資料診斷（為闆仔備課備料）');

  var industryItem = form.addTextItem();
  industryItem.setTitle('7. 您目前從事的行業或主要業務內容')
    .setHelpText('例如：早午餐店、伴手禮電商、長照服務、社區營造、接案業務等')
    .setRequired(true);

  var problemItem = form.addCheckboxItem();
  problemItem.setTitle('8. 本次上課，您最想帶哪種資料丟進 AI 幫您解決問題？（可複選）')
    .setChoiceValues([
      '店內菜單、商品規格或歷史進貨報價單（精算與自動答覆）',
      '密密麻麻的活動企劃案、長篇補助案公文（快速摘要與深挖）',
      '顧客常見疑難雜症、客服問答紀錄（打造零幻覺客服庫）',
      '店鋪營運規章、員工教育訓練手冊（打造數位店長）',
      '其他個人研究資料或筆記'
    ])
    .setRequired(true);

  // 區塊四：名額與加開分流意願
  form.addSectionHeaderItem().setTitle('🔒 第四部分：限額 10 席與加開梯次分流');

  var queueItem = form.addMultipleChoiceItem();
  queueItem.setTitle('9. 入席承諾與候補加開意願')
    .setChoiceValues([
      '我已確認時間（每週三 14:00-16:00），審查通過我一定準時出席！',
      '若本週 10 名正取已滿，我非常希望參加【第二梯次加開場】，請第一時間通知我！'
    ])
    .setRequired(true);

  Logger.log('Published URL: ' + form.getPublishedUrl());
  Logger.log('Edit URL: ' + form.getEditUrl());
}
