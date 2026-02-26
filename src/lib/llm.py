import os
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from openai import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    OpenAIError,
    PermissionDeniedError,
    RateLimitError,
    OpenAI,
)
from src.types import UserInput
from src.destinations.new_zealand import get_context
from src.lib.prompt import SYSTEM_PROMPT, build_user_prompt
from src.lib.validator import validate_plan
from src.lib.formatter import format_plan_readable
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 默认 120s 覆盖冷启动+生成；Render 免费版约 30s 请求上限，可在环境变量设 25 以先返回 TIMEOUT 并依赖前端重试
DEFAULT_DEEPSEEK_TIMEOUT = int(os.getenv("DEEPSEEK_TIMEOUT_SECONDS", "120"))
DEFAULT_DEEPSEEK_MAX_RETRIES = int(os.getenv("DEEPSEEK_RETRY_MAX", "1"))
DEFAULT_DEEPSEEK_RETRY_BASE_DELAY = float(
    os.getenv("DEEPSEEK_RETRY_BASE_DELAY", "1.0")
)


class DeepSeekError(Exception):
    """标准化的 DeepSeek 调用错误。"""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        retryable: bool = False,
        http_status: int | None = None,
        ds_error_body: str | None = None,
        ds_trace_id: str | None = None,
    ):
        self.code = code
        self.retryable = retryable
        self.http_status = http_status
        self.ds_error_body = ds_error_body
        self.ds_trace_id = ds_trace_id
        super().__init__(message)


def _extract_http_info(exc: OpenAIError) -> tuple[int | None, str | None, str | None]:
    """从 OpenAI 异常中提取 HTTP 状态码、错误 body 摘要和 trace id（若有）。"""
    status: int | None = getattr(exc, "status_code", None) or getattr(
        exc, "status", None
    )
    body: str | None = None
    trace_id: str | None = None

    response = getattr(exc, "response", None)
    if response is not None:
        # 尝试从 response 中拿到 body 和 headers
        try:
            data = getattr(response, "json", None)
            if callable(data):
                data = data()
            if data is None:
                text = getattr(response, "text", None)
                if callable(text):
                    text = text()
                body = str(text) if text is not None else None
            else:
                body = str(data)
        except Exception:
            pass

        try:
            headers = getattr(response, "headers", None)
            if headers:
                # DeepSeek 若有专门 trace id 头可在此补充
                trace_id = (
                    headers.get("x-ds-trace-id")
                    or headers.get("x-request-id")
                    or headers.get("x-trace-id")
                )
        except Exception:
            pass

    if body is not None and len(body) > 200:
        body = body[:200] + "..."

    return status, body, trace_id


def call_deepseek(messages: list[dict]) -> tuple[str, int]:
    """带超时、重试和错误分类的 DeepSeek 调用入口。

    返回 (content, attempts)，其中 attempts 为实际尝试次数。
    """
    timeout = DEFAULT_DEEPSEEK_TIMEOUT
    max_retries = DEFAULT_DEEPSEEK_MAX_RETRIES
    base_delay = DEFAULT_DEEPSEEK_RETRY_BASE_DELAY

    attempts = 0

    while attempts <= max_retries:
        attempts += 1
        try:
            response = _client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                timeout=timeout,
            )
            content = response.choices[0].message.content
            return content, attempts
        except (
            APITimeoutError,
            APIConnectionError,
            AuthenticationError,
            PermissionDeniedError,
            RateLimitError,
            BadRequestError,
            APIError,
            OpenAIError,
        ) as e:
            message = str(e) or repr(e)
            status, body, trace_id = _extract_http_info(e)

            # 细化错误分类
            if isinstance(e, APITimeoutError):
                code = "TIMEOUT"
                retryable = True
            elif isinstance(e, APIConnectionError):
                code = "NETWORK_ERROR"
                retryable = True
            elif isinstance(
                e,
                (
                    AuthenticationError,
                    PermissionDeniedError,
                    RateLimitError,
                    BadRequestError,
                ),
            ):
                code = "DEEPSEEK_ERROR"
                # 鉴权/配额/请求错误通常不适合自动重试
                retryable = False
            elif isinstance(e, APIError):
                code = "DEEPSEEK_ERROR"
                # 5xx 可重试，4xx 不重试
                if status is not None and status >= 500:
                    retryable = True
                else:
                    retryable = False
            else:
                code = "UNKNOWN_ERROR"
                retryable = False

            if not retryable or attempts > max_retries:
                raise DeepSeekError(
                    code,
                    message,
                    retryable=retryable,
                    http_status=status,
                    ds_error_body=body,
                    ds_trace_id=trace_id,
                ) from e

            # 退避等待后重试（仅在可重试场景）
            delay = base_delay * (2 ** (attempts - 2)) if attempts > 1 else base_delay
            time.sleep(delay)

    # 理论上不会到达这里
    raise DeepSeekError("UNKNOWN_ERROR", "unknown error", retryable=False)


