import os

print("=== Python 可見的環境變數清單 ===\n")
for key, value in os.environ.items():
    print(f"{key} = {value}")

print("\n=== 單獨測試指定變數 ===")
print("ANTHROPIC_API_KEY =", os.getenv("ANTHROPIC_API_KEY"))