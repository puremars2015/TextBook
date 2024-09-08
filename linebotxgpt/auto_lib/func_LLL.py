import pandas as pd

# 讀取Excel檔案
data = pd.read_excel('import_temp_excel.xls', header=None)

# 擷取指定範圍的資料
extracted_data = data.iloc[8:30, [3, 5, 6]]

# 儲存為CSV檔案
extracted_data.to_csv('output_file_name.csv', index=False, header=False)