# generate_plan 输出格式验证报告

**执行时间**: 2026-02-22  
**测试场景**: 奥克兰落地、南北岛都玩、3月、7天、2人  
**环境**: 项目 venv + DEEPSEEK_API_KEY（真实 API 调用）

---

## 1. 验证结论

**✅ 通过**：返回的 JSON 符合 `OUTPUT_FORMAT_SPEC.md` 定义的结构要求。

---

## 2. 结构验证结果

| 检查项 | 规范要求 | 实际结果 | 状态 |
|--------|----------|----------|------|
| 顶层 title | 必填 string | `新西兰南北岛7日精华自驾行程` | ✅ |
| 顶层 plan | 必填 string | 1–2 段总览，已提供 | ✅ |
| 顶层 days | 必填 array | 7 个单日对象 | ✅ |
| 顶层 tips | 可选 array of string | 5 条注意事项 | ✅ |
| days[i].day | 必填 number | 1–7 | ✅ |
| days[i].morning/afternoon/evening | 必填 object | 每日均包含 | ✅ |
| 时段 transport | 必填 string | 含「地点→地点（时长）」或 `""` | ✅ |
| 时段 sights | 必填 string | 景点描述或 `""` | ✅ |
| 时段 activities | 必填 string | 活动描述或 `""` | ✅ |
| 时段 accommodation | 必填 string | 通常 evening 有值，其余多 `""` | ✅ |

---

## 3. 发现的问题

无。本次输出在结构层面完全符合规范。

---

## 4. 建议

1. **Schema 校验**：当前仅做结构存在性检查，建议在 `src/lib/llm.py` 解析后增加 JSON Schema 校验（参考 BACKLOG #5），捕获类型错误、字段名拼写等。
2. **CLI 入口**：可将 `scripts/test_generate_plan.py` 作为验证脚本保留，或并入未来的 `main.py` / `cli.py` 作为 `--validate` 子命令。
3. **输出持久化**：`_append_plan_to_file` 已正常工作，`output_plan.txt` 中可见完整 JSON。建议在 CI 中定期运行该脚本以回归验证。

---

## 5. 附录：测试脚本

验证逻辑位于 `scripts/test_generate_plan.py`，执行：

```bash
source venv/bin/activate
python scripts/test_generate_plan.py
```
