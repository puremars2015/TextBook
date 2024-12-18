import pyodbc

def query_mssql_table():
    # 連線字串
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=10.200.16.11;"
        "DATABASE=MES;"
        "UID=itapadmin;"
        "PWD=itapadmin*2025;"
        "Max Pool Size=30;"
    )

    try:
        # 建立資料庫連線
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        # 查詢語句
        query = "SELECT data FROM TB_SP_SPLIT WITH (nolock) WHERE wip_entity_name = 'A00028-01' AND organization_code = 'WPN'"

        # 執行查詢
        cursor.execute(query)
        rows = cursor.fetchall()

        # 將查詢結果儲存到txt檔案
        with open('query_results.txt', 'w', encoding='utf-8') as file:
            for row in rows:
                file.write(f"{row}\n")

        print("查詢結果已儲存到 query_results.txt")

    except pyodbc.Error as e:
        print(f"資料庫連線或查詢時發生錯誤: {e}")

    finally:
        # 確保資源被釋放
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def update_mssql_table(update_data):
    # 連線字串
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=10.200.16.11;"
        "DATABASE=MES;"
        "UID=itapadmin;"
        "PWD=itapadmin*2025;"
        "Max Pool Size=30;"
    )

    try:
        # 建立資料庫連線
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        # 更新語句
        update_query = """
        UPDATE TB_SP_SPLIT
        SET data = ?
        WHERE wip_entity_name = 'A00028-01' AND organization_code = 'WPN'
        """

        # 執行更新語句
        cursor.execute(update_query, update_data)

        # 提交更新
        connection.commit()
        print("資料更新成功！")

    except pyodbc.Error as e:
        print(f"資料庫連線或更新時發生錯誤: {e}")

    finally:
        # 確保資源被釋放
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    query_mssql_table()
    # 更新範例
    # update_data = {
    #     'ColumnName': 'NewValue',
    #     'Id': 1
    # }
    # update_mssql_table(update_data)
