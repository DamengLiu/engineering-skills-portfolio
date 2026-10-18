---
name: datax-table-modify
description: 修改或排查已有的单表 DataX 迁移交付物，定位运行问题并追踪字段映射、日期参数、写入和核验的直接影响。新建单表使用 datax-table-migration；批量编排使用 datax-batch-migration。
---

# DataX 单表修改

以现有目标表目录为范围，定位问题、修复或迭代 mapping、DataX Python、Shell 和核验 SQL。保留已确认的业务行为、文件接口和历史命名；局部修复不要求补建历史缺失交付物。

## 1. 任务入口

先确定本次是分析、明确变更，还是已授权继续执行。仅确认当前阶段需要的表、环境、现象或需求、日期与范围。

- 排障：定位现象与实际作业 → 查证原因 → 检查影响 → 按授权修改 → 验证。
- 明确变更：确认现有基线 → 检查影响 → 修改 → 验证；不强制经过故障诊断。
- 只读分析：在证据与结论处交付；“只给 SQL”“不要改文件”时不写入交付物。数据库查询另按既有授权判断。

## 2. 工作流程

| 阶段 | 要解决的问题 | 按需读取 |
|---|---|---|
| 定位与诊断 | 实际发生了什么，证据能说明什么？ | [定位与诊断](references/01-diagnosis.md) |
| 基线与修改 | 哪条规则改变，直接影响哪些位置？ | [变更影响与修改](references/02-change-impact.md) |
| 验证与交付 | 本次改动是否正确，哪些尚未验证？ | [验证与交付](references/03-verification.md) |

每阶段沿用已有证据，只读当前任务需要的参考文件。没有确认关键业务规则时交付分析或待确认方案，不生成可直接执行的推测修改。

## 3. 协作边界

- [AGENTS.md](../../../AGENTS.md) 负责权限、通用代码质量和完成判定；本 Skill 负责已有单表的诊断、变更影响和局部验收。
- 当前表有效 mapping 规定预期行为，实际作业说明当前行为；二者不一致时记录差异，不将现有实现自动视为正确需求。
- 新建整套交付物使用 [单表新建 Skill](../datax-table-migration/SKILL.md)；共享字段规则按需引用其 references，不重复复制。
- 批量清单、跨表顺序和批次失败策略交给 [批量迁移 Skill](../datax-batch-migration/SKILL.md)，交接受影响任务、范围与验证结论。
- 新增异常数据恢复、分片、统一日志等能力时，先单独明确需求和设计，再由本 Skill 完成单表侧修改与验证。

## 4. 完成条件

分析交付证据、结论及待确认项；修改交付实际文件、mapping 与运行影响、检查结果及剩余风险。局部静态检查通过只说明其覆盖范围，迁移完成仍须满足项目级执行和数据核验条件。


## 5. 英文译文 | English translation

This reference belongs to the DataX migration project. Follow the Chinese workflow above for scope, mapping, execution, and verification. Confirm project-specific field semantics and obtain explicit authorization before database access or migration execution.
