import uno
from com.sun.star.awt import FontWeight

# 連線到執行中的 LibreOffice 服務
local_ctx = uno.getComponentContext()
resolver = local_ctx.ServiceManager.createInstanceWithContext(
    "com.sun.star.bridge.UnoUrlResolver", local_ctx)
ctx = resolver.resolve(
    "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")

# 建立 Desktop 物件
desktop = ctx.ServiceManager.createInstanceWithContext(
    "com.sun.star.frame.Desktop", ctx)

# 載入 ODP / PPTX 檔案（注意：必須是完整 file:/// URL 格式）
input_path = "file:///C:/slides/input.odp"
output_path = "file:///C:/slides/output_modified.odp"

doc = desktop.loadComponentFromURL(input_path, "_blank", 0, ())

# 取得投影片集合
slides = doc.getDrawPages()

# === 一、修改每張投影片背景 ===
for i in range(slides.getCount()):
    slide = slides.getByIndex(i)

    bg = slide.getPropertyValue("Background")
    bg.FillStyle = 2  # 1=Solid, 2=Gradient, 3=Hatch, 4=Bitmap
    bg.GradientName = "Blue to White"  # 系統預設漸層名稱
    slide.setPropertyValue("Background", bg)

# === 二、修改所有文字樣式 ===
for i in range(slides.getCount()):
    slide = slides.getByIndex(i)
    shapes = slide.getShapes()
    for j in range(shapes.getCount()):
        shape = shapes.getByIndex(j)
        if not shape.supportsService("com.sun.star.drawing.TextShape"):
            continue
        text_range = shape.getText()
        cursor = text_range.createTextCursor()
        cursor.CharColor = 0x2F5597       # 深藍色字
        cursor.CharFontName = "Microsoft JhengHei"
        cursor.CharHeight = 28
        cursor.CharWeight = FontWeight.BOLD

# === 三、套用模板樣式（可選） ===
# doc.StyleFamilies 內有 "PageStyles"、"GraphicStyles" 等可用
# 例如改用 BlueGradient 版面：
page_styles = doc.StyleFamilies.getByName("PageStyles")
if "BlueGradient" in page_styles.ElementNames:
    for i in range(slides.getCount()):
        slide = slides.getByIndex(i)
        slide.PageStyleName = "BlueGradient"

# 儲存並關閉
doc.storeToURL(output_path, ())
doc.close(True)
print("已完成修改並輸出：", output_path)
