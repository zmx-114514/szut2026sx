"""AI 智能助手 — 主页（Streamlit Multipage App 入口）"""
import streamlit as st

st.set_page_config(page_title="AI 智能助手", page_icon="🤖", layout="centered")

st.title("🤖 AI 智能助手")
st.caption("苏州工学院 2026 级 25 届暑期实训团队作业")

st.markdown("## 📋 功能介绍")
st.write("请在左侧侧边栏选择要使用的应用。")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🍳 AI 厨房助手")
    st.write("上传食材照片，AI 识别食材并推荐食谱。")
    st.write("- 图片识别")
    st.write("- 流式对话")
    st.write("- LangGraph Agent")

    st.markdown("### 💗 AI 伴侣")
    st.write("多角色人设陪伴聊天，倾听你的心事。")
    st.write("- 五种人设随心切换")
    st.write("- 流式对话体验")
    st.write("- 温暖陪伴与情感支持")

with col2:
    st.markdown("### 📅 智能万年历")
    st.write("农历、节气、节日、星座查询与 AI 日历助手。")
    st.write("- 农历/节气/节日")
    st.write("- 实时天气查询")
    st.write("- AI 日期问答")

    st.markdown("### 🔍 看图搜索 Agent")
    st.write("上传图片或输入 URL，AI 看图并联网搜索相关知识。")
    st.write("- 视觉模型识图")
    st.write("- 联网搜索资讯")
    st.write("- Agent 工具调用过程可视化")

st.divider()
st.info("💡 使用左侧侧边栏的页面导航切换应用。")
