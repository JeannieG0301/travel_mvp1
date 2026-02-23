# travel_mvp1 架构文档

> **更新约定**：每次架构发生变更时，必须同步更新此文件。建议在 PR 或提交说明中注明「架构变更：……」

---

## 一、概述

本项目是基于 LLM 的旅行行程规划应用。MVP1 聚焦 **新西兰自驾** 板块：中国用户落地新西兰后的行程规划，不包含机票/酒店/租车预订。

| 版本 | 说明 |
|------|------|
| MVP1 | 单一目的地（新西兰），单轮交互，匿名使用，无登录 |

---

## 二、MVP1 范围（产品边界）

| 维度 | 决策 |
|------|------|
| 落地城市 | 仅奥克兰、基督城 |
| 游览区域 | 北岛 / 南岛 / 南北岛都玩 |
| 行程输出 | 见 `OUTPUT_FORMAT_SPEC.md` |
| 对话模式 | 单轮：一次输入 → 一次生成 |
| 用户身份 | 匿名，不登录，无历史保存 |
| 端形态 | Web（响应式，支持小红书链接分享）；CLI 保留供调试 |

---

## 三、目录结构

```
travel_mvp1/
├── main.py                  # CLI 入口（argparse）
├── ARCHITECTURE.md          # 本架构文档
├── OUTPUT_FORMAT_SPEC.md    # 行程输出格式规范
├── INPUT_PARAMS_SPEC.md     # 用户输入参数规范
├── output_plan.json         # 行程 JSON 持久化（追加写入）
├── output_plan.txt          # 行程可读文本持久化（追加写入）
├── .env                     # 环境变量（API Key）
├── requirements.txt
├── backend/                 # HTTP API 服务
│   └── app.py               # FastAPI 应用，暴露 /api/generate-plan
├── frontend/                # Web 前端（响应式）
│   ├── index.html           # 单页：表单 + 行程展示
│   ├── style.css            # 样式，含移动端适配
│   └── app.js               # 表单提交、API 调用、结果渲染
└── src/                     # 核心逻辑（CLI 与 API 共用）
    ├── types.py             # 用户输入数据模型
    ├── lib/
    │   ├── prompt.py        # Prompt 组装
    │   ├── llm.py           # LLM 编排与输出
    │   ├── validator.py     # 行程输出结构校验
    │   └── formatter.py     # 行程可读性格式化
    └── destinations/
        └── new_zealand.py   # 新西兰目的地配置
```

---

## 四、分层架构

### 4.1 逻辑分层

