from dotenv import load_dotenv
load_dotenv()

# 1.测试模型
from utils.model import get_model
model = get_model()
print("===模型测试===")
res = model.invoke("你好")
print(res.content)

# 2.测试工具
from utils.tools import get_current_date, get_weather
print("\n===工具测试===")
print(get_current_date.invoke(''))
print(get_weather.invoke("北京"))

#3.测试agent
from utils.agent import get_agent
from langchain_core.messages import HumanMessage
agent = get_agent()
config = {"configurable": {"thread_id": "test_001"}}
resp = agent.invoke({
    "messages":[HumanMessage(content="告诉我今天日期，北京天气")]
}, config=config)
print("\n===Agent测试===")
print(resp["messages"][-1].content)
