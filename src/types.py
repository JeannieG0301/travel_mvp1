"""用户输入参数类型定义。

重要：修改 UserInput 或 VALID_* 常量时，必须同步更新项目根目录的 INPUT_PARAMS_SPEC.md。
"""

from dataclasses import dataclass

VALID_LANDING_CITIES = ("奥克兰", "基督城")
VALID_REGIONS = ("北岛", "南岛", "南北岛都玩")
VALID_TIME_SLOTS = ("早上", "下午", "傍晚", "深夜")
VALID_BUDGET_LEVELS = ("经济实惠", "舒适享受")
VALID_STYLES = ("自然风光", "户外冒险", "城市探索", "文化体验", "美食之旅")


@dataclass
class UserInput:
    """用户输入参数"""

    # 必选
    landing_city: str  # 奥克兰 / 基督城
    region: str  # 北岛 / 南岛 / 南北岛都玩
    month: int  # 1-12
    days: int  # 1-100，不含飞行日
    travelers: int  # 1-5

    # 可选
    landing_time: str = ""  # 早上 / 下午 / 傍晚 / 深夜
    departure_time: str = ""  # 早上 / 下午 / 傍晚 / 深夜
    styles: list[str] | None = None  # 最多5个：自然风光/户外冒险/城市探索/文化体验/美食之旅
    budget_level: str = ""  # 经济实惠 / 舒适享受
    must_see: str = ""  # 自由文本

    def __post_init__(self) -> None:
        if self.landing_city not in VALID_LANDING_CITIES:
            raise ValueError("landing_city 必须是 奥克兰 或 基督城")

        if self.region not in VALID_REGIONS:
            raise ValueError("region 必须是 北岛 / 南岛 / 南北岛都玩")

        if not 1 <= self.month <= 12:
            raise ValueError("month 必须在 1-12 之间")

        if not 1 <= self.days <= 100:
            raise ValueError("days 必须在 1-100 之间")

        if not 1 <= self.travelers <= 5:
            raise ValueError("travelers 必须在 1-5 之间")

        if self.landing_time and self.landing_time not in VALID_TIME_SLOTS:
            raise ValueError("landing_time 非空时必须是 早上/下午/傍晚/深夜 之一")

        if self.departure_time and self.departure_time not in VALID_TIME_SLOTS:
            raise ValueError("departure_time 非空时必须是 早上/下午/傍晚/深夜 之一")

        if self.budget_level and self.budget_level not in VALID_BUDGET_LEVELS:
            raise ValueError("budget_level 非空时必须是 经济实惠 或 舒适享受")

        if self.styles is not None:
            if len(self.styles) > 5:
                raise ValueError("styles 最多5个")
            for s in self.styles:
                if s not in VALID_STYLES:
                    raise ValueError(f"styles 中的 '{s}' 不在合法标签内: {VALID_STYLES}")
