from utils.agent import agent
from langchain_core.messages import HumanMessage

def send_msg_stream(question, session_id):
    config = {"configurable": {"thread_id": session_id}}
    stream = agent.stream(
        {"messages": [HumanMessage(content=question)]},
        config=config,
        stream_mode='messages',
    )
    return stream
