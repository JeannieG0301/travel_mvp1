# 待办事项 Backlog

> 按优先级排序，完成事项可移至「已完成」或打勾。**更新时保持本文件同步。**

---

## P0 - 必须完成

| # | 事项 | 来源 | 状态 |
|---|------|------|------|
| 1 | 更新 `src/lib/prompt.py`：SYSTEM_PROMPT 约束完整输出结构（title, plan, days, tips 及单日/时段字段） | OUTPUT_FORMAT_SPEC | ✅ 已完成 |

**#1 分解：**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 1.1 | 在 SYSTEM_PROMPT 中声明顶层结构（title, plan, days, tips 四字段及类型） | 顶层结构约束清晰 |
| 1.2 | 在 SYSTEM_PROMPT 中声明单日结构 days[i]（day, morning, afternoon, evening） | 单日结构约束清晰 |
| 1.3 | 在 SYSTEM_PROMPT 中声明时段结构（morning/afternoon/evening 各含 transport, sights, activities, accommodation） | 时段结构约束清晰 |
| 1.4 | 在 SYSTEM_PROMPT 中补充业务约定（交通格式、不含餐饮、tips 内容等） | 与 OUTPUT_FORMAT_SPEC 一致 |
| 1.5 | 在 SYSTEM_PROMPT 中提供完整 JSON 示例 | 示例可直接作为格式参考 |
| 1.6 | 验证 llm.py 与新结构兼容（_append_plan_to_file、json 解析） | 无需改动或完成适配 |

---

## P1 - 高优先级

| # | 事项 | 来源 | 状态 |
|---|------|------|------|
| 2 | 更新 OUTPUT_FORMAT_SPEC.md 第六节「实现状态」 | 文档同步 | ✅ 已完成 |
| 3 | 更新 ARCHITECTURE.md：5.5 节、架构变更记录 | 文档同步 | ✅ 已完成 |

---

## P2 - 中优先级

| # | 事项 | 来源 | 状态 |
|---|------|------|------|
| 4 | 增加 CLI 入口（main.py 或 cli.py） | ARCHITECTURE 后续演进 | ✅ 已完成 |
| 5 | 增加输出结构校验（解析后校验 title/plan/days/tips 及 days 结构） | 可靠性 | ✅ 已完成 |
| 9 | 可读性输出：formatter 模块 + 双文件输出（JSON + 可读 txt） | 可维护性/扩展性 | ✅ 已完成 |

**#4 分解：**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 4.1 | 创建 main.py 或 cli.py 入口文件，使用 argparse 或 click | 可执行 `python main.py --help` 有输出 |
| 4.2 | 实现必填参数解析：landing_city, region, month, days, travelers | 命令行可传入上述 5 项 |
| 4.3 | 实现可选参数解析：landing_time, departure_time, styles, budget_level, must_see | 命令行可传入可选参数 |
| 4.4 | 参数校验与 UserInput 构造（复用 types.UserInput） | 非法参数抛出明确错误 |
| 4.5 | 调用 generate_plan 并输出结果（打印 JSON 或写入提示） | 成功时输出行程，失败时有错误提示 |
| 4.6 | 支持 --help 显示用法与参数说明 | help 文案含所有参数及示例 |

**#5 分解：**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 5.1 | 定义顶层校验：result 含 title(str)、plan(str)、days(list)、tips(list/可选) 且类型正确 | 顶层缺失或类型错误时校验失败 |
| 5.2 | 定义单日校验：days[i] 含 day(number)、morning(object)、afternoon(object)、evening(object) | 单日结构缺失时校验失败 |
| 5.3 | 定义时段校验：morning/afternoon/evening 各含 transport、sights、activities、accommodation(string) | 时段字段缺失或非 string 时校验失败 |
| 5.4 | 在 llm.py 中 json.loads 成功后、_append_plan_to_file 前接入校验 | 校验通过才写入文件并返回 |
| 5.5 | 校验失败时抛出明确异常（含字段路径及错误原因），不写入 output_plan.txt | 异常信息可定位问题，且未写入无效数据 |

**#9 分解：**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 9.1 | 新建 src/lib/formatter.py，实现 format_plan_readable(plan) -> str | 将 plan dict 转为可读文本（标题、总览、按天、上午/下午/晚上、tips） |
| 9.2 | 输出层：JSON 追加到 output_plan.json，可读文本追加到 output_plan.txt | 双文件分离，格式符合 OUTPUT_FORMAT_SPEC |
| 9.3 | 原 output_plan.txt 若存 JSON，迁移或兼容处理；main.py 终端仅输出「已保存到 xxx」 | 不向终端输出行程内容 |

