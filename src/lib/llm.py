import os
import json
from datetime import datetime
from pathlib import Path

from openai import OpenAI
from src.types import UserInput
from src.destinations.new_zealand import get_context
from src.lib.prompt import SYSTEM_PROMPT, build_user_prompt
from src.lib.validator import validate_plan
from src.lib.formatter import format_plan_readable
from dotenv import load_dotenv

load_dotenv()

_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def generate_plan(user_input: UserInput) -> dict:
    context = get_context(
        user_input.landing_city, user_input.region, user_input.month
    )
    user_prompt = build_user_prompt(user_input, context)

    def _call(prompt: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ]
        response = _client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
        )
        return response.choices[0].message.content

    retry_hint = "\n\n注意：只返回合法 JSON，不要有任何其他文字"

    raw = _call(user_prompt)
    try:
        result = json.loads(raw)
        validate_plan(result)
        _append_plan_to_file(result)
        return result
    except (json.JSONDecodeError, KeyError, TypeError, IndexError):
        raw = _call(user_prompt + retry_hint)
        try:
            result = json.loads(raw)
            validate_plan(result)
            _append_plan_to_file(result)
            return result
        except (json.JSONDecodeError, KeyError, TypeError, IndexError) as e:
            raise ValueError(f"无法解析 LLM 返回为 JSON，原始内容: {raw}") from e
        except ValueError:
            raise


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
