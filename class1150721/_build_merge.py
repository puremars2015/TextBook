import os

BASE = os.environ.get("MERGE_BASE", r"c:\Users\sean.ma\Documents\TextBook\AI教學課程")
OUT = os.environ.get("MERGE_OUT", r"c:\Users\sean.ma\Documents\TextBook\class1150721\_generated_merge.md")

sessions = [
    ("7/21", "第01堂-AI原生開發與LLM核心架構.md"),
    ("7/28", "第02堂-AI Agent邏輯建構與自動化引擎配置.md"),
    ("8/04", "第03堂-巨量數據調度工程與非結構化資料轉換.md"),
    ("8/11", "第04堂-跨平台Web數據擷取與異質系統整合.md"),
    ("8/18", "第05堂-智慧通訊協作：電子郵件與Office流程自動化.md"),
    ("8/25", "第06堂-檔案系統運維與傳統系統介面整合.md"),
    ("9/01", "第07堂-Vibe Coding驅動：智慧動態報表系統開發.md"),
    ("9/08", "第08堂-實作：智慧多通路內容行銷與分發系統.md"),
    ("9/15", "第09堂-實作：AI智慧研報與商務情報搜集系統.md"),
    ("9/22", "第10堂-實作：AI智慧驅動視覺化簡報生成.md"),
    ("9/29", "第11堂-實作：智慧客服郵件決策支援系統.md"),
    ("10/06", "第12堂-進階實務：Vibe Coding與Agent系統協作.md"),
    ("10/13", "第13堂-案例分析：企業供應鏈數據管理與結構化工程.md"),
    ("10/20", "第14堂-案例分析：敏捷管理自動化—智慧週報生成系統.md"),
]

def demote_line(line):
    stripped = line.lstrip('#')
    n_hashes = len(line) - len(stripped)
    if n_hashes == 0:
        return line
    # only demote if it's an actual header (# followed by space)
    if not stripped.startswith(' '):
        return line
    return ('#' * (n_hashes + 1)) + stripped

def demote_lines_outside_code(lines):
    result = []
    in_code = False
    for l in lines:
        if l.lstrip().startswith("```"):
            in_code = not in_code
            result.append(l)
            continue
        if in_code:
            result.append(l)
        else:
            result.append(demote_line(l))
    return result

def read_file(base, fname):
    path = os.path.join(base, fname)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

toc_lines = []
sections = []
overview_rows = []

for idx, (date, fname) in enumerate(sessions, start=1):
    text = read_file(BASE, fname)
    lines = text.splitlines()
    # first non-empty line should be the H1 title
    first_idx = next(i for i, l in enumerate(lines) if l.strip())
    h1 = lines[first_idx]
    title_text = h1.lstrip('#').strip()
    anchor_id = f"week-{idx:02d}"
    heading = f'<a id="{anchor_id}"></a>\n\n## {date}｜{title_text}'
    rest = lines[first_idx + 1:]
    demoted_rest = demote_lines_outside_code(rest)
    section_text = heading + "\n\n" + "\n".join(demoted_rest).strip("\n")
    sections.append(section_text)
    toc_lines.append(f"{idx}. [{date}｜{title_text}](#{anchor_id})")
    overview_rows.append((date, title_text, anchor_id))

doc = []
doc.append("# 教材與每日課程說明\n")
doc.append("本文件依照課程日期，彙整每一堂課的學習目標、核心概念說明、實作步驟、程式碼範例（虛擬碼）與課後作業，方便學員依日期查閱當週教材。\n")

doc.append("## 課程總覽\n")
doc.append("| 日期 | 主題 |")
doc.append("|------|------|")
for date, title_text, anchor_id in overview_rows:
    doc.append(f"| [{date}](#{anchor_id}) | {title_text} |")
doc.append("")

doc.append("## 目錄\n")
doc.append("\n".join(toc_lines))
doc.append("")

doc.append("---\n")
doc.append(("\n\n---\n\n").join(sections))

final_text = "\n".join(doc) + "\n"

with open(OUT, "w", encoding="utf-8") as f:
    f.write(final_text)

print("done, length:", len(final_text))
