from lib.gpt_helper import MyGPT

gpt = MyGPT()

while True:
    msg = input("Ask GPT: ")
    if msg == "exit":
        break
    response = gpt.MemoryGPT(msg)
    print(response)