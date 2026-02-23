"""行程可读性格式化。按 OUTPUT_FORMAT_SPEC 将 plan dict 转为可读文本。"""


def _format_time_slot(slot: dict, label: str) -> str:
    """格式化单个时段（morning/afternoon/evening）"""
    lines: list[str] = []
    t = slot.get("transport", "")
    s = slot.get("sights", "")
    a = slot.get("activities", "")
    acc = slot.get("accommodation", "")

    if t:
        lines.append(f"  交通：{t}")
    if s:
        lines.append(f"  景点：{s}")
    if a:
        lines.append(f"  活动：{a}")
    if acc:
        lines.append(f"  住宿：{acc}")

    if not lines:
        return f"  【{label}】无安排\n"
    return f"  【{label}】\n" + "\n".join(lines) + "\n"


def format_plan_readable(plan: dict) -> str:
    """将 plan dict 转为可读文本。

    结构：标题、总览、按天行程（上午/下午/晚上，每段含 transport、sights、activities、
    accommodation）、tips。参考 OUTPUT_FORMAT_SPEC 的顶层、单日、时段结构。
    """
    parts: list[str] = []

    title = plan.get("title", "")
    if title:
        parts.append(f"# {title}\n")

    plan_overview = plan.get("plan", "")
    if plan_overview:
        parts.append("## 行程总览\n")
        parts.append(plan_overview)
        parts.append("\n")

    days = plan.get("days", [])
    if days:
        parts.append("## 按天行程\n")
        for d in days:
            day_num = d.get("day", "?")
            parts.append(f"### 第 {day_num} 天\n")
            morning = d.get("morning", {})
            afternoon = d.get("afternoon", {})
            evening = d.get("evening", {})
            parts.append(_format_time_slot(morning, "上午"))
            parts.append(_format_time_slot(afternoon, "下午"))
            parts.append(_format_time_slot(evening, "晚上"))
            parts.append("\n")

    tips = plan.get("tips", [])
    if tips and isinstance(tips, list):
        parts.append("## 注意事项\n")
        for i, tip in enumerate(tips):
            if isinstance(tip, str):
                parts.append(f"- {tip}\n")

    return "".join(parts).rstrip()
