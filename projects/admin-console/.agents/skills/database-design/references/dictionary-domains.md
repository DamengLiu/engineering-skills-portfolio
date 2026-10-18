# 字典值域（虚构样例） | Dictionary Domains (Fictional Sample)

本公开版保留七列目录结构、别名关联和废弃编码处理。目录含 46 条虚构值域记录，覆盖多场景状态、标志和动作；仅用于演示查询工具，不能代替真实值域。

`REVIEW_RESULT` 与 `DECISION_STATUS` 为跨场景关联示例，不可跨场景直接替换；分别核对完整值域。
`OLD_ARCHIVE_FLAG` 已废弃，应核对 `IS_ARCHIVED` 的现行值域与历史数据迁移规则。

| 字段代码 | 字段名称 | 编码 | 编码名称 | 适用场景 | 来源 | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| REQUEST_STATUS | 申请状态 | DRAFT | 草稿 | 申请 | 虚构样例 v1 | 可编辑 |
| REQUEST_STATUS | 申请状态 | SUBMITTED | 待审核 | 申请 | 虚构样例 v1 | 不可直接终结 |
| REQUEST_STATUS | 申请状态 | APPROVED | 已通过 | 申请 | 虚构样例 v1 | 终态 |
| REQUEST_STATUS | 申请状态 | REJECTED | 已驳回 | 申请 | 虚构样例 v1 | 终态 |
| REVIEW_RESULT | 审核结果 | APPROVE | 通过 | 审核 | 虚构样例 v1 | 审核动作 |
| REVIEW_RESULT | 审核结果 | REJECT | 驳回 | 审核 | 虚构样例 v1 | 审核动作 |
| DECISION_STATUS | 决定状态 | YES | 同意 | 决定 | 虚构样例 v1 | 不与审核码等价 |
| DECISION_STATUS | 决定状态 | NO | 不同意 | 决定 | 虚构样例 v1 | 不与审核码等价 |
| IS_ARCHIVED | 归档标志 | 0 | 否 | 文档 | 虚构样例 v1 | 当前编码 |
| IS_ARCHIVED | 归档标志 | 1 | 是 | 文档 | 虚构样例 v1 | 当前编码 |
| REVIEW_STATUS | 审核状态 | PENDING | 待审核 | 审核 | 虚构样例 v1 | 非终态 |
| REVIEW_STATUS | 审核状态 | PROCESSING | 审核中 | 审核 | 虚构样例 v1 | 非终态 |
| REVIEW_STATUS | 审核状态 | COMPLETED | 已完成 | 审核 | 虚构样例 v1 | 终态 |
| REVIEW_STATUS | 审核状态 | CANCELLED | 已撤销 | 审核 | 虚构样例 v1 | 终态 |
| TASK_STATUS | 任务状态 | NEW | 新建 | 任务 | 虚构样例 v1 | 可分配 |
| TASK_STATUS | 任务状态 | RUNNING | 执行中 | 任务 | 虚构样例 v1 | 非终态 |
| TASK_STATUS | 任务状态 | SUCCESS | 成功 | 任务 | 虚构样例 v1 | 终态 |
| TASK_STATUS | 任务状态 | FAILED | 失败 | 任务 | 虚构样例 v1 | 可重试 |
| NOTICE_STATUS | 通知状态 | PENDING | 待发送 | 通知 | 虚构样例 v1 | 非终态 |
| NOTICE_STATUS | 通知状态 | SENT | 已发送 | 通知 | 虚构样例 v1 | 非终态 |
| NOTICE_STATUS | 通知状态 | READ | 已阅读 | 通知 | 虚构样例 v1 | 终态 |
| NOTICE_STATUS | 通知状态 | FAILED | 发送失败 | 通知 | 虚构样例 v1 | 可重试 |
| SUBJECT_STATUS | 主体状态 | ACTIVE | 生效 | 主体 | 虚构样例 v1 | 当前可用 |
| SUBJECT_STATUS | 主体状态 | SUSPENDED | 暂停 | 主体 | 虚构样例 v1 | 不可操作 |
| SUBJECT_STATUS | 主体状态 | CLOSED | 关闭 | 主体 | 虚构样例 v1 | 终态 |
| SUBJECT_STATUS | 主体状态 | UNKNOWN | 未知 | 主体 | 虚构样例 v1 | 不静默视为正常 |
| DOCUMENT_STATUS | 文档状态 | DRAFT | 草稿 | 文档 | 虚构样例 v1 | 可编辑 |
| DOCUMENT_STATUS | 文档状态 | PUBLISHED | 已发布 | 文档 | 虚构样例 v1 | 对外可见另定 |
| DOCUMENT_STATUS | 文档状态 | EXPIRED | 已失效 | 文档 | 虚构样例 v1 | 终态 |
| DOCUMENT_STATUS | 文档状态 | WITHDRAWN | 已撤回 | 文档 | 虚构样例 v1 | 终态 |
| EVENT_LEVEL | 事件等级 | INFO | 提示 | 事件 | 虚构样例 v1 |  |
| EVENT_LEVEL | 事件等级 | WARN | 警告 | 事件 | 虚构样例 v1 | 可恢复 |
| EVENT_LEVEL | 事件等级 | ERROR | 错误 | 事件 | 虚构样例 v1 | 需处理 |
| EVENT_LEVEL | 事件等级 | CRITICAL | 严重 | 事件 | 虚构样例 v1 | 需升级 |
| CONFIG_STATUS | 配置状态 | ACTIVE | 生效 | 配置 | 虚构样例 v1 | 当前版本 |
| CONFIG_STATUS | 配置状态 | INACTIVE | 未生效 | 配置 | 虚构样例 v1 | 不加载 |
| CONFIG_STATUS | 配置状态 | EXPIRED | 已失效 | 配置 | 虚构样例 v1 | 不加载 |
| CONFIG_STATUS | 配置状态 | DISABLED | 已禁用 | 配置 | 虚构样例 v1 | 不加载 |
| PROCESS_STAGE | 处理阶段 | PREPARE | 准备 | 流程 | 虚构样例 v1 | 替代历史阶段 |
| PROCESS_STAGE | 处理阶段 | EXECUTE | 执行 | 流程 | 虚构样例 v1 | 非终态 |
| PROCESS_STAGE | 处理阶段 | VERIFY | 核验 | 流程 | 虚构样例 v1 | 非终态 |
| PROCESS_STAGE | 处理阶段 | CLOSE | 收尾 | 流程 | 虚构样例 v1 | 终态 |
| ACCESS_LEVEL | 访问级别 | VIEW | 查看 | 权限 | 虚构样例 v1 | 最低权限 |
| ACCESS_LEVEL | 访问级别 | EDIT | 编辑 | 权限 | 虚构样例 v1 | 受资源约束 |
| ACCESS_LEVEL | 访问级别 | APPROVE | 审核 | 权限 | 虚构样例 v1 | 受职责约束 |
| ACCESS_LEVEL | 访问级别 | ADMIN | 管理 | 权限 | 虚构样例 v1 | 最小授权 |
