---
name: admin-feature-delivery
description: Deliver a complete administrative web feature from requirements and user flow through design, implementation slices, and acceptance checks. Use for a feature spanning multiple layers, not for a narrow fix.
---

# Admin Feature Delivery

## 1. Define the user journey

Identify the target user, main task, entry point, success state, and out-of-scope behavior. Record the current requirement, decisions, open questions, and acceptance criteria in a project-local document. Ask only about missing rules that would make implementation incorrect, such as approval roles or state transitions.

Use realistic but clearly fictional sample data for prototypes. Keep pages navigable and show loading, empty, and error states where they affect the journey.

## 2. Design and implement in slices

Trace the journey through UI, API, service, persistence, and permissions. Reuse existing components, request and response shapes, error handling, and transaction conventions. If a table or constraint changes, use the schema design workflow. If a focused existing behavior needs repair, use the admin change workflow.

Split work into reviewable slices, such as list and detail, submit action, and audit display. For each slice, note affected files, contract changes, migration or rollout needs, and a focused check. Avoid creating a new framework or generic layer for one feature.

## 3. Accept the feature

Check the complete flow with authorized roles, invalid transitions, duplicate requests, and failure responses. Distinguish a page that renders from an API that works and from a complete end-to-end acceptance test. Keep the requirement record current so another engineer can resume from the latest facts and remaining work.
