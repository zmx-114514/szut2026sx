"""AI 伴侣：多角色人设、流式对话、情感陪伴聊天应用。"""
import os

import openai
import streamlit as st
from dotenv import load_dotenv

from models import resolve_model

load_dotenv()

# ---------- 人设定义 ----------
PERSONAS = {
    "💕 贴心伴侣": {
        "avatar": "💕",
        "greeting": "今天过得怎么样呀？我在呢，慢慢说给我听～",
        "system": (
            "你是一位温柔体贴的 AI 伴侣，说话温暖亲切，善于倾听与共情。"
            "你会关心对方的日常起居与情绪变化，适时给予鼓励和安慰，"
            "回复简短自然，像日常聊天一样，不说教、不啰嗦。"
        ),
    },
    "😄 幽默段子手": {
        "avatar": "😄",
        "greeting": "哈哈哈来啦？今天想听点啥乐子，我段子库存管够！",
        "system": (
            "你是一位幽默风趣的 AI 伴侣，擅长讲段子、玩梗和自嘲，"
            "总能用轻松搞笑的方式化解烦恼。回复轻松活泼，偶尔夸张搞笑，"
            "但分寸得当，不冒犯人。"
        ),
    },
    "🌙 深夜树洞": {
        "avatar": "🌙",
        "greeting": "夜深了，想说的话都可以倒给我，我安静听着。",
        "system": (
            "你是一位深夜倾听者 AI 伴侣，安静温和，先倾听再回应，"
            "不急于给建议，善于接住对方的情绪，回复简短有温度，"
            "像深夜里陪着的朋友。若对方流露出强烈的负面情绪，"
            "温柔提醒寻求专业帮助或身边人的支持。"
        ),
    },
    "🧑‍🏫 学习搭子": {
        "avatar": "🧑‍🏫",
        "greeting": "今天也要一起加油鸭！学到哪儿了，卡在哪啦？",
        "system": (
            "你是一位元气满满的学习搭子 AI 伴侣，陪伴对方学习、打卡、制定计划，"
            "鼓励为主，讲解耐心，会用提问引导对方思考，语气积极有感染力。"
        ),
    },
    "💼 职场导师": {
        "avatar": "💼",
        "greeting": "嗨，工作上有啥烦心事或者拿不准的事？咱们一起捋捋。",
        "system": (
            "你是一位经验丰富的职场导师 AI 伴侣，理性可靠，善于分析问题、"
            "拆解任务、给出可执行建议，同时关心对方的工作压力与成长，"
            "语气专业但亲切。"
        ),
    },
}

MODEL_NAME = resolve_model(os.getenv("OPENAI_MODEL", "Qwen/Qwen3.5-4B"))


def _get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE") or os.getenv("OPENAI_BASE_URL")
    if not api_key:
        return None
    return openai.OpenAI(api_key=api_key, base_url=base_url)


def stream_reply(messages, temperature):
    """流式获取 AI 回复，逐段产出文本。"""
    client = _get_client()
    if client is None:
        yield "（未配置 OPENAI_API_KEY，无法连接 AI 服务，请在 .env 中配置后重试）"
        return
    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=temperature,
            max_tokens=800,
            stream=True,
            extra_body={"enable_thinking": False},
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                yield delta
    except Exception as e:
        yield f"❌ AI 调用失败：{e}"


def run_app():
    """AI 伴侣界面入口。"""
    st.title("💗 AI 伴侣")
    st.caption("选择一位伙伴，随时随地陪你聊天")

    # ---------- 侧边栏设置 ----------
    with st.sidebar:
        st.header("⚙️ 伴侣设置")
        persona = st.radio("选择人设", list(PERSONAS.keys()), label_visibility="collapsed")
        temperature = st.slider("回复风格（创造性）", 0.0, 1.5, 0.8, 0.1)
        if st.button("🗑️ 清空对话记录", use_container_width=True):
            st.session_state.companion_messages = []
            st.session_state.companion_greeted = False
            st.rerun()
        st.divider()
        st.caption("💡 对话记录仅保存在当前会话中，刷新页面即清空。")

    cfg = PERSONAS[persona]
    system_prompt = {"role": "system", "content": cfg["system"]}

    # ---------- 初始化会话状态 ----------
    if "companion_messages" not in st.session_state:
        st.session_state.companion_messages = []
    if st.session_state.get("companion_persona") != persona:
        # 切换人设时重置对话
        st.session_state.companion_messages = []
        st.session_state.companion_persona = persona
        st.session_state.companion_greeted = False

    # ---------- 欢迎语 ----------
    if not st.session_state.companion_greeted:
        with st.chat_message("assistant", avatar=cfg["avatar"]):
            st.write(cfg["greeting"])
        st.session_state.companion_greeted = True

    # ---------- 渲染历史 ----------
    for msg in st.session_state.companion_messages:
        avatar = cfg["avatar"] if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    # ---------- 输入与流式回复 ----------
    if user_input := st.chat_input("说点什么吧…"):
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.companion_messages.append({"role": "user", "content": user_input})

        messages = [system_prompt] + st.session_state.companion_messages
        # st.write_stream 内置流式优化：过程中轻量更新，结束时仅渲染一次完整 markdown
        with st.chat_message("assistant", avatar=cfg["avatar"]):
            reply = st.write_stream(stream_reply(messages, temperature))
        st.session_state.companion_messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    run_app()
