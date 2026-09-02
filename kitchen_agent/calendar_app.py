import streamlit as st
import calendar
from datetime import datetime, date
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
import openai
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# ---------- 节日数据 ----------
solar_festivals = {
    (1, 1): "元旦", (2, 14): "情人节", (3, 8): "妇女节", (3, 12): "植树节",
    (4, 1): "愚人节", (5, 1): "劳动节", (6, 1): "儿童节", (7, 1): "建党节",
    (8, 1): "建军节", (9, 10): "教师节", (10, 1): "国庆节", (12, 25): "圣诞节",
}
lunar_festivals = {
    (1, 1): "春节", (1, 15): "元宵节", (5, 5): "端午节",
    (7, 7): "七夕节", (7, 15): "中元节", (8, 15): "中秋节",
    (9, 9): "重阳节", (12, 30): "除夕",
}


def get_zodiac_sign(month, day):
    """根据公历日期返回星座"""
    cutoffs = [(1, 20), (2, 19), (3, 21), (4, 20), (5, 21), (6, 22),
               (7, 23), (8, 23), (9, 23), (10, 24), (11, 23), (12, 22)]
    signs = ["摩羯座", "水瓶座", "双鱼座", "白羊座", "金牛座", "双子座",
             "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座"]
    for i, (m, d) in enumerate(cutoffs):
        if (month, day) < (m, d):
            return signs[i]
    return signs[-1]


