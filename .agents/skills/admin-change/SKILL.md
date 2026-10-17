---
name: admin-change
description: 审查、排查或实施管理后台页面与接口的局部修改，并按影响范围验证；完整新功能使用 admin-feature-delivery。 / Review or implement a focused admin UI or API change with impact-aware checks.
---

# 管理后台局部修改 | Admin Change

## 1 定位真实行为

阅读请求和当前 Git 差异，优先按路由、接口路径、组件、字段或错误文案在目标模块精确搜索。编辑前检查直接调用链和相邻可用实现；只读审查只报告证据，不修改代码。

## 2 按风险确定范围

- 单文件文案或样式：修改明确目标并查看呈现结果。
- 单页面或单接口行为：追踪请求、响应、状态和错误路径。
- 跨层、权限、状态或公共契约变化：明确调用方、兼容性、回滚方式和组合验收。

遵循现有项目约定。若当前架构由 Service 管理业务规则，就保留该职责；Controller 和组件保持原有边界。SQL 使用参数绑定，不自行编造角色、状态码或外部系统行为。

## 3 实施与验证

只修改直接相关文件。先做与变更相称的最低充分检查，再覆盖相邻路径，例如页面动作及接口响应，或新状态及非法转换。汇报改动、已测试内容，以及仍需目标环境或业务决定确认的事项。

## 4 英文译文 | English translation

### 4.1 Locate the actual behavior

Read the request and the current Git diff. Search first by route, API path, component, field, or error text in the relevant module. Inspect the direct call chain and a nearby working pattern before editing. For a review-only request, report evidence without changing code.

### 4.2 Match effort to risk

- Copy or style within one known component: change the target and inspect the rendered state.
- One page or one API behavior: trace its request, response, state, and error path.
- Cross-layer changes, permissions, state transitions, or shared contracts: identify callers, compatibility, rollback, and combined acceptance checks.

Preserve project conventions. Keep business decisions in the service layer where that is the existing architecture; keep controllers and components focused on their current responsibilities. Parameterize SQL rather than constructing it from user input. Do not invent roles, status codes, or external service behavior.

### 4.3 Implement and verify

Edit only directly affected files. Verify the changed behavior with the lowest sufficient check, then cover the relevant adjacent path: for example, a UI action and its API response, or a new state and its invalid transition. Report what changed, what was tested, and what still requires a target environment or user decision.
