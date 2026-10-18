# 工程实践作品集 | Engineering Skills Portfolio

这份作品集展示我如何把复杂工程工作沉淀为可复用的项目约定和 Codex Skill。重点是保留真实的工作流程、决策边界、参考资料与离线工具，同时将公司专有标识、目录数据和案例替换为可公开的虚构内容。

## 项目一：DataX 数据迁移

**问题。** 字段数量相同，也可能发生字段错位、转换失真、日期边界错误或重跑造成部分写入。

**方法。** [项目目录](projects/data-migration/README.md)由 [AGENTS.md](projects/data-migration/AGENTS.md) 约束权限和质量，再以[单表新建](projects/data-migration/.agents/skills/datax-table-migration/SKILL.md)、[单表修改](projects/data-migration/.agents/skills/datax-table-modify/SKILL.md)、[批量迁移](projects/data-migration/.agents/skills/datax-batch-migration/SKILL.md)分别处理映射、修复和编排。保留前检、执行和迁后核验的分段结论。

**证据。** 三个 Skill 均包含原有专项 references；新建和批量 Skill 带离线检查脚本。[虚构订单案例](projects/data-migration/examples/README.md)演示字段结构检查，明确不替代真实数据核验。

## 项目二：管理后台功能交付

**问题。** 一项需求可能同时影响页面、接口、权限、双人复核、状态与数据库，局部通过不足以证明整项功能完成。

**方法。** [项目目录](projects/admin-console/README.md)由 [AGENTS.md](projects/admin-console/AGENTS.md) 规定分层和公共组件使用；[功能交付](projects/admin-console/.agents/skills/mgt-feature-delivery/SKILL.md)记录需求到最终测试，[局部修改](projects/admin-console/.agents/skills/mgt-modification/SKILL.md)按 L0/L1/L2 控制风险，[数据库设计](projects/admin-console/.agents/skills/database-design/SKILL.md)按需查询字段与字典来源。

**证据。** 保留 Skill 的阶段资料、案例经验、模板、目录查询脚本和测试。公开字段目录使用标明虚构的数据；[审批案例](projects/admin-console/examples/README.md)展示跨 Skill 交接。

## 如何检查 | How to verify

离线示例与目录查询测试只需 Python 3，不需数据库或 DataX：

```bash
python -X utf8 projects/data-migration/examples/check_job_columns.py projects/data-migration/examples/mapping.csv projects/data-migration/examples/job-manifest.json
python -X utf8 -m unittest discover -s projects/data-migration/examples -p "test_*.py"
python -X utf8 -m unittest discover -s projects/admin-console/.agents/skills/database-design/scripts -p "test_*.py"
```

## 作品边界

公开内容是经脱敏的项目副本；原工程、原仓库和其中的 Skill 未被修改。虚构目录和案例用于说明方法，不宣称生产收益或真实系统验收结果。将 Skill 用于其他项目时，应以该项目已批准的字段、字典、组件和权限约定为准。

## English translation

This portfolio presents two project-based bodies of work: DataX migration and admin-console delivery. Each project contains its own AGENTS.md, three focused skills, supporting references, and representative offline tools or templates. The original workflows and decision boundaries are preserved while proprietary identifiers and catalog entries are replaced with fictional examples. The checks above are offline evidence, not claims of production execution or measured business impact.
