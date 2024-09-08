from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

from gptcycle_app import auto_generate_code

import pandas as pd
import pyodbc

import csv

# def exec_code(code, additional_globals=None):
#     if additional_globals is None:
#         additional_globals = {}
#     exec_globals = globals().copy()
#     exec_globals.update(additional_globals)
#     exec(code, exec_globals)

def read_csv_as_array(file_path):
    """
    讀取 CSV 文件中的每一行並將值存儲在一個陣列中。
    
    :param file_path: CSV 文件的路徑
    :return: 包含 CSV 文件中每一行值的陣列
    """
    result = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row:  # 確保行不為空
                    result.append(row[0])  # 假設每行只有一個值
        return result
    except FileNotFoundError:
        print(f"檔案未找到: {file_path}")
        return None
    except Exception as e:
        print(f"讀取CSV檔案時發生錯誤: {e}")
        return None

def read_csv_file(file_path) -> pd.DataFrame:
    """
    讀取指定路徑的 CSV 檔案並返回為 DataFrame。
    
    :param file_path: CSV 檔案的路徑
    :return: DataFrame 格式的資料
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"檔案未找到: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print("CSV檔案為空")
        return None
    except pd.errors.ParserError:
        print("CSV檔案解析錯誤")
        return None
    except Exception as e:
        print(f"發生錯誤: {e}")
        return None

def write_to_sql_server_with_pyodbc(dataframe, server, database, table_name, inner_lot_number, org, supplier, username=None, password=None):
    """
    將 DataFrame 資料寫入 SQL Server 資料庫。

    :param dataframe: 要寫入的 DataFrame 資料
    :param server: SQL Server 的伺服器名稱或IP地址
    :param database: 資料庫名稱
    :param table_name: 要寫入的表名稱
    :param username: 使用者名稱（可選，如果不使用 Windows 認證）
    :param password: 密碼（可選，如果不使用 Windows 認證）
    :return: None
    """
    try:
        if username and password:
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
        else:
            # 使用 Windows 認證
            connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"

        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # 構建插入語句
        # columns = ', '.join(dataframe.columns)
        # placeholders = ', '.join(['?'] * len(dataframe.columns))
        # insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        value_sqls = []

        for r in dataframe:
            value_sqls.append(f"('{inner_lot_number}', '{r}', '{org}', '{supplier}')")

        insert_sql = f"INSERT INTO TB_LOTNO_MAPPER (inner_lot_no, outer_lot_no, organization, supplier) VALUES {', '.join(value_sqls)}"

        # 執行插入操作
        # for row in dataframe.itertuples(index=False, name=None):
        #     cursor.execute(insert_sql, row)

        cursor.execute(insert_sql)
        
        # 提交事務
        conn.commit()
        print(f"資料已成功寫入 {table_name} 表中")

    except Exception as e:
        print(f"寫入資料庫時發生錯誤: {e}")
    finally:
        cursor.close()
        conn.close()

def get_file_extension(file_name):
    # 使用 os.path.splitext 方法分離文件名和擴展名
    _, file_extension = os.path.splitext(file_name)
    return file_extension

def get_filename_without_extension(file_name):
    # 使用 os.path.splitext 方法分離文件名和擴展名
    file_name_without_extension = os.path.splitext(file_name)[0]
    return file_name_without_extension

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'json' not in request.form:
        return jsonify({"error": "Missing file or JSON data"}), 400
    
    file = request.files['file']
    json_data = request.form['json']

    # 將 JSON 字符串轉換為 Python 字典
    data = json.loads(json_data)

    # 取得json_data裡面的area_description_prompt的資料
    issue = data['area_description_prompt']

    supplier = data['supplier']
    inner_lot_number = data['inner_lotno']
    org = data['factory']
    
    # Save the uploaded file
    # file_path = os.path.join('uploads_temp', file.filename)
    # file_path = os.makedirs(os.path.dirname(file_path), exist_ok=True)
    temp_file_name = 'import_temp_excel' + get_file_extension(file.filename)
    file.save(temp_file_name)
    
    # Save the JSON data
    json_path = os.path.join('uploads_temp', 'data.json')
    with open(json_path, 'w') as json_file:
        json_file.write(json_data)
    
    # 檢查有沒有func_{supplier}.py這個檔案
    # if os.path.exists(f'auto_lib/func_{supplier}.py'):
    #     return jsonify({"error": f"func_{supplier}.py already exists"}), 400

    try:
        auto_generate_code(issue, supplier, temp_file_name, 'output_file_name.csv')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

    # 讀取輸出的 CSV 檔案
    try:
        ary = read_csv_as_array('output_file_name.csv')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    try:
        write_to_sql_server_with_pyodbc(ary, 'oci-eip01', 'MES', 'TB_LOTNO_MAPPER', inner_lot_number, org, supplier, 'itapadmin', 'itapadmin*2025')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "上傳成功"}), 200

if __name__ == '__main__':
    app.run()