```
┌─────────────────────────────────────────────────────────────────┐
│  接入层      main.py (CLI) / backend/app.py (HTTP API)           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│  输入层      UserInput (types.py)                                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│  上下文层    get_context() (destinations/new_zealand.py)         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│  Prompt 层   build_user_prompt() (lib/prompt.py)                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│  LLM 层      generate_plan() (lib/llm.py)                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│  输出层      _append_plan_to_file() / return (lib/llm.py)        │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 各层职责与实现

| 层 | 文件 | 职责 | 主要函数/常量 |
|----|------|------|---------------|
| 接入层 | `main.py` | CLI 入口，argparse 解析，调用 generate_plan | `main()` |
| 接入层 | `backend/app.py` | HTTP API，接收 JSON 请求，调用 generate_plan，返回 JSON | `POST /api/generate-plan` |
| 前端层 | `frontend/` | Web UI：表单、API 调用、行程展示，响应式适配手机 | `index.html`, `app.js` |
| 输入层 | `src/types.py` | 定义用户输入模型，校验合法性 | `UserInput`, `VALID_*` |
| 上下文层 | `src/destinations/new_zealand.py` | 根据目的地参数生成 prompt 上下文 | `get_context(landing_city, region, month)` |
| Prompt 层 | `src/lib/prompt.py` | 组装 system prompt 与 user prompt | `SYSTEM_PROMPT`, `build_user_prompt()` |
| LLM 层 | `src/lib/llm.py` | 调用 LLM、解析 JSON、校验、重试、输出 | `generate_plan(user_input)` |
| 校验层 | `src/lib/validator.py` | 校验行程输出符合 OUTPUT_FORMAT_SPEC | `validate_plan(result)` |
| 格式化层 | `src/lib/formatter.py` | 将 plan 转为可读文本 | `format_plan_readable(plan)` |
| 输出层 | `src/lib/llm.py` | 结果持久化（JSON→output_plan.json，可读→output_plan.txt） | `_append_plan_to_file(plan)` |

---

## 五、模块详解

### 5.1 输入层 `src/types.py`

**UserInput 必填字段：**

| 字段 | 类型 | 校验 |
|------|------|------|
| landing_city | str | `VALID_LANDING_CITIES` |
| region | str | `VALID_REGIONS` |
| month | int | 1–12 |
| days | int | 1–100 |
| travelers | int | 1–5 |

**UserInput 可选字段：**

| 字段 | 类型 | 默认 |
|------|------|------|
| landing_time | str | "" |
| departure_time | str | "" |
| styles | list[str] \| None | None（最多 5 个） |
| budget_level | str | "" |
| must_see | str | "" |

**常量：**

- `VALID_LANDING_CITIES`: ("奥克兰", "基督城")
- `VALID_REGIONS`: ("北岛", "南岛", "南北岛都玩")
- `VALID_TIME_SLOTS`: ("早上", "下午", "傍晚", "深夜")
- `VALID_BUDGET_LEVELS`: ("经济实惠", "舒适享受")
- `VALID_STYLES`: ("自然风光", "户外冒险", "城市探索", "文化体验", "美食之旅")

### 5.2 上下文层 `src/destinations/new_zealand.py`

**接口：**

```python
def get_context(landing_city: str, region: str, month: int) -> str
```

**输出结构：** 多段文本，包含：

- 【城市背景】
- 【区域特点】
- 【月份季节】{month}月
- 【通用须知】

**依赖：** 仅从 `src.types` 复用 `VALID_*` 常量（供 __all__ 导出）

### 5.3 Prompt 层 `src/lib/prompt.py`

**常量：**

- `SYSTEM_PROMPT`: 定义 LLM 角色与 JSON 输出要求

**接口：**

```python
def build_user_prompt(user_input: UserInput, context: str) -> str
```

**输出：** 包含【目的地背景】和【用户需求】的完整 user prompt 字符串

### 5.4 LLM 层 `src/lib/llm.py`

**外部依赖：**

- `DEEPSEEK_API_KEY`（.env）
- `OpenAI` 兼容 API（base_url: https://api.deepseek.com）
- 模型：`deepseek-chat`

**接口：**

```python
def generate_plan(user_input: UserInput) -> dict
```

**流程：**

1. 调用 `get_context()` 获取上下文
2. 调用 `build_user_prompt()` 生成 user prompt
3. 发送 `[system, user]` 消息到 LLM
4. 解析返回的 JSON；若失败则附加重试 hint 再调一次
5. 调用 `validate_plan(result)` 校验输出结构；失败则抛出异常，不写入文件
6. 调用 `_append_plan_to_file(result)`：JSON 追加到 `output_plan.json`，可读文本（经 `format_plan_readable`）追加到 `output_plan.txt`
7. 返回 `result` dict

**内部函数：**

- `_append_plan_to_file(plan: dict) -> None`: 将 plan 追加写入项目根目录；JSON 写入 `output_plan.json`，可读文本（经 `format_plan_readable`）写入 `output_plan.txt`；格式为分隔线 + 时间戳 + 内容

### 5.5 校验层 `src/lib/validator.py`

**接口：**

```python
def validate_plan(result: dict) -> None
```

**职责**：按 `OUTPUT_FORMAT_SPEC.md` 校验 `result` 的顶层（title、plan、days、tips）、单日（day、morning、afternoon、evening）、时段（transport、sights、activities、accommodation）结构。校验失败时抛出 `ValueError`，含字段路径及错误原因。`llm.py` 在 `json.loads` 成功后、`_append_plan_to_file` 前调用；校验失败则不写入文件。

### 5.6 格式化层 `src/lib/formatter.py`

**接口：**

```python
def format_plan_readable(plan: dict) -> str
```

**职责**：将 plan dict 转为可读文本，包含标题、总览、按天行程（上午/下午/晚上，每段含 transport、sights、activities、accommodation）、tips。按 `OUTPUT_FORMAT_SPEC.md` 结构组织。

**依赖**：无项目内依赖。

### 5.7 CLI 入口 `main.py`

**用法**：`python main.py -l 奥克兰 -r 南岛 -m 3 -d 7 -t 2 [可选参数]`

**必填参数**：`-l/--landing_city`、`-r/--region`、`-m/--month`、`-d/--days`、`-t/--travelers`  
**可选参数**：`--landing_time`、`--departure_time`、`--styles`（逗号分隔）、`--budget_level`、`--must_see`

**流程**：解析参数 → 构造 `UserInput`（复用 `types.UserInput` 做校验）→ 调用 `generate_plan()` → 成功时输出「已保存到 output_plan.json、output_plan.txt」，失败时输出错误信息

### 5.9 API 层 `backend/app.py`

**技术栈**：FastAPI（与现有 Python 后端一致，支持异步、自动 OpenAPI 文档）

**接口**：`POST /api/generate-plan`

**请求体**（JSON，与 INPUT_PARAMS_SPEC 对应）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| landing_city | string | 是 | 奥克兰 / 基督城 |
| region | string | 是 | 北岛 / 南岛 / 南北岛都玩 |
| month | int | 是 | 1–12 |
| days | int | 是 | 1–100 |
| travelers | int | 是 | 1–5 |
| landing_time | string | 否 | 早上/下午/傍晚/深夜，默认 "" |
| departure_time | string | 否 | 同上，默认 "" |
| styles | string[] | 否 | 最多 5 个，默认 [] |
| budget_level | string | 否 | 经济实惠/舒适享受，默认 "" |
| must_see | string | 否 | 自由文本，默认 "" |

**响应体**（200 OK）：按 OUTPUT_FORMAT_SPEC 的 JSON（title、plan、days、tips）

**错误处理**：

| 场景 | HTTP 状态码 | 响应体 |
|------|-------------|--------|
| 参数校验失败（UserInput 抛出 ValueError） | 400 Bad Request | `{ "error": "错误信息" }` |
| LLM 调用失败或解析失败 | 500 Internal Server Error | `{ "error": "错误信息" }` |

**集成方式**：API 路由解析请求体 → 构造 `UserInput`（复用 `types.UserInput`）→ 调用 `src.lib.llm.generate_plan(user_input)` → 返回 result 或错误 JSON。不修改 generate_plan 内部逻辑，仅作为 HTTP 入口。

**部署说明**：开发时前后端可分离（不同端口），API 需配置 CORS；生产可由后端托管 `frontend/` 静态文件实现同源。

### 5.10 Web 前端 `frontend/`

**技术选型**：纯 HTML + CSS + JavaScript（无构建工具），便于 MVP 快速迭代；通过 fetch 调用 API。

**页面结构**：单页应用
- **表单区**：落地城市、游览区域、月份、天数、人数（必填）；落地/离程时间、旅行风格、预算、必去清单（选填）。选项与 INPUT_PARAMS_SPEC 一致。
- **结果区**：提交后显示 loading，成功后展示行程（标题、总览、按天、tips）；可复用 formatter 的可读结构或直接渲染 days 的 morning/afternoon/evening。

**响应式**：CSS 媒体查询，移动端优先（min-width 断点）；适配手机浏览器及小红书链接打开场景。

**与 API 的调用**：`fetch("POST", "/api/generate-plan", { body: JSON.stringify(formData) })`，Content-Type: application/json；成功后渲染返回的 JSON。

### 5.11 输出规范

输出格式以 `OUTPUT_FORMAT_SPEC.md` 为准。`prompt.py` 的 `SYSTEM_PROMPT` 已按规范更新，约束 LLM 返回完整的 `title`、`plan`、`days[]`、`tips[]` 及单日、时段结构（morning/afternoon/evening 各含 transport、sights、activities、accommodation）。`llm.py` 的 `_append_plan_to_file` 与 JSON 解析已兼容该结构。

---

## 六、数据流

### 6.1 CLI 入口到 generate_plan

```
main.py (CLI)
    │
    ├── argparse 解析参数（-l/-r/-m/-d/-t 必填，--landing_time 等可选）
    │
    ├── UserInput(...)   # 复用 types.UserInput，校验失败则退出
    │
    └── generate_plan(user_input)  ──► 成功：输出「已保存到 output_plan.json、output_plan.txt」；失败：输出错误
