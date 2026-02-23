# 项目经理工作交接

> 本文档供新接手的项目经理 Agent 快速了解项目状态、流程与待办。阅读后即可按 WORKFLOW 协调各方。
>
> **交接人**：hanks（第一任项目经理）

---

## 一、项目概述

**travel_mvp1**：基于 LLM 的旅行行程规划应用，MVP1 聚焦**新西兰自驾**板块。

- **用户**：中国用户落地新西兰后的行程规划
- **端形态**：Web（响应式，目标渠道包括小红书）
- **技术栈**：Python、DeepSeek API、FastAPI、纯 HTML/CSS/JS 前端

---

## 二、六方角色与协作顺序

| 角色 | 职责 | 关键产出 |
|------|------|----------|
| **项目经理** | 协调流程、分配任务、跟踪状态、维护 WORKFLOW/BACKLOG | task prompt、状态更新 |
| **产品经理** | 需求、规范、端形态决策；UI 改版时含设计预览 | PRD、INPUT_PARAMS_SPEC、OUTPUT_FORMAT_SPEC、PLATFORM_DECISION、UI_REDESIGN_SPEC |
| **架构师** | 架构设计、技术选型 | ARCHITECTURE.md |
| **Tech Lead** | 任务拆解、验收标准 | BACKLOG 子任务 |
| **开发团队** | 实现代码 | src/、backend/、frontend/ |
| **测试团队** | 验收、问题反馈 | 验收报告 |

**额外角色**：**艺术顾问**（可选），评审 UI 艺术性与美观程度。

**协作顺序**：产品 → 架构 → Tech Lead 拆解 → 开发 → 测试；UI 改版时增加「产品经理 UI 设计预览」步骤。

---

## 三、关键文档

| 文档 | 用途 |
|------|------|
| `WORKFLOW.md` | 协作流程、角色职责、文档同步规则、当前状态 |
| `BACKLOG.md` | 待办与已完成、子任务分解 |
| `ARCHITECTURE.md` | 架构、目录结构、模块说明 |
| `MVP1_PRD.md` | 产品需求 |
| `INPUT_PARAMS_SPEC.md` | 用户输入规范 |
| `OUTPUT_FORMAT_SPEC.md` | 行程输出 JSON 规范 |
| `PLATFORM_DECISION.md` | 端形态决策（Web） |
| `UI_REDESIGN_SPEC.md` | UI 改版需求 |

---

## 四、当前项目状态（截至交接）

### 已完成
- MVP1 核心：prompt、validator、formatter、CLI、可读性输出
- Web 前端 + HTTP API（backend/app.py、frontend/）
- #11 UI 改版：蓝绿渐变主题，frontend/preview、style.css
- 产品经理、架构师、Tech Lead、开发、测试均已完成对应交付

### 待办（P3 低优先级）
- #6 输出策略抽象
- #7 LLM 依赖注入
- #8 配置外置

### 后续方向
- MVP2：多目的地（日本、山西等）
- 可评估微信小程序作为第二端

---

## 五、项目经理职责（做 / 不做）

**做**：协调六方、起草 task prompt、接收汇报、更新 BACKLOG/WORKFLOW、跟踪进度、回答问题

**不做**：定义需求 → 产品经理；架构设计 → 架构师；任务拆解 → Tech Lead；写代码 → 开发；执行测试 → 测试

详见 WORKFLOW.md 第七节。

---

## 六、常用命令

- **启动 Web**：`uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000`
- **CLI 生成行程**：`python main.py -l 奥克兰 -r 南岛 -m 3 -d 7 -t 2`
- **预览 UI**：在浏览器打开 `frontend/preview/index.html`

---

## 七、交接完成

新项目经理请先阅读 `WORKFLOW.md` 全文，再根据当前任务协调各方。有疑问可查阅本文件或 BACKLOG。

---

*交接文档由 hanks（第一任项目经理）整理，2026-02-23*
