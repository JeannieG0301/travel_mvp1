"""FastAPI 应用：POST /api/generate-plan 生成行程。"""

import sys
from pathlib import Path

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# 确保项目根在 path 中
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from src.types import UserInput
from src.lib.llm import generate_plan, DeepSeekError
from backend.share_store import save_plan, get_plan

app = FastAPI(title="新西兰行程规划 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/generate-plan")
def api_generate_plan(body: dict = Body(...)) -> dict:
    """接收 JSON 请求体，构造 UserInput，调用 generate_plan，返回行程 JSON。"""
    try:
        user_input = UserInput(
            landing_city=body.get("landing_city", ""),
            region=body.get("region", ""),
            month=int(body.get("month", 0)),
            days=int(body.get("days", 0)),
            travelers=int(body.get("travelers", 0)),
            landing_time=body.get("landing_time") or "",
            departure_time=body.get("departure_time") or "",
            styles=body.get("styles") or None,
            budget_level=body.get("budget_level") or "",
            must_see=body.get("must_see") or "",
        )
    except (ValueError, TypeError, KeyError) as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

    try:
        result = generate_plan(user_input)
        share_id = save_plan(result)
        out = {**result, "share_id": share_id}
        return out
    except DeepSeekError as e:
        code = e.code
        if code in ("NETWORK_ERROR", "TIMEOUT"):
            status = 503
            msg = "服务暂时不可用，请稍后重试"
        elif code == "DEEPSEEK_ERROR":
            status = 502
            msg = "上游服务异常，请稍后重试"
        elif code == "JSON_DECODE_ERROR":
            status = 502
            msg = "生成结果异常，请稍后重试"
        elif code == "VALIDATION_ERROR":
            status = 500
            msg = "生成结果结构不合法，请稍后重试"
        else:
            status = 500
            msg = "未知错误，请稍后重试"

        return JSONResponse(
            status_code=status,
            content={"error": msg, "code": code},
        )


@app.get("/api/plans/{share_id}")
def api_get_plan(share_id: str):
    """根据 share_id 返回行程 JSON；不存在或已过期返回 404。"""
    plan = get_plan(share_id)
    if plan is None:
        return JSONResponse(status_code=404, content={"error": "链接已过期或不存在"})
    return plan


# 托管 frontend 静态文件（开发/生产均可）
frontend_dir = root / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="static")
