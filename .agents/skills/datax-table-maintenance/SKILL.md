---
name: datax-table-maintenance
description: 排查并最小化修改已有单表 DataX 作业，追踪映射、参数、写入与核验影响；不用于新建作业。 / Diagnose and make a focused change to an existing single-table DataX job, including verification impact.
---

# DataX 单表维护 | DataX Table Maintenance

## 1 根据证据定位

检查当前作业、映射、调用方式、配置和相关日志，区分源查询、转换、写入、环境与核验问题。编辑前查看 Git 差异并保护用户已有改动。当前表的业务规则以其有效映射为准，不用其他表的映射代替。

## 2 追踪直接影响

字段变化沿“源表达式 → Reader 输出 → 转换 → Writer 列 → 目标约束 → 核验”检查；日期或主键范围变化同步检查调用参数、源过滤、目标清理和对比 SQL；执行行为变化检查退出码、日志、部分写入及重跑范围。只修证据支持的问题。若修复会改变去重、覆盖或清理策略，先确认业务决定。

## 3 验证修改

对实际修改的文件做语法和限定范围的离线检查，用样例输入与预期输出复核转换。集成或数据库检查仅在获得授权后执行。汇报原因、改动、已完成检查、剩余风险与安全重跑范围。

## 4 英文译文 | English translation

### 4.1 Diagnose from evidence

Inspect the current job, mapping, invocation, configuration, and relevant logs. Reproduce the failure condition from actual inputs where possible. Separate a source query issue, transformation issue, writer issue, environment issue, and verification gap before selecting a fix.

Read the current Git diff before editing. Treat uncommitted changes as user work. Do not use a different table's mapping as a substitute for the current table's approved rule.

### 4.2 Trace the direct impact

For a changed field, follow source expression → reader output → transformation → writer column → target constraint → reconciliation. For a changed date or key range, check the caller, job parameter, source filter, target cleanup, and comparison SQL. For changed execution behavior, check exit status, logs, partial writes, and rerun scope.

Make the smallest change that resolves the evidenced problem. Preserve the existing invocation and business behavior outside the requested range. If a proposed repair changes deduplication, overwrite, or cleanup policy, obtain the missing business decision first.

### 4.3 Verify the change

Run syntax and focused offline checks for modified files. Review any changed transformation against sample input and expected output. Run the relevant integration or database checks only when authorized. Report the cause, exact change, checks completed, residual risk, and safe rerun boundary.
