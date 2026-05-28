const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Hermes Agent 實戰監控手冊";
pres.author = "Hermes Agent 學院";

// Color palette - Ocean Fintech theme
const C = {
  navy: "0F2C4A",
  teal: "0288A8",
  mint: "00B4A0",
  light: "E8F4F8",
  white: "FFFFFF",
  dark: "1A1A2E",
  gray: "64748B",
  lightGray: "CBD5E1",
  gold: "F59E0B",
};

function makeShadow() {
  return { type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.12 };
}

// =============================================
// SLIDE 1: Title
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.dark };

  // Decorative gradient bar top
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.08,
    fill: { color: C.teal }
  });

  // Large icon circle
  slide.addShape(pres.shapes.OVAL, {
    x: 4.1, y: 0.7, w: 1.8, h: 1.8,
    fill: { color: C.teal },
    shadow: makeShadow()
  });
  slide.addText("📡", {
    x: 4.1, y: 0.85, w: 1.8, h: 1.5,
    fontSize: 54, align: "center", valign: "middle"
  });

  // Title
  slide.addText("Hermes Agent", {
    x: 0.5, y: 2.6, w: 9, h: 0.9,
    fontSize: 46, fontFace: "Arial Black", bold: true,
    color: C.white, align: "center", margin: 0
  });
  slide.addText("實戰監控手冊", {
    x: 0.5, y: 3.4, w: 9, h: 0.8,
    fontSize: 36, fontFace: "Georgia", italic: true,
    color: C.mint, align: "center", margin: 0
  });

  // Subtitle
  slide.addText("學院專用 / 對話式操作教材", {
    x: 0.5, y: 4.4, w: 9, h: 0.5,
    fontSize: 18, color: C.lightGray, align: "center"
  });

  // Bottom bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.3, w: 10, h: 0.325,
    fill: { color: C.teal }
  });
  slide.addText("台積電 · 白銀 · 台股加權指數 · TradingView · 自動監控", {
    x: 0.5, y: 5.32, w: 9, h: 0.3,
    fontSize: 13, color: C.dark, align: "center", bold: true
  });
}

// =============================================
// SLIDE 2: 目錄
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.light };

  // Header
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.1,
    fill: { color: C.navy }
  });
  slide.addText("📋  內容大綱", {
    x: 0.6, y: 0.3, w: 8.8, h: 0.6,
    fontSize: 32, fontFace: "Arial Black", bold: true,
    color: C.white, margin: 0
  });

  const chapters = [
    { num: "01", title: "事前準備", desc: "環境確認與第一次上課檢查清單" },
    { num: "02", title: "查台積電股價", desc: "3 個來源：investing.com · Yahoo Finance · TWSE" },
    { num: "03", title: "查白銀價格", desc: "investing.com · goldprice.org 即時報價" },
    { num: "04", title: "查台股加權指數", desc: "Yahoo Finance 台灣加權股價指數報價" },
    { num: "05", title: "TradingView 圖表", desc: "日K、KD 指標、均線技術分析" },
    { num: "06", title: "自動監控設定", desc: "每小時/每日推播、Cron Job 實作" },
    { num: "07", title: "多重監控組合", desc: "三合一報價、晨報自動推播" },
  ];

  chapters.forEach((ch, i) => {
    const col = i < 4 ? 0 : 1;
    const row = i < 4 ? i : i - 4;
    const x = col === 0 ? 0.5 : 5.2;
    const y = 1.35 + row * 1.0;

    // Number badge
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.55, h: 0.75,
      fill: { color: C.teal }, margin: 0
    });
    slide.addText(ch.num, {
      x, y: y + 0.1, w: 0.55, h: 0.55,
      fontSize: 16, bold: true, color: C.white, align: "center", valign: "middle"
    });

    // Content card
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.6, y, w: 3.9, h: 0.75,
      fill: { color: C.white },
      shadow: makeShadow(), margin: 0
    });
    slide.addText(ch.title, {
      x: x + 0.75, y: y + 0.05, w: 3.6, h: 0.38,
      fontSize: 14, bold: true, color: C.navy, margin: 0
    });
    slide.addText(ch.desc, {
      x: x + 0.75, y: y + 0.38, w: 3.6, h: 0.32,
      fontSize: 10, color: C.gray, margin: 0
    });
  });
}

