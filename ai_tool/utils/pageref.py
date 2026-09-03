"""页面引用注册表：app.py 构建 Page 对象后注册，供各应用内跳转（st.switch_page）。"""
_pages: dict = {}


def register(key: str, page) -> None:
    _pages[key] = page


def get(key: str):
    """获取已注册的 st.Page 对象；未注册返回 None。"""
    return _pages.get(key)
