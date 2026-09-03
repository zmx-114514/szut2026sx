"""AI 智能助手 — 主入口（st.navigation 动态导航）。

所有应用页面异步加载：页面先渲染框架，重型模块后台导入，就绪后自动呈现。
厨房助手侧边栏提供其他应用的跳转入口（utils/pageref）。
"""
import streamlit as st

from utils.pageref import register
from utils.prewarm import (
    _import_calendar,
    _import_companion,
    _import_kitchen,
    _import_vision,
    ensure_ready,
    start_prewarm,
)

st.set_page_config(page_title="AI 智能助手", page_icon="🤖", layout="centered")
start_prewarm()


# ---------- 通用：异步加载包装 ----------
def _lazy_render(key: str, import_fn, render, loading_tip: str):
    """模块就绪则渲染，否则显示加载占位并轮询（fragment 每 0.4s 检查一次）。"""
    if ensure_ready(key, import_fn):
        render()
    else:
        @st.fragment(run_every=0.4)
        def _wait_ready():
            if ensure_ready(key, import_fn):
                st.rerun(scope="app")

        _wait_ready()
        st.info(loading_tip)


# ---------- 各页面 ----------
def _page_home():
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

        st.markdown("### 📅 智能万年历")
        st.write("农历、节气、节日、星座查询与 AI 日历助手。")
        st.write("- 农历/节气/节日")
        st.write("- 实时天气查询")
        st.write("- AI 日期问答")

    with col2:
        st.markdown("### 🔍 看图搜索 Agent")
        st.write("上传图片或输入 URL，AI 看图并联网搜索相关知识。")
        st.write("- 视觉模型识图")
        st.write("- 联网搜索资讯")
        st.write("- Agent 工具调用过程可视化")

        st.markdown("### 💗 AI 伴侣")
        st.write("多角色人设陪伴聊天，倾听你的心事。")
        st.write("- 五种人设随心切换")
        st.write("- 流式对话体验")
        st.write("- 温暖陪伴与情感支持")


def _page_kitchen():
    st.title("🍳 AI 厨房助手")

    def render():
        from main import run_app
        run_app()

    _lazy_render("main", _import_kitchen, render, "⏳ 正在加载厨房助手…首次启动需要几秒钟")


def _page_calendar():
    st.title("📅 智能万年历")

    def render():
        from calendar_app import run_app
        run_app()

    _lazy_render("calendar_app", _import_calendar, render, "⏳ 正在加载万年历…首次启动需要几秒钟")


def _page_vision():
    st.title("🔍 看图 + 联网搜索 Agent")

    def render():
        from vision_app import run_app
        run_app()

    _lazy_render("image_agent", _import_vision, render, "⏳ 正在加载看图搜索 Agent…首次启动需要几秒钟")


def _page_companion():
    st.title("💗 AI 伴侣")

    def render():
        from companion_app import run_app
        run_app()

    _lazy_render("companion_app", _import_companion, render, "⏳ 正在加载 AI 伴侣…首次启动需要几秒钟")


# ---------- 导航 ----------
page_kitchen = st.Page(_page_kitchen, title="AI 厨房助手", icon="🍳")
page_calendar = st.Page(_page_calendar, title="智能万年历", icon="📅")
page_vision = st.Page(_page_vision, title="看图搜索", icon="🔍")
page_companion = st.Page(_page_companion, title="AI 伴侣", icon="💗")

# 注册页面引用，供各应用内跳转（如厨房助手侧边栏入口）
register("kitchen", page_kitchen)
register("calendar", page_calendar)
register("vision", page_vision)
register("companion", page_companion)

nav = st.navigation(
    [
        st.Page(_page_home, title="主页", icon="🏠", default=True),
        page_kitchen,
        page_calendar,
        page_vision,
        page_companion,
    ]
)
nav.run()
