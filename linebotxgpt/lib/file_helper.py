import datetime
import random
import string


def save_to_file(file_name, content):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)
        file.close()

def generate_random_filename_with_timestamp(extension="py"):
    # 獲取當前時間
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    # 生成隨機部分
    letters_and_digits = string.ascii_letters + string.digits
    random_part = ''.join(random.choice(letters_and_digits) for i in range(8))
    # 合成檔案名稱
    filename = f"source_{current_time}_{random_part}.{extension}"
    return filename