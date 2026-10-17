# 虚构审批功能示例 | Fictional Approval Feature

本例描述一个小型管理后台功能，是设计与验收材料，**不代表已部署的应用**。名称、状态和规则均为虚构。

## 用户路径

申请人提交草稿，审核人在待审列表中批准或驳回，申请人随后查看决定和时间。

| 角色 | 主要动作 | 成功状态 |
| --- | --- | --- |
| 申请人 | 提交草稿 | 状态变为 `SUBMITTED`，申请进入待审列表。 |
| 审核人 | 批准或驳回 | 只记录一次决定，申请人可查看结果。 |

## 设计决定与边界

- 草稿可转为 `SUBMITTED`，只有已提交的申请可转为 `APPROVED` 或 `REJECTED`。
- 审核接口拒绝第二次决定和无审核权限的调用者；具体错误码和授权机制由实际项目确定。
- 申请状态和审核记录应原子化保存；按项目选定的重复请求策略设计唯一决定键或并发控制。
- 列表页展示加载、空状态、错误和成功状态；详情页在提供审核操作前展示当前状态。
- 真实表结构、接口路径、角色名称和保留规则由实际项目决定，本例不替真实系统设定。

## Skill 交接

1. [admin-feature-delivery](../../.agents/skills/admin-feature-delivery/SKILL.md)记录用户路径、范围、验收条件和开发批次。
2. 持久化需要变化时，[database-schema-design](../../.agents/skills/database-schema-design/SKILL.md)审查状态、唯一性、审计与迁移需求。
3. [admin-change](../../.agents/skills/admin-change/SKILL.md)指导局部页面、接口实施及影响检查。

## 应收集的验收证据

检查正常流程、非法状态转换、越权审核、重复提交、并发审核及失败响应。逐项注明验证层级：视觉检查、单元测试、集成测试或端到端运行。不要把此虚构案例报告为已测试的应用。

## 英文译文 | English translation

This example describes a small admin-console feature. It is a design and acceptance artifact, not a claim that an application was deployed. Names, states, and rules are invented for the demonstration.

### User journey

A requester submits a draft purchase request. A reviewer sees submitted requests and approves or rejects one. The requester then sees the decision and its timestamp.

| Actor | Primary action | Success state |
| --- | --- | --- |
| Requester | Submit a draft | State becomes `SUBMITTED`; the request appears in review queue. |
| Reviewer | Approve or reject | Exactly one decision is recorded; the requester can see it. |

### Decisions and boundaries

- A draft may become `SUBMITTED`. Only a submitted request may become `APPROVED` or `REJECTED`.
- The review API must reject a second decision and a caller without the reviewer role. The project must decide the exact error codes and authorization mechanism.
- Persist the request state and review record atomically. A unique decision key or concurrency control must support the chosen duplicate-request behavior.
- The list page needs loading, empty, error, and success states. The detail page must show the current state before offering a decision action.
- The actual schema, API paths, role names, and retention rules remain project-specific; this example does not define them for a real system.

### Skill handoff

1. [admin-feature-delivery](../../.agents/skills/admin-feature-delivery/SKILL.md) records the journey, scope, acceptance criteria, and delivery slices.
2. [database-schema-design](../../.agents/skills/database-schema-design/SKILL.md) reviews state, uniqueness, audit, and migration needs if persistence changes.
3. [admin-change](../../.agents/skills/admin-change/SKILL.md) guides focused UI and API implementation and impact checks.

### Acceptance evidence to collect

Exercise the happy path, invalid transition, unauthorized review, duplicate submission, concurrent review, and failure response. Record the test level for each result: visual review, unit test, integration test, or end-to-end run. Do not report this fictional example as a tested application.
