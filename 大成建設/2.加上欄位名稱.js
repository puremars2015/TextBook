function setupStructuredWorksheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // 定義工作表與其對應的欄位標題 (字典格式)
  const config = {
    "Raw_Orders": ["日期", "訂單編號", "客戶", "產品", "數量", "單價", "金額", "是否新客", "是否退貨", "來源渠道", "員工", "訪客數"],
    "Raw_Customers": ["公司", "聯絡人", "電話", "Email", "需求", "狀態", "最後聯絡日", "業務負責人"],
    "Raw_Feedback": ["日期", "客戶", "留言", "來源", "處理狀態"],
    "Raw_HR_Attendance": ["員工", "日期", "上班時間", "下班時間", "加班時數"],
    "Raw_HR_Recruit": ["姓名", "職位", "來源", "面試狀態", "評價摘要"],
    "Raw_Inventory": ["商品", "當前庫存", "安全庫存", "本月進貨", "本月出貨", "補貨建議"],
    "Dashboard_Daily": ["日期", "訂單數", "銷售額", "新客戶數", "退貨數", "總訪客數", "轉換率"],
    "KPI_Staff": ["員工", "銷售額", "目標", "達成率", "排名", "AI評語"],
    "Project_Tracker": ["任務", "負責人", "開始日", "截止日", "狀態", "進度%", "延誤風險", "AI週報摘要"],
    "CRM": ["公司", "聯絡人", "電話", "需求", "狀態", "最後聯絡日", "下一步建議"],
    "Sales_Funnel": ["階段", "客戶數"],
    "Feedback_Analysis": ["日期", "客戶留言", "情緒", "分類", "建議處理"],
    "Finance_Cashflow": ["日期", "項目", "收入", "支出", "類別", "月份"],
    "Finance_Cost": ["產品", "材料", "人工", "物流", "總成本"],
    "Order_Analysis": ["日期", "客戶", "產品", "數量", "金額", "月份"]
  };

  for (let sheetName in config) {
    let sheet = ss.getSheetByName(sheetName);
    
    // 如果不存在則建立
    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
    } else {
      sheet.clear(); // 如果已存在，清除舊資料重新寫入標題
    }

    // 1. 寫入標題列 (A1 開始)
    const headers = config[sheetName];
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

    // 2. 格式化標題列
    sheet.getRange(1, 1, 1, headers.length)
         .setBackground("#444444") // 深灰色背景
         .setFontColor("#ffffff") // 白色文字
         .setFontWeight("bold")   // 粗體
         .setHorizontalAlignment("center");

    // 3. 凍結第一列
    sheet.setFrozenRows(1);

    // 4. 根據類型上色分頁標籤
    setTabTheme(sheet, sheetName);
  }

  SpreadsheetApp.getUi().alert("🚀 15 個分頁已建立，欄位標題與格式化已自動完成！");
}

// 輔助函式：根據名稱為分頁標籤上色
function setTabTheme(sheet, name) {
  if (name.includes("Raw_")) {
    sheet.setTabColor("#ea4335"); // 紅：原始數據
  } else if (name.includes("Dashboard") || name.includes("KPI")) {
    sheet.setTabColor("#4285f4"); // 藍：關鍵指標
  } else if (name.includes("Finance")) {
    sheet.setTabColor("#34a853"); // 綠：財務
  } else {
    sheet.setTabColor("#fbbc04"); // 黃：分析與管理
  }
}