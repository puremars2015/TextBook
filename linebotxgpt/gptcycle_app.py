from lib.gpt_helper import MyGPT
from lib.file_helper import save_to_file, generate_random_filename_with_timestamp
from lib.package_helper import install_package
import traceback

def exec_code(code, additional_globals=None):
    if additional_globals is None:
        additional_globals = {}
    exec_globals = globals().copy()
    exec_globals.update(additional_globals)
    exec(code, exec_globals)


def auto_generate_code(issue, supplier_name, input_file_name, output_file_name):
        
    helper = MyGPT()

    prompt = helper.PromptHelperForAnalysisExcelCode(issue, input_file_name, output_file_name)

    code = helper.CodeGPT(prompt)

    file_name = generate_random_filename_with_timestamp()
    save_to_file(f'generate_record/{file_name}', code)


    condition = True
    counter = 0
    while condition:
        counter = counter + 1
        print(f"Counter: {counter}")
        try:
            exec(code)
            condition = False

            # Save the code to auto_lib
            save_to_file(f'auto_lib/func_{supplier_name}.py', code)

        except Exception as e:
            print(e)
            traceback.print_exc()  # 打印完整的錯誤訊息
            if counter > 9:
                raise Exception("Counter is over 9 times, please check the code.")
                

            errorMessage = str(e) + traceback.format_exc()

            if 'Missing optional dependency' in errorMessage:
                print("Missing optional dependency detected.")
                pip_command = helper.PipGPT(errorMessage)
                print(pip_command)
                install_package(pip_command)
            else:
                code = helper.FixCodeGPT(code, str(e))
                file_name = generate_random_filename_with_timestamp()
                save_to_file(f'generate_record/{file_name}', code)



if __name__ == "__main__":
    issue = '取出A7到J51的資料,並移除空白行'
    supplier_name = 'Lanzing'
    input_file_name = 'import_temp_excel.xls'
    output_file_name = 'output_file_name.csv'
    auto_generate_code(issue, supplier_name, input_file_name, output_file_name)