def generate_plan(user_input: UserInput) -> dict:
    """生成行程计划。

    成功时返回行程 dict；失败时抛出 DeepSeekError。
    """
    request_id = str(uuid4())
    start_time = datetime.now()
    start_monotonic = time.perf_counter()
    attempts_total = 0
    success = False
    error_code: str | None = None
    error_message: str | None = None
    http_status: int | None = None
    ds_error_body: str | None = None
    ds_trace_id: str | None = None

    context = get_context(
        user_input.landing_city, user_input.region, user_input.month
    )
    user_prompt = build_user_prompt(user_input, context)
    retry_hint = "\n\n注意：只返回合法 JSON，不要有任何其他文字"

    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
        raw, attempts = call_deepseek(messages)
        attempts_total += attempts

        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            # 带 hint 重试一次
            messages_hint = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt + retry_hint},
            ]
            raw, attempts = call_deepseek(messages_hint)
            attempts_total += attempts
            try:
                result = json.loads(raw)
            except json.JSONDecodeError as e:
                error_code = "JSON_DECODE_ERROR"
                error_message = "生成结果格式异常，请稍后重试"
                raise DeepSeekError(
                    error_code,
                    error_message,
                    retryable=False,
                ) from e

        try:
            validate_plan(result)
        except ValueError as e:
            error_code = "VALIDATION_ERROR"
            error_message = str(e) or "生成结果结构不合法，请稍后重试"
            raise DeepSeekError(error_code, error_message, retryable=False) from e

        _append_plan_to_file(result)
        success = True
        return result
    except DeepSeekError as e:
        if error_code is None:
            error_code = e.code
        if error_message is None:
            error_message = str(e)
        http_status = getattr(e, "http_status", None)
        ds_error_body = getattr(e, "ds_error_body", None)
        ds_trace_id = getattr(e, "ds_trace_id", None)
        raise
    except Exception as e:
        error_code = "UNKNOWN_ERROR"
        error_message = str(e) or repr(e)
        raise DeepSeekError(
            error_code,
            error_message,
            retryable=False,
        ) from e
    finally:
        duration_ms = int((time.perf_counter() - start_monotonic) * 1000)
        log_payload = {
            "event": "deepseek_call",
            "request_id": request_id,
            "landing_city": user_input.landing_city,
            "region": user_input.region,
            "days": user_input.days,
            "start_time": start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration_ms": duration_ms,
            "attempts": attempts_total,
            "success": success,
            "error_code": error_code,
            "error_message": error_message,
            "http_status": http_status,
            "ds_error_body": ds_error_body,
            "ds_trace_id": ds_trace_id,
        }
        # 使用 JSON 形式便于后续日志收集与分析
        try:
            logger.info(json.dumps(log_payload, ensure_ascii=False))
        except Exception:
            # 日志失败不影响主流程
            logger.info("deepseek_call %s", log_payload)


def _append_plan_to_file(plan: dict) -> None:
    """将 plan 追加写入 output_plan.json（JSON）和 output_plan.txt（可读文本）"""
    root = Path(__file__).resolve().parent.parent.parent
    sep = f"\n{'='*60}\n"
    ts = f"[{datetime.now().isoformat()}]\n"

    json_path = root / "output_plan.json"
    with open(json_path, "a", encoding="utf-8") as f:
        f.write(sep)
        f.write(ts)
        f.write(json.dumps(plan, ensure_ascii=False, indent=2))
        f.write("\n")

    txt_path = root / "output_plan.txt"
    with open(txt_path, "a", encoding="utf-8") as f:
        f.write(sep)
        f.write(ts)
        f.write(format_plan_readable(plan))
        f.write("\n")