```

### 6.2 generate_plan 内部数据流

```
UserInput
    │
    ├──► get_context(landing_city, region, month)
    │         │
    │         └──► context: str
    │
    └──► build_user_prompt(user_input, context)
              │
              └──► user_prompt: str
                        │
                        ▼
              [SYSTEM_PROMPT, user_prompt]  ─► messages
                        │
                        ▼
              DeepSeek API  ─► raw: str
                        │
                        ▼
              json.loads(raw) [含重试]  ─► result: dict
                        │
                        ├──► validate_plan(result)  ─► 校验通过
                        │
                        ├──► _append_plan_to_file(result)
                        │         │
                        │         ├──► 写 JSON 到 output_plan.json（追加）
                        │         │
                        │         ├──► format_plan_readable(plan)  ─► 可读文本
                        │         │
                        │         └──► 写可读文本到 output_plan.txt（追加）
                        │
                        └──► return result
```

### 6.3 Web 入口到 generate_plan

```
浏览器 (frontend/index.html)
    │
    ├── 用户填写表单
    │
    ├── fetch POST /api/generate-plan { landing_city, region, month, ... }
    │
    └── backend/app.py
            │
            ├── 解析 JSON 请求体
            │
            ├── UserInput(...)   # 校验失败 → 400
            │
            ├── generate_plan(user_input)   # 失败 → 500
            │
            └── 返回 200 + plan JSON
                    │
                    └── 前端渲染行程（标题、总览、按天、tips）
