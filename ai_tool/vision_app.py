"""看图 + 联网搜索 Agent 网页版（Streamlit）"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

import os
import tempfile

import streamlit as st
from langchain_core.messages import AIMessage, ToolMessage

from image_agent import agent


def run_app():
    """看图 + 联网搜索 Agent 界面入口。"""
    st.title("🔍 看图 + 联网搜索 Agent")
    st.caption("上传图片或输入图片 URL，agent 会看图并联网搜索相关知识")

    # === 1. 图片输入 ===
    st.subheader("1. 提供图片")
    col1, col2 = st.columns(2)
    with col1:
        upload = st.file_uploader("上传本地图片", type=["png", "jpg", "jpeg", "webp"])
    with col2:
        url = st.text_input("或输入图片 URL", placeholder="https://example.com/photo.jpg")

    # === 2. 问题 ===
    st.subheader("2. 你的问题")
    question = st.text_input(
        "想问 agent 什么？",
        value="这张图里是什么？联网搜索它的相关知识并介绍",
    )

    # === 3. 运行 ===
    if st.button("开始分析", type="primary"):
        # 确定图片来源
        image_ref = None
        if upload is not None:
            suffix = os.path.splitext(upload.name)[1] or ".png"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(upload.getvalue())
            tmp.close()
            image_ref = tmp.name
            st.image(upload, caption="已上传图片", use_container_width=True)
        elif url:
            image_ref = url
            try:
                st.image(url, caption="图片 URL", use_container_width=True)
            except Exception:
                st.warning("无法预览该 URL 图片，但 agent 仍会尝试识别")
        else:
            st.warning("请上传图片或输入图片 URL")
            st.stop()

        user_msg = f"图片：{image_ref}\n问题：{question}"

        final_answer = ""
        with st.status("agent 正在思考...", expanded=True) as status:
            for chunk in agent.stream(
                {"messages": [{"role": "user", "content": user_msg}]},
                stream_mode="values",
            ):
                msg = chunk["messages"][-1]
                if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
                    for tc in msg.tool_calls:
                        st.write(f"🔧 调用工具: {tc['name']}  参数: {tc.get('args')}")
                elif isinstance(msg, ToolMessage):
                    content = msg.content if isinstance(msg.content, str) else str(msg.content)
                    st.write(f"📋 工具结果: {content[:300]}")
                elif isinstance(msg, AIMessage) and msg.content:
                    final_answer = msg.content
                    st.write(f"💬 {final_answer}")
            status.update(label="完成", state="complete")

        # 清理临时文件
        if upload is not None and image_ref and os.path.exists(image_ref):
            try:
                os.unlink(image_ref)
            except OSError:
                pass

        st.subheader("最终回答")
        st.write(final_answer or "（agent 未返回内容）")


if __name__ == "__main__":
    run_app()
