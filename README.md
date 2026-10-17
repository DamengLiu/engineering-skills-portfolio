# 工程实践作品集 | Engineering Skills Portfolio

这组作品展示我如何用可复用的 Codex Skill 处理 **DataX 数据迁移** 和 **管理后台功能交付**：先明确需求与授权边界，再形成可审阅的产物，最后用证据说明验证结果。

仓库中的场景、字段和示例数据均为虚构；不包含生产配置、客户数据、内部组件或专有表结构。

## 一分钟概览

| 方向 | 要解决的问题 | 可查看的作品 |
| --- | --- | --- |
| 数据迁移 | 语法通过仍可能存在字段错位、转换错误或部分写入。 | [三项数据迁移 Skill](.agents/skills/datax-table-setup/SKILL.md)、[虚构迁移案例](examples/data-migration/README.md)与可运行的离线检查。 |
| 管理后台 | 一项需求可能同时影响页面状态、接口契约、权限和持久化。 | [功能交付](.agents/skills/admin-feature-delivery/SKILL.md)、[局部修改](.agents/skills/admin-change/SKILL.md)、[数据库设计](.agents/skills/database-schema-design/SKILL.md)与虚构功能案例。 |

## 案例一：数据迁移

**问题。** 字段名和数量一致，仍不能证明转换值、日期边界或重跑行为正确。

**做法。** 先确认字段映射与运行范围，再分别处理单表新建、已有作业修改和批量编排。离线检查对照读取列、映射顺序和写入列；业务值与源目标数据另行核验。

**取舍。** 示例检查器只证明结构对应，不声称 SQL、转换语义或迁移结果正确。连接数据库、执行迁移和查询数据，都需明确环境、对象、范围与动作的授权。

**证据。** [虚构订单迁移案例](examples/data-migration/README.md)提供映射、作业清单和两项测试，覆盖正确映射与写入列不一致的情况。

## 案例二：管理后台交付

**问题。** 审批功能跨越需求、页面、接口、授权和数据库约束。遗漏重复请求或非法状态转换，会使表面完成的功能在真实流程中出错。

**做法。** 记录用户路径和验收条件，检查页面、接口、服务与数据契约，分批实现，再做端到端验收。局部修复和数据结构设计由独立 Skill 处理。

**取舍。** 现有项目规范是事实依据。Skill 不自行编造角色、状态码或字段；[虚构审批案例](examples/admin-feature/README.md)展示三个 Skill 之间的交接。

## Skill 目录

| Skill | 适用任务 |
| --- | --- |
| [datax-table-setup](.agents/skills/datax-table-setup/SKILL.md) | 新建单表迁移方案与作业。 |
| [datax-table-maintenance](.agents/skills/datax-table-maintenance/SKILL.md) | 排查并修改已有单表作业。 |
| [datax-batch-coordination](.agents/skills/datax-batch-coordination/SKILL.md) | 编排多个已确认的单表作业。 |
| [admin-feature-delivery](.agents/skills/admin-feature-delivery/SKILL.md) | 从需求到验收交付完整管理后台功能。 |
| [admin-change](.agents/skills/admin-change/SKILL.md) | 审查或实施局部页面、接口修改。 |
| [database-schema-design](.agents/skills/database-schema-design/SKILL.md) | 设计新表或影响数据语义的结构变更。 |

## 运行虚构示例

离线检查需要 Python 3.10 或更新版本，不需要第三方包、数据库连接或 DataX 安装。在仓库根目录运行：

```bash
python -X utf8 examples/data-migration/check_job_columns.py examples/data-migration/mapping.csv examples/data-migration/job-manifest.json
python -X utf8 -m unittest discover -s examples/data-migration -p "test_*.py"
```

使用 Skill 时，把对应目录从 `.agents/skills/` 复制到支持 Codex Skill 的项目，再结合该项目的架构和权限调整。示例作业清单仅用于静态演示，不能作为迁移命令执行。

## 作品边界

- 这里展示的是工作流程与虚构案例，不宣称已取得真实生产环境的量化收益。
- 静态检查、编译、集成测试与真实数据核验分别报告。
- 仓库只包含重新编写的通用说明与虚构示例。

## 英文译文 | English translation

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
python -X utf8 examples/data-migration/check_job_columns.py examples/data-migration/mapping.csv examples/data-migration/job-manifest.json
python -X utf8 -m unittest discover -s examples/data-migration -p "test_*.py"
```

To use a skill, copy its folder from `.agents/skills/` into a project that supports Codex skills, then adapt it to that project's architecture and permissions. The sample job manifest is for static review only; it is not a migration command.

## Scope and evidence · 边界与证据

- These are workflow artifacts and synthetic demonstrations, not a claim of measured production impact.
- Static checks, compile results, integration tests, and live data reconciliation are reported separately.
- This repository contains newly written, generalized guidance and fictional examples.
