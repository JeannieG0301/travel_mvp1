# UI 设计修订说明

> 产品经理输出，基于当前预览与规范的偏差进行修订。
>
> 修订日期：2026-02-22

---

## 一、问题识别

| 类别 | 当前状态 | 问题 |
|------|----------|------|
| **配色** | 蓝绿渐变（#0891b2 → #0d9488 → #2d6a4f），背景青绿渐变 | 偏离规范：规范要求主色草地绿或湖蓝二选一、背景米白/暖灰；当前偏冷、蓝绿混用 |
| **渐变使用** | 标题、按钮、卡片头、背景、总览、tips 均为渐变 | 过于花哨，规范未要求渐变，宜用纯色营造氛围 |
| **按钮** | 渐变背景，hover 用 opacity | 反馈感弱，纯色 + hover 加深更直观 |
| **背景** | ecfeff→f0fdf4 青绿渐变 | 偏冷，规范要求米白/暖灰 #f8f6f3 |

---

## 二、修订方向

| 修订项 | 目标效果 |
|--------|----------|
| **配色回归** | 主色用单一草地绿 `#2d6a4f`，背景用米白/暖灰 `#f8f6f3`，去除蓝绿色系 |
| **去除渐变** | 标题、按钮、卡片头、总览、tips 改为纯色，背景改为纯色 |
| **按钮更突出** | 主色纯色背景，hover 时 `#1e4d3a` 加深，增强点击反馈 |
| **保持克制** | 用配色与排版营造氛围，不靠渐变叠加 |

---

## 三、具体修改

### 3.1 配色变量

| 变量 | 修订前 | 修订后 |
|------|--------|--------|
| --bg | 青绿渐变 | `#f8f6f3` 米白/暖灰 |
| --card-bg | #fefefe | `#fefdfb` 略暖白 |
| --primary | #0d9488 | `#2d6a4f` 草地绿 |
| --primary-hover | #0f766e | `#1e4d3a` 深绿 |
| --primary-light | rgba(13,148,136,0.12) | `rgba(45,106,79,0.12)` |
| --primary-border | rgba(13,148,136,0.4) | `rgba(45,106,79,0.35)` |

删除：--gradient-earth、--gradient-earth-soft、--primary-green、--primary-blue

### 3.2 组件调整

- **标题 h1 / result-card h2**：由 gradient text 改为纯色 `color: var(--primary)`
- **按钮**：由 gradient 改为 `background: var(--primary)`，hover 改为 `background: var(--primary-hover)`
- **day-card h4**：由 gradient 改为 `background: var(--primary)` 纯色
- **plan-overview / tips**：由渐变背景改为 `background: var(--primary-light)` 纯色浅绿
- **preview-banner**：由 gradient 改为 `background: var(--primary)`（仅预览页）

---

## 四、与 UI_REDESIGN_SPEC 的对齐

修订后与规范「配色」条目一致：

> 主色建议：草地绿（如 `#2d6a4f`）或湖蓝（如 `#0077b6`）；辅色：米白/暖灰作为背景（如 `#f8f6f3`）；去除偏「科技蓝」的冷感。

本次采纳**草地绿**单主色方案，背景采用米白/暖灰。