// =============================================
// SLIDE 3: 事前準備
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.white };

  // Left accent bar
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.12, h: 5.625,
    fill: { color: C.teal }
  });

  // Header
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.12, y: 0, w: 9.88, h: 1.1,
    fill: { color: C.navy }
  });
  slide.addText("01  事前準備", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontSize: 30, fontFace: "Arial Black", bold: true,
    color: C.white, margin: 0
  });

  // Requirements table
  const reqData = [
    ["項目", "說明", "驗證方式"],
    ["Telegram 帳號", "與 Hermes Agent 已連線", "傳「你好」有回覆"],
    ["Hermes Agent 已啟動", "Docker 或本機皆可", "curl localhost:8642/health → {\"status\":\"ok\"}"],
    ["網路連線正常", "能訪問目標網站", "瀏覽器能開啟 investing.com"],
    ["學員等級", "不需技術背景，會用網頁即可", "—"],
  ];
  slide.addTable(reqData, {
    x: 0.5, y: 1.25, w: 9, h: 2.0,
    colW: [2.2, 3.5, 3.3],
    fontFace: "Arial",
    fontSize: 12,
    color: C.navy,
    border: { pt: 0.5, color: C.lightGray },
    rowH: [0.4, 0.4, 0.4, 0.4, 0.4],
    fill: { color: C.white },
  });

  // Checklist title
  slide.addText("✅ 第一次上課檢查清單", {
    x: 0.5, y: 3.4, w: 4, h: 0.4,
    fontSize: 16, bold: true, color: C.navy, margin: 0
  });

  const checks = [
    "在 Telegram 傳送「你好」→ 確認 Agent 有回覆",
    "嘗試查天氣：「今天台北天氣如何？」",
    "確認瀏覽器工具可用：「幫我打開 Google 首頁」",
  ];
  checks.forEach((txt, i) => {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.5, y: 3.85 + i * 0.5, w: 4.2, h: 0.42,
      fill: { color: i === 0 ? "DCFCE7" : i === 1 ? "DBEAFE" : "FEF9C3" },
      margin: 0
    });
    slide.addText(txt, {
      x: 0.6, y: 3.88 + i * 0.5, w: 4.0, h: 0.36,
      fontSize: 11, color: C.dark, margin: 0, valign: "middle"
    });
  });

  // Right side highlight
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5.1, y: 3.35, w: 4.4, h: 2.0,
    fill: { color: C.navy },
    shadow: makeShadow(), margin: 0
  });
  slide.addText("💡 學習提示", {
    x: 5.3, y: 3.5, w: 4, h: 0.4,
    fontSize: 14, bold: true, color: C.mint, margin: 0
  });
  slide.addText([
    { text: "所有指令皆可 ", options: {} },
    { text: "直接貼給 Agent", options: { bold: true } },
    { text: "，無需打字。", options: { breakLine: true } },
    { text: "Agent 會自動開啟瀏覽器、", options: { breakLine: true } },
    { text: "讀取資料、分析、回覆。", options: { breakLine: true } },
    { text: "不需要自己查網站！", options: { bold: true } },
  ], {
    x: 5.3, y: 3.95, w: 4.0, h: 1.2,
    fontSize: 12, color: C.white, margin: 0
  });
}

