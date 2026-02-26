# 待办事项 Backlog

> 按优先级排序，完成事项可移至「已完成」或打勾。**更新时保持本文件同步。**

---

## P0 - 必须完成

| # | 事项 | 来源 | 状态 |
|---|------|------|------|
| 13 | 提升 DeepSeek 调用稳定性（超时、重试、错误提示、JSON 合法性） | POC 已知问题 | ✅ 已完成（第二轮真实环境压测 20/20 成功，见 docs/reports/DeepSeek_压测结果_真实环境.md） |
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

**#13 分解：**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 13.1 | 输出「DeepSeek 调用稳定性技术方案」文档（docs/DEEPSEEK_STABILITY_PLAN.md），覆盖超时、重试、错误分类、日志与指标 | 文档存在且内容覆盖任务说明中的四大点，并与开发/测试任务文档对齐 |
| 13.2 | 在 llm 层实现统一 DeepSeek 调用封装（如 call_deepseek），支持显式超时配置与可恢复错误的有限重试 | 代码中不再直接散落调用 DeepSeek；可配置超时与重试次数，网络/超时错误在重试上限内自动重试 |
| 13.3 | 定义标准化错误类与错误码（NETWORK_ERROR/TIMEOUT/DEEPSEEK_ERROR/JSON_DECODE_ERROR/VALIDATION_ERROR/UNKNOWN_ERROR），并在 CLI 与 API 中返回统一错误结构 | backend 与 main.py 可根据错误码输出一致的 HTTP 状态码与中文错误提示，区分「可重试」与「稍后再试」场景 |
| 13.4 | 为 generate_plan 链路增加结构化日志（包含请求摘要、开始/结束时间、耗时、attempts、success、error_code 等字段） | 本地运行时可在日志中看到上述字段，失败场景下 error_code 与错误信息清晰可见 |
| 13.5 | 编写压测/稳定性脚本（如 scripts/stress_test_generate_plan.py），支持配置调用次数与并发度，输出成功率、错误类型统计与平均/p95 耗时 | 脚本可在 README 或脚本内帮助说明下执行一轮压测并输出预期统计信息 |
| 13.6 | 测试团队基于压测脚本完成至少一轮稳定性测试，并产出结构化「DeepSeek 稳定性报告」与通过/不通过结论 | 存在测试报告文档（如 docs/reports/DeepSeek_稳定性报告.md），包含成功率、错误分布、耗时指标与清晰的结论 |
| 13.7 | 优化 DeepSeekError 错误分类与日志字段，区分 NETWORK_ERROR/TIMEOUT/DEEPSEEK_ERROR 与解析/校验错误 | call_deepseek 基于异常类型/HTTP 状态码分类；日志包含 http_status、ds_error_body、ds_trace_id 等字段，CLI/API/前端文案能区分「网络问题」与「服务/配置问题」 |

---

## P1 - 高优先级

| # | 事项 | 来源 | 状态 |
|---|------|------|------|
| 19 | 行程质量与输出可读性优化 | ROADMAP P1-1、MVP1 体感 | ✅ 已完成（测试验收 3/3 通过，见 docs/reports/2026-02-26-测试团队.md） |
| 2 | 更新 OUTPUT_FORMAT_SPEC.md 第六节「实现状态」 | 文档同步 | ✅ 已完成 |
| 3 | 更新 ARCHITECTURE.md：5.5 节、架构变更记录 | 文档同步 | ✅ 已完成 |

**#19 分解：**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 19.1 | 提示词优化：在 SYSTEM_PROMPT 中强化行程可读性要求（标题简洁、总览概括、按天逻辑清晰、交通/景点/活动表述具体可执行） | 产品/开发评审 prompt 变更；抽样生成结果可读性达标 |
| 19.2 | 前端展示优化：行程结果区标题/总览/按天/ tips 的排版与层次（字号、间距、分段），与 formatter 可读格式对齐 | 用户端展示与 output_plan.txt 可读性一致，易扫读 |
| 19.3 | formatter 与 OUTPUT_FORMAT_SPEC 复核：确保按天、上午/下午/晚上、交通/景点/活动/住宿的呈现无遗漏、无错位 | 导出/分享内容与规范一致，无格式错乱 |