---

## P2 - 前端与 API

| # | 事项 | 来源 | 状态 |
|---|------|------|------|
| 10 | Web 前端 + HTTP API | PLATFORM_DECISION | ✅ 已完成 |

**#10 架构设计**（已由架构师完成）：
- API：POST /api/generate-plan，FastAPI，backend/app.py
- 前端：纯 HTML/CSS/JS，frontend/，单页、响应式

**#10 分解：**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 10.1 | 创建 backend/app.py，初始化 FastAPI 应用并配置 CORS（允许跨域） | 执行 `uvicorn backend.app:app` 可启动服务，浏览器可跨域请求 |
| 10.2 | 实现 POST /api/generate-plan：解析 JSON 请求体、构造 UserInput、调用 generate_plan、返回 200 + plan JSON | 请求体符合 INPUT_PARAMS_SPEC 时返回行程 JSON，字段符合 OUTPUT_FORMAT_SPEC |
| 10.3 | 错误处理：UserInput 校验失败返回 400 + `{"error":"..."}`；LLM 调用/解析失败返回 500 + `{"error":"..."}` | 非法参数或 LLM 异常时返回对应状态码和错误 JSON |
| 10.4 | 在 requirements.txt 中增加 fastapi、uvicorn，并在 README 或文档中说明 backend 启动命令 | `pip install -r requirements.txt` 后可用 uvicorn 启动 API |
| 10.5 | 创建 frontend/index.html：表单含必填 5 项（landing_city、region、month、days、travelers）及选填 5 项（landing_time、departure_time、styles、budget_level、must_see），选项与 INPUT_PARAMS_SPEC 一致 | 打开 index.html 可见完整表单，下拉/选项正确 |
| 10.6 | 创建 frontend/app.js：表单 submit 时收集数据、fetch POST /api/generate-plan、显示 loading 状态、失败时展示错误信息 | 提交后显示 loading，成功/失败均有对应 UI 反馈 |
| 10.7 | 行程展示区：成功返回后渲染 title、plan、days（按天展示 morning/afternoon/evening 的 transport、sights、activities、accommodation）、tips | 返回的 plan JSON 能正确展示为可读行程结构 |
| 10.8 | 创建 frontend/style.css：移动端优先响应式样式，媒体查询适配手机与桌面 | 手机端与桌面端布局正常，表单与结果区可用 |
| 10.9 | 开发环境集成：后端托管 frontend 静态文件，或提供前后端分离的启动说明（API 端口 + 前端静态服务）；CORS/API 地址可配置 | 按文档启动后，前端可成功调用 API 并展示行程 |

---

## P2 - UI 改版（待拆解）

| # | 事项 | 来源 | 状态 |
|---|------|------|------|
| 11 | Web UI 改版 | UI_REDESIGN_SPEC | ✅ 已完成 |

**#11 分解：**

**P0 - 必须完成**

| 子任务 | 改版点 | 具体内容 | 验收 |
|--------|--------|----------|------|
| 11.1 | 配色 | 主色改为新西兰/自然系（如 `#2d6a4f` 或 `#0077b6`），辅色米白/暖灰背景（如 `#f8f6f3`），深色文字可读；去除 `#2563eb` 及蓝系残留 | 全页搜索无 `#2563eb`、`#1d4ed8`；主色、背景符合 spec |
| 11.2 | 字体 | 标题使用思源宋体、霞鹜文楷或系统衬线/手写感字体（`font-family` 引入或 `serif` 替代），正文保持无衬线可读 | 标题与正文字体可区分，正文易读 |
| 11.3 | 头部/品牌区 | 增加 slogan 或副标题强化「新西兰自驾」定位；加大标题字号、调整 header 间距，形成清晰品牌区 | header 含 slogan/副标题，字号与间距明显优于正文 |

**P1 - 高优先级**

| 子任务 | 改版点 | 具体内容 | 验收 |
|--------|--------|----------|------|
| 11.4 | 表单卡片 | 卡片增加圆角、柔和阴影，与背景区分明显；必填区与选填区（details/summary）视觉分隔更清晰，summary 样式柔和 | 表单卡片与背景层次分明；必填/选填分隔明显 |
| 11.5 | 按钮与输入控件 | 主按钮使用新主色、圆角与整体一致；select/input/textarea 边框颜色与主色呼应，hover 态有轻微反馈 | 主按钮、输入控件风格统一，hover 有可见反馈 |
| 11.6 | 结果区：行程卡片 | 每天卡片有明确标题栏（「第 X 天」+ 当日主题）；上午/下午/晚上用标签或小标题区分；交通/景点/活动/住宿分行或小图标增强可读 | 按天卡片有标题与时段标签，各字段易扫读 |

