from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from utils.model import model
from utils.tools import tools

# 关键：给模型绑定工具！
model_with_tools = model.bind_tools(tools)

agent = create_agent(
    checkpointer=InMemorySaver(),
    model=model_with_tools,   # 这里改成绑定后的 model_with_tools，不要写 model
    tools=tools,
)
