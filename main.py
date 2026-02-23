#!/usr/bin/env python3
"""CLI 入口：新西兰行程规划。"""

import argparse
import sys

from src.types import UserInput
from src.lib.llm import generate_plan


def _parse_styles(value: str | None) -> list[str] | None:
    """解析 styles：逗号分隔字符串 -> list[str]，空或 None -> None"""
    if not value or not value.strip():
        return None
    return [s.strip() for s in value.split(",") if s.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="新西兰自驾行程规划（基于 LLM）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --landing_city 奥克兰 --region 南岛 --month 3 --days 7 --travelers 2
  python main.py -l 基督城 -r 南北岛都玩 -m 6 -d 10 -t 3 --budget_level 舒适享受
  python main.py -l 奥克兰 -r 北岛 -m 9 -d 5 -t 2 --styles 自然风光,文化体验 --must_see "霍比特村"
        """,
    )

    # 必填参数
    parser.add_argument(
        "-l",
        "--landing_city",
        required=True,
        choices=["奥克兰", "基督城"],
        help="落地城市",
    )
    parser.add_argument(
        "-r",
        "--region",
        required=True,
        choices=["北岛", "南岛", "南北岛都玩"],
        help="游览区域",
    )
    parser.add_argument(
        "-m",
        "--month",
        required=True,
        type=int,
        help="出发月份（1-12）",
    )
    parser.add_argument(
        "-d",
        "--days",
        required=True,
        type=int,
        help="游玩天数（1-100，不含飞行日）",
    )
    parser.add_argument(
        "-t",
        "--travelers",
        required=True,
        type=int,
        help="出行人数（1-5）",
    )

    # 可选参数
    parser.add_argument(
        "--landing_time",
        default="",
        metavar="时段",
        help="落地时间：早上/下午/傍晚/深夜（默认：未提供）",
    )
    parser.add_argument(
        "--departure_time",
        default="",
        metavar="时段",
        help="离程时间：早上/下午/傍晚/深夜（默认：未提供）",
    )
    parser.add_argument(
        "--styles",
        type=str,
        default=None,
        metavar="S1,S2,...",
        help="旅行风格，逗号分隔，最多5个。可选：自然风光、户外冒险、城市探索、文化体验、美食之旅",
    )
    parser.add_argument(
        "--budget_level",
        default="",
        choices=["经济实惠", "舒适享受"],
        help="预算级别：经济实惠/舒适享受（默认：未指定，不传即可）",
    )
    parser.add_argument(
        "--must_see",
        default="",
        metavar="TEXT",
        help="必去清单（自由文本）",
    )

    args = parser.parse_args()

    try:
        user_input = UserInput(
            landing_city=args.landing_city,
            region=args.region,
            month=args.month,
            days=args.days,
            travelers=args.travelers,
            landing_time=args.landing_time or "",
            departure_time=args.departure_time or "",
            styles=_parse_styles(args.styles),
            budget_level=args.budget_level or "",
            must_see=(args.must_see or "").strip(),
        )
    except ValueError as e:
        print(f"参数校验失败: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        generate_plan(user_input)
        print("已保存到 output_plan.json、output_plan.txt")
    except ValueError as e:
        print(f"生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