**说明**：与 #17 并列为 MVP1 最高优先级；先做 #17（含体感三块 17.4～17.6）再做 #19，或开发按 docs/tasks 安排并行。任务已写入 docs/tasks/2026-02-26-开发团队.md、测试团队.md。

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
| 12 | 上线部署：供朋友测试 | 项目经理分配 | ✅ 已完成 https://travel-mvp1.onrender.com/ |

**#12 说明**：已于 2026-02-24 部署上线，公网 URL：https://travel-mvp1.onrender.com/

---

## P1 - 生成行程超时与重试体感（产品经理 2026-02-26 评估结论）

来源：`docs/reports/2026-02-26-产品经理.md`（用户体感：约 2 分钟报错「网络或服务暂时不可用」；评估结论为超时偏短 + TIMEOUT 文案 + 重试按钮）。

| # | 事项 | 来源 | 状态 | 执行 |
|---|------|------|------|------|
| 20 | 生成行程超时与重试体感：调大超时、TIMEOUT 文案、重试按钮 | 产品经理 2026-02-26 评估 | ✅ 已完成 | 汇报见 docs/reports/2026-02-26-开发团队-超时重试.md；Render 约 30s 上限结论已记录，建议免费版设 DEEPSEEK_TIMEOUT_SECONDS=25 |

**#20 分解：**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 20.1 | **调大「生成行程」超时**：将 DeepSeek 单次超时调为 90～120 秒（环境变量 `DEEPSEEK_TIMEOUT_SECONDS` 或接口级配置）；可选将重试次数减为 1。**先确认 Render 请求超时上限**：若免费 tier 为 30s 会杀请求，需架构/开发确认方案（升级或异步等）并与后端超时对齐。 | 配置生效后单次尝试可覆盖「冷启动+生成」；Render 超时结论已记录 |
| 20.2 | **TIMEOUT 专用文案**：前端对 `code === 'TIMEOUT'` 展示「生成超时，请点击重试」类提示（与「上游服务暂时不可用，请稍后再试」区分）。 | 用户看到超时时为「可重试」类文案 |
| 20.3 | **失败态「重试」按钮**：错误展示区增加「重试」按钮，点击后用**上次提交参数**再次请求 `/api/generate-plan`，不刷新页面、不丢失表单。 | 失败后一点重试即可再次生成，无需重新填表 |

---

## P2 - 体验与可达性优化（不阻塞 POC）

以下三项为 POC 体感反馈的后续可选优化；已知限制已在 ROADMAP「POC 已知限制」与 DEPLOY/推广方案中写明，**不阻塞 POC 收尾**。有预算或需求时由产品/运维/开发按需排期。

| # | 事项 | 来源 | 状态 | 可分配 |
|---|------|------|------|--------|
| 14 | Render 加载慢：升级实例或常驻，缩短冷启动 | POC 已知限制 L1 | 待办 | 运维/项目经理（预算决策） |
| 15 | 国内可达性：国内部署或 OpenClaw 等通道，减少拦截 | POC 已知限制 L2、推广方案 4.4 | 待办 | 运维/开发；产品可补充话术 |
| 16 | 生成行程体感：按钮/等待文案加「约需 1 分钟内」；可选提示词精简、流式输出或分步进度 | POC 已知限制 L3 | 待办 | 产品（文案）、开发（流式/进度） |

**说明**：
- **#14**：ROADMAP L1、DEPLOY 已写「首次访问可能需等待约半分钟」；若升级 Render 付费实例或配置常驻即可改善。
- **#15**：DEPLOY 第七、八节已有国内访问说明与香港部署步骤；本项为「正式选型国内节点或 OpenClaw」等方案落地。
- **#16**：压测单次约 42s/p95 95s，主要为 DeepSeek 耗时；先做文案预期管理，再考虑流式/分步进度等体验优化。

---

## MVP1 - 必做方向（已排期）

产品已定稿 MVP1_PRD（目标用户、核心场景、成功指标）；MVP1 仅保留必做 ①，与 ROADMAP、MVP1_PRD 一致。任务已写入 docs/tasks/，按角色分配执行。

