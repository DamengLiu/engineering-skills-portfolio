# Fictional approval feature · 虚构审批功能示例

This example describes a small admin-console feature. It is a design and acceptance artifact, not a claim that an application was deployed. Names, states, and rules are invented for the demonstration.

## User journey

A requester submits a draft purchase request. A reviewer sees submitted requests and approves or rejects one. The requester then sees the decision and its timestamp.

| Actor | Primary action | Success state |
| --- | --- | --- |
| Requester | Submit a draft | State becomes `SUBMITTED`; the request appears in review queue. |
| Reviewer | Approve or reject | Exactly one decision is recorded; the requester can see it. |

## Decisions and boundaries

- A draft may become `SUBMITTED`. Only a submitted request may become `APPROVED` or `REJECTED`.
- The review API must reject a second decision and a caller without the reviewer role. The project must decide the exact error codes and authorization mechanism.
- Persist the request state and review record atomically. A unique decision key or concurrency control must support the chosen duplicate-request behavior.
- The list page needs loading, empty, error, and success states. The detail page must show the current state before offering a decision action.
- The actual schema, API paths, role names, and retention rules remain project-specific; this example does not define them for a real system.

## Skill handoff

1. [admin-feature-delivery](../../.agents/skills/admin-feature-delivery/SKILL.md) records the journey, scope, acceptance criteria, and delivery slices.
2. [database-schema-design](../../.agents/skills/database-schema-design/SKILL.md) reviews state, uniqueness, audit, and migration needs if persistence changes.
3. [admin-change](../../.agents/skills/admin-change/SKILL.md) guides focused UI and API implementation and impact checks.

## Acceptance evidence to collect

Exercise the happy path, invalid transition, unauthorized review, duplicate submission, concurrent review, and failure response. Record the test level for each result: visual review, unit test, integration test, or end-to-end run. Do not report this fictional example as a tested application.
