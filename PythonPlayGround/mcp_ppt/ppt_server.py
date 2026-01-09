import os
import win32com.client
from fastmcp import FastMCP

# 创建 FastMCP 实例
mcp = FastMCP("PPT Server")


class PPTHandler:
    """处理 PowerPoint 操作的类"""
    
    def __init__(self):
        self.ppt_app = None
        self.presentation = None
        self.current_file_path = None
    
    def open_powerpoint(self, file_path: str) -> dict:
        """打开 PowerPoint 文件"""
        try:
            # 检查文件是否存在
            if not os.path.exists(file_path):
                return {"success": False, "error": f"文件不存在: {file_path}"}
            
            abs_path = os.path.abspath(file_path)
            
            # 如果已经打开同一个文件，直接返回
            if self.presentation and self.current_file_path == abs_path:
                return {
                    "success": True,
                    "file_name": os.path.basename(file_path),
                    "file_path": abs_path,
                    "slide_count": self.presentation.Slides.Count,
                    "message": f"文件已打开，共 {self.presentation.Slides.Count} 张投影片",
                    "already_open": True
                }
            
            # 如果打开了其他文件，先关闭
            if self.presentation:
                self.close_presentation()
            
            # 创建 PowerPoint 应用程序实例
            if self.ppt_app is None:
                self.ppt_app = win32com.client.Dispatch("PowerPoint.Application")
                self.ppt_app.Visible = True
            
            # 打开演示文稿
            self.presentation = self.ppt_app.Presentations.Open(abs_path)
            self.current_file_path = abs_path
            
            # 获取基本信息
            slide_count = self.presentation.Slides.Count
            file_name = os.path.basename(file_path)
            
            return {
                "success": True,
                "file_name": file_name,
                "file_path": os.path.abspath(file_path),
                "slide_count": slide_count,
                "message": f"成功打开文件，共 {slide_count} 张投影片"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close_presentation(self):
        """关闭当前演示文稿"""
        try:
            if self.presentation:
                self.presentation.Close()
                self.presentation = None
                self.current_file_path = None
        except:
            pass


# 创建 PPT 处理器实例
ppt_handler = PPTHandler()


@mcp.tool()
def read_ppt(file_path: str) -> dict:
    """
    读取 PowerPoint 文件的内容
    
    Args:
        file_path: PPT 文件的完整路径
        
    Returns:
        包含文件信息和所有投影片内容的字典
    """
    try:
        # 先打开文件
        result = ppt_handler.open_powerpoint(file_path)
        if not result["success"]:
            return result
        
        slides_data = []
        
        # 遍历所有投影片
        for i in range(1, ppt_handler.presentation.Slides.Count + 1):
            slide = ppt_handler.presentation.Slides(i)
            slide_info = {
                "slide_number": i,
                "shapes": []
            }
            
            # 遍历投影片中的所有形状
            for j in range(1, slide.Shapes.Count + 1):
                shape = slide.Shapes(j)
                shape_info = {
                    "shape_index": j,
                    "name": shape.Name,
                    "type": shape.Type
                }
                
                # 如果是文本框，读取文本内容
                if shape.HasTextFrame:
                    if shape.TextFrame.HasText:
                        shape_info["text"] = shape.TextFrame.TextRange.Text
                
                slide_info["shapes"].append(shape_info)
            
            slides_data.append(slide_info)
        
        return {
            "success": True,
            "file_name": result["file_name"],
            "file_path": result["file_path"],
            "slide_count": result["slide_count"],
            "slides": slides_data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def write_to_ppt(file_path: str, slide_number: int, shape_index: int, text: str) -> dict:
    """
    写入文字到指定投影片的指定形状中
    
    Args:
        file_path: PPT 文件的完整路径
        slide_number: 投影片编号（从 1 开始）
        shape_index: 形状索引（从 1 开始）
        text: 要写入的文字内容
        
    Returns:
        包含操作结果的字典
    """
    try:
        # 打开文件
        result = ppt_handler.open_powerpoint(file_path)
        if not result["success"]:
            return result
        
        # 检查投影片编号是否有效
        if slide_number < 1 or slide_number > ppt_handler.presentation.Slides.Count:
            return {
                "success": False,
                "error": f"投影片编号无效。有效范围: 1-{ppt_handler.presentation.Slides.Count}"
            }
        
        slide = ppt_handler.presentation.Slides(slide_number)
        
        # 检查形状索引是否有效
        if shape_index < 1 or shape_index > slide.Shapes.Count:
            return {
                "success": False,
                "error": f"形状索引无效。有效范围: 1-{slide.Shapes.Count}"
            }
        
        shape = slide.Shapes(shape_index)
        
        # 检查形状是否有文本框
        if not shape.HasTextFrame:
            return {
                "success": False,
                "error": "该形状不支持文本"
            }
        
        # 写入文本
        shape.TextFrame.TextRange.Text = text
        
        # 保存文件
        ppt_handler.presentation.Save()
        
        return {
            "success": True,
            "message": f"成功写入文本到投影片 {slide_number}，形状 {shape_index}",
            "slide_number": slide_number,
            "shape_index": shape_index,
            "text": text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def add_slide(file_path: str, title: str, content: str) -> dict:
    """
    添加新的投影片并写入标题和内容
    
    Args:
        file_path: PPT 文件的完整路径
        title: 投影片标题
        content: 投影片内容
        
    Returns:
        包含操作结果的字典
    """
    try:
        # 打开文件
        result = ppt_handler.open_powerpoint(file_path)
        if not result["success"]:
            return result
        
        # 添加新投影片（使用标题和内容布局）
        slide_index = ppt_handler.presentation.Slides.Count + 1
        slide = ppt_handler.presentation.Slides.Add(slide_index, 2)  # 2 = ppLayoutText (标题和文本布局)
        
        # 设置标题
        if slide.Shapes.Count >= 1:
            slide.Shapes(1).TextFrame.TextRange.Text = title
        
        # 设置内容
        if slide.Shapes.Count >= 2:
            slide.Shapes(2).TextFrame.TextRange.Text = content
        
        # 保存文件
        ppt_handler.presentation.Save()
        
        return {
            "success": True,
            "message": f"成功添加新投影片（第 {slide_index} 张）",
            "slide_number": slide_index,
            "title": title,
            "content": content
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def update_table(file_path: str, slide_number: int, table_index: int, row: int, col: int, text: str) -> dict:
    """
    修改投影片上表格的内容
    
    Args:
        file_path: PPT 文件的完整路径
        slide_number: 投影片编号（从 1 开始）
        table_index: 表格在投影片中的索引（从 1 开始）
        row: 表格的行号（从 1 开始）
        col: 表格的列号（从 1 开始）
        text: 要写入的文字内容
        
    Returns:
        包含操作结果的字典
    """
    try:
        # 打开文件
        result = ppt_handler.open_powerpoint(file_path)
        if not result["success"]:
            return result
        
        # 检查投影片编号是否有效
        if slide_number < 1 or slide_number > ppt_handler.presentation.Slides.Count:
            return {
                "success": False,
                "error": f"投影片编号无效。有效范围: 1-{ppt_handler.presentation.Slides.Count}"
            }
        
        slide = ppt_handler.presentation.Slides(slide_number)
        
        # 查找表格
        table_count = 0
        target_table = None
        
        for i in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(i)
            # 检查是否为表格类型 (Type = 19 表示表格)
            if shape.HasTable:
                table_count += 1
                if table_count == table_index:
                    target_table = shape.Table
                    break
        
        if target_table is None:
            return {
                "success": False,
                "error": f"未找到第 {table_index} 个表格。投影片中共有 {table_count} 个表格"
            }
        
        # 检查行列是否有效
        if row < 1 or row > target_table.Rows.Count:
            return {
                "success": False,
                "error": f"行号无效。有效范围: 1-{target_table.Rows.Count}"
            }
        
        if col < 1 or col > target_table.Columns.Count:
            return {
                "success": False,
                "error": f"列号无效。有效范围: 1-{target_table.Columns.Count}"
            }
        
        # 修改表格单元格内容
        cell = target_table.Cell(row, col)
        cell.Shape.TextFrame.TextRange.Text = text
        
        # 保存文件
        ppt_handler.presentation.Save()
        
        return {
            "success": True,
            "message": f"成功修改投影片 {slide_number} 的表格（第 {table_index} 个），单元格 ({row}, {col})",
            "slide_number": slide_number,
            "table_index": table_index,
            "row": row,
            "col": col,
            "text": text
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def read_table(file_path: str, slide_number: int, table_index: int = 1) -> dict:
    """
    读取投影片上表格的内容
    
    Args:
        file_path: PPT 文件的完整路径
        slide_number: 投影片编号（从 1 开始）
        table_index: 表格在投影片中的索引（从 1 开始，默认为 1）
        
    Returns:
        包含表格数据的字典
    """
    try:
        # 打开文件
        result = ppt_handler.open_powerpoint(file_path)
        if not result["success"]:
            return result
        
        # 检查投影片编号是否有效
        if slide_number < 1 or slide_number > ppt_handler.presentation.Slides.Count:
            return {
                "success": False,
                "error": f"投影片编号无效。有效范围: 1-{ppt_handler.presentation.Slides.Count}"
            }
        
        slide = ppt_handler.presentation.Slides(slide_number)
        
        # 查找表格
        table_count = 0
        target_table = None
        
        for i in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(i)
            if shape.HasTable:
                table_count += 1
                if table_count == table_index:
                    target_table = shape.Table
                    break
        
        if target_table is None:
            return {
                "success": False,
                "error": f"未找到第 {table_index} 个表格。投影片中共有 {table_count} 个表格"
            }
        
        # 读取表格内容
        table_data = []
        for r in range(1, target_table.Rows.Count + 1):
            row_data = []
            for c in range(1, target_table.Columns.Count + 1):
                cell = target_table.Cell(r, c)
                cell_text = cell.Shape.TextFrame.TextRange.Text
                row_data.append(cell_text)
            table_data.append(row_data)
        
        return {
            "success": True,
            "slide_number": slide_number,
            "table_index": table_index,
            "rows": target_table.Rows.Count,
            "columns": target_table.Columns.Count,
            "data": table_data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def update_table_row(file_path: str, slide_number: int, table_index: int, row: int, data: list) -> dict:
    """
    一次写入表格一整行的数据
    
    Args:
        file_path: PPT 文件的完整路径
        slide_number: 投影片编号（从 1 开始）
        table_index: 表格在投影片中的索引（从 1 开始）
        row: 表格的行号（从 1 开始）
        data: 要写入的数据列表，按列顺序排列
        
    Returns:
        包含操作结果的字典
    """
    try:
        # 打开文件
        result = ppt_handler.open_powerpoint(file_path)
        if not result["success"]:
            return result
        
        # 检查投影片编号是否有效
        if slide_number < 1 or slide_number > ppt_handler.presentation.Slides.Count:
            return {
                "success": False,
                "error": f"投影片编号无效。有效范围: 1-{ppt_handler.presentation.Slides.Count}"
            }
        
        slide = ppt_handler.presentation.Slides(slide_number)
        
        # 查找表格
        table_count = 0
        target_table = None
        
        for i in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(i)
            if shape.HasTable:
                table_count += 1
                if table_count == table_index:
                    target_table = shape.Table
                    break
        
        if target_table is None:
            return {
                "success": False,
                "error": f"未找到第 {table_index} 个表格。投影片中共有 {table_count} 个表格"
            }
        
        # 检查行号是否有效
        if row < 1 or row > target_table.Rows.Count:
            return {
                "success": False,
                "error": f"行号无效。有效范围: 1-{target_table.Rows.Count}"
            }
        
        # 检查数据长度是否超过列数
        if len(data) > target_table.Columns.Count:
            return {
                "success": False,
                "error": f"数据长度 ({len(data)}) 超过表格列数 ({target_table.Columns.Count})"
            }
        
        # 写入每一列的数据
        updated_cells = []
        for col_index, value in enumerate(data, start=1):
            cell = target_table.Cell(row, col_index)
            cell.Shape.TextFrame.TextRange.Text = str(value)
            updated_cells.append(f"({row}, {col_index})")
        
        # 保存文件
        ppt_handler.presentation.Save()
        
        return {
            "success": True,
            "message": f"成功写入表格第 {row} 行，共 {len(data)} 个单元格",
            "slide_number": slide_number,
            "table_index": table_index,
            "row": row,
            "columns_updated": len(data),
            "data": data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def delete_table_row(file_path: str, slide_number: int, table_index: int, row: int) -> dict:
    """
    删除表格中的指定行
    
    Args:
        file_path: PPT 文件的完整路径
        slide_number: 投影片编号（从 1 开始）
        table_index: 表格在投影片中的索引（从 1 开始）
        row: 要删除的行号（从 1 开始）
        
    Returns:
        包含操作结果的字典
    """
    try:
        # 打开文件
        result = ppt_handler.open_powerpoint(file_path)
        if not result["success"]:
            return result
        
        # 检查投影片编号是否有效
        if slide_number < 1 or slide_number > ppt_handler.presentation.Slides.Count:
            return {
                "success": False,
                "error": f"投影片编号无效。有效范围: 1-{ppt_handler.presentation.Slides.Count}"
            }
        
        slide = ppt_handler.presentation.Slides(slide_number)
        
        # 查找表格
        table_count = 0
        target_table = None
        
        for i in range(1, slide.Shapes.Count + 1):
            shape = slide.Shapes(i)
            if shape.HasTable:
                table_count += 1
                if table_count == table_index:
                    target_table = shape.Table
                    break
        
        if target_table is None:
            return {
                "success": False,
                "error": f"未找到第 {table_index} 个表格。投影片中共有 {table_count} 个表格"
            }
        
        # 检查行号是否有效
        if row < 1 or row > target_table.Rows.Count:
            return {
                "success": False,
                "error": f"行号无效。有效范围: 1-{target_table.Rows.Count}"
            }
        
        # 记录删除前的行数
        original_row_count = target_table.Rows.Count
        
        # 删除指定行
        target_table.Rows.Item(row).Delete()
        
        # 保存文件
        ppt_handler.presentation.Save()
        
        return {
            "success": True,
            "message": f"成功删除表格第 {row} 行",
            "slide_number": slide_number,
            "table_index": table_index,
            "deleted_row": row,
            "original_row_count": original_row_count,
            "new_row_count": original_row_count - 1
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def close_ppt() -> dict:
    """
    关闭当前打开的 PowerPoint 文件
    
    Returns:
        包含操作结果的字典
    """
    try:
        if ppt_handler.presentation is None:
            return {
                "success": True,
                "message": "没有打开的 PowerPoint 文件"
            }
        
        file_name = os.path.basename(ppt_handler.current_file_path) if ppt_handler.current_file_path else "未知文件"
        ppt_handler.close_presentation()
        
        return {
            "success": True,
            "message": f"已关闭文件: {file_name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    print("=" * 60)
    print("PPT MCP Server 启动中...")
    print("=" * 60)
    print("可用工具:")
    print("  1. read_ppt - 读取 PowerPoint 文件内容")
    print("  2. write_to_ppt - 写入文字到指定位置")
    print("  3. add_slide - 添加新投影片")
    print("  4. update_table - 修改表格单个单元格内容")
    print("  5. update_table_row - 一次写入表格一整行数据")
    print("  6. delete_table_row - 删除表格中的指定行")
    print("  7. read_table - 读取表格内容")
    print("  8. close_ppt - 关闭当前打开的文件")
    print("=" * 60)
    print("提示: 文件会保持打开状态，完成所有操作后请使用 close_ppt 关闭")
    print("=" * 60)
    print(f"Server 地址: http://127.0.0.1:8801")
    print("=" * 60)
    
    mcp.run(transport='sse', host="127.0.0.1", port=8801)
