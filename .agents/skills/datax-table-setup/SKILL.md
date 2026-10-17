---
name: datax-table-setup
description: Plan and create one DataX table migration with an explicit field mapping, run boundary, offline checks, and reconciliation plan. Use for a new job, not for repairing an existing one or coordinating a batch.
---

# DataX Table Setup

## 1. Establish the migration contract

Identify the source and target datasets, database engines from actual configuration, migration mode, date or key boundary, rerun policy, and approved field mapping. Record unknown business semantics as questions. Do not infer a transformation from a similarly named table or a prior job.

Confirm which actions are authorized. Reading local files and preparing SQL are separate from connecting to a database, running DataX, deleting target rows, or executing reconciliation queries.

## 2. Build the smallest complete job

For each target field, record its source expression, type or length constraint, transformation, null handling, and validation rule. Keep reader output and writer column order aligned with that mapping. Use the project's existing job format, connection configuration, error handling, and invocation pattern.

If multiple source rows can map to one target key, resolve the business rule before creating a deduplication or overwrite behavior. For dates, state whether boundaries are inclusive and how time zones are handled. Keep cleanup statements disabled until their exact environment and range are approved.

Deliver a short requirements baseline, mapping, job configuration or script, invocation instructions, and preflight and reconciliation SQL appropriate to the project.

## 3. Verify and report

Run syntax and local structural checks on files actually created. Compare mapping order with reader and writer columns, then review transformations semantically; matching counts do not prove correct values. Where authorized, preflight source conditions, run the job, and reconcile counts, duplicate keys, required fields, and selected business values.

Report what was prepared, what was executed, evidence for each check, and what remains unverified. Do not call a migration complete from static checks alone.
