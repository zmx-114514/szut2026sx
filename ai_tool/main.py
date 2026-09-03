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

    # ---------- 侧边栏：其他应用入口 ----------
    from utils.pageref import get

    with st.sidebar:
        st.header("🧰 更多应用")
        for key, label in (
            ("calendar", "📅 智能万年历"),
            ("vision", "🔍 看图搜索"),
            ("companion", "💗 AI 伴侣"),
        ):
            page = get(key)
            if page and st.button(label, use_container_width=True, key=f"nav_{key}"):
                st.switch_page(page)

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

        content = [{"type": "text", "text": input_text or "识别图片食材，搜索对应的食谱推荐"}]
        if image_name:
            image_url = upload_image(display_image, image_name)
            content.append({"type": "image_url", "image_url": {"url": image_url}})

        # 历史记录存图床 URL 而非图片 bytes，避免 session_state 累积大量字节导致浏览器内存暴涨
        st.session_state.history.append({
            "role": "user",
            "content": {"text": input_text or "(图片)", "image": image_url or display_image}
        })

        stream = send_msg_stream(content, st.session_state.thread_id)

        def token_iter():
            for token, meta in stream:
                if isinstance(token, AIMessageChunk) and token.content != "":
                    yield token.content

        # st.write_stream 内置流式优化：过程中轻量更新，结束时仅渲染一次完整 markdown
        with st.chat_message('assistant'):
            ai_reply = st.write_stream(token_iter())
        st.session_state.history.append({"role": "assistant", "content": ai_reply})


if __name__ == "__main__":
    run_app()
