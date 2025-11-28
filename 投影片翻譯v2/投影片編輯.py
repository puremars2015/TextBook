import os
import win32com.client
from win32com.client import constants


class PPTEditor:
    """PowerPoint 編輯器類別"""
    
    def __init__(self, ppt_path=None):
        """
        初始化 PowerPoint 編輯器
        
        Args:
            ppt_path: PowerPoint 檔案路徑（可選）
        """
        self.powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        self.powerpoint.Visible = True
        self.presentation = None
        
        if ppt_path:
            self.open_presentation(ppt_path)
    
    def open_presentation(self, ppt_path):
        """
        開啟 PowerPoint 檔案
        
        Args:
            ppt_path: PowerPoint 檔案路徑
        """
        abs_path = os.path.abspath(ppt_path)
        self.presentation = self.powerpoint.Presentations.Open(abs_path)
        print(f"已開啟: {ppt_path}")
    
    def create_presentation(self):
        """建立新的 PowerPoint 簡報"""
        self.presentation = self.powerpoint.Presentations.Add()
        print("已建立新簡報")
    
    def save_presentation(self, output_path):
        """
        儲存 PowerPoint 檔案
        
        Args:
            output_path: 輸出檔案路徑
        """
        if not self.presentation:
            print("錯誤：沒有開啟的簡報")
            return
        
        abs_path = os.path.abspath(output_path)
        self.presentation.SaveAs(abs_path)
        print(f"已儲存: {output_path}")
    
    def close(self):
        """關閉 PowerPoint"""
        if self.presentation:
            self.presentation.Close()
        self.powerpoint.Quit()
        print("已關閉 PowerPoint")
    
    # ===== 功能 1: 新增特定類型的投影片 =====
    
    def add_slide_by_layout(self, layout_index, position=-1):
        """
        根據版面配置新增投影片
        
        Args:
            layout_index: 版面配置索引 (1-based)
                1: 標題投影片
                2: 標題與內容
                3: 區段標題
                4: 兩欄內容
                5: 比較
                6: 僅標題
                7: 空白
                8: 含標題的內容
                9: 圖片與標題
                10: 標題與縱向文字
                11: 縱向標題與文字
            position: 插入位置 (預設 -1 表示最後)
        
        Returns:
            新增的投影片物件
        """
        if not self.presentation:
            print("錯誤：沒有開啟的簡報")
            return None
        
        try:
            # 取得版面配置
            layout = self.presentation.SlideMaster.CustomLayouts(layout_index)
            
            # 決定插入位置
            if position == -1:
                position = self.presentation.Slides.Count + 1
            
            # 新增投影片
            slide = self.presentation.Slides.AddSlide(position, layout)
            print(f"已新增投影片 (版面配置 {layout_index}) 於位置 {position}")
            return slide
        
        except Exception as e:
            print(f"新增投影片錯誤: {e}")
            return None
    
    def add_title_slide(self, title="", subtitle="", position=-1):
        """
        新增標題投影片
        
        Args:
            title: 標題文字
            subtitle: 副標題文字
            position: 插入位置
        
        Returns:
            新增的投影片物件
        """
        slide = self.add_slide_by_layout(1, position)
        if slide and (title or subtitle):
            try:
                if title:
                    slide.Shapes.Title.TextFrame.TextRange.Text = title
                if subtitle and len(slide.Shapes) > 1:
                    slide.Shapes(2).TextFrame.TextRange.Text = subtitle
            except Exception as e:
                print(f"設定文字錯誤: {e}")
        return slide
    
    def add_content_slide(self, title="", content="", position=-1):
        """
        新增標題與內容投影片
        
        Args:
            title: 標題文字
            content: 內容文字
            position: 插入位置
        
        Returns:
            新增的投影片物件
        """
        slide = self.add_slide_by_layout(2, position)
        if slide and (title or content):
            try:
                if title:
                    slide.Shapes.Title.TextFrame.TextRange.Text = title
                if content and len(slide.Shapes) > 1:
                    slide.Shapes(2).TextFrame.TextRange.Text = content
            except Exception as e:
                print(f"設定文字錯誤: {e}")
        return slide
    
    def add_blank_slide(self, position=-1):
        """
        新增空白投影片
        
        Args:
            position: 插入位置
        
        Returns:
            新增的投影片物件
        """
        return self.add_slide_by_layout(7, position)
    
    def add_section_header_slide(self, title="", subtitle="", position=-1):
        """
        新增區段標題投影片
        
        Args:
            title: 標題文字
            subtitle: 副標題文字
            position: 插入位置
        
        Returns:
            新增的投影片物件
        """
        slide = self.add_slide_by_layout(3, position)
        if slide and (title or subtitle):
            try:
                if title:
                    slide.Shapes.Title.TextFrame.TextRange.Text = title
                if subtitle and len(slide.Shapes) > 1:
                    slide.Shapes(2).TextFrame.TextRange.Text = subtitle
            except Exception as e:
                print(f"設定文字錯誤: {e}")
        return slide
    
    # ===== 功能 2: 編輯特定頁面的文字 =====
    
    def get_slide(self, slide_number):
        """
        取得特定投影片
        
        Args:
            slide_number: 投影片編號 (1-based)
        
        Returns:
            投影片物件，若不存在則回傳 None
        """
        if not self.presentation:
            print("錯誤：沒有開啟的簡報")
            return None
        
        try:
            if 1 <= slide_number <= self.presentation.Slides.Count:
                return self.presentation.Slides(slide_number)
            else:
                print(f"錯誤：投影片編號 {slide_number} 超出範圍 (1-{self.presentation.Slides.Count})")
                return None
        except Exception as e:
            print(f"取得投影片錯誤: {e}")
            return None
    
    def edit_slide_title(self, slide_number, new_title):
        """
        編輯投影片標題
        
        Args:
            slide_number: 投影片編號
            new_title: 新標題文字
        
        Returns:
            是否成功
        """
        slide = self.get_slide(slide_number)
        if not slide:
            return False
        
        try:
            if slide.Shapes.HasTitle:
                slide.Shapes.Title.TextFrame.TextRange.Text = new_title
                print(f"已更新第 {slide_number} 頁標題: {new_title}")
                return True
            else:
                print(f"第 {slide_number} 頁沒有標題")
                return False
        except Exception as e:
            print(f"編輯標題錯誤: {e}")
            return False
    
    def edit_shape_text(self, slide_number, shape_index, new_text):
        """
        編輯特定形狀的文字
        
        Args:
            slide_number: 投影片編號
            shape_index: 形狀索引 (1-based)
            new_text: 新文字內容
        
        Returns:
            是否成功
        """
        slide = self.get_slide(slide_number)
        if not slide:
            return False
        
        try:
            if 1 <= shape_index <= slide.Shapes.Count:
                shape = slide.Shapes(shape_index)
                if shape.HasTextFrame:
                    shape.TextFrame.TextRange.Text = new_text
                    print(f"已更新第 {slide_number} 頁形狀 {shape_index} 的文字")
                    return True
                else:
                    print(f"第 {slide_number} 頁形狀 {shape_index} 無文字框")
                    return False
            else:
                print(f"形狀索引 {shape_index} 超出範圍")
                return False
        except Exception as e:
            print(f"編輯形狀文字錯誤: {e}")
            return False
    
    def edit_all_text_in_slide(self, slide_number, text_mapping):
        """
        編輯投影片中所有文字
        
        Args:
            slide_number: 投影片編號
            text_mapping: 文字對應字典 {舊文字: 新文字}
        
        Returns:
            是否成功
        """
        slide = self.get_slide(slide_number)
        if not slide:
            return False
        
        try:
            for shape in slide.Shapes:
                self._replace_shape_text(shape, text_mapping)
            print(f"已更新第 {slide_number} 頁的所有文字")
            return True
        except Exception as e:
            print(f"編輯所有文字錯誤: {e}")
            return False
    
    def _replace_shape_text(self, shape, text_mapping):
        """
        遞迴替換形狀中的文字（處理群組、表格等）
        
        Args:
            shape: 形狀物件
            text_mapping: 文字對應字典
        """
        try:
            # 處理群組
            if shape.Type == 6:  # msoGroup
                for s in shape.GroupItems:
                    self._replace_shape_text(s, text_mapping)
            
            # 處理表格
            elif shape.HasTable:
                table = shape.Table
                for r in range(1, table.Rows.Count + 1):
                    for c in range(1, table.Columns.Count + 1):
                        cell = table.Cell(r, c)
                        text = cell.Shape.TextFrame.TextRange.Text
                        for old_text, new_text in text_mapping.items():
                            if old_text in text:
                                text = text.replace(old_text, new_text)
                        cell.Shape.TextFrame.TextRange.Text = text
            
            # 處理文字框
            elif shape.HasTextFrame:
                text = shape.TextFrame.TextRange.Text
                for old_text, new_text in text_mapping.items():
                    if old_text in text:
                        text = text.replace(old_text, new_text)
                shape.TextFrame.TextRange.Text = text
        
        except Exception as e:
            print(f"替換形狀文字錯誤: {e}")
    
    def list_all_text_in_slide(self, slide_number):
        """
        列出投影片中所有文字內容
        
        Args:
            slide_number: 投影片編號
        
        Returns:
            文字列表
        """
        slide = self.get_slide(slide_number)
        if not slide:
            return []
        
        texts = []
        try:
            for i, shape in enumerate(slide.Shapes, 1):
                shape_texts = self._extract_shape_text(shape, i)
                texts.extend(shape_texts)
            return texts
        except Exception as e:
            print(f"列出文字錯誤: {e}")
            return []
    
    def _extract_shape_text(self, shape, shape_index):
        """
        遞迴提取形狀中的文字
        
        Args:
            shape: 形狀物件
            shape_index: 形狀索引
        
        Returns:
            文字列表
        """
        texts = []
        try:
            # 處理群組
            if shape.Type == 6:  # msoGroup
                for s in shape.GroupItems:
                    texts.extend(self._extract_shape_text(s, shape_index))
            
            # 處理表格
            elif shape.HasTable:
                table = shape.Table
                for r in range(1, table.Rows.Count + 1):
                    for c in range(1, table.Columns.Count + 1):
                        cell = table.Cell(r, c)
                        text = cell.Shape.TextFrame.TextRange.Text.strip()
                        if text:
                            texts.append(f"[形狀 {shape_index}, 表格 ({r},{c})] {text}")
            
            # 處理文字框
            elif shape.HasTextFrame:
                text = shape.TextFrame.TextRange.Text.strip()
                if text:
                    texts.append(f"[形狀 {shape_index}] {text}")
        
        except Exception as e:
            pass
        
        return texts
    
    def get_slide_count(self):
        """取得投影片總數"""
        if self.presentation:
            return self.presentation.Slides.Count
        return 0


