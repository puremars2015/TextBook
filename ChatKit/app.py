from agents import WebSearchTool, Agent, ModelSettings, Runner, RunConfig
from pydantic import BaseModel, Field
from openai.types.shared.reasoning import Reasoning
import asyncio
from typing import Optional

# Tool definitions
web_search_preview = WebSearchTool(
  search_context_size="medium",
  user_location={
    "type": "approximate"
  }
)
class ClassifierSchema(BaseModel):
  classification: str  # "flight_info" or "itinerary"


class FlightAgentSchema__Ticket(BaseModel):
  pnr: str
  flight_class: str = Field(alias="class")
  seat: str


class FlightAgentSchema(BaseModel):
  fromCode: str
  toCode: str
  from_location: str = Field(alias="from")
  to: str
  timeRange: str
  duration: str
  ticket: FlightAgentSchema__Ticket


classifier = Agent(
  name="Travel Classifier",
  instructions="""You are a helpful travel assistant classifier. 
  Classify the user's message into one of these categories:
  - "flight_info": Questions about flights, airlines, booking, flight times, airports
  - "itinerary": Questions about trip planning, things to do, places to visit, travel itineraries
  
  Provide a brief reason for your classification.""",
  model="gpt-5-nano",
  output_type=ClassifierSchema,
  model_settings=ModelSettings(
    store=True,
    reasoning=Reasoning(
      effort="low",
      summary="auto"
    )
  )
)


flight_agent = Agent(
  name="Flight Agent",
  instructions="""You are a professional travel assistant specializing in flight information.
  
  When users ask about flights:
  1. Search for relevant flight information using the web search tool
  2. Recommend specific flights with details (airline, flight number, times, duration)
  3. Use proper airport codes (IATA codes)
  4. Format times in 24-hour format without timezones
  5. Provide ticket class recommendations (Economy, Business, First)
  6. Include estimated prices when available
  
  Always be helpful and provide actionable information.""",
  model="gpt-5-nano",
  tools=[web_search_preview],
  output_type=FlightAgentSchema,
  model_settings=ModelSettings(
    store=True,
    reasoning=Reasoning(
      effort="medium",
      summary="auto"
    )
  )
)


itinerary_agent = Agent(
  name="Itinerary Agent",
  instructions="""You are an expert travel planner specializing in creating detailed itineraries.
  
  When planning trips:
  1. Consider the duration of the trip
  2. Include must-see attractions and hidden gems
  3. Suggest restaurants and local cuisine
  4. Provide practical tips (transportation, best times to visit)
  5. Balance sightseeing with relaxation time
  6. Consider the traveler's interests and preferences
  
  回覆時請用繁體中文，內容要具體實用，包含時間安排建議。""",
  model="gpt-5-nano",
  model_settings=ModelSettings(
    store=True,
    reasoning=Reasoning(
      effort="medium",
      summary="auto"
    )
  )
)


