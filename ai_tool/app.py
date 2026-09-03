"""统一入口 UI：整合 AI 厨房助手、智能万年历与 AI 伴侣。"""
import streamlit as st

from main import run_app as run_kitchen_app
from calendar_app import run_app as run_calendar_app
from companion_app import run_app as run_companion_app

st.set_page_config(page_title="AI 智能助手", page_icon="🤖", layout="centered")

st.title("🤖 AI 智能助手")
st.caption("苏州工学院 2026 级 25 届暑期实训团队作业")

app = st.sidebar.selectbox(
    "选择应用",
    ["🏠 主页", "🍳 AI 厨房助手", "📅 智能万年历", "💗 AI 伴侣"],
)

if app == "🏠 主页":
    st.markdown("## 📋 功能介绍")
    st.write("")
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
    st.divider()
    st.info("请在左侧选择要使用的应用。")
elif app == "🍳 AI 厨房助手":
    run_kitchen_app()
elif app == "📅 智能万年历":
    run_calendar_app()
elif app == "💗 AI 伴侣":
    run_companion_app()
