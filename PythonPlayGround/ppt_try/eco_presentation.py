import uno
from com.sun.star.awt import Size, Point, FontWeight
from com.sun.star.drawing.FillStyle import SOLID
from com.sun.star.presentation.AnimationEffect import NONE

def create_presentation():
    """使用 LibreOffice 組件創建環保主題投影片"""
    
    # 連線到執行中的 LibreOffice 服務
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_ctx)
    
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    
    # 建立 Desktop 物件
    desktop = ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.frame.Desktop", ctx)
    
    # 創建新的簡報文件
    doc = desktop.loadComponentFromURL(
        "private:factory/simpress", "_blank", 0, ())
    
    # 取得投影片集合
    slides = doc.getDrawPages()
    
    # === 首頁：地球只有一個，環保是緊急的課題 ===
    slide1 = slides.getByIndex(0)  # 第一張投影片已經存在
    setup_slide_background(slide1)
    
    # 新增標題
    add_title(slide1, "地球只有一個", 4000, 2000)
    add_subtitle(slide1, "環保是緊急的課題", 4000, 6000)
    
    # === 第一頁：我們還有多少時間？ ===
    slide2 = slides.insertNewByIndex(1)
    setup_slide_background(slide2)
    
    add_title(slide2, "我們還有多少時間？", 4000, 2000)
    add_content(slide2, "我們時間有限，工業革命後\n環境問題越來越嚴重", 4000, 6000)
    
    # === 第二頁：我們該怎麼辦 ===
    slide3 = slides.insertNewByIndex(2)
    setup_slide_background(slide3)
    
    add_title(slide3, "我們該怎麼辦", 4000, 2000)
    add_content(slide3, "• 配合環保法規\n• 少用塑膠製品", 4000, 6000)
    
    # === 結束頁：謝謝你的聆聽 ===
    slide4 = slides.insertNewByIndex(3)
    setup_slide_background(slide4)
    
    add_title(slide4, "謝謝你的聆聽", 4000, 4500)
    
    # 儲存檔案
    output_path = "file:///C:/Users/purem/Documents/TextBook/PythonPlayGround/ppt_try/環保主題.odp"
    doc.storeToURL(output_path, ())
    
    print(f"投影片已成功建立：{output_path}")
    print("投影片共有 4 張")
    
    # 不關閉文件，讓使用者可以查看
    # doc.close(True)
    
    return doc


def setup_slide_background(slide):
    """設定投影片背景為淺綠色（環保主題）"""
    try:
        # 取得背景物件
        bg = slide.getPropertyValue("Background")
        if bg is not None:
            bg.FillStyle = SOLID
            bg.FillColor = 0xE8F5E9  # 淺綠色
            slide.setPropertyValue("Background", bg)
    except:
        # 如果無法設定背景，就跳過
        pass


def add_title(slide, text, x_pos, y_pos):
    """新增標題文字"""
    # 使用 document 的 service manager 創建 shape
    shape = slide.getParent().getParent().createInstance("com.sun.star.drawing.TextShape")
    
    # 設定位置和大小
    shape.Position = Point(x_pos, y_pos)
    shape.Size = Size(20000, 3000)  # 寬 x 高（1/100 mm）
    
    # 新增到投影片
    slide.add(shape)
    
    # 設定文字
    text_range = shape.getText()
    text_range.setString(text)
    
    # 設定文字樣式
    cursor = text_range.createTextCursor()
    cursor.CharFontName = "Microsoft JhengHei"  # 微軟正黑體
    cursor.CharHeight = 44  # 字體大小
    cursor.CharWeight = FontWeight.BOLD  # 粗體
    cursor.CharColor = 0x1B5E20  # 深綠色
    cursor.ParaAdjust = 3  # 置中對齊
    
    return shape


def add_subtitle(slide, text, x_pos, y_pos):
    """新增副標題文字"""
    shape = slide.getParent().getParent().createInstance("com.sun.star.drawing.TextShape")
    
    # 設定位置和大小
    shape.Position = Point(x_pos, y_pos)
    shape.Size = Size(20000, 2500)
    
    # 新增到投影片
    slide.add(shape)
    
    # 設定文字
    text_range = shape.getText()
    text_range.setString(text)
    
    # 設定文字樣式
    cursor = text_range.createTextCursor()
    cursor.CharFontName = "Microsoft JhengHei"
    cursor.CharHeight = 32
    cursor.CharWeight = FontWeight.BOLD
    cursor.CharColor = 0x388E3C  # 綠色
    cursor.ParaAdjust = 3  # 置中對齊
    
    return shape


def add_content(slide, text, x_pos, y_pos):
    """新增內容文字"""
    shape = slide.getParent().getParent().createInstance("com.sun.star.drawing.TextShape")
    
    # 設定位置和大小
    shape.Position = Point(x_pos, y_pos)
    shape.Size = Size(20000, 8000)
    
    # 新增到投影片
    slide.add(shape)
    
    # 設定文字
    text_range = shape.getText()
    text_range.setString(text)
    
    # 設定文字樣式
    cursor = text_range.createTextCursor()
    cursor.CharFontName = "Microsoft JhengHei"
    cursor.CharHeight = 28
    cursor.CharColor = 0x2E7D32  # 深綠色
    cursor.ParaAdjust = 0  # 左對齊
    
    return shape


if __name__ == "__main__":
    print("開始創建環保主題投影片...")
    print("請確保 LibreOffice 已經在背景執行並監聽 port 2002")
    print("啟動指令：soffice --accept='socket,host=localhost,port=2002;urp;' --norestore --nofirststartwizard")
    print("-" * 60)
    
    try:
        doc = create_presentation()
        print("\n✓ 投影片創建成功！")
    except Exception as e:
        print(f"\n✗ 發生錯誤：{e}")
        print("\n請確認：")
        print("1. LibreOffice 是否已啟動並監聽 port 2002")
        print("2. Python 的 uno 模組是否已安裝")
