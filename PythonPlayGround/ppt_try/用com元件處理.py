import zipfile
import io
import xml.etree.ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main"
}

# colors: 用 12 個鍵：dk1, lt1, dk2, lt2, accent1..accent6, hlink, folHlink
# 值用 6 碼 HEX（不含 #），例如 "2F5597"
DEFAULT_COLORS = {
    "dk1": "000000", "lt1": "FFFFFF",
    "dk2": "1F1F1F", "lt2": "F2F2F2",
    "accent1": "2F5597", "accent2": "ED7D31", "accent3": "A5A5A5",
    "accent4": "FFC000", "accent5": "4472C4", "accent6": "70AD47",
    "hlink": "0563C1", "folHlink": "954F72",
}

def _set_srgb(node, hexval):
    # node 例如 <a:dk1>，其下通常是 <a:srgbClr val="..."/>
    srgb = node.find("a:srgbClr", NS)
    if srgb is None:
        # 某些主題用 schemeClr 等，先清掉子節點再新建 srgbClr
        for c in list(node):
            node.remove(c)
        srgb = ET.SubElement(node, f"{{{NS['a']}}}srgbClr")
    srgb.set("val", hexval.upper())

def patch_theme_colors(theme_xml_bytes, colors):
    tree = ET.ElementTree(ET.fromstring(theme_xml_bytes))
    root = tree.getroot()
    # a:theme/a:themeElements/a:clrScheme
    clr = root.find("a:themeElements/a:clrScheme", NS)
    if clr is None:
        raise ValueError("theme1.xml 無 clrScheme，無法修改")

    # 依鍵名尋找對應節點並覆寫
    for key, val in colors.items():
        node = clr.find(f"a:{key}", NS)
        if node is None:
            # 若缺少該節點，建立它（保持順序不是必要，但可行）
            node = ET.SubElement(clr, f"{{{NS['a']}}}{key}")
        _set_srgb(node, val)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def patch_theme_fonts(theme_xml_bytes, major_latin="Calibri", minor_latin="Calibri"):
    tree = ET.ElementTree(ET.fromstring(theme_xml_bytes))
    root = tree.getroot()
    # a:theme/a:themeElements/a:fontScheme
    fsch = root.find("a:themeElements/a:fontScheme", NS)
    if fsch is None:
        # 若完全沒有，建立基本結構
        te = root.find("a:themeElements", NS)
        if te is None:
            te = ET.SubElement(root, f"{{{NS['a']}}}themeElements")
        fsch = ET.SubElement(te, f"{{{NS['a']}}}fontScheme", {"name": "Custom"})

        major = ET.SubElement(fsch, f"{{{NS['a']}}}majorFont")
        minor = ET.SubElement(fsch, f"{{{NS['a']}}}minorFont")
        ET.SubElement(major, f"{{{NS['a']}}}latin", {"typeface": major_latin})
        ET.SubElement(minor, f"{{{NS['a']}}}latin", {"typeface": minor_latin})
    else:
        major = fsch.find("a:majorFont", NS)
        minor = fsch.find("a:minorFont", NS)
        if major is None:
            major = ET.SubElement(fsch, f"{{{NS['a']}}}majorFont")
        if minor is None:
            minor = ET.SubElement(fsch, f"{{{NS['a']}}}minorFont")

        major_lat = major.find("a:latin", NS)
        if major_lat is None:
            major_lat = ET.SubElement(major, f"{{{NS['a']}}}latin", {"typeface": major_latin})
        else:
            major_lat.set("typeface", major_latin)

        minor_lat = minor.find("a:latin", NS)
        if minor_lat is None:
            minor_lat = ET.SubElement(minor, f"{{{NS['a']}}}latin", {"typeface": minor_latin})
        else:
            minor_lat.set("typeface", minor_latin)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)

def modify_pptx_theme(src_pptx_path, dst_pptx_path,
                      colors=DEFAULT_COLORS,
                      major_latin="Microsoft JhengHei",
                      minor_latin="Microsoft JhengHei",
                      theme_rel_path="ppt/theme/theme1.xml"):
    # 讀取原檔
    with open(src_pptx_path, "rb") as f:
        src_bytes = f.read()

    with zipfile.ZipFile(io.BytesIO(src_bytes), "r") as zin:
        # 先取出 theme1.xml
        try:
            theme_xml = zin.read(theme_rel_path)
        except KeyError:
            raise FileNotFoundError(f"{theme_rel_path} 不存在，可能此檔使用不同主題編號或無主題")

        # 改色
        theme_xml = patch_theme_colors(theme_xml, colors)
        # 改字型（可略）
        theme_xml = patch_theme_fonts(theme_xml, major_latin=major_latin, minor_latin=minor_latin)

        # 重打包
        with zipfile.ZipFile(dst_pptx_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == theme_rel_path:
                    data = theme_xml
                zout.writestr(item, data)

# === 使用範例 ===
if __name__ == "__main__":
    custom_colors = {
        "dk1": "0B0B0B", "lt1": "FFFFFF",
        "dk2": "1E2A44", "lt2": "E9EEF7",
        "accent1": "2F5597", "accent2": "2D9CDB", "accent3": "6FCF97",
        "accent4": "F2C94C", "accent5": "EB5757", "accent6": "9B51E0",
        "hlink": "1A73E8", "folHlink": "7B1FA2",
    }
    modify_pptx_theme(
        src_pptx_path="input.pptx",
        dst_pptx_path="output.pptx",
        colors=custom_colors,
        major_latin="Microsoft JhengHei",
        minor_latin="Microsoft JhengHei",
        theme_rel_path="ppt/theme/theme1.xml"  # 若有多主題，改成 theme2.xml 等
    )
    print("done")
