function createWorksheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // 定義要建立的所有工作表名稱
  const sheetNames = [
    "Raw_Orders", "Raw_Customers", "Raw_Feedback", 
    "Raw_HR_Attendance", "Raw_HR_Recruit", "Raw_Inventory",
    "Dashboard_Daily", "KPI_Staff", "Project_Tracker", 
    "CRM", "Sales_Funnel", "Feedback_Analysis", 
    "Finance_Cashflow", "Finance_Cost", "Order_Analysis"
  ];
  
  sheetNames.forEach(name => {
    // 檢查工作表是否已存在，避免重複建立導致報錯
    let sheet = ss.getSheetByName(name);
    if (!sheet) {
      sheet = ss.insertSheet(name);
      
      // 根據分類自動上色，讓介面更易讀
      if (name.startsWith("Raw_")) {
        sheet.setTabColor("#ea4335"); // 紅色：原始數據
      } else if (name.startsWith("Dashboard") || name.startsWith("KPI")) {
        sheet.setTabColor("#4285f4"); // 藍色：視覺化/指標
      } else if (name.startsWith("Finance")) {
        sheet.setTabColor("#34a853"); // 綠色：財務
      } else {
        sheet.setTabColor("#fbbc04"); // 黃色：管理/分析
      }
      
      // 簡單的標題初始化範例
      sheet.getRange(1, 1).setValue(name + " 表頭預留位").setFontWeight("bold");
    }
  });
  
  SpreadsheetApp.getUi().alert("✅ 所有工作表已建立並分類完成！");
}