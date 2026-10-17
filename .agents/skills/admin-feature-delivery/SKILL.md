---
name: admin-feature-delivery
description: 从需求、用户路径到设计、分批实施和验收，交付跨多层的管理后台功能；局部修复使用 admin-change。 / Deliver a cross-layer admin feature from requirements to acceptance; use admin-change for a narrow fix.
---

# 管理后台功能交付 | Admin Feature Delivery

## 1 定义用户路径

明确目标用户、主要任务、入口、成功状态及本期范围，在项目内记录当前需求、决定、待确认项和验收条件。只有缺少角色或状态转换等规则会导致错误实现时才提问。原型使用标明虚构的样例数据，并保持页面可导航，展示影响主流程的加载、空状态和错误状态。

## 2 分批设计与实施

沿页面、接口、服务、持久化和权限追踪用户路径，复用已有组件、请求响应格式、错误处理和事务约定。表或约束变化进入数据库设计流程；局部已有行为修复进入管理后台修改流程。把功能拆成可审阅批次，逐批记录文件、契约变化、迁移或发布条件及限定检查，不为一个功能新增无必要的框架或通用层。

## 3 完成验收

检查授权角色、非法状态转换、重复请求及失败响应的完整流程。区分页面可展示、接口可用和端到端验收；持续更新需求记录，供下一位工程师接续。

## 4 英文译文 | English translation

### 4.1 Define the user journey

Identify the target user, main task, entry point, success state, and out-of-scope behavior. Record the current requirement, decisions, open questions, and acceptance criteria in a project-local document. Ask only about missing rules that would make implementation incorrect, such as approval roles or state transitions.

Use realistic but clearly fictional sample data for prototypes. Keep pages navigable and show loading, empty, and error states where they affect the journey.

### 4.2 Design and implement in slices

Trace the journey through UI, API, service, persistence, and permissions. Reuse existing components, request and response shapes, error handling, and transaction conventions. If a table or constraint changes, use the schema design workflow. If a focused existing behavior needs repair, use the admin change workflow.

Split work into reviewable slices, such as list and detail, submit action, and audit display. For each slice, note affected files, contract changes, migration or rollout needs, and a focused check. Avoid creating a new framework or generic layer for one feature.

### 4.3 Accept the feature

Check the complete flow with authorized roles, invalid transitions, duplicate requests, and failure responses. Distinguish a page that renders from an API that works and from a complete end-to-end acceptance test. Keep the requirement record current so another engineer can resume from the latest facts and remaining work.