def get_weather(city="北京"):
    """获取指定城市的当前天气"""
    try:
        response = requests.get(
            f"https://wttr.in/{city}",
            params={"format": "j1"},
            headers={"Accept-Language": "zh-CN,zh;q=0.9"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        current = data.get("current_condition", [{}])[0]
        weather_desc = current.get("lang_zh", [{}])
        if not weather_desc:
            weather_desc = current.get("weatherDesc", [{}])
        desc = weather_desc[0].get("value", "未知") if weather_desc else "未知"
        temp_c = current.get("temp_C", "未知")
        feels_like = current.get("FeelsLikeC", "未知")
        humidity = current.get("humidity", "未知")
        wind_speed = current.get("windspeedKmph", "未知")
        wind_dir = current.get("winddir16Point", "未知")
        area = data.get("nearest_area", [{}])[0]
        area_name_list = area.get("areaName", [{}])
        region = area_name_list[0].get("value", city) if area_name_list else city
        return f"{region}：{desc}，气温 {temp_c}°C（体感 {feels_like}°C），湿度 {humidity}%，风速 {wind_speed} km/h（{wind_dir}方向）"
    except Exception as e:
        return f"获取天气失败：{e}"


def get_lunar_info(year, month, day):
    """返回 (农历月, 农历日, 是否闰月, 月名, 日名, 节日列表, 节气名称)"""
    try:
        solar = Solar(year, month, day)
        lunar = Converter.Solar2Lunar(solar)
        lunar_month = lunar.month
        lunar_day = lunar.day
        is_leap = lunar.isleap

        month_names = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "冬", "腊"]
        month_name = ("闰" if is_leap else "") + month_names[lunar_month - 1] + "月"
        day_names = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                     "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                     "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
        day_name = day_names[lunar_day - 1] if lunar_day <= 30 else str(lunar_day)

        festivals = []
        if (month, day) in solar_festivals:
            festivals.append(solar_festivals[(month, day)])
        if (lunar_month, lunar_day) in lunar_festivals:
            festivals.append(lunar_festivals[(lunar_month, lunar_day)])
        if lunar_month == 12 and lunar_day >= 29:
            try:
                next_day = Solar(year, month, day + 1)
                next_lunar = Converter.Solar2Lunar(next_day)
                if next_lunar.month == 1 and next_lunar.day == 1:
                    festivals.append("除夕")
            except:
                pass

        term = solar.term if hasattr(solar, 'term') else None
        return lunar_month, lunar_day, is_leap, month_name, day_name, festivals, term
    except DateNotExist:
        return None, None, None, "", "", [], None


def get_lunar_display(year, month, day):
    info = get_lunar_info(year, month, day)
    if info[0] is None:
        return ""
    _, _, _, month_name, day_name, festivals, term = info
    parts = [f"{month_name}{day_name}"]
    if term:
        parts.append(f"【{term}】")
    if festivals:
        parts.append("🎉" + ",".join(festivals))
    return " ".join(parts)


def local_agent_response(query, context):
    """离线规则响应，作为 AI 不可用时的后备"""
    query_lower = query.lower()
    if "节日" in query_lower or "今天什么节" in query_lower:
        if "节日有：" in context:
            start = context.find("节日有：") + 4
            end = context.find("。", start)
            festivals = context[start:end] if end != -1 else context[start:]
            return f"根据日历，{festivals}" if festivals else "今天没有特别的节日。"
        else:
            return "今天没有特别的节日。"
    elif "农历" in query_lower:
        if "农历" in context:
            start = context.find("农历") + 2
            end = context.find("。", start)
            lunar = context[start:end] if end != -1 else context[start:]
            return f"今天的农历是{lunar}。"
        else:
            return "无法获取农历信息。"
    elif "节气" in query_lower:
        if "节气为" in context:
            start = context.find("节气为") + 3
            end = context.find("。", start)
            term = context[start:end] if end != -1 else context[start:]
            return f"今天的节气是{term}。"
        else:
            return "今天没有节气。"
    else:
        return f"我是智能日历助手。{context} 关于您的问题“{query}”，我暂时无法提供更详细的回答（未配置 AI API）。您可以设置 OPENAI_API_KEY 获取更智能的回复。"


def call_ai_agent(user_query, context_date):
    """调用 OpenAI 兼容 API 作为智能助手；未配置 Key 时使用本地规则响应。"""
    y, m, d = context_date.year, context_date.month, context_date.day
    info = get_lunar_info(y, m, d)
    lunar_str = f"{info[3]}{info[4]}" if info[0] is not None else "未知农历"
    festivals = info[5] if info[0] is not None else []
    term = info[6] if info[0] is not None else None
    context = f"今天是公历{y}年{m}月{d}日，农历{lunar_str}"
    if term:
        context += f"，节气为{term}"
    if festivals:
        context += f"，节日有：{', '.join(festivals)}"
    context += "。"

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE")
    if api_key:
        try:
            client = openai.OpenAI(api_key=api_key, base_url=base_url)
            messages = [
                {"role": "system", "content": f"你是一个中国传统文化和日历助手。{context} 请根据这个日期回答用户的问题。"},
                {"role": "user", "content": user_query}
            ]
            response = client.chat.completions.create(
                model="Qwen/Qwen3.5-4B",
                messages=messages,
                temperature=0.7,
                max_tokens=300,
                extra_body={"enable_thinking": False},
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI 调用失败：{str(e)}。请检查 API Key 或网络。"
    else:
        return local_agent_response(user_query, context)


def run_app():
    """智能万年历界面入口。"""
    st.title("📅 智能万年历（农历 · 节日 · 星座 · 天气 · AI 助手）")

    # ---------- 初始化会话状态 ----------
    if 'year' not in st.session_state:
        st.session_state.year = datetime.now().year
    if 'month' not in st.session_state:
        st.session_state.month = datetime.now().month
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = datetime.now().date()

    # ---------- 日历界面 ----------
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("◀ 上月"):
            if st.session_state.month == 1:
                st.session_state.year -= 1
                st.session_state.month = 12
            else:
                st.session_state.month -= 1
    with col2:
        st.markdown(f"<h3 style='text-align: center;'>{st.session_state.year}年 {st.session_state.month}月</h3>", unsafe_allow_html=True)
    with col3:
        if st.button("下月 ▶"):
            if st.session_state.month == 12:
                st.session_state.year += 1
                st.session_state.month = 1
            else:
                st.session_state.month += 1

    cal = calendar.monthcalendar(st.session_state.year, st.session_state.month)
    weekdays = ['一', '二', '三', '四', '五', '六', '日']
    header_cols = st.columns(7)
    for idx, day in enumerate(weekdays):
        header_cols[idx].markdown(f"<p style='text-align: center; font-weight: bold;'>{day}</p>", unsafe_allow_html=True)

    today = datetime.now().date()
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            else:
                current_date = date(st.session_state.year, st.session_state.month, day)
                is_today = (current_date == today)
                lunar_display = get_lunar_display(st.session_state.year, st.session_state.month, day)
                info = get_lunar_info(st.session_state.year, st.session_state.month, day)
                has_festival = len(info[5]) > 0 if info[0] is not None else False
                has_term = info[6] is not None if info[0] is not None else False

                if is_today:
                    style = "background-color: #ff6b6b; border-radius: 10px; padding: 4px; color: white;"
                elif has_festival or has_term:
                    style = "background-color: #fff3cd; border: 2px solid #ffc107; border-radius: 10px; padding: 4px;"
                else:
                    style = "padding: 4px;"

                day_html = f"<div style='{style} text-align: center; cursor: pointer;' onclick=''>"
                day_html += f"<div style='font-size: 20px; font-weight: bold;'>{day}</div>"
                if lunar_display:
                    day_html += f"<div style='font-size: 10px; color: {'#fff' if is_today else '#666'};'>{lunar_display}</div>"
                day_html += "</div>"
                cols[i].markdown(day_html, unsafe_allow_html=True)

    st.divider()

    # ---------- 日期详情与 AI 助手 ----------
    st.subheader("📋 日期详情与 AI 助手")

    selected_date = st.date_input("选择日期", value=st.session_state.selected_date)
    st.session_state.selected_date = selected_date

    if selected_date:
        y, m, d = selected_date.year, selected_date.month, selected_date.day
        info = get_lunar_info(y, m, d)
        if info[0] is not None:
            lunar_month, lunar_day, is_leap, month_name, day_name, festivals, term = info
            col_left, col_right = st.columns([1, 1])
            with col_left:
                st.write(f"**公历**：{y}年{m}月{d}日")
                st.write(f"**农历**：{month_name}{day_name}" + (" (闰月)" if is_leap else ""))
                st.write(f"**♈ 星座**：{get_zodiac_sign(m, d)}")
                if term:
                    st.write(f"**节气**：{term}")
                if festivals:
                    st.write(f"**🎉 节日**：{', '.join(festivals)}")
                else:
                    st.write("**📌 节日**：无")
            with col_right:
                st.write("**📖 今日宜忌**（仅供参考）")
                st.write("宜：出行、会友")
                st.write("忌：动土、嫁娶")
        else:
            st.warning("无法获取农历信息")

        # ---------- 今日天气 ----------
        st.markdown("#### 🌤️ 今日天气")
        weather_city = st.text_input("输入城市查询天气", value="北京", key="weather_city")
        if st.button("查询天气", key="weather_btn"):
            with st.spinner("获取天气中..."):
                weather_info = get_weather(weather_city)
            st.info(weather_info)

    # ---------- AI 助手聊天 ----------
    st.markdown("### 🤖 问智能助手")
    with st.form("chat_form", clear_on_submit=True):
        user_query = st.text_input("请输入您的问题", placeholder="例如：今天适合做什么？春节的由来是什么？")
        submitted = st.form_submit_button("发送")

    if submitted and user_query:
        with st.spinner("AI 思考中..."):
            reply = call_ai_agent(user_query, selected_date)
        st.session_state.chat_history.append((user_query, reply))

    if st.session_state.chat_history:
        for q, a in st.session_state.chat_history:
            st.chat_message("user").write(q)
            st.chat_message("assistant").write(a)
    else:
        st.info("💡 您可以提问关于农历、节日、节气或任何与日期相关的问题。")

    # ---------- 当月节日一览 ----------
    st.divider()
    st.subheader("📌 当月节日一览")
    festivals_in_month = []
    for day in range(1, calendar.monthrange(st.session_state.year, st.session_state.month)[1] + 1):
        info = get_lunar_info(st.session_state.year, st.session_state.month, day)
        if info[0] is not None and info[5]:
            festivals_in_month.append((day, info[5]))
    if festivals_in_month:
        for d, f in festivals_in_month:
            st.write(f"• **{d}日**：{', '.join(f)}")
    else:
        st.info("本月暂无节日")


if __name__ == "__main__":
    run_app()
