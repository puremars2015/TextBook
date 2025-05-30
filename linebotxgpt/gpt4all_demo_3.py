from gpt4all import GPT4All

# 載入指定的模型
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

# 啟動聊天會話
with model.chat_session() as session:
    # 添加系統提示詞
    session.generate("你是一個擅長使用中文的美食專家")
    # 使用者輸入
    response = session.generate("請介紹一下台灣的美食。")
    print(response)