```

---

## 七、依赖关系

```
types.py          (无项目内依赖)
    ▲
    │
new_zealand.py    ◄── types (仅常量)
    ▲
    │
prompt.py         ◄── types
    ▲
    │
llm.py            ◄── types, new_zealand, prompt, validator, formatter
    ▲
    │
main.py           ◄── types, llm
backend/app.py    ◄── types, llm
    ▲
    │
frontend/         ──► 通过 HTTP 调用 backend (fetch)
```

**说明：** `llm.py` 直接 import `new_zealand.get_context`，目前无目的地路由；MVP2 新增目的地时需在此增加路由逻辑。`frontend/` 与 `backend/` 通过 HTTP 解耦，前端可单独部署或由后端静态托管。

---

## 八、配置

| 配置项 | 来源 | 说明 |
|--------|------|------|
| DEEPSEEK_API_KEY | .env | DeepSeek API 密钥 |
| model | 代码 | `deepseek-chat` |
| base_url | 代码 | `https://api.deepseek.com` |

---

## 九、架构变更记录

| 日期 | 变更内容 |
|------|----------|
| 2026-02-22 | 初始版本：MVP1 四层架构（输入 / 上下文 / Prompt / LLM+输出） |
| 2026-02-22 | prompt.py SYSTEM_PROMPT 按 OUTPUT_FORMAT_SPEC 更新，约束完整输出结构（title/plan/days/tips 及单日、时段字段） |
| 2026-02-22 | 新增 main.py CLI 入口、src/lib/validator.py 输出结构校验，llm.py 接入校验 |
| 2026-02-22 | #9 可读性输出：formatter.py、双文件 output_plan.json/.txt、main.py 简化输出 |
| 2026-02-22 | Web 前端 + HTTP API 架构设计：backend/app.py (FastAPI)、frontend/ 纯 HTML/CSS/JS、POST /api/generate-plan、响应式适配小红书 |
| 2026-02-22 | #10 实现：backend/app.py、frontend/index.html+app.js+style.css、双文件托管、CORS、启动说明见 README |

---

## 十、后续演进（非 MVP1）

- **MVP2 多目的地**：引入 `destination` 字段，增加 `get_context_for(destination, ...)` 路由，按目的地注册 `get_context` 实现
- **输出格式对齐**：已完成，`prompt.py` 已按 `OUTPUT_FORMAT_SPEC.md` 约束输出
- **Web 与 API**：已完成，`backend/app.py` 与 `frontend/` 已实现
- **输出策略**：将 `_append_plan_to_file` 抽象为可配置的输出策略
