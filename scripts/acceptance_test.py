#!/usr/bin/env python3
"""验收测试：#4 CLI 入口、#5 输出结构校验。
使用 mock LLM 避免真实 API 调用。
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

# 合法 JSON（符合 OUTPUT_FORMAT_SPEC）
VALID_PLAN_JSON = json.dumps({
    "title": "新西兰南岛7日自驾行程",
    "plan": "本行程从奥克兰落地...",
    "days": [
        {
            "day": 1,
            "morning": {"transport": "", "sights": "", "activities": "", "accommodation": ""},
            "afternoon": {"transport": "", "sights": "", "activities": "", "accommodation": ""},
            "evening": {"transport": "", "sights": "", "activities": "", "accommodation": "酒店"},
        },
    ],
    "tips": ["建议1", "建议2"],
}, ensure_ascii=False)

# 非法 JSON：缺 title
INVALID_MISSING_TITLE = json.dumps({"plan": "x", "days": [], "tips": []}, ensure_ascii=False)

# 非法 JSON：days[i] 缺 morning
INVALID_DAY_MISSING_MORNING = json.dumps({
    "title": "x",
    "plan": "x",
    "days": [{"day": 1, "afternoon": {}, "evening": {}}],
    "tips": [],
}, ensure_ascii=False)

# 非法 JSON：时段 transport 非 string
INVALID_SLOT_NON_STRING = json.dumps({
    "title": "x",
    "plan": "x",
    "days": [{
        "day": 1,
        "morning": {"transport": 123, "sights": "", "activities": "", "accommodation": ""},
        "afternoon": {"transport": "", "sights": "", "activities": "", "accommodation": ""},
        "evening": {"transport": "", "sights": "", "activities": "", "accommodation": ""},
    }],
    "tips": [],
}, ensure_ascii=False)


def test_validator():
    """#5 输出结构校验"""
    from src.lib.validator import validate_plan
    from src.lib.llm import _append_plan_to_file

    print("=== #5 输出结构校验 ===")
    ok_count = 0

    # 5.1 合法通过
    try:
        validate_plan(json.loads(VALID_PLAN_JSON))
        print("  5.1 合法 plan 校验通过 ✓")
        ok_count += 1
    except Exception as e:
        print(f"  5.1 合法 plan 失败: {e}")

    # 5.1 缺 title 失败
    try:
        validate_plan(json.loads(INVALID_MISSING_TITLE))
        print("  5.1 缺 title 应失败但未失败 ✗")
    except ValueError as e:
        if "title" in str(e):
            print(f"  5.1 缺 title 正确失败: {e} ✓")
            ok_count += 1
        else:
            print(f"  5.1 缺 title 失败信息不明确: {e}")

    # 5.2 单日缺 morning 失败
    try:
        validate_plan(json.loads(INVALID_DAY_MISSING_MORNING))
        print("  5.2 单日缺 morning 应失败但未失败 ✗")
    except ValueError as e:
        if "morning" in str(e) or "缺少字段" in str(e):
            print(f"  5.2 单日缺 morning 正确失败: {e} ✓")
            ok_count += 1
        else:
            print(f"  5.2 单日缺 morning 失败信息: {e}")

    # 5.3 时段 transport 非 string 失败
    try:
        validate_plan(json.loads(INVALID_SLOT_NON_STRING))
        print("  5.3 transport 非 string 应失败但未失败 ✗")
    except ValueError as e:
        if "transport" in str(e) or "string" in str(e):
            print(f"  5.3 transport 非 string 正确失败: {e} ✓")
            ok_count += 1
        else:
            print(f"  5.3 transport 非 string 失败信息: {e}")

    return ok_count == 4


def test_llm_validation_before_write():
    """5.4 5.5 校验失败不写入、校验通过才写入"""
    from src.lib.llm import generate_plan
    from src.types import UserInput

    user_input = UserInput(
        landing_city="奥克兰",
        region="南岛",
        month=3,
        days=7,
        travelers=2,
    )

    write_called = []

    def track_append(plan):
        write_called.append(plan)

    with patch("src.lib.llm._client") as mock_client:
        # 非法 JSON -> 校验失败 -> 不写入
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=INVALID_MISSING_TITLE))]
        )
        with patch("src.lib.llm._append_plan_to_file", side_effect=track_append):
            try:
                generate_plan(user_input)
            except ValueError:
                pass
        if len(write_called) == 0:
            print("  5.4 校验失败时未写入 output_plan.txt ✓")
        else:
            print("  5.4 校验失败时不应写入但写入了 ✗")

    write_called.clear()
    with patch("src.lib.llm._client") as mock_client:
        mock_client.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=VALID_PLAN_JSON))]
        )
        with patch("src.lib.llm._append_plan_to_file", side_effect=track_append):
            result = generate_plan(user_input)
        if len(write_called) == 1 and result.get("title"):
            print("  5.5 校验通过时正常写入并返回 ✓")
        else:
            print("  5.5 校验通过时写入/返回异常 ✗")


def main():
    v_ok = test_validator()
    print()
    test_llm_validation_before_write()
    print()
    print("=== 结论 ===")
    print("  validator 单元测试: " + ("通过" if v_ok else "部分失败"))
    return 0 if v_ok else 1


if __name__ == "__main__":
    sys.exit(main())
