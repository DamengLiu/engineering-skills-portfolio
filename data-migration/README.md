# DataX 数据迁移项目 | DataX Migration Project

这个项目沉淀的是“让迁移结果可解释、可审阅”的方法，而不是一组只会生成 DataX 脚本的提示词。它面向单表迁移、已有作业修复和多表编排，重点处理字段语义、运行范围和重跑风险。

## 适合阅读的对象与关注点

适合关注数据工程、迁移正确性与可审计交付的技术读者。以下问题可用于选择需要深入的材料。

| 关注点 | 仓库中的回答 |
| --- | --- |
| 如何避免“任务成功但数据错位”？ | 先冻结 mapping，再让查询列、转换、Writer 与核验 SQL 围绕它闭环；[结构检查器](.agents/skills/datax-table-migration/scripts/check_artifacts.py)只证明自己能证明的内容。 |
| 如何处理多来源和重跑？ | mapping 逐来源记录业务键、优先级、覆盖规则、顺序、清理位置和恢复影响；清理需要单独授权且最多执行一次。 |
| 如何避免把小修复变成隐性回归？ | [单表修改 Skill](.agents/skills/datax-table-modify/SKILL.md)先确认实际入口，再追踪 mapping、查询、Writer、Shell 和核验 SQL 的直接影响。 |
| 如何让批量执行不掩盖单表问题？ | [批量迁移 Skill](.agents/skills/datax-batch-migration/SKILL.md)只编排已确认的单表作业，保留逐表前检、失败停止和批次结论。 |

## 复用入口

先阅读本项目的 [AGENTS.md](AGENTS.md)，再按下面的“三条工作流”选择主 Skill。新建单表至少需要可靠的源/目标结构、当前业务规则、参考作业、运行范围、键和写入/重跑策略；已有作业修改还需实际调用入口、现有 mapping（如有）与故障或变更证据；批量编排需要已确认的单表作业及任务清单。目标环境的数据库连接、DataX 配置和真实业务规则须由使用者在自己的项目中提供，公开副本不能直接执行真实迁移。

希望先检查方法而不接入数据库，可运行[虚构订单案例](examples/README.md)中的离线命令：它展示列顺序正确时通过、Writer 错列时失败。新建单表的预期交付是 mapping、逐来源 Python 作业、Shell 和核验 SQL；数据库前检、迁移执行与迁后校验各有独立的授权和完成条件。

## 三条工作流

1. [新建单表](.agents/skills/datax-table-migration/SKILL.md)：从需求基线、五列字段映射到 Python、Shell、核验 SQL 四类交付物。它把“需求确认完成”“脚本生成完成”“迁移前检通过”“迁移执行成功”“迁移校验通过”作为不同状态，防止静态检查越级代表真实运行。
2. [修改已有单表](.agents/skills/datax-table-modify/SKILL.md)：用于诊断运行异常或变更已有规则。先读取诊断资料，再检查修改影响，最后按实际风险做局部验证。
3. [批量迁移](.agents/skills/datax-batch-migration/SKILL.md)：用于任务清单、日期传递、执行顺序、失败处理和批次收尾；不接管当前表已经确认的字段规则。

## 值得展开讨论的设计

### 1. mapping 是当前表的事实基线

字段名相似不足以推断语义。每个来源独立记录来源字段、目标字段、转换/固定值、不迁移字段和依据，并明确业务键与物理主键的区别。这样多来源覆盖、加密字段、日期参数和重跑策略都能回溯到同一份可审阅资料。

### 2. 离线检查服务于边界清晰，而非制造“绿灯”

单表检查器会对照 mapping、Writer 和可静态提取的查询列，并尝试渲染日期参数；批量检查器会检查入口、任务清单和单表 Shell。两者都明确不验证 SQL 业务语义、源目标记录数或 DataX 执行结果。这种区分让后续前检和迁后核验仍是必须完成的工程步骤。

### 3. 授权被建模为流程条件

读取资料、生成脚本、数据库前检、执行 DataX 与迁后查询的权限相互独立。涉及数据库、清理、全表操作或生产环境时，必须说明环境、对象、范围和动作；没有授权时只产出可审阅的方案或 SQL。

## 可验证证据

- [虚构订单案例](examples/README.md)包含已确认的 mapping、Reader/Writer 清单和两项单元测试：一项验证顺序一致，一项验证错列能被识别。
- [单表检查器](.agents/skills/datax-table-migration/scripts/check_artifacts.py)和[批量检查器](.agents/skills/datax-batch-migration/scripts/check_batch_artifacts.py)都带 `--self-test`，只使用临时样例，不需要数据库或 DataX。
- [项目约定](AGENTS.md)定义何时可以报告“脚本生成完成”与“数据迁移完成”，防止报告把局部证据扩大解释。

## English overview

This project preserves three distinct migration workflows: creating a single-table job, safely changing an existing job, and coordinating a batch. Its main idea is to keep an approved mapping as the table-level source of truth and to distinguish static structural checks from preflight, execution, and live data reconciliation. Readers need their own approved schemas, rules, and runtime configuration to adapt the Skills; the included examples and tests are fictional and offline only.
