import os
import base64
import io
import requests
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import win32com.client
import tempfile

client = OpenAI()


# ===== 檢查圖片是否包含中文 =====
def check_chinese_in_image(image_bytes):
    """使用 OpenAI Responses API 檢查圖片中是否有中文"""

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.responses.create(
        model="gpt-5.1",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "請檢查這張圖片中是否包含中文文字。只回答「是」或「否」，不要其他解釋。"},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image_b64}"
                    }
                ]
            }
        ],
        reasoning={"effort": "low"},
        max_output_tokens=50
    )

    result = response.output_text.strip()
    return "是" in result or "yes" in result.lower()


# ===== 翻譯文字 =====
def translate_text_to_indonesian(text):
    """將文字翻譯成印尼文"""
    if not text.strip():
        return text

    response = client.responses.create(
        model="gpt-5.1",
        input=[
            {"role": "system", "content": "Translate the following text to Indonesian."},
            {"role": "user", "content": text}
        ],
        reasoning={"effort": "low"},
        max_output_tokens=2000
    )
    return response.output_text.strip()


# ===== 使用 OpenAI 翻譯圖片 =====
def translate_image_to_indonesian(image_bytes):
    """使用 OpenAI Vision API 和 Image Edit API 保留原圖並翻譯文字為印尼文"""

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    
    # 步驟 1: 使用 Responses API 提取中文文字並翻譯成印尼文
    print("  [步驟 1] 識別並翻譯文字...")
    response = client.responses.create(
        model="gpt-5.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "請完整提取這張圖片中的所有中文文字，並將它們翻譯成印尼文。請以「原文 -> 印尼文」的格式列出所有翻譯。"
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image_b64}"
                    }
                ]
            }
        ],
        reasoning={"effort": "low"},
        max_output_tokens=500
    )
    
    translation_pairs = response.output_text.strip()
    print(f"  [翻譯對照] {translation_pairs[:100]}...")
    
    # 步驟 2: 準備圖片用於編輯（需要轉成 RGBA 並調整為正方形）
    img = Image.open(io.BytesIO(image_bytes))
    
    # 轉換為 RGBA（DALL-E edit 需要）
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # 調整為正方形（DALL-E edit 的要求）
    width, height = img.size
    size = max(width, height)
    square_img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    square_img.paste(img, ((size - width) // 2, (size - height) // 2))
    
    # 調整大小到 DALL-E 支援的尺寸 (1024x1024)
    square_img = square_img.resize((1024, 1024), Image.Resampling.LANCZOS)
    
    # 儲存為臨時檔案
    temp_dir = tempfile.gettempdir()
    temp_image_path = os.path.join(temp_dir, "temp_edit_image.png")
    square_img.save(temp_image_path, format='PNG')
    
    # 步驟 3: 使用 DALL-E 2 Image Edit API（保留原圖，只修改文字部分）
    print("  [步驟 2] 使用 Image Edit API 編輯圖片...")
    
    prompt = f"Replace all Chinese text in this image with Indonesian text according to these translations: {translation_pairs}. Keep everything else exactly the same - same colors, same layout, same design, same images. Only change the text from Chinese to Indonesian."
    
    response = client.images.edit(
            model="gpt-image-1",
            image=[
                open(temp_image_path, "rb")
            ],
            prompt=prompt,
            # n=1,
            # size="1024x1024"
        )
        
    
    # 下載編輯後的圖片
    image_base64 = response.data[0].b64_json
    edited_image = base64.b64decode(image_base64)
    
    return edited_image


# ===== 處理圖片：檢查是否有中文 → 翻譯圖片 =====
def process_picture_shape(slide, shape):
    try:
        if shape.Type != 13:  # 僅處理 msoPicture
            return

        print("  [圖片] Export 中...")

        # 1. 匯出圖片
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"ppt_img_{shape.Id}.png")
        shape.Export(temp_path, 2)

        if not os.path.exists(temp_path):
            print("  [圖片] Export 失敗")
            return

        with open(temp_path, "rb") as f:
            img_bytes = f.read()

        # 2. 檢查是否有中文
        print("  [圖片] 檢查是否包含中文...")
        has_chinese = check_chinese_in_image(img_bytes)
        
        if not has_chinese:
            print("  [圖片] 無中文，略過")
            return
        
        print("  [圖片] 發現中文，開始翻譯...")

        # 3. 使用 OpenAI 直接翻譯圖片
        print("  [圖片] 使用 OpenAI 翻譯圖片...")
        translated_image = translate_image_to_indonesian(img_bytes)
        
        new_png = os.path.join(temp_dir, f"translated_{shape.Id}.png")
        with open(new_png, "wb") as f:
            f.write(translated_image)

        # 4. 記錄原位置與大小
        left = shape.Left
        top = shape.Top
        width = shape.Width
        height = shape.Height

        # 5. 刪除舊圖片
        shape.Delete()

        # 6. 插入新圖片（真正替換）
        slide.Shapes.AddPicture(
            FileName=new_png,
            LinkToFile=False,
            SaveWithDocument=True,
            Left=left,
            Top=top,
            Width=width,
            Height=height
        )
        
        print("  [圖片] 翻譯完成！")

    except Exception as e:
        print(f"  [圖片錯誤] {e}")


# ===== 處理一般 shape =====
def process_shape(slide, shape, indent="  "):
    try:
        # 1. 群組
        if shape.Type == 6:
            for s in shape.GroupItems:
                process_shape(slide, s, indent + "  ")

        # 2. 表格
        elif shape.HasTable:
            table = shape.Table
            for r in range(1, table.Rows.Count + 1):
                for c in range(1, table.Columns.Count + 1):
                    cell = table.Cell(r, c)
                    text = cell.Shape.TextFrame.TextRange.Text.strip()
                    if text:
                        translated = translate_text_to_indonesian(text)
                        cell.Shape.TextFrame.TextRange.Text = translated

        # 3. 文字框
        elif shape.HasTextFrame:
            text = shape.TextFrame.TextRange.Text.strip()
            if text:
                translated = translate_text_to_indonesian(text)
                shape.TextFrame.TextRange.Text = translated

        # 4. 圖片 OCR
        elif shape.Type == 13:  # msoPicture
            process_picture_shape(slide, shape)

    except Exception as e:
        print(f"{indent}形狀錯誤: {e}")


# ===== 開始 PowerPoint 處理 =====
powerpoint = win32com.client.Dispatch("PowerPoint.Application")
powerpoint.Visible = True

ppt_path = r"C:\Users\sean.ma\Documents\TextBook\投影片翻譯v2\114年菸害防制宣導講座 (翻譯泰國、越南、印尼).pptx"
presentation = powerpoint.Presentations.Open(os.path.abspath(ppt_path))

for slide in presentation.Slides:
    print(f"\n=== 處理第 {slide.SlideIndex} 頁 ===")
    for shape in list(slide.Shapes):
        process_shape(slide, shape, "  ")

output_path = r"C:\Users\sean.ma\Documents\TextBook\投影片翻譯v2\114年菸害防制宣導講座_印尼文.pptx"
presentation.SaveAs(os.path.abspath(output_path))

print(f"\n完成! 已輸出：{output_path}")

presentation.Close()
powerpoint.Quit()
