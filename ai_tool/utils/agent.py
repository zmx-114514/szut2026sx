import functools

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


@functools.cache
def get_agent():
    """懒加载 LangGraph Agent，首次调用时才构建模型与工具绑定。"""
    from utils.model import get_model
    from utils.tools import tools

    # 关键：给模型绑定工具！
    model_with_tools = get_model().bind_tools(tools)

    return create_agent(
        checkpointer=InMemorySaver(),
        model=model_with_tools,
        tools=tools,
    )
