import functools
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# 从 .env 加载 SiliconFlow 的 OPENAI_API_KEY / OPENAI_API_BASE
load_dotenv()


@functools.cache
def get_model():
    """懒加载聊天模型，避免模块导入时即发起网络/重型初始化。"""
    return init_chat_model(
        model="openai:Qwen/Qwen3-VL-8B-Thinking",
    )
