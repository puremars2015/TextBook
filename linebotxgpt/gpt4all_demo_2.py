from gpt4all import GPT4All
model = GPT4All("Llama-3.2-1B-Instruct.Q4_0.gguf") # downloads / loads a 4.66GB LLM
with model.chat_session():
    print(model.generate("你可以改用中文回答嗎", max_tokens=1024))


# Meta-Llama-3-8B-Instruct.Q4_0.gguf
# meta-llama/Llama-3.2-1B-Instruct.Q4_0.gguf