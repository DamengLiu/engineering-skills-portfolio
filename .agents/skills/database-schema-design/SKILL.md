---
name: database-schema-design
description: 设计或审查新表及重要结构变更，覆盖字段语义、约束、索引、兼容性和迁移回滚；普通查询修改不进入此流程。 / Design or review consequential schema changes, including constraints, compatibility, and rollback.
---

# 数据库结构设计 | Database Schema Design

## 1 收集数据约定

确认实体含义、生命周期、读写模式、唯一性、允许值、空值、预期数据量及保留要求；从实际配置确认数据库类型和既有结构规范。相似表只作为兼容性证据，不作为新业务规则的依据。

## 2 输出可审阅设计

列明字段类型、长度、默认值、空值和注释，并结合实际查询条件与排序说明主键、外键、唯一约束和索引。追踪模型、查询、接口、页面和历史数据影响；已有表变更给出限定范围的迁移与回滚方案。不编造编码值或保留期限；存在字典时读取相关完整值域并记录来源。

## 3 按实际条件验证

针对真实数据库引擎检查 SQL 语法、历史数据兼容性、空值、重复值及 ORM 映射。获得授权且有代表性数据时，查看执行计划并说明局限。准备 SQL 不等于取得 DDL 或生产变更授权。汇报设计、依据、检查和待确认决定。

## 4 英文译文 | English translation

### 4.1 Gather the data contract

Confirm the entity's meaning, lifecycle, write and read patterns, uniqueness, allowed values, nullability, expected volume, and retention. Inspect the actual database engine and existing schema conventions. Treat similar tables as compatibility evidence, not as authority for a new business rule.

### 4.2 Produce a reviewable design

Specify columns with types, lengths, defaults, nullability, and comments. Explain keys, foreign keys where appropriate, unique constraints, and indexes against actual predicates and sort order. Trace the change into models, queries, API fields, UI values, and historical data. For an existing table, include a bounded migration and rollback plan.

Do not manufacture code lists, values, or a retention period. If a domain dictionary exists, read its complete relevant value set and record the source. Present unresolved semantics as questions before applying them to stored data.

### 4.3 Verify at the right level

Review SQL syntax for the actual engine, data compatibility, null and duplicate cases, and affected ORM mappings. Use an execution plan on representative queries when authorized and available; explain its limits. Preparing SQL does not authorize DDL or production changes. Report the design, evidence, checks performed, and pending decisions.
