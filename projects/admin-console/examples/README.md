# 虚构审批功能案例 | Fictional Approval Feature Case

本例是用于说明设计与验收边界的虚构材料，不代表已部署或已验收的应用。名称、状态和规则均为示例。

## 问题

一个“提交并审核”的功能同时涉及页面状态、接口权限、重复请求、并发决定和数据库一致性。若只验证列表能展示或接口返回成功，第二次审核、越权调用或非法状态转换仍可能破坏流程。

## 方案

申请人提交草稿；审核人在待审列表中批准或驳回；申请人随后查看决定和时间。

| 角色 | 主要动作 | 成功状态 |
| --- | --- | --- |
| 申请人 | 提交草稿 | 状态变为 `SUBMITTED`，申请进入待审列表。 |
| 审核人 | 批准或驳回 | 只记录一次决定，申请人可查看结果。 |

三项 Skill 的分工如下：

1. [mgt-feature-delivery](../.agents/skills/mgt-feature-delivery/SKILL.md)记录用户路径、本期范围、验收条件和开发批次。
2. 持久化需要变化时，[database-design](../.agents/skills/database-design/SKILL.md)审查状态值域、唯一性、审计字段与迁移方案。
3. [mgt-modification](../.agents/skills/mgt-modification/SKILL.md)从真实页面或接口入口定位，实现局部改动并检查直接影响。

## 关键取舍

- 草稿可转为 `SUBMITTED`；只有已提交的申请可转为 `APPROVED` 或 `REJECTED`。
- 审核接口拒绝第二次决定和无审核权限的调用者；重复请求策略不能只依赖前端按钮禁用。
- 申请状态和审核记录应原子化保存；根据项目既有能力使用唯一决定键、幂等控制或并发控制。
- 列表页应覆盖加载、空、错误和成功状态；详情页在展示审核操作前先展示当前状态。
- 真实表结构、接口路径、角色名称、错误码和保留规则由接入项目决定，本例不替真实系统设定它们。

## 可验证效果

验收应至少覆盖：正常提交与审核、非法状态转换、越权审核、重复提交、并发审核和失败响应。每项结果注明验证层级：视觉检查、单元测试、集成测试或端到端运行。这样“一个字段已回显”不会被误写成整个功能包已验收。

## English overview

This fictional approval case demonstrates how feature delivery, database design, and focused modification cooperate. A valid acceptance plan tests the happy path, invalid transitions, authorization, duplicate requests, concurrent decisions, and failure responses. The case is an engineering design artifact, not a deployed application claim.
