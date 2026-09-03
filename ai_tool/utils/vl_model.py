"""视觉模型：Qwen3-VL-8B-Instruct via SiliconFlow"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

vl_model = ChatOpenAI(
    model=os.getenv("VL_MODEL_NAME", "Qwen/Qwen2-VL-7B-Instruct"),
    base_url=os.getenv("VL_BASE_URL"),
    api_key=os.getenv("VL_API_KEY"),
)
