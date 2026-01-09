from pdf2image import convert_from_path
from PIL import Image

# 轉換PDF為圖像
pdf_path = 'c:/Users/sean.ma/Downloads/來源導向_智慧創作.pdf'
images = convert_from_path(pdf_path)
print(f"PDF轉換成功，共{len(images)}頁")

# 保存第一張圖像用於檢查
images[0].save('c:/Users/sean.ma/Downloads/page1.png')
print("第一頁已保存為 page1.png")
