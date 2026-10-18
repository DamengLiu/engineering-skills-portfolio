# 工程实践作品集 | Engineering Skills Portfolio

这不是把工作清单改写成六段说明，而是两组可审阅的工程方法：把容易被“看起来能跑”掩盖的风险，拆成有明确输入、决策边界和验证结论的工作流。

公开版保留了原有 Skill 的核心分工、参考资料、离线检查脚本和失败处理思路；公司专有名称、真实字段目录、环境配置和业务案例已替换为通用描述或虚构样例。

## 面向的岗位与阅读方式

适合后端、数据工程、平台工程，以及需要同时处理前后端协作与数据约束的工程岗位。建议按下面顺序阅读，约 5 分钟可判断我的工程方法：

1. 先看两个项目的“问题—设计—证据”，了解我处理什么风险。
2. 再打开某个 Skill，检查规则是否能落到输入、产物和完成条件。
3. 最后运行离线脚本，确认仓库中的可执行证据与文字结论一致。

| 项目 | 要解决的工程问题 | 核心设计 | 可直接检查的证据 |
| --- | --- | --- | --- |
| [DataX 数据迁移](projects/data-migration/README.md) | 列数相等并不意味着数据正确：字段顺序、转换、日期边界和重跑都可能出错。 | 把单表新建、既有作业修改和批量编排拆开；用 mapping 作为当前表的事实基线；把生成、前检、执行和迁后校验分成不同结论。 | 两个离线检查器、迁移结构示例、覆盖正确与错误列顺序的测试。 |
| [管理后台功能交付](projects/admin-console/README.md) | 一个需求可能同时改变页面状态、接口契约、权限、并发语义和数据库值域。 | 将完整功能交付、局部修改与数据库设计分工；按 L0/L1/L2 风险控制定位和验证；字段/字典查询保留来源、行号和变更指纹。 | 目录查询工具及测试、需求模板、前后端与数据库的验收清单、虚构审批案例。 |

## 项目一：DataX 数据迁移

### 要解决的问题

迁移作业最危险的情况不是语法报错，而是“成功结束但搬错数据”。常见根因包括读取列与 Writer 列顺序不一致、固定值或日期转换被遗漏、多来源覆盖规则未确认，以及重跑前清理范围不清。

### 方法与关键设计

- [单表新建](projects/data-migration/.agents/skills/datax-table-migration/SKILL.md)要求先形成需求基线和五列字段映射，确认业务键、物理主键、运行范围、重跑策略后才生成脚本。映射、Python、Shell、核验 SQL 分别承担依据、搬运、顺序和人工复核的职责。
- [单表修改](projects/data-migration/.agents/skills/datax-table-modify/SKILL.md)先证明“实际执行的是哪一个作业”，再沿 mapping、查询、Writer、Shell 和核验 SQL 追踪直接影响，避免只改表面文件。
- [批量迁移](projects/data-migration/.agents/skills/datax-batch-migration/SKILL.md)不重新定义单表字段规则，只负责任务清单、启动判断、逐表失败处理和批次结论，防止编排层覆盖已确认的表级事实。

### 为什么这些设计有用

最重要的取舍是把“结构闭环”和“业务正确”分开报告。离线检查可以验证 mapping、读取列和 Writer 列的顺序关系，也能检查交付物是否齐全；它不会冒充数据库前检、DataX 运行结果或真实数据核验。这样，静态通过不被误写成迁移完成，未获得授权的数据库动作也不会被脚本生成阶段顺带执行。

### 可验证证据

[虚构订单迁移案例](projects/data-migration/examples/README.md)提供字段映射、作业清单和错误列顺序的失败测试。Skill 内还保留单表与批量交付物检查器；它们均不连接数据库、不执行 DataX，可在本地审阅规则和错误信息。

## 项目二：管理后台功能交付

### 要解决的问题

后台功能常以“小改动”出现，却可能跨越动态路由、列表/详情状态、接口兼容性、角色权限、重复提交、双人复核和持久化约束。只验证一个页面或一次接口响应，无法证明整条业务链路可靠。

### 方法与关键设计

- [完整功能交付](projects/admin-console/.agents/skills/mgt-feature-delivery/SKILL.md)把需求、原型、设计、开发批次和最终功能性测试沉淀为可续接材料。它把当前范围、后续能力、待确认项和变更原因分开，避免迭代后仍依据过期需求实现。
- [局部修改](projects/admin-console/.agents/skills/mgt-modification/SKILL.md)用 L0/L1/L2 分级：只有文件唯一且无契约变化的文案/样式才走 L0；页面、接口、权限、状态、外部调用和数据库设计会升级，并要求对应范围的验证与回滚考虑。
- [数据库设计](projects/admin-console/.agents/skills/database-design/SKILL.md)不靠模型猜字段和码值。目录查询工具返回完整值域、来源行号、关联提示与 fingerprint；资料、查询条件或工具变化时，旧结论不能被静默复用。

### 为什么这些设计有用

核心取舍是把“代码改动很小”与“业务风险很低”分开判断。风险来自运行入口、状态转换和公共契约，而不是 diff 行数。另一个关键设计是把字段目录做成可查询、可测试、可失效的证据来源：查询工具不建立持久缓存，且源码或资料任一变化都会改变指纹，降低引用旧结论的风险。

### 可验证证据

[虚构审批案例](projects/admin-console/examples/README.md)展示三个 Skill 如何交接需求、数据模型和局部实现；数据库 Skill 的查询工具测试覆盖完整值域、关联码、废弃码、未知项、表格格式和指纹失效。

## 运行离线证据 | Run the offline evidence

以下命令只运行虚构样例和静态检查，不连接数据库、不执行 DataX：

```bash
python -X utf8 projects/data-migration/examples/check_job_columns.py projects/data-migration/examples/mapping.csv projects/data-migration/examples/job-manifest.json
python -X utf8 -m unittest discover -s projects/data-migration/examples -p "test_*.py"
python -X utf8 -m unittest discover -s projects/admin-console/.agents/skills/database-design/scripts -p "test_*.py"
```

## 作品边界

- 公开内容是脱敏副本，原工程、原仓库和原 Skill 未被修改。
- 虚构目录与案例说明方法，不是生产数据、客户数据或真实系统验收记录。
- 不声称未被执行的数据库查询、迁移运行或量化业务收益；每类证据只支持它实际验证的结论。

## English overview

This portfolio is organized as two engineering case studies rather than a generic skill list. The DataX project separates mapping, job generation, preflight, execution, and reconciliation so a static check is never presented as a successful migration. The admin-console project separates feature delivery, focused changes, and database design; it uses risk-based verification and source-traceable catalog lookups. All examples are fictional, while the workflows, validation boundaries, and offline tools are preserved in sanitized form.