// =============================================
// SLIDE 4: 台積電查詢 - 3來源
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.white };

  // Left accent
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.teal }
  });

  // Header
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.12, y: 0, w: 9.88, h: 1.1, fill: { color: C.navy }
  });
  slide.addText("02  查詢台積電股價", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontSize: 30, fontFace: "Arial Black", bold: true,
    color: C.white, margin: 0
  });

  // 3 cards
  const sources = [
    {
      name: "investing.com",
      tag: "📈 台股個股",
      price: "2,265 元",
      change: "昨收 2,270｜-0.22%",
      items: ["即時價格", "今日高低", "成交量", "本益比"],
      color: "0D9488",
      emoji: "🌐",
    },
    {
      name: "Yahoo Finance",
      tag: "📊 ADR 報價",
      price: "$66.45 USD",
      change: "美股報價",
      items: ["52週高低", "市值", "開盤/收盤", "ADR溢價"],
      color: "7C3AED",
      emoji: "📈",
    },
    {
      name: "台灣證券交易所",
      tag: "🏛️ 官方最準",
      price: "2,265 元",
      change: "技術分析",
      items: ["日K線", "本益比", "殖利率", "支撐/壓力"],
      color: "B45309",
      emoji: "🏛️",
    },
  ];

  sources.forEach((src, i) => {
    const x = 0.35 + i * 3.2;

    // Card
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.2, w: 3.0, h: 4.2,
      fill: { color: C.white },
      line: { color: C.lightGray, width: 1 },
      shadow: makeShadow(), margin: 0
    });

    // Top color bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.2, w: 3.0, h: 0.08,
      fill: { color: src.color }, margin: 0
    });

    // Emoji + name
    slide.addText(src.emoji, {
      x, y: 1.35, w: 3.0, h: 0.45,
      fontSize: 26, align: "center"
    });
    slide.addText(src.name, {
      x, y: 1.78, w: 3.0, h: 0.35,
      fontSize: 13, bold: true, align: "center", color: C.navy, margin: 0
    });
    slide.addText(src.tag, {
      x, y: 2.1, w: 3.0, h: 0.3,
      fontSize: 10, align: "center", color: src.color, margin: 0
    });

    // Price highlight
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.15, y: 2.5, w: 2.7, h: 0.85,
      fill: { color: src.color }, margin: 0
    });
    slide.addText(src.price, {
      x: x + 0.15, y: 2.52, w: 2.7, h: 0.55,
      fontSize: 18, bold: true, align: "center", color: C.white, margin: 0
    });
    slide.addText(src.change, {
      x: x + 0.15, y: 3.02, w: 2.7, h: 0.3,
      fontSize: 10, align: "center", color: "FFFFFF", margin: 0
    });

    // Bullet items
    src.items.forEach((item, j) => {
      slide.addText("• " + item, {
        x: x + 0.2, y: 3.45 + j * 0.38, w: 2.6, h: 0.34,
        fontSize: 11, color: C.dark, margin: 0
      });
    });
  });
}

// =============================================
// SLIDE 5: 白銀查詢
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.dark };

  // Header
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.1,
    fill: { color: C.teal }
  });
  slide.addText("03  查詢白銀（即時）價格", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontSize: 30, fontFace: "Arial Black", bold: true,
    color: C.white, margin: 0
  });

  // Silver icon
  slide.addShape(pres.shapes.OVAL, {
    x: 0.5, y: 1.3, w: 1.2, h: 1.2,
    fill: { color: "A8A8A8" }, shadow: makeShadow()
  });
  slide.addText("🥈", {
    x: 0.5, y: 1.38, w: 1.2, h: 1.0,
    fontSize: 40, align: "center", valign: "middle"
  });

  // Big price callout
  slide.addText("$77.55", {
    x: 1.9, y: 1.25, w: 4, h: 0.9,
    fontSize: 54, bold: true, color: C.mint, margin: 0
  });
  slide.addText("/ 盎司（USD）", {
    x: 1.9, y: 2.05, w: 3, h: 0.4,
    fontSize: 14, color: C.lightGray, margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 1.9, y: 2.5, w: 1.6, h: 0.4,
    fill: { color: "DC2626" }, margin: 0
  });
  slide.addText("-8.67%", {
    x: 1.9, y: 2.52, w: 1.6, h: 0.36,
    fontSize: 14, bold: true, align: "center", color: C.white, margin: 0
  });

  // Two source cards
  const silverSources = [
    {
      site: "investing.com",
      features: ["即時現貨價格", "24小時變動", "日內高低", "年內高低"],
      cmd: "幫我查白銀在 investing.com 的即時價格",
    },
    {
      site: "goldprice.org",
      features: ["無廣告、速度快", "30天/年初變化", "每盎司美元報價", "即時更新"],
      cmd: "用瀏覽器查白銀現貨即時價格",
    },
  ];

  silverSources.forEach((src, i) => {
    const x = 0.5 + i * 4.7;
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: 3.05, w: 4.4, h: 2.35,
      fill: { color: "1E3A5F" },
      shadow: makeShadow(), margin: 0
    });
    slide.addText(src.site, {
      x: x + 0.2, y: 3.15, w: 4, h: 0.4,
      fontSize: 14, bold: true, color: C.mint, margin: 0
    });
    src.features.forEach((f, j) => {
      slide.addText("• " + f, {
        x: x + 0.2, y: 3.55 + j * 0.33, w: 4, h: 0.3,
        fontSize: 11, color: C.white, margin: 0
      });
    });
    // Command sample
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.1, y: 4.85, w: 4.2, h: 0.42,
      fill: { color: "0F2C4A" }, margin: 0
    });
    slide.addText("▸ " + src.cmd, {
      x: x + 0.2, y: 4.87, w: 4.0, h: 0.38,
      fontSize: 9, color: C.mint, margin: 0, italic: true
    });
  });
}

