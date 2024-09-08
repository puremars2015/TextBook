import pandas as pd

# 讀取 Excel 檔案
file_path = 'import_temp_excel.xls'
data = pd.read_excel(file_path, usecols='E', skiprows=6, nrows=24)

# 儲存為 CSV 檔案
output_file_name = 'output_file_name.csv'
data.to_csv(output_file_name, index=False)