import os
from openai import OpenAI

# 以com元件讀取ppt檔案
import win32com.client

client = OpenAI()

# 讀取投影片內容並翻譯成越南文
def translate_to_vietnamese(text):
    """使用ChatGPT API翻譯文字為越南文"""
    if not text.strip():
        return text
    
    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {"role": "system", "content": "You are a professional translator. Translate the following text to Indonesian."},
            {"role": "user", "content": text}
        ]
    )
    return response.output_text

# 創建PowerPoint應用程序對象
powerpoint = win32com.client.Dispatch("PowerPoint.Application")

# 設置可見性
powerpoint.Visible = True

# 打開PPT文件
ppt_path = os.path.abspath(r"C:\Users\sean.ma\Documents\TextBook\投影片翻譯\114年菸害防制宣導講座 (翻譯泰國、越南、印尼).pptx")
presentation = powerpoint.Presentations.Open(ppt_path)

# 遞迴處理形狀以處理群組形狀
def process_shape(shape, indent="  "):
    """遞迴處理形狀，包括群組形狀和表格"""
    try:
        # 處理群組形狀
        if shape.Type == 6:  # msoGroup
            print(f"{indent}[群組形狀]")
            for sub_shape in shape.GroupItems:
                process_shape(sub_shape, indent + "  ")
        
        # 處理表格
        elif shape.HasTable:
            print(f"{indent}[表格]")
            table = shape.Table
            for row_idx in range(1, table.Rows.Count + 1):
                for col_idx in range(1, table.Columns.Count + 1):
                    cell = table.Cell(row_idx, col_idx)
                    原文 = cell.Shape.TextFrame.TextRange.Text
                    if 原文.strip():
                        print(f"{indent}儲存格({row_idx},{col_idx}) 原文: {原文[:50]}...")
                        翻譯文 = translate_to_vietnamese(原文)
                        print(f"{indent}儲存格({row_idx},{col_idx}) 譯文: {翻譯文[:50]}...")
                        cell.Shape.TextFrame.TextRange.Text = 翻譯文
        
        # 處理一般文字框
        elif shape.HasTextFrame:
            原文 = shape.TextFrame.TextRange.Text
            if 原文.strip():
                print(f"{indent}原文: {原文[:50]}...")
                翻譯文 = translate_to_vietnamese(原文)
                print(f"{indent}譯文: {翻譯文[:50]}...")
                shape.TextFrame.TextRange.Text = 翻譯文
        
        # 處理 SmartArt (通常在 GroupItems 中)
        elif shape.Type == 15:  # msoSmartArt
            print(f"{indent}[SmartArt - 嘗試提取文字]")
            # SmartArt 通常需要轉換為形狀才能提取文字
            try:
                if hasattr(shape, 'GroupItems'):
                    for sub_shape in shape.GroupItems:
                        process_shape(sub_shape, indent + "  ")
            except:
                pass
    
    except Exception as e:
        print(f"{indent}處理形狀時發生錯誤: {e}")

# 遍歷每個投影片並翻譯文字
for slide in presentation.Slides:
    print(f"\n{'='*50}")
    print(f"處理投影片 {slide.SlideIndex}:")
    print(f"{'='*50}")
    for shape in slide.Shapes:
        process_shape(shape)

# 儲存翻譯後的PPT
output_path = os.path.abspath(f"C:\\Users\\sean.ma\\Documents\\TextBook\\powerpoint\\測試範本_越南文.pptx")
presentation.SaveAs(output_path)
print(f"\n翻譯完成! 檔案已儲存至: {output_path}")

# 關閉演示文稿
presentation.Close()
powerpoint.Quit()