// =============================================
// SLIDE 6: 台指期貨
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.white };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.teal }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.12, y: 0, w: 9.88, h: 1.1, fill: { color: C.navy }
  });
  slide.addText("04  查詢台指期貨", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontSize: 30, fontFace: "Arial Black", bold: true,
    color: C.white, margin: 0
  });

  // Futures info box
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.25, w: 9, h: 0.7,
    fill: { color: "FFF7ED" }, margin: 0
  });
  slide.addText("📌 台指期（TX）是台灣期貨交易所的加權指數期貨，24小時交易，可對沖股票風險、判斷明日台股方向。", {
    x: 0.7, y: 1.33, w: 8.6, h: 0.55,
    fontSize: 12, color: "92400E", margin: 0, valign: "middle"
  });

  // Price card
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 2.1, w: 3.5, h: 2.0,
    fill: { color: C.navy }, shadow: makeShadow(), margin: 0
  });
  slide.addText("📊 台股加權指數", {
    x: 0.7, y: 2.25, w: 3.1, h: 0.4,
    fontSize: 16, bold: true, color: C.white, margin: 0
  });
  slide.addText("41,172", {
    x: 0.7, y: 2.7, w: 3.1, h: 0.8,
    fontSize: 48, bold: true, color: C.mint, margin: 0
  });
  slide.addText("點", {
    x: 2.9, y: 3.05, w: 0.8, h: 0.4,
    fontSize: 18, color: C.lightGray, margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 3.6, w: 1.8, h: 0.35,
    fill: { color: "DC2626" }, margin: 0
  });
  slide.addText("-579 (-1.39%)", {
    x: 0.7, y: 3.62, w: 1.8, h: 0.3,
    fontSize: 11, bold: true, align: "center", color: C.white, margin: 0
  });

  // Data table
  const futData = [
    ["項目", "數值", "說明"],
    ["加權指數", "41,172 點", "TSE 現貨大盤"],
    ["昨日收盤", "41,751 點", ""],
    ["今日最高", "41,960 點", ""],
    ["今日最低", "41,089 點", ""],
    ["成交量", "約 3,200 億", "集中市場"],
    ["資料來源", "Yahoo Finance", ""],
  ];
  slide.addTable(futData, {
    x: 4.2, y: 2.1, w: 5.3, h: 2.0,
    colW: [1.6, 2.0, 1.7],
    fontFace: "Arial",
    fontSize: 11,
    color: C.navy,
    border: { pt: 0.5, color: C.lightGray },
    rowH: [0.32, 0.28, 0.28, 0.28, 0.28, 0.28, 0.28],
    fill: { color: C.white },
  });

  // Two sources
  const futSources = [
    { name: "Yahoo Finance", cmd: "幫我查詢台股加權指數的即時報價" },
    { name: "證交所官網", cmd: "幫我去台灣證券交易所查加權指數" },
  ];
  futSources.forEach((src, i) => {
    const x = 0.5 + i * 4.7;
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: 4.3, w: 4.4, h: 1.1,
      fill: { color: C.light }, margin: 0
    });
    slide.addText(src.name, {
      x: x + 0.15, y: 4.38, w: 4.1, h: 0.35,
      fontSize: 13, bold: true, color: C.navy, margin: 0
    });
    slide.addText("▸ " + src.cmd, {
      x: x + 0.15, y: 4.73, w: 4.1, h: 0.55,
      fontSize: 10, color: C.gray, margin: 0, italic: true
    });
  });
}

