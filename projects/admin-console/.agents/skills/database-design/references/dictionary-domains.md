# 字典值域（虚构样例） | Dictionary Domains (Fictional Sample)

本公开版保留七列目录结构、别名关联和废弃编码处理。仅用于演示查询工具，不能代替真实值域。

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

## English translation

The seven-column data is fictional. Related codes are not interchangeable. Query every value and governance note for the selected scenario; verify retired codes against approved project data.
