"""行程输出结构校验。

按 OUTPUT_FORMAT_SPEC.md 校验 LLM 返回的 JSON 结构。
"""


def _check_str(obj: object, path: str, field: str) -> None:
    if not isinstance(obj, str):
        raise ValueError(
            f"校验失败 [{path}.{field}]：期望 string，实际 {type(obj).__name__}"
        )


def _check_number(obj: object, path: str, field: str) -> None:
    if not isinstance(obj, (int, float)) or isinstance(obj, bool):
        raise ValueError(
            f"校验失败 [{path}.{field}]：期望 number，实际 {type(obj).__name__}"
        )


def _check_list(obj: object, path: str, field: str) -> None:
    if not isinstance(obj, list):
        raise ValueError(
            f"校验失败 [{path}.{field}]：期望 array，实际 {type(obj).__name__}"
        )


def _check_dict(obj: object, path: str, field: str) -> None:
    if not isinstance(obj, dict):
        raise ValueError(
            f"校验失败 [{path}.{field}]：期望 object，实际 {type(obj).__name__}"
        )


def _validate_time_slot(slot: object, path: str) -> None:
    _check_dict(slot, path, "(时段)")
    d = slot
    for key in ("transport", "sights", "activities", "accommodation"):
        if key not in d:
            raise ValueError(f"校验失败 [{path}]：缺少字段 {key!r}")
        _check_str(d[key], path, key)


def _validate_day(day: object, path: str) -> None:
    _check_dict(day, path, "(单日)")
    d = day
    for key in ("day", "morning", "afternoon", "evening"):
        if key not in d:
            raise ValueError(f"校验失败 [{path}]：缺少字段 {key!r}")
    _check_number(d["day"], path, "day")
    _validate_time_slot(d["morning"], f"{path}.morning")
    _validate_time_slot(d["afternoon"], f"{path}.afternoon")
    _validate_time_slot(d["evening"], f"{path}.evening")


def validate_plan(result: dict) -> None:
    """校验行程输出结构，不符合 OUTPUT_FORMAT_SPEC 时抛出 ValueError。

    Args:
        result: json.loads 解析后的 dict

    Raises:
        ValueError: 含字段路径及错误原因
    """
    if not isinstance(result, dict):
        raise ValueError(
            f"校验失败 [根]：期望 object，实际 {type(result).__name__}"
        )

    # 5.1 顶层校验
    for key in ("title", "plan", "days"):
        if key not in result:
            raise ValueError(f"校验失败 [根]：缺少字段 {key!r}")
    _check_str(result["title"], "根", "title")
    _check_str(result["plan"], "根", "plan")
    _check_list(result["days"], "根", "days")

    # tips 可选，若存在须为 list of string
    if "tips" in result:
        tips = result["tips"]
        if not isinstance(tips, list):
            raise ValueError(
                f"校验失败 [根.tips]：期望 array，实际 {type(tips).__name__}"
            )
        for i, item in enumerate(tips):
            if not isinstance(item, str):
                raise ValueError(
                    f"校验失败 [根.tips[{i}]]：期望 string，实际 {type(item).__name__}"
                )

    # 5.2 单日校验 5.3 时段校验
    for i, day in enumerate(result["days"]):
        _validate_day(day, f"days[{i}]")