// =============================================
// SLIDE 7: TradingView KD 指標
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.dark };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.1,
    fill: { color: C.teal }
  });
  slide.addText("05  TradingView 技術分析", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontSize: 30, fontFace: "Arial Black", bold: true,
    color: C.white, margin: 0
  });

  // Left - KD explanation
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.3, w: 4.5, h: 4.0,
    fill: { color: "1E3A5F" }, shadow: makeShadow(), margin: 0
  });
  slide.addText("KD 隨機指標", {
    x: 0.7, y: 1.45, w: 4.1, h: 0.45,
    fontSize: 18, bold: true, color: C.mint, margin: 0
  });
  slide.addText("用於判斷股價短期趨勢", {
    x: 0.7, y: 1.88, w: 4.1, h: 0.3,
    fontSize: 11, color: C.lightGray, margin: 0
  });

  const kdInfo = [
    { label: "K 值", desc: "快速移動平均線，對股價變動敏感" },
    { label: "D 值", desc: "慢速移動平均線，過濾短期噪音" },
    { label: "黃金交叉", desc: "K 穿越 D 往上 → 買進信號 📗" },
    { label: "死亡交叉", desc: "K 穿越 D 往下 → 賣出信號 📕" },
  ];
  kdInfo.forEach((item, i) => {
    const isSignal = i >= 2;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.65, y: 2.3 + i * 0.72, w: 0.9, h: 0.55,
      fill: { color: isSignal ? (i === 2 ? "16A34A" : "DC2626") : C.teal },
      margin: 0
    });
    slide.addText(item.label, {
      x: 0.65, y: 2.35 + i * 0.72, w: 0.9, h: 0.45,
      fontSize: 11, bold: true, align: "center", color: C.white, margin: 0
    });
    slide.addText(item.desc, {
      x: 1.65, y: 2.35 + i * 0.72, w: 3.2, h: 0.45,
      fontSize: 11, color: C.white, margin: 0, valign: "middle"
    });
  });

  // Right - example chart placeholder + command
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5.2, y: 1.3, w: 4.3, h: 2.5,
    fill: { color: "0F2C4A" }, shadow: makeShadow(), margin: 0
  });
  slide.addText("📈 台積電日K示意", {
    x: 5.4, y: 1.42, w: 3.9, h: 0.35,
    fontSize: 13, bold: true, color: C.white, margin: 0
  });
  // Simulated chart lines
  const chartData = [70, 65, 68, 72, 69, 74, 71, 76, 73, 78, 75];
  const maxD = Math.max(...chartData);
  const minD = Math.min(...chartData);
  chartData.forEach((v, i) => {
    const bx = 5.5 + i * 0.36;
    const bh = 0.5 + ((v - minD) / (maxD - minD)) * 1.0;
    const by = 3.5 - bh;
    slide.addShape(pres.shapes.RECTANGLE, {
      x: bx, y: by, w: 0.22, h: bh,
      fill: { color: i % 2 === 0 ? "0D9488" : "0288A8" }, margin: 0
    });
  });
  slide.addText("日K線圖（示意）", {
    x: 5.4, y: 3.58, w: 3.9, h: 0.2,
    fontSize: 9, color: C.gray, margin: 0, align: "center"
  });

  // Command sample
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5.2, y: 4.0, w: 4.3, h: 1.3,
    fill: { color: "1E3A5F" }, margin: 0
  });
  slide.addText("🤖 語音指令範例", {
    x: 5.4, y: 4.1, w: 3.9, h: 0.35,
    fontSize: 12, bold: true, color: C.mint, margin: 0
  });
  slide.addText("「設定每小時去 TradingView 查看台積電日K KD指標，如果 K 值穿越 D 值，馬上通知我（買進/賣出信號）」", {
    x: 5.4, y: 4.45, w: 3.9, h: 0.75,
    fontSize: 10, color: C.white, margin: 0, italic: true
  });
}

