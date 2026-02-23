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
from src.lib.llm import generate_plan

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
        return result
    except ValueError as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# 托管 frontend 静态文件（开发/生产均可）
frontend_dir = root / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="static")
