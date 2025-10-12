from agents import WebSearchTool, Agent, ModelSettings, Runner, RunConfig
from openai.types.shared.reasoning import Reasoning
from pydantic import BaseModel
import asyncio

# Tool definitions
web_search_preview = WebSearchTool(
  search_context_size="medium",
  user_location={
    "type": "approximate",
    "country": "TW"
  }
)
my_agent = Agent(
  name="Legal Research Assistant",
  instructions="""你是一個熟讀台灣歷年法院判例的法學研究人員。

當使用者查詢判例時：
1. 使用網路搜尋工具在 https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx 網站查找相關案件
2. 提供案件的判決字號、案由、裁判日期
3. 說明判決要旨和重點法律見解
4. 引用相關法條

請用繁體中文回覆，內容要詳細且專業。""",
  model="gpt-5",
  tools=[
    web_search_preview
  ],
  model_settings=ModelSettings(
    store=True,
    reasoning=Reasoning(
      effort="medium",
      summary="auto"
    )
  )
)


class LegalAssistant:
  """法律判例查詢助手主類"""
  
  def __init__(self):
    self.conversation_history = []
    
  async def handle_query(self, user_input: str) -> dict:
    """處理用戶查詢"""
    try:
      print("\n🔍 正在搜尋相關判例...")
      
      # 直接調用 agent 搜尋判例
      response = await Runner.run(
        my_agent,
        input=user_input,
        run_config=RunConfig(
          trace_metadata={
            "__trace_source__": "legal-assistant",
            "step": "case_search"
          }
        )
      )
      
      # 直接將輸出轉換為字串
      try:
        result = response.final_output_as(str)
      except:
        # 如果 final_output_as 失敗，嘗試直接取得 final_output
        result = str(response.final_output) if response.final_output else "未找到結果"
      
      return {
        "success": True,
        "data": result,
        "response": response
      }
        
    except Exception as e:
      print(f"❌ 錯誤: {str(e)}")
      import traceback
      traceback.print_exc()
      return {
        "success": False,
        "error": str(e)
      }
  
  def format_result(self, data: str) -> str:
    """格式化查詢結果"""
    output = []
    output.append("\n" + "="*60)
    output.append("⚖️  法院判例查詢結果")
    output.append("="*60)
    output.append(f"\n{data}")
    
    return "\n".join(output)


async def interactive_mode():
  """互動模式：持續對話"""
  assistant = LegalAssistant()
  
  print("="*60)
  print("⚖️  台灣法院判例查詢助手")
  print("="*60)
  print("\n我可以幫您:")
  print("  📖 查詢台灣法院判例")
  print("  🔍 搜尋特定關鍵字的案件")
  print("  📋 提供判決要旨和相關法條")
  print("\n輸入 'quit' 或 'exit' 結束對話\n")
  
  while True:
    try:
      user_input = input("\n💬 您: ").strip()
      
      if not user_input:
        continue
        
      if user_input.lower() in ['quit', 'exit', '退出', '結束']:
        print("\n👋 感謝使用！")
        break
      
      # 處理查詢
      result = await assistant.handle_query(user_input)
      
      if result['success']:
        print(assistant.format_result(result['data']))
      else:
        print(f"\n❌ 處理失敗: {result.get('error', '未知錯誤')}")
        
    except KeyboardInterrupt:
      print("\n\n👋 收到中斷信號，感謝使用！")
      break
    except Exception as e:
      print(f"\n❌ 發生錯誤: {str(e)}")


async def single_query_mode(query: str):
  """單次查詢模式"""
  assistant = LegalAssistant()
  
  print("\n⚖️  台灣法院判例查詢助手")
  print(f"📝 查詢: {query}\n")
  
  result = await assistant.handle_query(query)
  
  if result['success']:
    print(assistant.format_result(result['data']))
  else:
    print(f"\n❌ 處理失敗: {result.get('error', '未知錯誤')}")
  
  return result


# Main execution
if __name__ == "__main__":
  import sys
  
  # 檢查命令行參數
  if len(sys.argv) > 1:
    # 單次查詢模式：python app6.py "你的問題"
    query = " ".join(sys.argv[1:])
    asyncio.run(single_query_mode(query))
  else:
    # 互動模式：持續對話
    asyncio.run(interactive_mode())