# ===== 使用範例 =====
def main():
    """主程式範例"""
    
    # 範例 1: 建立新簡報並新增不同類型的投影片
    print("\n=== 範例 1: 建立新簡報 ===")
    editor = PPTEditor()
    editor.create_presentation()
    
    # 新增標題投影片
    editor.add_title_slide("我的簡報", "副標題內容")
    
    # 新增內容投影片
    editor.add_content_slide("第一章", "這是第一章的內容\n• 重點一\n• 重點二\n• 重點三")
    
    # 新增區段標題
    editor.add_section_header_slide("第二部分", "詳細說明")
    
    # 新增空白投影片
    editor.add_blank_slide()
    
    # 儲存檔案
    output_path = r"C:\Users\sean.ma\Documents\TextBook\投影片翻譯v2\新簡報範例.pptx"
    editor.save_presentation(output_path)
    editor.close()
    
    # 範例 2: 開啟現有簡報並編輯文字
    print("\n=== 範例 2: 編輯現有簡報 ===")
    ppt_path = r"C:\Users\sean.ma\Documents\TextBook\投影片翻譯v2\新簡報範例.pptx"
    editor = PPTEditor(ppt_path)
    
    # 列出第 2 頁的所有文字
    print(f"\n投影片總數: {editor.get_slide_count()}")
    print("\n第 2 頁的文字內容:")
    texts = editor.list_all_text_in_slide(2)
    for text in texts:
        print(f"  {text}")
    
    # 編輯第 2 頁標題
    editor.edit_slide_title(2, "第一章（已修改）")
    
    # 批量替換文字
    text_mapping = {
        "重點一": "重點 A",
        "重點二": "重點 B",
        "重點三": "重點 C"
    }
    editor.edit_all_text_in_slide(2, text_mapping)
    
    # 儲存修改
    output_path = r"C:\Users\sean.ma\Documents\TextBook\投影片翻譯v2\編輯後的簡報.pptx"
    editor.save_presentation(output_path)
    editor.close()


if __name__ == "__main__":
    main()
