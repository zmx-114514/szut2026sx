"""图片识别：传入图片 URL 或本地路径，视觉模型描述内容"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

from langchain_core.messages import HumanMessage
from utils.vl_model import vl_model


def recognize_image(image_input: str, question: str = "请详细描述这张图片的内容") -> str:
    """
    识别图片内容。
    image_input: 图片 URL（http/https）或本地文件路径
    question: 想问视觉模型的问题
    """
    if image_input.startswith(("http://", "https://")):
        url = image_input
    else:
        # 本地图片转 base64 data URL
        import os
        import base64
        import mimetypes
        if not os.path.exists(image_input):
            return f"错误：本地图片文件不存在：{image_input}。请提供有效的图片路径或 URL。"
        mime = mimetypes.guess_type(image_input)[0] or "image/png"
        with open(image_input, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        url = f"data:{mime};base64,{b64}"

    message = HumanMessage(content=[
        {"type": "text", "text": question},
        {"type": "image_url", "image_url": {"url": url}},
    ])
    return vl_model.invoke([message]).content


if __name__ == "__main__":
    image = sys.argv[1] if len(sys.argv) > 1 else "https://picsum.photos/seed/cat/400/300"
    print(recognize_image(image, "请详细描述这张图片里的内容"))