| # | 事项 | 来源 | 状态 | 执行 |
|---|------|------|------|------|
| 17 | 体验与可分享（含 CEO 体感三块）：等待文案、导出/分享、首屏提示、生成进度提示、国内用户说明 | MVP1_PRD 必做 ①、CEO 体感反馈 | ✅ 已完成（测试验收 6/6 通过，见 docs/reports/2026-02-26-测试团队.md） | — |

**说明**：#18 目的地扩展已移出 MVP1，留待新西兰行程质量验证后再排，见 P3 / 留待 MVP2。#17 与 #19 并列 MVP1 最高优先级；#14/#15 留待有预算或后续阶段。

**#17 分解：**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 17.1 | 等待文案：生成中展示「约需 1 分钟内，请稍候」（或产品认可的等价文案） | 前端 loading 态可见该文案 |
| 17.2 | 导出 PDF：生成完成后支持一键导出为 PDF，用户可保存/打印 | 导出文件可打开、内容与当前行程一致 |
| 17.3 | 可分享链接：生成完成后可生成只读链接，他人打开可查看该行程 | 链接可访问、内容与生成结果一致；可选：短期持久化（如 7 天） |
| 17.4 | **首屏/冷启动提示**：首屏或落地页增加「首次打开约需 20～30 秒，请稍候」类提示（CEO 体感：打开慢有交代） | 用户首次进入页面可见该提示或等价文案 |
| 17.5 | **生成中阶段提示**：在 17.1 基础上，增加生成中进度/阶段提示（如「正在规划路线…」或简单阶段文案），让等待有反馈 | 生成过程中有至少 1 条阶段/进度类文案轮播或展示 |
| 17.6 | **国内用户说明**：在落地页、关于页或分享话术增加「国内用户说明」——若链接无法打开可尝试换浏览器、关闭安全软件误报、换网络或 VPN；并注明「服务部署在海外，国内访问可能不稳定」 | 用户可在页面或关于/帮助处看到上述说明 |

---

## P3 - 低优先级 / MVP2 或后续迭代

**#18 目的地扩展（已移出 MVP1，留待新西兰行程质量验证后再排）**

| 子任务 | 事项 | 验收 |
|--------|------|------|
| 18.1 | 多目的地架构：前端支持目的地选择（新西兰 + 新目的地）；后端/API 支持 destination 参数并路由到对应 prompt/逻辑 | 架构师评估并更新 ARCHITECTURE；Tech Lead 拆解到开发任务 |
| 18.2 | 新目的地板块输入与 prompt（首选山西）：定义输入参数、专用或可复用 prompt，输出兼容 OUTPUT_FORMAT_SPEC | 新目的地行程可生成，结构符合现有规范或文档化扩展 |
| 18.3 | 前端：目的地选择器、新目的地表单字段与 /api/generate-plan 对接 | 用户可选择新西兰或新目的地并填写对应参数，提交后正确调用 API |
| 18.4 | 后端：POST /api/generate-plan 支持 destination，按目的地调用对应 LLM 逻辑 | 新西兰与新目的地均能返回完整行程 JSON |

---

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
| 2026-02-23 | #12 本地 Git 就绪：git init/add/commit、main 分支、.gitignore、PUSH_TO_GITHUB.md（开发团队）；待项目负责人创建仓库并 push |
| 2026-02-24 | #12 部署上线完成：Render 部署，公网 URL https://travel-mvp1.onrender.com/ |
| 2026-02-25 | #13 提升 DeepSeek 调用稳定性：第二轮真实环境压测 20/20 成功，报告已更新（docs/reports/DeepSeek_压测结果_真实环境.md），状态已关闭 |
| 2026-02-26 | #17 体验与可分享（17.1～17.6，含首屏提示、生成进度提示、国内用户说明）：开发完成，测试验收 6/6 通过 |
| 2026-02-26 | #19 行程质量与输出可读性（19.1～19.3）：开发完成，测试验收 3/3 通过 |

---

## 备注

- **MVP1 收尾**：P0–P2 已完成，MVP1 功能范围已交付（2026-02-22）
- **#12 部署**：已上线，可分享 https://travel-mvp1.onrender.com/ 供朋友测试
- **P3**：低优先级，留待 MVP2 或后续迭代
- **MVP2**：多目的地（日本、山西等）相关事项另行列入
