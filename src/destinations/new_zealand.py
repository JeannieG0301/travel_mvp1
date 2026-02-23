"""新西兰目的地配置：表单选项常量 + prompt 上下文"""

from src.types import (
    VALID_BUDGET_LEVELS,
    VALID_LANDING_CITIES,
    VALID_REGIONS,
    VALID_STYLES,
)

# 第一部分：表单选项常量（给前端用，从 types 直接复用）
__all__ = [
    "VALID_LANDING_CITIES",
    "VALID_REGIONS",
    "VALID_STYLES",
    "VALID_BUDGET_LEVELS",
    "get_context",
]

# 城市背景
_LANDING_CITY_BACKGROUND = {
    "奥克兰": (
        "北岛最大城市，交通便利，适合北岛路线起点，"
        "周边有酒庄、海滩、火山地貌"
    ),
    "基督城": (
        "南岛门户，城市重建后充满活力，"
        "适合南岛自驾起点，靠近库克山和峡湾"
    ),
}

# 区域特点
_REGION_FEATURES = {
    "北岛": (
        "奥克兰、罗托鲁瓦、陶波、惠灵顿为核心，"
        "地热温泉、毛利文化、萤火虫洞"
    ),
    "南岛": (
        "皇后镇、米尔福德峡湾、库克山、但尼丁为核心，"
        "极限运动、峡湾风光、自驾天堂"
    ),
    "南北岛都玩": (
        "建议北岛2-3天，南岛重点游，"
        "两岛之间可乘国内航班或渡轮"
    ),
}

# 月份季节（1-12月）
_MONTH_SEASON = {
    1: "盛夏旺季，温暖晴朗，需提前预订",
    2: "盛夏旺季，温暖晴朗，需提前预订",
    3: "秋季，人少景美，性价比最高",
    4: "秋季，人少景美，性价比最高",
    5: "初冬，部分山区开始降雪",
    6: "冬季，南岛滑雪季，北岛温和",
    7: "冬季，南岛滑雪季，北岛温和",
    8: "冬季，南岛滑雪季，北岛温和",
    9: "春季，百花盛开，羊羔出生季",
    10: "春季，百花盛开，羊羔出生季",
    11: "初夏，日照长，适合户外活动",
    12: "初夏，日照长，适合户外活动",
}

# 通用须知
_GENERAL_TIPS = """
【通用须知】
- 驾车靠左行驶，建议提前适应
- 热门景点如米尔福德峡湾需在 DOC 网站提前预约
- 部分山区无手机信号，建议下载离线地图
- 货币为新西兰元 NZD，刷卡普及，便利店可取现
- 新西兰紫外线强，防晒必备
""".strip()


def get_context(landing_city: str, region: str, month: int) -> str:
    """生成新西兰行程规划的 prompt 上下文。"""
    city_text = _LANDING_CITY_BACKGROUND.get(
        landing_city, f"降落城市：{landing_city}"
    )
    region_text = _REGION_FEATURES.get(region, f"区域：{region}")
    month_text = _MONTH_SEASON.get(month, "请根据具体月份安排行程")

    return "\n\n".join([
        f"【城市背景】\n{city_text}",
        f"【区域特点】\n{region_text}",
        f"【月份季节】{month}月：{month_text}",
        _GENERAL_TIPS,
    ])
