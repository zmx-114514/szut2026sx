from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(
    model="openai:Qwen/Qwen3-VL-8B-Thinking",
)
