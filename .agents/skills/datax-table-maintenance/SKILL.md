---
name: datax-table-maintenance
description: Diagnose and make a focused change to an existing single-table DataX job, tracing its mapping, parameters, write behavior, and verification impact. Use for existing jobs rather than new job creation.
---

# DataX Table Maintenance

## 1. Diagnose from evidence

Inspect the current job, mapping, invocation, configuration, and relevant logs. Reproduce the failure condition from actual inputs where possible. Separate a source query issue, transformation issue, writer issue, environment issue, and verification gap before selecting a fix.

Read the current Git diff before editing. Treat uncommitted changes as user work. Do not use a different table's mapping as a substitute for the current table's approved rule.

## 2. Trace the direct impact

For a changed field, follow source expression → reader output → transformation → writer column → target constraint → reconciliation. For a changed date or key range, check the caller, job parameter, source filter, target cleanup, and comparison SQL. For changed execution behavior, check exit status, logs, partial writes, and rerun scope.

Make the smallest change that resolves the evidenced problem. Preserve the existing invocation and business behavior outside the requested range. If a proposed repair changes deduplication, overwrite, or cleanup policy, obtain the missing business decision first.

## 3. Verify the change

Run syntax and focused offline checks for modified files. Review any changed transformation against sample input and expected output. Run the relevant integration or database checks only when authorized. Report the cause, exact change, checks completed, residual risk, and safe rerun boundary.
