from agents import WebSearchTool, Agent, ModelSettings, TResponseInputItem, Runner, RunConfig
from openai.types.shared.reasoning import Reasoning
from pydantic import BaseModel

# Tool definitions
web_search_preview = WebSearchTool(
  filters={
    "allowed_domains": [
      "judgment.judicial.gov.tw"
    ]
  },
  search_context_size="medium",
  user_location={
    "country": "TW",
    "type": "approximate"
  }
)
my_agent = Agent(
  name="My agent",
  instructions="""你是一個熟讀台灣歷年法院判例的法學研究人員,可以根據指定的關鍵字,在指定的網站找出有關的案件

指定網站網址:
https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx""",
  model="gpt-5",
  tools=[
    web_search_preview
  ],
  model_settings=ModelSettings(
    store=True,
    reasoning=Reasoning(
      effort="low",
      summary="auto"
    )
  )
)


class WorkflowInput(BaseModel):
  input_as_text: str


# Main code entrypoint
async def run_workflow(workflow_input: WorkflowInput):
  state = {

  }
  workflow = workflow_input.model_dump()
  conversation_history: list[TResponseInputItem] = [
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": workflow["input_as_text"]
        }
      ]
    }
  ]
  my_agent_result_temp = await Runner.run(
    my_agent,
    input=[
      *conversation_history
    ],
    run_config=RunConfig(trace_metadata={
      "__trace_source__": "agent-builder",
      "workflow_id": "wf_68e624a916688190b49d79bc913d38480a37fa89001df389"
    })
  )

  conversation_history.extend([item.to_input_item() for item in my_agent_result_temp.new_items])

  my_agent_result = {
    "output_text": my_agent_result_temp.final_output_as(str)
  }
  
  # 返回結果
  return my_agent_result


# ============== 以下為新增的執行代碼 ==============

import asyncio


async def interactive_mode():
  """互動模式：持續對話"""
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
      print("\n🔍 正在搜尋相關判例...")
      
      workflow_input = WorkflowInput(input_as_text=user_input)
      result = await run_workflow(workflow_input)
      
      # 顯示結果
      print("\n" + "="*60)
      print("⚖️  查詢結果")
      print("="*60)
      print(f"\n{result['output_text']}")
        
    except KeyboardInterrupt:
      print("\n\n👋 收到中斷信號，感謝使用！")
      break
    except Exception as e:
      print(f"\n❌ 發生錯誤: {str(e)}")


async def single_query_mode(query: str):
  """單次查詢模式"""
  print("\n⚖️  台灣法院判例查詢助手")
  print(f"📝 查詢: {query}\n")
  
  try:
    print("🔍 正在搜尋相關判例...")
    
    workflow_input = WorkflowInput(input_as_text=query)
    result = await run_workflow(workflow_input)
    
    # 顯示結果
    print("\n" + "="*60)
    print("⚖️  查詢結果")
    print("="*60)
    print(f"\n{result['output_text']}")
    
    return result
    
  except Exception as e:
    print(f"\n❌ 處理失敗: {str(e)}")
    return None


# Main execution
if __name__ == "__main__":
  import sys
  
  # 檢查命令行參數
  if len(sys.argv) > 1:
    # 單次查詢模式：python app8.py "你的問題"
    query = " ".join(sys.argv[1:])
    asyncio.run(single_query_mode(query))
  else:
    # 互動模式：持續對話
    asyncio.run(interactive_mode())


