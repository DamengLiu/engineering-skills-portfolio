# 虚构订单迁移案例 | Fictional Order Migration Case

本案例只用于展示迁移方法与离线验证，名称、字段和值均为虚构；它不是可执行的 DataX 作业，也不代表真实迁移完成。

## 问题

旧订单数据有五列，新报表表使用不同字段名，并以“分”保存金额。即使 Reader、Writer 的列数相同，仍可能发生三类隐性错误：金额精度处理不一致、旧状态码漏映射、时区转换改变日期筛选边界。

## 方案

[字段映射](mapping.csv)作为当前案例的唯一列顺序基线；[作业清单](job-manifest.json)单独列出读取列和写入列。真实作业需要把 `transform` 中的决策实现为明确的 SQL 或转换逻辑，并把业务值验证放到迁移前检和迁后核验。

| 决策 | 示例规则 | 真实项目还要验证 |
| --- | --- | --- |
| 金额 | 按已确认的舍入规则把十进制金额转换为整数分。 | 边界值、精度与溢出。 |
| 状态 | 将旧状态码映射到目标值域，拒绝未知码。 | 完整码表与未知码数量。 |
| 时间 | 按源时区把时间转换为 UTC。 | 跨日样例及日期筛选的开闭边界。 |

## 关键取舍

检查器只验证“结构关系”：Reader、mapping 与 Writer 是否按相同顺序对应。它故意不解析业务转换的正确性，也不访问数据库。这避免了一个常见误导：把静态检查通过写成数据迁移完成。

## 可验证效果

在仓库根目录运行：

```bash
python -X utf8 data-migration/examples/check_job_columns.py data-migration/examples/mapping.csv data-migration/examples/job-manifest.json
python -X utf8 -m unittest discover -s data-migration/examples -p "test_*.py"
```

第一条命令验证当前样例的列顺序一致；两项测试覆盖正确配置与故意篡改一个 Writer 字段后的失败结果。通过这些检查只能得出“静态列关系正确”，不能得出转换语义、真实记录数或数据库结果正确。

## 真实项目的验收边界

执行前确认实际源目标配置、数据范围、重跑策略、主键唯一性、码值与转换实现。取得环境、对象、范围和动作的授权后，才执行作业并核对记录数、重复键、必填字段和代表性转换值；未执行的检查必须明确列出。

## English overview

This fictional case shows a five-column order migration. The mapping is the source of truth for column order, and the offline checker proves only Reader/mapping/Writer alignment. Its two tests cover a valid order and a deliberately mismatched writer column. Transformation semantics and live data reconciliation remain separate acceptance work.
