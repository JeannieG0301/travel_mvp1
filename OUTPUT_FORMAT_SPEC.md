# 行程输出格式规范（MVP1）

> 本规范来源于产品功能管理 Agent 对话 [541121cb-89a5-469e-936a-fae0b8705690]，为行程规划输出的权威定义。

## 一、顶层结构

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 行程标题，如「新西兰南岛 14 日行程」 |
| plan | string | 是 | 行程总览，1–2 段概括路线、风格、节奏 |
| days | array | 是 | 按天的行程数组 |
| tips | array of string | 否 | 注意事项（预定提醒、装备等），可为空数组 |

## 二、单日结构 `days[i]`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| day | number | 是 | 第几天（1, 2, 3...） |
| morning | object | 是 | 上午安排 |
| afternoon | object | 是 | 下午安排 |
| evening | object | 是 | 晚上安排 |

## 三、时段结构 `morning` / `afternoon` / `evening`

每个时段均为对象，包含以下字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| transport | string | 是 | 交通，含地点与驾车时长。格式如「奥克兰机场→市区酒店（约30分钟）」；无交通则为空字符串 `""` |
| sights | string | 是 | 景点 / 观景点，无则为空字符串 |
| activities | string | 是 | 活动，无则为空字符串 |
| accommodation | string | 是 | 住宿建议；通常晚上有，上午/下午可为空字符串 |

## 四、补充约定

- **目的地**：仅新西兰
- **交通方式**：以自驾为主
- **餐饮**：不包含在输出中
- **交通字段**：用自然语言描述，包含「地点→地点（时长）」
- **tips 内容**：主要包含预定提醒（按淡旺季）、装备建议等；不接入路况/天气 API

## 五、JSON 示例

```json
{
  "title": "新西兰南岛7日自驾行程",
  "plan": "本行程从奥克兰落地，经皇后镇、瓦纳卡、库克山至但尼丁，覆盖南岛精华。以自驾为主，兼顾峡湾、极限运动与自然风光，节奏适中。",
  "days": [
    {
      "day": 1,
      "morning": {
        "transport": "奥克兰机场→市区租车点（约20分钟）",
        "sights": "",
        "activities": "办理租车手续",
        "accommodation": ""
      },
      "afternoon": {
        "transport": "市区→天空塔（约15分钟）",
        "sights": "天空塔、使命湾海滩",
        "activities": "轻松游览",
        "accommodation": ""
      },
      "evening": {
        "transport": "",
        "sights": "",
        "activities": "市区休息",
        "accommodation": "市中心或海滨区域酒店"
      }
    },
    {
      "day": 2,
      "morning": {
        "transport": "奥克兰机场→皇后镇机场（国内航班约2小时），皇后镇机场→湖畔酒店（约15分钟）",
        "sights": "",
        "activities": "取车、入住",
        "accommodation": ""
      },
      "afternoon": {
        "transport": "",
        "sights": "瓦卡蒂普湖全景",
        "activities": "Skyline缆车、滑板车 或 Shotover Jet喷气快艇",
        "accommodation": ""
      },
      "evening": {
        "transport": "",
        "sights": "",
        "activities": "镇中心晚餐",
        "accommodation": "皇后镇湖畔酒店"
      }
    }
  ],
  "tips": [
    "3月旺季，米尔福德峡湾游船建议提前在DOC网站预约",
    "山区可能降温，建议准备防风防水外套和徒步鞋"
  ]
}
```

## 六、实现状态

| 项目 | 当前实现 | 规范要求 |
|------|----------|----------|
| 顶层 | `src/lib/prompt.py` 已约束 title, plan, days, tips | title, plan, days, tips |
| 单日 | 已约束 day, morning, afternoon, evening | day, morning, afternoon, evening |
| 时段 | 已约束 transport, sights, activities, accommodation | transport, sights, activities, accommodation |

`prompt.py` 的 SYSTEM_PROMPT 已按本规范更新，LLM 输出应满足上述完整结构。`src/lib/validator.py` 在解析后对输出做 schema 校验，校验失败时不写入文件。
