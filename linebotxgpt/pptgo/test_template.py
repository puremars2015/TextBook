#!/usr/bin/env python3
"""
測試使用模板生成 PPT 的功能
"""

import os
import sys
from datetime import datetime

# 先安裝必要的模組
try:
    import anthropic
except ImportError:
    print("anthropic 模組未安裝，正在安裝...")
    os.system("pip install anthropic")
    
from makepptv3 import AIpptGenerator, SlideContent

def test_template_generation():
    """測試使用模板生成 PPT"""
    
    # 設定模板路徑
    template_path = "/Users/maenqi/TextBook/linebotxgpt/pptgo/週報20250919馬恩奇.pptx"
    
    # 創建生成器（不需要 API key 進行測試）
    generator = AIpptGenerator("test-api-key")
    
    # 手動創建一些測試內容
    test_slides = [
        SlideContent(
            title="測試簡報標題",
            content=["使用模板生成的測試簡報"],
            layout="title"
        ),
        SlideContent(
            title="第一個內容頁",
            content=[
                "這是第一個要點",
                "這是第二個要點", 
                "這是第三個要點"
            ],
            layout="content"
        ),
        SlideContent(
            title="雙欄內容頁",
            content=[
                "左欄第一點",
                "左欄第二點",
                "右欄第一點", 
                "右欄第二點"
            ],
            layout="two_column"
        ),
        SlideContent(
            title="另一個內容頁",
            content=[
                "更多內容要點",
                "詳細說明事項",
                "重要結論總結"
            ],
            layout="content"
        )
    ]
    
    try:
        print("正在使用模板生成簡報...")
        
        # 使用模板創建簡報
        presentation = generator.create_presentation(
            slides=test_slides, 
            template_path=template_path,
            add_ending_slide=True
        )
        
        # 儲存檔案
        output_filename = f"test_template_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        generator.save_presentation(output_filename)
        
        print(f"✓ 成功生成簡報：{output_filename}")
        print(f"✓ 總共生成 {len(presentation.slides)} 張投影片")
        
        # 顯示生成的投影片資訊
        print("\n生成的投影片清單:")
        for i, slide in enumerate(presentation.slides):
            layout_name = slide.slide_layout.name
            title_text = ""
            if slide.shapes.title:
                title_text = slide.shapes.title.text
            print(f"投影片 {i+1}: {layout_name} - '{title_text}'")
        
        return True
        
    except Exception as e:
        print(f"✗ 生成簡報時發生錯誤：{e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*50)
    print("測試模板 PPT 生成功能")
    print("="*50)
    
    success = test_template_generation()
    
    if success:
        print("\n🎉 測試成功！模板功能正常運作。")
    else:
        print("\n❌ 測試失敗，請檢查錯誤訊息。")