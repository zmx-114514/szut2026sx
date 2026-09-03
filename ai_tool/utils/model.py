import os
import threading

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# 从 .env 加载 SiliconFlow 的 OPENAI_API_KEY / OPENAI_API_BASE
load_dotenv()

_model = None
_lock = threading.Lock()


def get_model():
    """懒加载聊天模型（双重检查锁：并发时只构建一次）。

    厨房助手需要识别食材图片，使用 VL 视觉模型（VL_MODEL_NAME 可在 .env 配置）。
    """
    global _model
    if _model is None:
        with _lock:
            if _model is None:
                vl_model = os.getenv("VL_MODEL_NAME", "Qwen/Qwen3-VL-8B-Thinking")
                _model = init_chat_model(model=f"openai:{vl_model}")
    return _model