class TravelAssistant:
  """旅遊助手主類，管理對話流程"""
  
  def __init__(self):
    self.conversation_history = []
    
  async def handle_query(self, user_input: str) -> dict:
    """處理用戶查詢"""
    try:
      # 1. 先用 classifier 分類
      print("\n🔍 正在分析您的問題...")
      classifier_response = await Runner.run(
        classifier,
        input=user_input,
        run_config=RunConfig(
          trace_metadata={
            "__trace_source__": "travel-assistant",
            "step": "classification"
          }
        )
      )
      
      classification = classifier_response.final_output.model_dump()
      print(f"📋 分類結果: {classification['classification']}")
      if classification.get('reason'):
        print(f"   理由: {classification['reason']}")
      
      # 2. 根據分類結果調用相應的 agent
      if classification['classification'] == "flight_info":
        return await self._handle_flight_query(user_input, classifier_response)
      else:
        return await self._handle_itinerary_query(user_input, classifier_response)
        
    except Exception as e:
      print(f"❌ 錯誤: {str(e)}")
      return {
        "success": False,
        "error": str(e)
      }
  
  async def _handle_flight_query(self, user_input: str, classifier_response) -> dict:
    """處理航班查詢"""
    print("\n✈️  正在搜尋航班資訊...")
    
    # 重新發送用戶的原始輸入給 flight_agent
    flight_response = await Runner.run(
      flight_agent,
      input=user_input,
      run_config=RunConfig(
        trace_metadata={
          "__trace_source__": "travel-assistant",
          "step": "flight_search"
        }
      )
    )
    
    result = flight_response.final_output.model_dump()
    
    return {
      "success": True,
      "type": "flight",
      "classification": "flight_info",
      "data": result,
      "response": flight_response
    }
  
  async def _handle_itinerary_query(self, user_input: str, classifier_response) -> dict:
    """處理行程規劃"""
    print("\n🗺️  正在規劃行程...")
    
    # 重新發送用戶的原始輸入給 itinerary_agent
    itinerary_response = await Runner.run(
      itinerary_agent,
      input=user_input,
      run_config=RunConfig(
        trace_metadata={
          "__trace_source__": "travel-assistant",
          "step": "itinerary_planning"
        }
      )
    )
    
    result = itinerary_response.final_output_as(str)
    
    return {
      "success": True,
      "type": "itinerary",
      "classification": "itinerary",
      "data": result,
      "response": itinerary_response
    }
  
  def format_flight_result(self, data: dict) -> str:
    """格式化航班結果"""
    output = []
    output.append("\n" + "="*60)
    output.append("✈️  航班資訊")
    output.append("="*60)
    
    output.append(f"\n📍 航線: {data.get('from_location', 'N/A')} ({data.get('fromCode', 'N/A')}) → "
                 f"{data.get('to', 'N/A')} ({data.get('toCode', 'N/A')})")
    output.append(f"⏰ 時間: {data.get('timeRange', 'N/A')}")
    output.append(f"⏱️  飛行時間: {data.get('duration', 'N/A')}")
    
    ticket = data.get('ticket', {})
    if ticket:
      output.append(f"\n🎫 票務資訊:")
      output.append(f"   訂位代號: {ticket.get('pnr', 'N/A')}")
      output.append(f"   艙等: {ticket.get('flight_class', 'N/A')}")
      output.append(f"   座位: {ticket.get('seat', 'N/A')}")
    
    return "\n".join(output)
  
  def format_itinerary_result(self, data: str) -> str:
    """格式化行程結果"""
    output = []
    output.append("\n" + "="*60)
    output.append("🗺️  行程規劃")
    output.append("="*60)
    output.append(f"\n{data}")
    
    return "\n".join(output)


async def interactive_mode():
  """互動模式：持續對話"""
  assistant = TravelAssistant()
  
  print("="*60)
  print("🌏 歡迎使用智能旅遊助手")
  print("="*60)
  print("\n我可以幫您:")
  print("  ✈️  查詢航班資訊")
  print("  🗺️  規劃旅遊行程")
  print("\n輸入 'quit' 或 'exit' 結束對話\n")
  
  while True:
    try:
      user_input = input("\n💬 您: ").strip()
      
      if not user_input:
        continue
        
      if user_input.lower() in ['quit', 'exit', '退出', '結束']:
        print("\n👋 感謝使用，祝您旅途愉快！")
        break
      
      # 處理查詢
      result = await assistant.handle_query(user_input)
      
      if result['success']:
        if result['type'] == 'flight':
          print(assistant.format_flight_result(result['data']))
        else:
          print(assistant.format_itinerary_result(result['data']))
      else:
        print(f"\n❌ 處理失敗: {result.get('error', '未知錯誤')}")
        
    except KeyboardInterrupt:
      print("\n\n👋 收到中斷信號，感謝使用！")
      break
    except Exception as e:
      print(f"\n❌ 發生錯誤: {str(e)}")


async def single_query_mode(query: str):
  """單次查詢模式"""
  assistant = TravelAssistant()
  
  print("\n🌏 智能旅遊助手")
  print(f"📝 查詢: {query}\n")
  
  result = await assistant.handle_query(query)
  
  if result['success']:
    if result['type'] == 'flight':
      print(assistant.format_flight_result(result['data']))
    else:
      print(assistant.format_itinerary_result(result['data']))
  else:
    print(f"\n❌ 處理失敗: {result.get('error', '未知錯誤')}")
  
  return result


# Main execution
if __name__ == "__main__":
  import sys
  
  # 檢查命令行參數
  if len(sys.argv) > 1:
    # 單次查詢模式：python app.py "你的問題"
    query = " ".join(sys.argv[1:])
    asyncio.run(single_query_mode(query))
  else:
    # 互動模式：持續對話
    asyncio.run(interactive_mode())
