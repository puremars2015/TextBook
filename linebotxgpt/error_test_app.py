def execute_code(code):
    try:
        exec(code)
    except Exception as e:
        return f"An error occurred: {e}"

# 使用範例
code_with_error = """
def divide(a, b):
    return a / b

result = divide(10, 0)  # 這裡會引發 ZeroDivisionError
print(result)
"""

code_without_error = """
def add(a, b):
    return a + b

result = add(10, 5)
print(result)
"""

# 執行有錯誤的程式碼
error_result = execute_code(code_with_error)
print(error_result)  # 輸出: An error occurred: division by zero

# 執行沒有錯誤的程式碼
success_result = execute_code(code_without_error)
print(success_result)  # 不會有錯誤訊息
