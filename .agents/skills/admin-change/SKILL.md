---
name: admin-change
description: Review, diagnose, or implement a focused change in an administrative web UI or API, with impact-aware checks. Use for existing behavior; use admin-feature-delivery for a full new feature.
---

# Admin Change

## 1. Locate the actual behavior

Read the request and the current Git diff. Search first by route, API path, component, field, or error text in the relevant module. Inspect the direct call chain and a nearby working pattern before editing. For a review-only request, report evidence without changing code.

## 2. Match effort to risk

- Copy or style within one known component: change the target and inspect the rendered state.
- One page or one API behavior: trace its request, response, state, and error path.
- Cross-layer changes, permissions, state transitions, or shared contracts: identify callers, compatibility, rollback, and combined acceptance checks.

Preserve project conventions. Keep business decisions in the service layer where that is the existing architecture; keep controllers and components focused on their current responsibilities. Parameterize SQL rather than constructing it from user input. Do not invent roles, status codes, or external service behavior.

## 3. Implement and verify

Edit only directly affected files. Verify the changed behavior with the lowest sufficient check, then cover the relevant adjacent path: for example, a UI action and its API response, or a new state and its invalid transition. Report what changed, what was tested, and what still requires a target environment or user decision.
