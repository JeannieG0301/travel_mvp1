# 角色变更检查清单

> 当你**新增、删除、修改角色**（职责、产出物、依赖等）时，按此清单逐项检查，避免遗漏同步。

---

## 变更后必做

| 步骤 | 文件/对象 | 动作 | 完成 |
|------|-----------|------|------|
| 1 | `ROLES.md` | 更新角色定义、职责、产出物、依赖 | ☐ |
| 2 | `WORKFLOW.md` | 更新协作流程（阶段顺序、依赖关系、各阶段说明） | ☐ |
| 3 | `PROJECT_CONTEXT.md` | 若存在角色总览表，同步简表 | ☐ |
| 4 | `.cursor/rules/travel-planner-agent.mdc` | 若规则中含角色列表，同步 | ☐ |
| 5 | 各 Cursor Agent | 按 `docs/AGENT_ROLE_SYNC.md` 在各 Agent 中同步（Instructions 或对话粘贴） | ☑ |
| 6 | 项目经理 | 下轮分配任务时，在 task prompt 中说明「角色分工已更新，详见 ROLES.md」 | ☑ |

---

## 说明

- **ROLES.md** 是单一信息源，角色相关变更应优先在此完成
- **WORKFLOW.md** 重点更新：协作流程图、角色表、各阶段详细说明、协作口诀
- **各 Cursor Agent**：若项目使用多个 Agent（产品、UI/UX、架构等），需按 `docs/AGENT_ROLE_SYNC.md` 逐一同步
- 若变更涉及其他文档（如 BACKLOG、ARCHITECTURE），按需补充到本清单
