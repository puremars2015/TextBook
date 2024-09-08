import pandas as pd

# 讀取Excel檔案
data = pd.read_excel('import_temp_excel.xls', usecols='E', skiprows=6, nrows=24)

# 將資料儲存為CSV檔案
data.to_csv('output_file_name.csv', index=False, header=False)