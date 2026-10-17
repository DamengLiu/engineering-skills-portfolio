# Engineering Skills Portfolio · 工程实践作品集

Reusable Codex skills for **DataX data migration** and **administrative web application delivery**. The repository shows how I turn ambiguous requests into scoped changes, reviewable artifacts, and evidence-based verification.

这是一组可复用的 Codex Skill，展示我处理 **DataX 数据迁移** 与 **管理后台功能交付** 的方法：明确边界、形成可审阅的产物，并用检查结果支持结论。

> All scenarios, identifiers, and sample data in this repository are fictional. No production configuration, customer data, internal package, or proprietary schema is included.
>
> 仓库中的场景、标识和示例数据均为虚构，不包含生产配置、客户数据、内部组件或专有表结构。

## 60-second overview · 一分钟概览

| Area | Engineering problem | What to inspect |
| --- | --- | --- |
| Data migration / 数据迁移 | A job can pass syntax checks while mapping the wrong values or leaving partial results. | [Three migration skills](.agents/skills/datax-table-setup/SKILL.md), [fictional migration case](examples/data-migration/README.md), and a runnable structural check. |
| Admin delivery / 管理后台 | A small request can affect UI state, API contracts, permissions, and persistence. | [Feature delivery](.agents/skills/admin-feature-delivery/SKILL.md), [change review](.agents/skills/admin-change/SKILL.md), [schema design](.agents/skills/database-schema-design/SKILL.md), and a fictional feature brief. |

## Case study 1 · Data migration

**Problem.** Field names and counts may line up while transformations, date boundaries, or rerun behavior remain wrong.

**Approach.** Capture an approved mapping and run boundary first. Keep table creation, maintenance, and batch coordination as separate workflows. Compare reader columns, mapping order, and writer columns with a small offline check; verify value semantics and source-to-target counts separately.

**Decision.** The checker intentionally proves only structural alignment. It never claims that SQL, transformations, or the database result are correct. Migration execution and data queries require explicit environment, object, range, and action authorization.

**Evidence.** The fictional [order migration example](examples/data-migration/README.md) includes a mapping, a DataX-shaped configuration, and tests for both a valid mapping and a mismatched writer column.

## Case study 2 · Admin application delivery

**Problem.** A new approval flow crosses requirements, page states, an API, authorization, and a database constraint. Missing one boundary creates a feature that looks complete but fails under duplicate requests or invalid state changes.

**Approach.** Record the user journey and acceptance criteria; review the affected UI, API, service, and schema contracts; implement in small slices; then test the end-to-end flow. Use a separate change skill for narrow fixes and a schema skill when persistence semantics change.

**Decision.** Existing project conventions remain the source of truth. The skills request missing business rules instead of inventing roles, status codes, or database fields. The [fictional approval feature](examples/admin-feature/README.md) shows the handoff between the three skills.

## Skills · 技能目录

| Skill | Use it for |
| --- | --- |
| [datax-table-setup](.agents/skills/datax-table-setup/SKILL.md) | Create a single-table migration plan and job. |
| [datax-table-maintenance](.agents/skills/datax-table-maintenance/SKILL.md) | Diagnose and safely change an existing job. |
| [datax-batch-coordination](.agents/skills/datax-batch-coordination/SKILL.md) | Coordinate several approved table jobs. |
| [admin-feature-delivery](.agents/skills/admin-feature-delivery/SKILL.md) | Carry a complete admin feature from brief to acceptance. |
| [admin-change](.agents/skills/admin-change/SKILL.md) | Review or implement a focused UI/API change. |
| [database-schema-design](.agents/skills/database-schema-design/SKILL.md) | Design a table or a consequential schema change. |

## Try the example · 运行示例

Requires Python 3.10+; no third-party package, database connection, or DataX installation is needed for the offline check.

```bash
python examples/data-migration/check_job_columns.py examples/data-migration/mapping.csv examples/data-migration/job.json
python -m unittest discover -s examples/data-migration -p "test_*.py"
```

To use a skill, copy its folder from `.agents/skills/` into a project that supports Codex skills, then adapt it to that project's architecture and permissions. The sample job is for static review only and contains placeholders; it is not a migration command.

## Scope and evidence · 边界与证据

- These are workflow artifacts and synthetic demonstrations, not a claim of measured production impact.
- Static checks, compile results, integration tests, and live data reconciliation are reported separately.
- This repository contains newly written, generalized guidance and fictional examples.
