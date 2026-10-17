# Fictional order migration · 虚构订单迁移示例

## Scenario

A legacy order feed has five columns. A new reporting table uses different names and stores the total in cents. This example demonstrates how a migration plan separates structural alignment from business correctness. All names and values are invented.

## Contract

The [mapping](mapping.csv) is the approved field order for this example. The [job manifest](job-manifest.json) lists the columns read and written. It is a static teaching artifact, **not an executable DataX job**. The `transform` column documents decisions that would need an implementation and value-level tests in a real job.

| Decision | Example rule | Separate verification needed |
| --- | --- | --- |
| Money | Convert decimal units to integer cents using an agreed rounding rule. | Boundary values, precision, and overflow. |
| Status | Map legacy codes to the target domain; reject unknown codes. | Complete code set and unknown-code count. |
| Time | Convert source timestamps to UTC using the source time zone. | Day-boundary samples and inclusive/exclusive filters. |

## Offline evidence

Run from the repository root:

```bash
python examples/data-migration/check_job_columns.py examples/data-migration/mapping.csv examples/data-migration/job-manifest.json
python -m unittest discover -s examples/data-migration -p "test_*.py"
```

The checker proves that the source and target column lists match the mapping in order. Its failure test changes one writer column and expects a nonzero result. Neither check validates transformation semantics or live database counts.

## Acceptance in a real project

Before execution, confirm the actual source and target configuration, data scope, rerun policy, key uniqueness, code values, and transformation implementation. With separate authorization, run the job and reconcile source and target counts, duplicate keys, required fields, and representative transformed values. State any unexecuted check explicitly.
