# 虚构订单迁移示例 | Fictional Order Migration

## 场景

旧订单数据有五列，新报表表使用不同字段名，并以“分”为单位保存金额。本例展示迁移方案如何区分字段结构对应和业务值正确性；所有名称和值均为虚构。

## 映射约定

[字段映射](mapping.csv)给出本例已确认的列顺序，[作业清单](job-manifest.json)列出读取列与写入列。清单仅用于静态教学，**不是可执行的 DataX 作业**。`transform` 列记录需要在真实作业中实现并按业务值验证的转换决定。

| 决定 | 示例规则 | 仍需单独验证 |
| --- | --- | --- |
| 金额 | 按已确认的舍入规则把十进制金额转换为整数分。 | 边界值、精度与溢出。 |
| 状态 | 将旧状态码映射到目标值域，拒绝未知码。 | 完整码表与未知码数量。 |
| 时间 | 按源时区把时间转换为 UTC。 | 跨日样例及日期筛选的开闭边界。 |

## 离线证据

在仓库根目录运行：

```bash
python -X utf8 examples/data-migration/check_job_columns.py examples/data-migration/mapping.csv examples/data-migration/job-manifest.json
python -X utf8 -m unittest discover -s examples/data-migration -p "test_*.py"
```

检查器只证明源、目标列清单与映射顺序一致。失败测试会改动一个 Writer 字段，并确认检查器报告不一致；两项检查均不能验证转换语义或真实数据库记录数。

## 真实项目的验收边界

执行前需确认实际源目标配置、数据范围、重跑策略、主键唯一性、码值与转换实现。另行取得授权后，才执行作业并核对记录数、重复键、必填字段和代表性转换值；未执行的检查要明确列出。

## 英文译文 | English translation

### Scenario

A legacy order feed has five columns. A new reporting table uses different names and stores the total in cents. This example demonstrates how a migration plan separates structural alignment from business correctness. All names and values are invented.

### Contract

The [mapping](mapping.csv) is the approved field order for this example. The [job manifest](job-manifest.json) lists the columns read and written. It is a static teaching artifact, **not an executable DataX job**. The `transform` column documents decisions that would need an implementation and value-level tests in a real job.

| Decision | Example rule | Separate verification needed |
| --- | --- | --- |
| Money | Convert decimal units to integer cents using an agreed rounding rule. | Boundary values, precision, and overflow. |
| Status | Map legacy codes to the target domain; reject unknown codes. | Complete code set and unknown-code count. |
| Time | Convert source timestamps to UTC using the source time zone. | Day-boundary samples and inclusive/exclusive filters. |

### Offline evidence

Run from the repository root:

```bash
python -X utf8 examples/data-migration/check_job_columns.py examples/data-migration/mapping.csv examples/data-migration/job-manifest.json
python -X utf8 -m unittest discover -s examples/data-migration -p "test_*.py"
```

The checker proves that the source and target column lists match the mapping in order. Its failure test changes one writer column and expects a nonzero result. Neither check validates transformation semantics or live database counts.

### Acceptance in a real project

Before execution, confirm the actual source and target configuration, data scope, rerun policy, key uniqueness, code values, and transformation implementation. With separate authorization, run the job and reconcile source and target counts, duplicate keys, required fields, and representative transformed values. State any unexecuted check explicitly.
