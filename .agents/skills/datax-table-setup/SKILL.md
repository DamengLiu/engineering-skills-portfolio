---
name: datax-table-setup
description: 新建单表 DataX 迁移，明确字段映射、运行范围、离线检查与核验方案；不处理已有作业修复或批量编排。 / Plan a new single-table DataX job with mapping, scope, checks, and reconciliation; exclude repairs and batches.
---

# DataX 单表新建 | DataX Table Setup

## 1 明确迁移约定

从实际配置确认源端、目标端和数据库类型，记录迁移模式、日期或主键范围、重跑规则及已确认的字段映射。业务语义不明时列为待确认项，不借用其他表的规则。区分读取本地文件、准备 SQL、连接数据库、执行 DataX、清理目标数据和运行核验查询各自的授权。

## 2 形成最小完整作业

逐个目标字段记录来源表达式、类型或长度限制、转换、空值处理与核验规则。使 Reader 输出、映射和 Writer 列顺序一致，复用项目现有配置、错误处理和调用方式。目标键可能重复、日期边界或时区不明确时，先确认业务规则；精确范围未获授权前不启用清理语句。交付需求基线、映射、作业文件、调用说明及适用的前检和核验 SQL。

## 3 验证并汇报

对新增文件做语法和离线结构检查，再单独复核转换语义；字段数量相同不能证明数据值正确。获得相应授权后，检查源数据、执行迁移，并核对记录数、重复键、必填字段和关键业务值。分别说明已准备、已执行、已验证和未验证的内容，不以静态检查宣称迁移完成。

## 4 英文译文 | English translation

### 4.1 Establish the migration contract

Identify the source and target datasets, database engines from actual configuration, migration mode, date or key boundary, rerun policy, and approved field mapping. Record unknown business semantics as questions. Do not infer a transformation from a similarly named table or a prior job.

Confirm which actions are authorized. Reading local files and preparing SQL are separate from connecting to a database, running DataX, deleting target rows, or executing reconciliation queries.

### 4.2 Build the smallest complete job

For each target field, record its source expression, type or length constraint, transformation, null handling, and validation rule. Keep reader output and writer column order aligned with that mapping. Use the project's existing job format, connection configuration, error handling, and invocation pattern.

If multiple source rows can map to one target key, resolve the business rule before creating a deduplication or overwrite behavior. For dates, state whether boundaries are inclusive and how time zones are handled. Keep cleanup statements disabled until their exact environment and range are approved.

Deliver a short requirements baseline, mapping, job configuration or script, invocation instructions, and preflight and reconciliation SQL appropriate to the project.

### 4.3 Verify and report

Run syntax and local structural checks on files actually created. Compare mapping order with reader and writer columns, then review transformations semantically; matching counts do not prove correct values. Where authorized, preflight source conditions, run the job, and reconcile counts, duplicate keys, required fields, and selected business values.

Report what was prepared, what was executed, evidence for each check, and what remains unverified. Do not call a migration complete from static checks alone.
