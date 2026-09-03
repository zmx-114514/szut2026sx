from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from utils.send_msg import send_msg_stream
from langchain_core.messages import AIMessageChunk
from uuid import uuid4
from utils.upload import upload_image


def run_app():
    """AI 厨房助手界面入口。"""
    st.title("AI厨房助手")
    st.write("智能厨房助手，你可以上传你的食材照片，我帮你推荐一些食谱。")

    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = "session_" + str(uuid4())

    if 'history' not in st.session_state:
        st.session_state.history = []

    #渲染聊天历史
    for msg in st.session_state.history:
        if msg["role"] == "user":
            with st.chat_message('user'):
                st.write(msg["content"]["text"])
                if msg["content"]["image"]:
                    st.image(msg["content"]["image"])
        elif msg["role"] == "assistant":
            with st.chat_message('assistant'):
                st.write(msg["content"])

    prompt = st.chat_input(
        "拍照或描述你的食材…",
        accept_file=True,
        file_type=["jpg", "jpeg", "png"],
        submit_mode="stop",
    )

    if prompt:
        input_text = prompt.text
        display_image = None
        image_name = ''
        image_url = ''

        if len(prompt.files) > 0:
            display_image = prompt.files[0].getvalue()
            image_name = prompt.files[0].name

        # 用户气泡
        with st.chat_message('user'):
            st.write(input_text)
            if display_image:
                st.image(display_image)

        st.session_state.history.append({
            "role": "user",
            "content": {"text": input_text or "(图片)", "image": display_image}
        })

        content = [{"type": "text", "text": input_text or "识别图片食材，搜索对应的食谱推荐"}]
        if image_name:
            image_url = upload_image(display_image, image_name)
            content.append({"type": "image_url", "image_url": {"url": image_url}})

        stream = send_msg_stream(content, st.session_state.thread_id)

        with st.chat_message('assistant'):
            container = st.empty()
            ai_reply = ""
            for token, meta in stream:
                if isinstance(token, AIMessageChunk) and token.content != "":
                    ai_reply += token.content
                    container.write(ai_reply)
            st.session_state.history.append({"role": "assistant", "content": ai_reply})


if __name__ == "__main__":
    run_app()
