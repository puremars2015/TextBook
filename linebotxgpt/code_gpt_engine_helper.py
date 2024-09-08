from lib.gpt_helper import MyGPT
from lib.file_helper import save_to_file, generate_random_filename_with_timestamp
import traceback

def exec_code(code, additional_globals=None):
    if additional_globals is None:
        additional_globals = {}
    exec_globals = globals().copy()
    exec_globals.update(additional_globals)
    exec(code, exec_globals)

def auto_generate_code(prompt,title_name):
        
    helper = MyGPT()

    code = helper.PromptCodeNoExecuteHelper(prompt)

    file_name = generate_random_filename_with_timestamp()
    save_to_file(f'generate_record/{file_name}', code)

    condition = True
    counter = 0
    while condition:
        counter = counter + 1
        print(f"Counter: {counter}")
        try:
            exec_code(code)
            condition = False
            # Save the code to auto_lib
            save_to_file(f'auto_lib/func_{title_name}.py', code)
            return f'產生成功，請查看auto_lib/func_{title_name}.py'
        except Exception as e:
            print(e)
            traceback.print_exc()  # 打印完整的錯誤訊息
            if counter > 9:
                # raise Exception("Counter is over 9 times, please check the code.")
                return "產生失敗，請聯絡管理員"
                

            errorMessage = str(e) + traceback.format_exc()
            print(errorMessage)

            code = helper.FixCodeGPT(code, str(e))
                

