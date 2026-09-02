import os
import requests
from dotenv import load_dotenv

load_dotenv()

_API_URL = os.getenv("BEEIMG_API_BASE", "https://www.beeimg.cn") + "/api/v2/upload"
_STORAGE_ID = os.getenv("BEEIMG_STORAGE_ID", "")
_TOKEN = os.getenv("BEEIMG_TOKEN", "")

def upload_image(image_bytes: bytes, filename: str) -> str:
    """上传图片到图床，返回公网URL"""
    headers = {"Accept": "application/json"}
    if _TOKEN:
        headers["Authorization"] = f"Bearer {_TOKEN}"

    resp = requests.post(
        _API_URL,
        headers=headers,
        files={"file": (filename, image_bytes)},
        data={"storage_id": str(_STORAGE_ID)},
        timeout=30,
    )
    result = resp.json()
    if result.get("status") == "success":
        return result["data"]["public_url"]
    raise RuntimeError(f"上传失败：{result.get('message', '未知错误')}")
