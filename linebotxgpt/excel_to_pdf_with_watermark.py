import argparse
import win32com.client as win32
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
import os

def excel_to_pdf(excel_path, pdf_path):
    """將 Excel 轉換為 PDF"""
    excel_app = win32.Dispatch("Excel.Application")
    excel_app.Visible = False

    try:
        workbook = excel_app.Workbooks.Open(excel_path)
        workbook.ExportAsFixedFormat(0, pdf_path)  # 0: xlTypePDF
        print(f"Excel 轉 PDF 完成: {pdf_path}")
    except Exception as e:
        print(f"轉換失敗: {e}")
    finally:
        workbook.Close(False)
        excel_app.Quit()

def create_watermark(watermark_path, watermark_text):
    """建立支援中文的浮水印 PDF"""
    # 註冊中文字型 (需要字型檔案)
    font_path = "C:\\Windows\\Fonts\\kaiu.ttf"  # 請替換為你的字型路徑
    pdfmetrics.registerFont(TTFont('MicrosoftKaiti', font_path))

     # 設定 PDF 頁面大小
    page_width, page_height = letter

    # 生成 PDF 浮水印
    c = canvas.Canvas(watermark_path, pagesize=letter)
    c.setFont("MicrosoftKaiti", 50)  # 使用註冊的字型
    c.setFillAlpha(0.1)  # 設定透明度
     # 平鋪式浮水印：控制位置與間隔
    x_spacing, y_spacing = 250, 250  # 水平與垂直間距
    for y in range(0, int(page_height), y_spacing):  # 垂直方向
        for x in range(0, int(page_width), x_spacing):  # 水平方向
            c.saveState()
            c.translate(x, y)  # 移動座標系統
            c.rotate(45)  # 旋轉角度 (45 度斜角)
            c.drawString(0, 0, watermark_text)  # 繪製文字
            c.restoreState()
    c.save()
    print(f"浮水印檔案已建立: {watermark_path}")

def add_watermark_to_pdf(input_pdf, output_pdf, watermark_pdf):
    """在 PDF 上加上浮水印"""
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()
    watermark = PdfReader(watermark_pdf).pages[0]

    for page in pdf_reader.pages:
        page.merge_page(watermark)
        pdf_writer.add_page(page)

    with open(output_pdf, "wb") as out_file:
        pdf_writer.write(out_file)
    print(f"浮水印添加完成: {output_pdf}")

def main():
    parser = argparse.ArgumentParser(description="將 Excel 轉換為 PDF 並加上浮水印")
    parser.add_argument("--excel", type=str, required=True, help="輸入 Excel 檔案路徑")
    parser.add_argument("--output", type=str, required=True, help="輸出最終 PDF 檔案路徑")
    parser.add_argument("--temp", type=str, required=True, help="暫存 PDF 檔案路徑")
    parser.add_argument("--watermark", type=str, default="CONFIDENTIAL", help="浮水印文字 (預設: CONFIDENTIAL)")

    args = parser.parse_args()

    excel_path = args.excel
    output_pdf_path = args.output
    temp_pdf_path = args.temp  # 暫存 PDF 檔案路徑
    watermark_pdf_path = "watermark.pdf"

    # 1. 將 Excel 轉換為 PDF
    excel_to_pdf(excel_path, temp_pdf_path)

    # 2. 建立浮水印 PDF
    create_watermark(watermark_pdf_path, args.watermark)

    # 3. 加浮水印到 PDF
    add_watermark_to_pdf(temp_pdf_path, output_pdf_path, watermark_pdf_path)

    # 4. 清理臨時檔案
    os.remove(temp_pdf_path)
    os.remove(watermark_pdf_path)
    print("所有步驟完成！")

    

if __name__ == "__main__":
    main()


# pip install pywin32 pypdf2 reportlab
# pip install pyinstaller
# pyinstaller --onefile excel_to_pdf_with_watermark.py
# excel_to_pdf_with_watermark.exe --excel "C:\Users\sean.ma\Downloads\sbox調查表.xlsx" --output "C:\Users\sean.ma\Downloads\sbox調查表.pdf" --temp "C:\Users\sean.ma\Downloads\temp_converted.pdf" --watermark "衛普資訊Jacky哥-路竹金城武"