// =============================================
// SLIDE 8: 自動監控設定
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.light };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.teal }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.12, y: 0, w: 9.88, h: 1.1, fill: { color: C.navy }
  });
  slide.addText("06  自動監控設定", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontSize: 30, fontFace: "Arial Black", bold: true,
    color: C.white, margin: 0
  });

  // Cron syntax
  slide.addText("⏰ Cron 語法速查", {
    x: 0.5, y: 1.2, w: 4, h: 0.4,
    fontSize: 15, bold: true, color: C.navy, margin: 0
  });
  const cronData = [
    ["語法", "意義"],
    ["0 * * * *", "每小時整點一次"],
    ["30 * * * *", "每小時30分執行"],
    ["0 9 * * *", "每天早上9點"],
    ["*/15 * * * *", "每15分鐘一次"],
    ["0 9 * * 1-5", "上班日早上9點"],
  ];
  slide.addTable(cronData, {
    x: 0.5, y: 1.6, w: 4.3, h: 1.85,
    colW: [2.0, 2.3],
    fontFace: "Arial",
    fontSize: 11,
    color: C.navy,
    border: { pt: 0.5, color: C.lightGray },
    rowH: [0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
    fill: { color: C.white },
  });

// 3 monitoring tasks with live data
  const tasks = [
    {
      title: "台積電股價",
      price: "2,265",
      unit: "元",
      change: "-0.22%",
      changeColor: "DC2626",
      trigger: "變動 >3%",
      push: "Telegram",
      color: "0D9488"
    },
    {
      title: "白銀",
      price: "$77.55",
      unit: "/oz",
      change: "-8.67%",
      changeColor: "DC2626",
      trigger: "24h >2%",
      push: "Telegram",
      color: "7C3AED"
    },
    {
      title: "台股加權",
      price: "41,172",
      unit: "點",
      change: "-1.39%",
      changeColor: "DC2626",
      trigger: "每30分",
      push: "Telegram",
      color: "B45309"
    },
  ];
  tasks.forEach((task, i) => {
    const x = 5.0 + i * 1.65;
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.2, w: 1.55, h: 2.3,
      fill: { color: task.color }, shadow: makeShadow(), margin: 0
    });
    slide.addText(task.title, {
      x, y: 1.28, w: 1.55, h: 0.35,
      fontSize: 10, bold: true, align: "center", color: C.white, margin: 0
    });
    slide.addText(task.price, {
      x, y: 1.6, w: 1.55, h: 0.55,
      fontSize: 20, bold: true, align: "center", color: C.white, margin: 0
    });
    slide.addText(task.unit, {
      x, y: 2.1, w: 1.55, h: 0.22,
      fontSize: 8, align: "center", color: "FFFFFF", margin: 0
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.25, y: 2.35, w: 1.05, h: 0.25,
      fill: { color: task.changeColor }, margin: 0
    });
    slide.addText(task.change, {
      x: x + 0.25, y: 2.36, w: 1.05, h: 0.23,
      fontSize: 10, bold: true, align: "center", color: C.white, margin: 0
    });
    slide.addText("觸發：" + task.trigger, {
      x, y: 2.68, w: 1.55, h: 0.28,
      fontSize: 8, align: "center", color: C.white, margin: 0
    });
    slide.addText("推：" + task.push, {
      x, y: 2.92, w: 1.55, h: 0.28,
      fontSize: 8, align: "center", color: C.white, margin: 0
    });
  });

  // Command sample
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 3.6, w: 9, h: 1.8,
    fill: { color: C.white }, shadow: makeShadow(), margin: 0
  });
  slide.addText("📨 設定指令範例", {
    x: 0.7, y: 3.72, w: 8.6, h: 0.35,
    fontSize: 13, bold: true, color: C.navy, margin: 0
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 4.1, w: 8.6, h: 1.15,
    fill: { color: "F1F5F9" }, margin: 0
  });
  slide.addText([
    { text: "「幫我設定每小時執行的任務，監控台積電（2330）在 investing.com 的", options: { breakLine: true } },
    { text: "即時股價，如果價格變動超過 3%，就推播到我的 Telegram」", options: {} },
  ], {
    x: 0.85, y: 4.18, w: 8.3, h: 0.95,
    fontSize: 12, color: "1E3A5F", margin: 0, italic: true
  });
}

