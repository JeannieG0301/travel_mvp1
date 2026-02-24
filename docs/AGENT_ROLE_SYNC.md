# 各 Agent 角色同步指南

> 角色分工变更后，需让各 Cursor Agent 知晓。按下列清单逐项执行。

---

## 需同步的 Agent 清单

| 序号 | Agent 名称 | 同步状态 |
|------|------------|----------|
| 1 | 产品经理 | ☑ |
| 2 | UIUX 设计师 | ☑ |
| 3 | 架构师 | ☑ |
| 4 | Tech Lead | ☑ |
| 5 | 测试团队 | ☑ |
| 6 | 后端开发团队 / 开发团队 | ☑ |
| 7 | 项目经理 | ☑ |

---

## 同步方式（任选其一）

### 方式 A：在 Agent 的 Instructions 中引用

若该 Agent 有可编辑的 Instructions，加入：

```
角色定义以 ROLES.md 为准，协作流程见 WORKFLOW.md。七方协作，UI/UX 设计师已独立于产品经理。
```

### 方式 B：在 Agent 对话中粘贴通知

打开该 Agent 的对话，发送以下内容作为首条消息：

---

**【角色分工已更新】**

七方协作，UI/UX 设计师已独立于产品经理。

- **产品经理**：负责需求文档（PRD、INPUT_PARAMS_SPEC、OUTPUT_FORMAT_SPEC、UI_REDESIGN_SPEC），**不再产出 UI 设计稿**
- **UI/UX 设计师**：负责界面设计、交互流程、视觉规范及可预览设计稿

完整角色定义见 `ROLES.md`，协作流程见 `WORKFLOW.md`。

---
