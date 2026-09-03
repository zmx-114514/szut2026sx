"""进程级预热管理：重型模块后台异步导入，界面先渲染、就绪后自动呈现。

- start_prewarm()：启动后台预热（进程级只执行一次，安全地在任意入口调用）
- ensure_ready(key, import_fn)：非阻塞查询模块是否已就绪；未就绪时自动在
  后台线程触发导入（幂等），就绪返回 True，进行中返回 False
"""
import functools
import sys
import threading

# key -> True(就绪) / False(导入中) / "error"(导入失败)
_state: dict[str, object] = {}
_state_lock = threading.Lock()
_threads: dict[str, threading.Thread] = {}


def _trigger(key: str, import_fn) -> None:
    """若该 key 尚无线程在工作，则启动一个后台导入线程（幂等）。"""
    with _state_lock:
        if _state.get(key) is True:  # 已就绪
            return
        t = _threads.get(key)
        if t is not None and t.is_alive():  # 导入中
            return

        def _work():
            try:
                import_fn()
                ok = True
            except Exception:
                ok = "error"
            with _state_lock:
                _state[key] = ok

        t = threading.Thread(target=_work, daemon=True, name=f"prewarm-{key}")
        _threads[key] = t
        if _state.get(key) is None:
            _state[key] = False
        t.start()


def ensure_ready(key: str, import_fn) -> bool:
    """非阻塞确保模块导入；就绪（或已在 sys.modules）返回 True，导入中返回 False。

    导入失败的 key 返回 True，让页面走同步路径自然抛错展示。
    """
    if key in sys.modules or _state.get(key) is True:
        return True
    if _state.get(key) == "error":
        return True
    _trigger(key, import_fn)
    return _state.get(key) is True


# ---------- 各应用的导入函数 ----------
def _import_kitchen():
    import main  # noqa: F401


def _import_calendar():
    import calendar_app  # noqa: F401


def _import_vision():
    import image_agent  # noqa: F401


def _import_companion():
    import companion_app  # noqa: F401


@functools.cache
def start_prewarm():
    """应用启动时后台预热全部重型模块（进程级只执行一次）。"""
    _trigger("main", _import_kitchen)
    _trigger("calendar_app", _import_calendar)
    _trigger("image_agent", _import_vision)
    _trigger("companion_app", _import_companion)
    return True