**P2 - 中优先级**

| 子任务 | 改版点 | 具体内容 | 验收 |
|--------|--------|----------|------|
| 11.7 | 结果区：总览与 tips | 行程总览用 `blockquote` 或高亮样式突出；tips 用列表或卡片式呈现，每条可读性更好 | 总览与 tips 视觉突出，易于阅读 |
| 11.8 | 加载与错误态 | 加载 spinner 使用新主色；错误提示卡片样式与整体一致，不突兀 | loading、error 视觉与主色/风格一致 |

**通用验收（11.9）**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 11.9 | 响应式保持 | 改版后 mobile（375px）、desktop（640px+）布局正常，无错位、溢出；与 UI_REDESIGN_SPEC 第五条对应 |

---

## P2 - 上线部署

| # | 事项 | 来源 | 状态 |
|---|------|------|------|
| 12 | 上线部署：供朋友测试 | 项目经理分配 | 配置完成，待执行平台部署 |

**#12 说明**：配置与文档已就绪。待人工执行：1）推送到 GitHub；2）在 Render 或 Railway 创建 Web Service；3）添加 DEEPSEEK_API_KEY；4）部署成功后汇报公网 URL。详见 DEPLOY.md「开发团队执行部署」。

---

## P3 - 低优先级 / MVP2 或后续迭代

| # | 事项 | 来源 | 状态 |
|---|------|------|------|
| 6 | 输出策略抽象：将 _append_plan_to_file 抽象为可配置 | ARCHITECTURE | 待办 |
| 7 | LLM 依赖注入（便于测试 mock） | ARCHITECTURE | 待办 |
| 8 | 配置外置：model、base_url 等移至配置 | 可维护性 | 待办 |

---

## 已完成

| 完成日期 | 事项 |
|----------|------|
| 2026-02-22 | #1 更新 prompt.py SYSTEM_PROMPT 约束完整输出结构（1.1–1.6 子任务） |
| 2026-02-22 | #2 更新 OUTPUT_FORMAT_SPEC.md 第六节「实现状态」 |
| 2026-02-22 | #3 更新 ARCHITECTURE.md 5.5 节及架构变更记录 |
| 2026-02-22 | 测试团队执行输出结构验证测试，通过 |
| 2026-02-22 | #4 CLI 入口 main.py（argparse、UserInput、generate_plan） |
| 2026-02-22 | #5 输出结构校验 src/lib/validator.py，llm.py 接入 |
| 2026-02-22 | #9 可读性输出：formatter.py、双文件（output_plan.json + output_plan.txt） |
| 2026-02-22 | 测试团队验收 #9 通过 |
| 2026-02-22 | 架构师更新 ARCHITECTURE，与 #9 一致 |
| 2026-02-22 | 产品经理完成端形态决策（Web）、PLATFORM_DECISION.md |
| 2026-02-22 | 架构师完成 Web + API 架构设计，已更新 ARCHITECTURE |
| 2026-02-22 | Tech Lead 完成 #10 拆解（10.1–10.9），已录入 BACKLOG |
| 2026-02-22 | #10 Web 前端 + HTTP API（backend/app.py、frontend/、POST /api/generate-plan） |
| 2026-02-22 | 测试团队验收 #10 通过 |
| 2026-02-22 | 产品经理完成 UI 改版需求定义，输出 UI_REDESIGN_SPEC.md |
| 2026-02-22 | Tech Lead 完成 #11 拆解（11.1–11.9），已录入 BACKLOG |
| 2026-02-23 | #11 Web UI 改版（蓝绿渐变主题、frontend/preview、style.css） |
| 2026-02-22 | #9 可读性输出：formatter.py、双文件 output_plan.json/.txt、main.py 简化输出 |
| 2026-02-22 | #10 Web 前端 + HTTP API：backend/app.py、frontend/、POST /api/generate-plan、响应式 UI |
| 2026-02-22 | #11 Web UI 改版：新西兰/自然系配色、Noto Serif SC 标题、slogan、表单/结果区样式优化 |
| 2026-02-23 | #12 上线部署配置：Procfile、render.yaml、runtime.txt、DEPLOY.md（开发团队） |
| 2026-02-23 | #12 DEPLOY.md 更新：「开发团队执行部署」章节、前置条件、Render 速查表（开发团队） |

---

## 备注

- **MVP1 收尾**：P0–P2 已完成，MVP1 功能范围已交付（2026-02-22）
- **P3**：低优先级，留待 MVP2 或后续迭代
- **MVP2**：多目的地（日本、山西等）相关事项另行列入
