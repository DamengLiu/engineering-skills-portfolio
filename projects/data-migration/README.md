# DataX 数据迁移项目 | DataX Migration Project

本项目按原有三条工作流组织：新建单表、修改已有单表、批量迁移。保留需求基线、字段映射、Python/Shell 交付、前检、DataX 执行和迁后核验的边界。公开版从原 Skill 副本脱敏；没有修改原始工程。

## 阅读顺序

1. [项目约定](AGENTS.md)：权限、质量和完成判定。
2. [新建单表](.agents/skills/datax-table-migration/SKILL.md)、[修改单表](.agents/skills/datax-table-modify/SKILL.md)、[批量迁移](.agents/skills/datax-batch-migration/SKILL.md)：按任务选择一条主工作流。
3. [虚构订单迁移案例](examples/README.md)：离线结构检查示例，不代表实际迁移完成。

## 保留的工程细节

- 新建单表保留五列映射、多来源优先级、加密字段、日期参数、四类交付物与语义复核。
- 单表修改保留现象诊断、直接影响检查和分级验证。
- 批量迁移保留任务定义、前检、逐表执行、失败收尾和批次结论；不接管单表字段规则。
- 两个离线脚本仍位于对应 Skill 的 `scripts/` 目录。

## English translation

The project retains three distinct DataX workflows: new single-table delivery, changes to an existing table job, and batch coordination. Its project-level AGENTS.md defines authorization and verification. The complete skill references and offline scripts are preserved in sanitized copies. The example is fictional and does not imply a production migration result.
