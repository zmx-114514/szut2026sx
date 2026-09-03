"""模型别名解析：models/ 目录下每个模型一个文件，文件名即别名。

用法（utils/model.py 等）：
    from models import resolve_model
    model_id = resolve_model("qwen3")          # -> models/qwen3.py 中的 MODEL_ID
    model_id = resolve_model("deepseek-ai/DeepSeek-V3")  # 完整 ID 原样返回
"""
import importlib
from pathlib import Path

# models/ 包所在目录
_DIR = Path(__file__).parent


def list_aliases():
    """列出所有可用别名（models/ 目录下的 .py 文件名，排除 __init__）。"""
    return sorted(
        p.stem for p in _DIR.glob("*.py")
        if p.stem != "__init__"
    )


def resolve_model(name: str) -> str:
    """解析模型名：别名 -> models/<别名>.py 的 MODEL_ID；完整模型 ID 原样返回。"""
    name = (name or "").strip()
    if not name:
        return ""
    # 含 "/" 视为完整模型 ID（如 deepseek-ai/DeepSeek-V3）
    if "/" in name:
        return name
    if (_DIR / f"{name}.py").exists():
        mod = importlib.import_module(f"models.{name}")
        model_id = getattr(mod, "MODEL_ID", "")
        if model_id:
            return model_id
    # 未匹配别名，原样返回（交由上层报错）
    return name
