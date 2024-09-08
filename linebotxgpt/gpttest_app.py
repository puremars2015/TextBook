from code_gpt_engine_helper import auto_generate_code


def test_auto_generate_code(issue, title_name):
    auto_generate_code(issue, title_name)

if __name__ == "__main__":
    issue = '請幫我產生一個猜數字的遊戲的function,0~9之間,猜對即結束,答案是7,function輸入參數是猜的數字,回傳值是猜的結果'
    test_auto_generate_code(issue,'guess_number')


