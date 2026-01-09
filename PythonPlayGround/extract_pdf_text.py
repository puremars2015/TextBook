from pdfminer.high_level import extract_text

pdf_path = 'c:/Users/sean.ma/Downloads/來源導向_智慧創作.pdf'
text = extract_text(pdf_path)
print(text)
