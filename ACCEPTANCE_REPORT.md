# 验收测试报告

> 执行日期：2026-02-22  
> 验收范围：BACKLOG #4 CLI 入口、#5 输出结构校验

---

## 一、验收结论

| 项目 | 结果 |
|------|------|
| **#4 CLI 入口** | ✅ 通过 |
| **#5 输出结构校验** | ✅ 通过 |

---

## 二、验收明细

### #4 CLI 入口

| 子项 | 验收标准 | 结果 | 说明 |
|------|----------|------|------|
| 4.1 | 执行 `python main.py --help` 有用法说明 | ✅ | 展示 description、所有参数、epilog 示例 |
| 4.2 | 必填参数可正确传入 | ✅ | -l, -r, -m, -d, -t 及长选项均支持，argparse choices 约束 landing_city/region |
| 4.3 | 可选参数可正确传入 | ✅ | landing_time, departure_time, styles, budget_level, must_see 均支持，styles 逗号分隔解析正确 |
| 4.4 | 非法参数抛出明确错误 | ✅ | landing_city 非奥克兰/基督城 → argparse 错误；month 超范围、landing_time 非法 → UserInput 校验，输出「参数校验失败: ...」 |
| 4.5 | 成功输出行程 / 失败有明确提示 | ✅ | 成功时 print JSON；失败时 catch ValueError 输出「生成失败: ...」到 stderr，exit 1 |
| 4.6 | --help 展示所有参数及示例 | ✅ | 含必填、可选、epilog 三行示例 |

### #5 输出结构校验

| 子项 | 验收标准 | 结果 | 说明 |
|------|----------|------|------|
| 5.1 | 顶层缺 title/plan/days 或类型错误能识别 | ✅ | 缺 title → `校验失败 [根]：缺少字段 'title'`；类型错误 → 含字段路径与期望类型 |
| 5.2 | 单日缺 day/morning/afternoon/evening 能识别 | ✅ | 缺 morning → `校验失败 [days[0]]：缺少字段 'morning'` |
| 5.3 | 时段缺字段或非 string 能识别 | ✅ | transport 为 int → `校验失败 [days[0].morning.transport]：期望 string，实际 int` |
| 5.4 | 校验失败不写入 output_plan.txt | ✅ | mock 验证：校验失败时 `_append_plan_to_file` 未被调用 |
| 5.5 | 校验通过正常写入并返回 | ✅ | mock 验证：校验通过时写入一次并返回 result |

---

## 三、验证方式

1. **CLI**：直接执行 `python main.py --help` 及多种非法参数组合
2. **Validator**：`scripts/acceptance_test.py` 用 mock 覆盖合法/非法 JSON，验证 `validate_plan` 与 `_append_plan_to_file` 调用顺序
3. **端到端**：因网络限制，未执行真实 API 调用；逻辑路径已通过 mock 覆盖

---

## 四、发现的问题

| 级别 | 描述 | 建议 |
|------|------|------|
| 低 | API 连接失败（如 ProxyError、APIConnectionError）时，main.py 仅 catch ValueError，会输出完整 traceback | 可考虑 catch `Exception` 输出「生成失败: {e}」以提升体验 |
| — | 无其他阻塞性问题 | — |

---

## 五、测试建议

1. **单元测试**：将 `scripts/acceptance_test.py` 中 validator 用例迁移至 `tests/`，使用 pytest 管理
2. **CLI 测试**：使用 `subprocess` 或 `argparse` 直接测试 `main()` 的 `sys.exit` 与 stderr 输出
3. **集成测试**：在网络可用环境下执行一次真实 `generate_plan` 调用，确认端到端流程

---

## 六、附件

- 验收脚本：`scripts/acceptance_test.py`
- 执行命令：`python scripts/acceptance_test.py`
