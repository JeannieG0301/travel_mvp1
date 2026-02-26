"""可分享行程短期存储：文件落盘，TTL 7 天。"""

import json
import time
import uuid
from pathlib import Path

# 项目根目录
_root = Path(__file__).resolve().parent.parent
SHARES_DIR = _root / "data" / "shares"
TTL_SECONDS = 7 * 24 * 3600  # 7 天


def _ensure_dir() -> Path:
    SHARES_DIR.mkdir(parents=True, exist_ok=True)
    return SHARES_DIR


def save_plan(plan: dict) -> str:
    """将行程保存到 data/shares/{id}.json，返回 share_id。"""
    _ensure_dir()
    share_id = str(uuid.uuid4())
    path = SHARES_DIR / f"{share_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    return share_id


def get_plan(share_id: str) -> dict | None:
    """根据 share_id 读取行程；不存在或已过期返回 None。"""
    if not share_id or "/" in share_id or "\\" in share_id:
        return None
    path = SHARES_DIR / f"{share_id}.json"
    if not path.is_file():
        return None
    try:
        mtime = path.stat().st_mtime
        if time.time() - mtime > TTL_SECONDS:
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
