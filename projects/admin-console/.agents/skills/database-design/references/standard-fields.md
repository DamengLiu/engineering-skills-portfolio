# 标准字段目录（虚构样例） | Standard Fields (Fictional Sample)

本公开版保留九列目录结构和按需查询方式；以下字段均为虚构，不能作为真实项目的字段标准。真实项目须接入已批准的完整字段目录。

## 1. 使用规则

精确检索字段代码或中文名称；同码多义时结合主题域、来源和修订记录判断。未匹配时不得臆造字段定义。

| 字段代码 | 中文名称 | 英文名称 | 数据类型 | 长度 | 默认值 | 主题域 | 来源 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQUEST_ID | 申请编号 | Request ID | varchar | 32 | 无 | 审批样例 | 虚构样例 v1 | 唯一业务标识 |
| REQUEST_STATUS | 申请状态 | Request Status | varchar | 16 | DRAFT | 审批样例 | 虚构样例 v1 | 见字典完整值域 |
| REVIEW_RESULT | 审核结果 | Review Result | varchar | 16 | 无 | 审批样例 | 虚构样例 v1 | 见字典完整值域 |
| IS_ARCHIVED | 归档标志 | Archive Flag | tinyint | 1 | 0 | 文档样例 | 虚构样例 v1 | 0 否，1 是 |
