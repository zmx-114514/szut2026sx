import threading

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

_agent = None
_lock = threading.Lock()


def get_agent():
    """懒加载 LangGraph Agent（双重检查锁：并发时只构建一次）。"""
    global _agent
    if _agent is None:
        with _lock:
            if _agent is None:
                from utils.model import get_model
                from utils.tools import tools

                # 关键：给模型绑定工具！
                model_with_tools = get_model().bind_tools(tools)

                _agent = create_agent(
                    checkpointer=InMemorySaver(),
                    model=model_with_tools,
                    tools=tools,
                )
    return _agent
