import pandas as pd

# 讀取Excel檔案
file_path = 'import_temp_excel.xls'
data = pd.read_excel(file_path, header=None)

# 取出A7到J51 (根據DataFrame的定位，實際上是第6行到第50行)
selected_data = data.iloc[6:51, 0:10]

# 移除空白行
cleaned_data = selected_data.dropna(how='all')

# 儲存為CSV檔案
output_file_name = 'output_file_name.csv'
cleaned_data.to_csv(output_file_name, index=False)