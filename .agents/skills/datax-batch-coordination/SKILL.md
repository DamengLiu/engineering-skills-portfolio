---
name: datax-batch-coordination
description: 编排多个已有 DataX 单表作业，管理任务清单、顺序、失败记录与批次核验；单表字段映射仍由单表流程负责。 / Coordinate existing DataX jobs, execution order, failures, and batch reconciliation without changing table mappings.
---

# DataX 批量编排 | DataX Batch Coordination

## 1 定义批次

盘点已确认的单表作业、入口、参数、依赖、目标环境和运行范围，区分计划清单与实际执行证据。标明可独立运行及必须等待前置任务的作业。字段映射修正交由单表维护流程处理，再更新受影响的批次范围。

## 2 让执行可追踪

复用项目现有运行器和结果格式，记录每项任务的命令、开始与结束时间、退出状态、可取得的 DataX 错误数及日志位置。必需任务失败时不得汇总为成功；保留失败和跳过任务的精确清单，供限定范围补跑。获授权运行前检查命令、配置、目标范围和必要数据条件，不把任务清单或日志文案当作成功证据。

## 3 完成批次收尾

在批准的运行边界内逐表核对记录数和关键字段，分别汇总成功、失败、跳过与待核验项目。只有全部必需任务及检查满足验收标准，才报告批次完成。

## 4 英文译文 | English translation

### 4.1 Define the batch

Inventory approved table jobs, their entrypoints, parameters, dependencies, target environments, and expected run ranges. Distinguish the plan from evidence of what actually ran. Record which tasks can run independently and which must wait for a predecessor.

Do not create or change a table's field mapping inside the batch plan. Route such a correction through the single-table maintenance workflow and update the affected batch range afterward.

### 4.2 Make execution observable

Use the project's existing runner and result format. Preserve each task's command, start and end time, exit status, DataX error count when available, and log location. A failed required task must prevent a misleading overall success result. Keep a precise list of failed and skipped tasks for a bounded rerun.

Preflight command availability, configuration, target scope, and required source or target checks before an authorized run. Do not treat a task list or a human-readable log line as proof of success.

### 4.3 Close the batch

For each executed job, reconcile the required row and key checks under the approved run boundary. Summarize successes, failures, skipped work, and remaining verification separately. Call the batch complete only when all required jobs and checks meet the agreed acceptance criteria.
