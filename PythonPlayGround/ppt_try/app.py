# from pptx import Presentation
# from pptx.util import Pt

# # 1. 新建空白簡報
# prs = Presentation()

# # 2. 頁1 主題頁
# slide_layout = prs.slide_layouts[0]  # 預設主題頁
# slide = prs.slides.add_slide(slide_layout)
# slide.shapes.title.text = "人生的價值"
# slide.placeholders[1].text = "漫漫長路,你需要學會的事"

# # 3. 頁2 內容頁1
# layout_content = prs.slide_layouts[1]  # 標題+內容樣式
# slide2 = prs.slides.add_slide(layout_content)
# slide2.shapes.title.text = "人生價值與目的"
# content = "1.對天\n2.對地\n3.對人"
# slide2.placeholders[1].text = content

# # 4. 頁3 內容頁2(左右內容)
# layout_content2 = prs.slide_layouts[3]  # 兩欄內容
# slide3 = prs.slides.add_slide(layout_content2)
# slide3.shapes.title.text = "人生的挑戰與困難"
# slide3.placeholders[1].text = "沉思的意義,挑戰的價值"  # 左欄
# slide3.placeholders[2].text = "孤獨與沉澱,聚眾與湧現"  # 右欄

# # 5. 頁4 結尾
# layout_final = prs.slide_layouts[1]
# slide4 = prs.slides.add_slide(layout_final)
# slide4.shapes.title.text = "謝謝您的聽講 Thank You"
# slide4.placeholders[1].text = ""

# # 6. 儲存檔案
# prs.save("人生的價值_sample.pptx")




from pptx_templater.core import convert

# 路徑設定
src = "template.pptx"
dest = "output.pptx"
model = {
    "slides": [
        {
            "layoutSlideNum": 0,
            "text": {
                "title": "人生的價值",
                "subtitle": "漫漫長路，你需要學會的事"
            }
        },
        {
            "layoutSlideNum": 1,
            "text": {
                "heading": "人生價值與目的",
                "content": "1. 對天\n2. 對地\n3. 對人"
            }
        },
        {
            "layoutSlideNum": 2,
            "text": {
                "heading": "人生的挑戰與困難",
                "left": "沉思的意義\n挑戰的價值",
                "right": "孤獨與沉澱\n聚眾與湧現"
            }
        },
        {
            "layoutSlideNum": 3,
            "text": {
                "thanks": "謝謝您的聽講\nThank You"
            }
        }
    ]
}

convert(src, dest, model)
print("已生成 output.pptx")
