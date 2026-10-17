---
name: datax-batch-coordination
description: Plan and coordinate a batch of existing DataX table jobs, including task inventory, execution order, failure recording, and batch-level reconciliation. Use when several jobs run together; leave each table's field mapping to its table workflow.
---

# DataX Batch Coordination

## 1. Define the batch

Inventory approved table jobs, their entrypoints, parameters, dependencies, target environments, and expected run ranges. Distinguish the plan from evidence of what actually ran. Record which tasks can run independently and which must wait for a predecessor.

Do not create or change a table's field mapping inside the batch plan. Route such a correction through the single-table maintenance workflow and update the affected batch range afterward.

## 2. Make execution observable

Use the project's existing runner and result format. Preserve each task's command, start and end time, exit status, DataX error count when available, and log location. A failed required task must prevent a misleading overall success result. Keep a precise list of failed and skipped tasks for a bounded rerun.

Preflight command availability, configuration, target scope, and required source or target checks before an authorized run. Do not treat a task list or a human-readable log line as proof of success.

## 3. Close the batch

For each executed job, reconcile the required row and key checks under the approved run boundary. Summarize successes, failures, skipped work, and remaining verification separately. Call the batch complete only when all required jobs and checks meet the agreed acceptance criteria.
