"""看图 + 联网搜索 agent：能识别图片并联网查资料"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

import os
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from models import resolve_model
from utils.tools import recognize_image_tool, web_search

# 搜索推理用文本模型（独立于厨房助手的视觉模型），按 .env 的 OPENAI_MODEL 选择，关闭思考模式保证输出干净
_model_name = resolve_model(os.getenv("OPENAI_MODEL", "Qwen/Qwen3.5-4B"))
search_model = ChatOpenAI(
    model=_model_name,
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key=os.getenv("OPENAI_API_KEY"),
    extra_body={"enable_thinking": False},
)

agent = create_agent(
    search_model,
    [recognize_image_tool, web_search],
    system_prompt=(
        "你是一个智能助手，具备【看图】和【联网搜索】两项能力。"
        "收到用户问题后：如果用户给了图片，先调用 recognize_image_tool 分析图片内容；"
        "如果需要网络上的最新信息或额外知识，调用 web_search 搜索；"
        "最后综合工具返回的信息给出回答。"
    ),
)

if __name__ == "__main__":
    image = sys.argv[1] if len(sys.argv) > 1 else "https://picsum.photos/seed/cat/400/300"
    question = sys.argv[2] if len(sys.argv) > 2 else "这张图里是什么？联网搜索它的相关知识并介绍"

    print(f"图片: {image}")
    print(f"问题: {question}")
    print("agent 开始思考（会依次调用看图/搜索工具，每步会打印进度）...\n")

    inputs = {"messages": [{"role": "user", "content": f"图片：{image}\n问题：{question}"}]}
    for chunk in agent.stream(inputs, stream_mode="values"):
        msg = chunk["messages"][-1]
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"\n🔧 调用工具: {tc['name']}  参数: {tc.get('args')}")
        elif hasattr(msg, "content") and msg.content:
            print(f"\n💬 {msg.content}")
        else:
            print(f"\n📋 {type(msg).__name__}")

    print("\n=== 完成 ===")