// =============================================
// SLIDE 9: 三合一晨報
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.dark };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 1.1,
    fill: { color: C.mint }
  });
  slide.addText("07  三合一晨報與多重監控組合", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontSize: 28, fontFace: "Arial Black", bold: true,
    color: C.dark, margin: 0
  });

  // 3-in-1 morning report
  slide.addText("🌅 每天早上 8:00 自動推播", {
    x: 0.5, y: 1.2, w: 9, h: 0.4,
    fontSize: 15, bold: true, color: C.mint, margin: 0
  });

  const reportItems = [
    { icon: "📈", name: "台積電 2330", price: "2,265 元", change: "-0.22%", changeColor: "DC2626", src: "Yahoo Finance" },
    { icon: "🥈", name: "白銀 XAG/USD", price: "$77.55", change: "-8.67%", changeColor: "DC2626", src: "Yahoo Finance" },
    { icon: "📊", name: "台股加權指數", price: "41,172 點", change: "-1.39%", changeColor: "DC2626", src: "Yahoo Finance" },
  ];

  reportItems.forEach((item, i) => {
    const x = 0.5 + i * 3.15;
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.7, w: 3.0, h: 2.2,
      fill: { color: "1E3A5F" }, shadow: makeShadow(), margin: 0
    });
    slide.addText(item.icon, {
      x, y: 1.8, w: 3.0, h: 0.5,
      fontSize: 28, align: "center"
    });
    slide.addText(item.name, {
      x, y: 2.3, w: 3.0, h: 0.35,
      fontSize: 13, bold: true, align: "center", color: C.white, margin: 0
    });
    slide.addText(item.price, {
      x, y: 2.68, w: 3.0, h: 0.55,
      fontSize: 22, bold: true, align: "center", color: C.mint, margin: 0
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.8, y: 3.28, w: 1.4, h: 0.35,
      fill: { color: item.changeColor || "16A34A" }, margin: 0
    });
    slide.addText(item.change, {
      x: x + 0.8, y: 3.3, w: 1.4, h: 0.3,
      fontSize: 12, bold: true, align: "center", color: C.white, margin: 0
    });
    slide.addText("來源：" + item.src, {
      x, y: 3.68, w: 3.0, h: 0.25,
      fontSize: 9, align: "center", color: C.gray, margin: 0
    });
  });

  // Bottom - command
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 4.1, w: 9, h: 1.25,
    fill: { color: "1E3A5F" }, margin: 0
  });
  slide.addText("🚀 一次查三個指令", {
    x: 0.7, y: 4.2, w: 8.6, h: 0.35,
    fontSize: 13, bold: true, color: C.mint, margin: 0
  });
  slide.addText("「幫我一次查三個：1）台積電在 Yahoo Finance 的即時報價與今日漲跌%  2）白銀現貨即時價格  3）台股加權指數行情」", {
    x: 0.7, y: 4.55, w: 8.6, h: 0.65,
    fontSize: 11, color: C.white, margin: 0, italic: true
  });
}

