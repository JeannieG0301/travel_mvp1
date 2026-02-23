#!/usr/bin/env python3
"""测试 generate_plan 输出是否符合 OUTPUT_FORMAT_SPEC。
用法: python scripts/test_generate_plan.py
"""

import json
import sys
from pathlib import Path

# 添加项目根目录到 path
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from src.types import UserInput
from src.lib.llm import generate_plan, _append_plan_to_file


def validate_output_spec(plan: dict) -> tuple[bool, list[str]]:
    """按 OUTPUT_FORMAT_SPEC 验证返回结构。返回 (通过?, 问题列表)。"""
    issues = []

    # 1. 顶层结构
    required_top = ("title", "plan", "days", "tips")
    for k in required_top:
        if k not in plan:
            issues.append(f"缺少顶层字段: {k}")
        elif k == "tips" and not isinstance(plan.get(k), list):
            issues.append("tips 必须是 array")
        elif k == "days" and not isinstance(plan.get(k), list):
            issues.append("days 必须是 array")

    if "days" not in plan or not isinstance(plan["days"], list):
        return False, issues

    # 2. 单日结构 days[i]
    required_day = ("day", "morning", "afternoon", "evening")
    required_slot = ("transport", "sights", "activities", "accommodation")

    for i, d in enumerate(plan["days"]):
        if not isinstance(d, dict):
            issues.append(f"days[{i}] 必须是对象")
            continue
        for k in required_day:
            if k not in d:
                issues.append(f"days[{i}] 缺少字段: {k}")
            elif k in ("morning", "afternoon", "evening") and isinstance(d.get(k), dict):
                slot = d[k]
                for sk in required_slot:
                    if sk not in slot:
                        issues.append(f"days[{i}].{k} 缺少字段: {sk}")

    passed = len(issues) == 0
    return passed, issues


def main():
    user_input = UserInput(
        landing_city="奥克兰",
        region="南北岛都玩",
        month=3,
        days=7,
        travelers=2,
    )

    try:
        result = generate_plan(user_input)
    except Exception as e:
        print(f"API 调用失败: {e}", file=sys.stderr)
        sys.exit(1)

    passed, issues = validate_output_spec(result)
    print("=" * 60)
    print("OUTPUT_FORMAT_SPEC 验证")
    print("=" * 60)
    print(f"通过: {passed}")
    if issues:
        for i in issues:
            print(f"  - {i}")
    print()
    print("返回结构摘要:")
    print(f"  title: {result.get('title', 'N/A')[:50]}...")
    print(f"  plan: {result.get('plan', 'N/A')[:80]}...")
    print(f"  days 数量: {len(result.get('days', []))}")
    print(f"  tips 数量: {len(result.get('tips', []))}")
    if result.get("days"):
        d0 = result["days"][0]
        for slot in ("morning", "afternoon", "evening"):
            s = d0.get(slot, {})
            keys = list(s.keys()) if isinstance(s, dict) else []
            print(f"  days[0].{slot} 字段: {keys}")

    if not passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
