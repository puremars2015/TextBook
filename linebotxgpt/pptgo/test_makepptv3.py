#!/usr/bin/env python3
"""
測試修正後的 makepptv3.py 模板功能
"""

import os
from makepptv3 import AIpptGenerator, SlideContent

def test_main_program():
    """測試主程式的模板功能"""
    
    # 模板路徑
    template_path = "/Users/maenqi/TextBook/linebotxgpt/pptgo/週報20250919馬恩奇.pptx"
    
    # 創建生成器
    generator = AIpptGenerator("test-api-key")
    
    # 創建測試內容
    test_slides = [
        SlideContent(
            title="AI 技術應用簡報",
            content=["探討 AI 在現代商業中的應用", "2025年9月版"],
            layout="title"
        ),
        SlideContent(
            title="AI 技術簡介",
            content=[
                "人工智慧發展歷程",
                "機器學習的核心概念",
                "深度學習的突破",
                "現代 AI 的應用場景"
            ],
            layout="content"
        ),
        SlideContent(
            title="應用領域對比",
            content=[
                "金融科技應用",
                "醫療健康創新",
                "製造業自動化",
                "零售電商優化"
            ],
            layout="two_column"
        ),
        SlideContent(
            title="實施策略",
            content=[
                "技術選型與評估",
                "團隊建設與培訓",
                "階段性部署計劃",
                "風險管理與控制"
            ],
            layout="content"
        )
    ]
    
    try:
        print("正在使用修正後的模板功能生成簡報...")
        
        # 使用模板創建簡報
        presentation = generator.create_presentation(
            slides=test_slides,
            template_path=template_path,
            add_ending_slide=True
        )
        
        # 儲存檔案
        from datetime import datetime
        output_filename = f"makepptv3_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        generator.save_presentation(output_filename)
        
        print(f"✅ 成功生成簡報：{output_filename}")
        print(f"✅ 總共生成 {len(presentation.slides)} 張投影片")
        
        # 顯示生成的投影片資訊
        print("\n📋 生成的投影片清單:")
        for i, slide in enumerate(presentation.slides):
            layout_name = slide.slide_layout.name
            title_text = "未設定"
            
            # 嘗試讀取標題
            for placeholder in slide.placeholders:
                try:
                    if hasattr(placeholder.placeholder_format, 'type'):
                        ph_type = placeholder.placeholder_format.type
                        if ph_type == 1 and hasattr(placeholder, 'text_frame'):
                            title_text = placeholder.text_frame.text or "未設定"
                            break
                except:
                    continue
            
            if title_text == "未設定" and slide.placeholders:
                try:
                    for placeholder in slide.placeholders:
                        if hasattr(placeholder, 'text_frame') and placeholder.text_frame.text:
                            title_text = placeholder.text_frame.text
                            break
                except:
                    pass
            
            print(f"  投影片 {i+1}: {layout_name} - '{title_text}'")
        
        return True
        
    except Exception as e:
        print(f"❌ 生成簡報時發生錯誤：{e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("測試 makepptv3.py 修正後的模板功能")
    print("="*60)
    
    success = test_main_program()
    
    if success:
        print("\n🎉 測試完成！修正後的模板功能正常運作。")
        print("現在您的程式可以正確使用模板中的首頁、內容頁和尾頁了！")
    else:
        print("\n❌ 測試失敗，請檢查錯誤訊息。")