// =============================================
// SLIDE 10: 常用輔助指令
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.white };

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.teal }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.12, y: 0, w: 9.88, h: 1.1, fill: { color: C.navy }
  });
  slide.addText("附錄  常用輔助指令", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontSize: 30, fontFace: "Arial Black", bold: true,
    color: C.white, margin: 0
  });

  const helperCmds = [
    { cmd: "我的監控任務目前狀態？", desc: "查詢所有已設定的監控任務" },
    { cmd: "取消台積電監控", desc: "停止特定監控任務" },
    { cmd: "今天台積電收盤了嗎？", desc: "主動查詢收盤狀態" },
    { cmd: "幫我解釋 KD 指標怎麼看", desc: "學習技術分析觀念" },
    { cmd: "設定每日晨報", desc: "建立每天固定時間的市場報價推播" },
    { cmd: "把台指期改成每15分鐘監控", desc: "修改現有監控頻率" },
  ];

  helperCmds.forEach((item, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.7;
    const y = 1.25 + row * 1.4;

    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.4, h: 1.25,
      fill: { color: C.light }, margin: 0
    });
    // Accent bar
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.08, h: 1.25,
      fill: { color: C.teal }, margin: 0
    });
    slide.addText("▸ " + item.cmd, {
      x: x + 0.2, y: y + 0.12, w: 4.0, h: 0.5,
      fontSize: 12, color: C.navy, bold: true, margin: 0
    });
    slide.addText(item.desc, {
      x: x + 0.2, y: y + 0.65, w: 4.0, h: 0.45,
      fontSize: 10, color: C.gray, margin: 0
    });
  });
}

// =============================================
// SLIDE 11: 網址速查 + 結尾
// =============================================
{
  let slide = pres.addSlide();
  slide.background = { color: C.navy };

  slide.addText("🔗 網址速查", {
    x: 0.5, y: 0.4, w: 9, h: 0.6,
    fontSize: 28, fontFace: "Arial Black", bold: true,
    color: C.white, margin: 0
  });

  const urls = [
    { name: "investing.com", url: "www.investing.com" },
    { name: "Yahoo Finance", url: "finance.yahoo.com" },
    { name: "台灣證券交易所", url: "www.twse.com.tw" },
    { name: "GoldPrice.org", url: "goldprice.org" },
    { name: "CMoney", url: "www.cmoney.tw" },
    { name: "TradingView", url: "www.tradingview.com" },
  ];

  urls.forEach((u, i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.5 + col * 3.1;
    const y = 1.1 + row * 1.0;

    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 2.9, h: 0.8,
      fill: { color: "1E3A5F" }, margin: 0
    });
    slide.addText(u.name, {
      x: x + 0.1, y: y + 0.08, w: 2.7, h: 0.35,
      fontSize: 12, bold: true, color: C.mint, margin: 0
    });
    slide.addText(u.url, {
      x: x + 0.1, y: y + 0.43, w: 2.7, h: 0.3,
      fontSize: 10, color: C.lightGray, margin: 0
    });
  });

  // Bottom CTA
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 3.3, w: 10, h: 2.325,
    fill: { color: C.teal }
  });
  slide.addText("開始你的第一個監控任務", {
    x: 0.5, y: 3.55, w: 9, h: 0.7,
    fontSize: 30, fontFace: "Arial Black", bold: true,
    color: C.white, align: "center", margin: 0
  });
  slide.addText("直接傳給 Agent → 「幫我設定每小時監控台積電股價」", {
    x: 0.5, y: 4.3, w: 9, h: 0.5,
    fontSize: 16, color: C.dark, align: "center", margin: 0
  });
  slide.addText("HERMES AGENT 學院", {
    x: 0.5, y: 5.0, w: 9, h: 0.4,
    fontSize: 12, bold: true, color: C.dark, align: "center",
    charSpacing: 4, margin: 0
  });
}

// Save
pres.writeFile({ fileName: "C:/Users/purem/OneDrive/文件/TextBook/HermesAgent_實戰監控手冊.pptx" })
  .then(() => console.log("DONE: HermesAgent_實戰監控手冊.pptx"))
  .catch(e => console.error("ERROR:", e));
