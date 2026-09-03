from langchain.tools import tool
from datetime import datetime
import requests
from langchain_tavily import TavilySearch


@tool
def get_current_date() -> str:
    """获取当前日期和时间。

    Returns:
        当前本地时间的格式化字符串，例如 "2026年09月02日 15:30:00 星期三"。
    """
    now = datetime.now()
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[now.weekday()]
    return now.strftime(f"%Y年%m月%d日 %H:%M:%S {weekday}")


@tool
def get_weather(city: str) -> str:
    """获取指定城市的当前天气信息。

    Args:
        city: 城市名称，例如 "北京"、"上海"、"Beijing"。

    Returns:
        该城市当前的天气描述，包括天气状况、温度、体感温度、湿度、风速等。
    """
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

        return (
            f"{region} 当前天气：{desc}，"
            f"气温 {temp_c}°C（体感 {feels_like}°C），"
            f"湿度 {humidity}%，"
            f"风速 {wind_speed} km/h（{wind_dir}方向）"
        )
    except requests.RequestException as e:
        return f"获取 {city} 天气失败：网络错误 - {e}"
    except (KeyError, IndexError, ValueError) as e:
        return f"解析 {city} 天气数据失败：{e}"


@tool
def recognize_image_tool(image_url: str, question: str = "请详细描述这张图片的内容") -> str:
    """识别图片内容。image_url 为图片的 URL 或本地文件路径。当需要分析、描述或理解图片时调用此工具。"""
    from image_recognition import recognize_image
    return recognize_image(image_url, question)


web_search = TavilySearch()

tools = [get_current_date, get_weather, web_search, recognize_image_tool]
