# 标准字段目录（虚构样例） | Standard Fields (Fictional Sample)

本目录保留原目录的九列契约、查询方式、同码多义与修订记录等治理要点。字段均为虚构，用于演示规模化目录的检索、追溯和冲突处理；接入真实项目时必须换成已批准的完整字段目录。

## 1. 使用规则

精确检索字段代码或中文名称；同码多义时结合主题域、来源和修订记录判断。未匹配时不得臆造字段定义。源系统类型、长度和默认值用于追溯，落到目标数据库仍须遵循物理设计规范。

## 2. 来源说明

本公开样例包含 132 条虚构字段，覆盖申请、审核、主体、文档、通知、任务、附件、事件、配置、审计与归档等主题域。`LEGACY_STAGE` 标为删除，仅保留历史追溯；`PROCESS_STAGE` 是其替代字段，不可按名称猜测互换。

## 3. 字段目录

| 字段代码 | 显示名称 | 数据类型 | 长度 | 小数位数 | 默认值 | 备注说明 | 主题域 | 修订记录 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQUEST_ID | 申请编号 | VARCHAR | 32 |  |  | 唯一业务标识 | 申请 |  |
| REQUEST_TITLE | 申请标题 | VARCHAR | 200 |  |  |  | 申请 |  |
| REQUEST_TYPE | 申请类型 | VARCHAR | 32 |  |  | 见完整值域 | 申请 |  |
| REQUEST_STATUS | 申请状态 | VARCHAR | 16 |  | DRAFT | 见完整值域 | 申请 |  |
| REQUEST_SOURCE | 申请来源 | VARCHAR | 32 |  |  |  | 申请 |  |
| REQUEST_PRIORITY | 申请优先级 | VARCHAR | 16 |  | NORMAL |  | 申请 |  |
| REQUEST_REASON | 申请原因 | VARCHAR | 500 |  |  |  | 申请 |  |
| REQUEST_AMOUNT | 申请金额 | DECIMAL | 18 | 2 | 0 | 单位由业务契约确定 | 申请 |  |
| REQUEST_DATE | 申请日期 | DATE |  |  |  |  | 申请 |  |
| REQUEST_CHANNEL | 申请渠道 | VARCHAR | 32 |  |  |  | 申请 |  |
| REQUEST_VERSION | 申请版本 | INT | 10 |  | 0 | 乐观锁候选 | 申请 |  |
| REQUEST_REMARK | 申请备注 | VARCHAR | 500 |  |  |  | 申请 |  |
| REVIEW_ID | 审核编号 | VARCHAR | 32 |  |  | 唯一业务标识 | 审核 |  |
| REVIEW_RESULT | 审核结果 | VARCHAR | 16 |  |  | 见完整值域 | 审核 |  |
| REVIEW_COMMENT | 审核意见 | VARCHAR | 1000 |  |  |  | 审核 |  |
| REVIEWER_ID | 审核人编号 | VARCHAR | 32 |  |  |  | 审核 |  |
| REVIEWER_NAME | 审核人名称 | VARCHAR | 100 |  |  | 展示冗余需确认 | 审核 |  |
| REVIEW_TIME | 审核时间 | DATETIME |  |  |  |  | 审核 |  |
| REVIEW_STAGE | 审核阶段 | VARCHAR | 32 |  |  |  | 审核 |  |
| REVIEW_ORDER | 审核顺序 | INT | 10 |  | 0 |  | 审核 |  |
| REVIEW_STATUS | 审核状态 | VARCHAR | 16 |  | PENDING | 见完整值域 | 审核 |  |
| REVIEW_VERSION | 审核版本 | INT | 10 |  | 0 | 乐观锁候选 | 审核 |  |
| REVIEW_REMARK | 审核备注 | VARCHAR | 500 |  |  |  | 审核 |  |
| REVIEW_SOURCE | 审核来源 | VARCHAR | 32 |  |  |  | 审核 |  |
| SUBJECT_ID | 主体编号 | VARCHAR | 32 |  |  |  | 主体 |  |
| SUBJECT_NAME | 主体名称 | VARCHAR | 200 |  |  |  | 主体 |  |
| SUBJECT_TYPE | 主体类型 | VARCHAR | 32 |  |  | 见完整值域 | 主体 |  |
| SUBJECT_STATUS | 主体状态 | VARCHAR | 16 |  | ACTIVE | 见完整值域 | 主体 |  |
| SUBJECT_CODE | 主体编码 | VARCHAR | 64 |  |  |  | 主体 |  |
| SUBJECT_LEVEL | 主体等级 | VARCHAR | 16 |  |  |  | 主体 |  |
| SUBJECT_REGION | 主体区域 | VARCHAR | 32 |  |  |  | 主体 |  |
| SUBJECT_CONTACT | 联系人 | VARCHAR | 100 |  |  |  | 主体 |  |
| SUBJECT_PHONE | 联系电话 | VARCHAR | 32 |  |  | 脱敏展示另定 | 主体 |  |
| SUBJECT_EMAIL | 联系邮箱 | VARCHAR | 128 |  |  | 脱敏展示另定 | 主体 |  |
| SUBJECT_ENABLED | 启用标志 | CHAR | 1 |  | 1 | 见完整值域 | 主体 |  |
| SUBJECT_REMARK | 主体备注 | VARCHAR | 500 |  |  |  | 主体 |  |
| DOCUMENT_ID | 文档编号 | VARCHAR | 32 |  |  |  | 文档 |  |
| DOCUMENT_NAME | 文档名称 | VARCHAR | 200 |  |  |  | 文档 |  |
| DOCUMENT_TYPE | 文档类型 | VARCHAR | 32 |  |  | 见完整值域 | 文档 |  |
| DOCUMENT_STATUS | 文档状态 | VARCHAR | 16 |  | DRAFT | 见完整值域 | 文档 |  |
| DOCUMENT_URL | 文档地址 | VARCHAR | 500 |  |  | 外部存储路径 | 文档 |  |
| DOCUMENT_SIZE | 文档大小 | BIGINT | 20 |  | 0 | 字节数 | 文档 |  |
| DOCUMENT_HASH | 文档摘要 | VARCHAR | 128 |  |  | 算法另定 | 文档 |  |
| DOCUMENT_VERSION | 文档版本 | VARCHAR | 32 |  |  |  | 文档 |  |
| DOCUMENT_OWNER | 文档所有人 | VARCHAR | 32 |  |  |  | 文档 |  |
| DOCUMENT_EXPIRE_TIME | 到期时间 | DATETIME |  |  |  |  | 文档 |  |
| DOCUMENT_REMARK | 文档备注 | VARCHAR | 500 |  |  |  | 文档 |  |
| DOCUMENT_ARCHIVED | 归档标志 | CHAR | 1 |  | 0 | 见完整值域 | 文档 |  |
| TASK_ID | 任务编号 | VARCHAR | 32 |  |  |  | 任务 |  |
| TASK_NAME | 任务名称 | VARCHAR | 200 |  |  |  | 任务 |  |
| TASK_TYPE | 任务类型 | VARCHAR | 32 |  |  | 见完整值域 | 任务 |  |
| TASK_STATUS | 任务状态 | VARCHAR | 16 |  | NEW | 见完整值域 | 任务 |  |
| TASK_OWNER | 任务负责人 | VARCHAR | 32 |  |  |  | 任务 |  |
| TASK_ASSIGNEE | 任务执行人 | VARCHAR | 32 |  |  |  | 任务 |  |
| TASK_START_TIME | 开始时间 | DATETIME |  |  |  |  | 任务 |  |
| TASK_END_TIME | 结束时间 | DATETIME |  |  |  |  | 任务 |  |
| TASK_PROGRESS | 任务进度 | INT | 3 |  | 0 | 0 至 100 | 任务 |  |
| TASK_RESULT | 任务结果 | VARCHAR | 32 |  |  | 见完整值域 | 任务 |  |
| TASK_RETRY_COUNT | 重试次数 | INT | 10 |  | 0 |  | 任务 |  |
| TASK_REMARK | 任务备注 | VARCHAR | 500 |  |  |  | 任务 |  |
| NOTICE_ID | 通知编号 | VARCHAR | 32 |  |  |  | 通知 |  |
| NOTICE_TYPE | 通知类型 | VARCHAR | 32 |  |  | 见完整值域 | 通知 |  |
| NOTICE_TITLE | 通知标题 | VARCHAR | 200 |  |  |  | 通知 |  |
| NOTICE_CONTENT | 通知内容 | VARCHAR | 2000 |  |  |  | 通知 |  |
| NOTICE_STATUS | 通知状态 | VARCHAR | 16 |  | PENDING | 见完整值域 | 通知 |  |
| NOTICE_CHANNEL | 通知渠道 | VARCHAR | 32 |  |  |  | 通知 |  |
| NOTICE_RECEIVER | 接收对象 | VARCHAR | 32 |  |  |  | 通知 |  |
| NOTICE_SEND_TIME | 发送时间 | DATETIME |  |  |  |  | 通知 |  |
| NOTICE_READ_TIME | 阅读时间 | DATETIME |  |  |  |  | 通知 |  |
| NOTICE_RETRY_COUNT | 重试次数 | INT | 10 |  | 0 |  | 通知 |  |
| NOTICE_ERROR_CODE | 错误码 | VARCHAR | 64 |  |  |  | 通知 |  |
| NOTICE_REMARK | 通知备注 | VARCHAR | 500 |  |  |  | 通知 |  |
| ATTACHMENT_ID | 附件编号 | VARCHAR | 32 |  |  |  | 附件 |  |
| ATTACHMENT_NAME | 附件名称 | VARCHAR | 255 |  |  |  | 附件 |  |
| ATTACHMENT_TYPE | 附件类型 | VARCHAR | 32 |  |  |  | 附件 |  |
| ATTACHMENT_SIZE | 附件大小 | BIGINT | 20 |  | 0 | 字节数 | 附件 |  |
| ATTACHMENT_URL | 附件地址 | VARCHAR | 500 |  |  | 外部存储路径 | 附件 |  |
| ATTACHMENT_HASH | 附件摘要 | VARCHAR | 128 |  |  | 算法另定 | 附件 |  |
| ATTACHMENT_STATUS | 附件状态 | VARCHAR | 16 |  | ACTIVE | 见完整值域 | 附件 |  |
| ATTACHMENT_OWNER | 附件所有人 | VARCHAR | 32 |  |  |  | 附件 |  |
| ATTACHMENT_UPLOAD_TIME | 上传时间 | DATETIME |  |  |  |  | 附件 |  |
| ATTACHMENT_EXPIRE_TIME | 到期时间 | DATETIME |  |  |  |  | 附件 |  |
| ATTACHMENT_SECRET | 保密标识 | CHAR | 1 |  | 0 | 见完整值域 | 附件 |  |
| ATTACHMENT_REMARK | 附件备注 | VARCHAR | 500 |  |  |  | 附件 |  |
| EVENT_ID | 事件编号 | VARCHAR | 32 |  |  |  | 事件 |  |
| EVENT_TYPE | 事件类型 | VARCHAR | 32 |  |  | 见完整值域 | 事件 |  |
| EVENT_STATUS | 事件状态 | VARCHAR | 16 |  | OPEN | 见完整值域 | 事件 |  |
| EVENT_SOURCE | 事件来源 | VARCHAR | 32 |  |  |  | 事件 |  |
| EVENT_LEVEL | 事件等级 | VARCHAR | 16 |  |  | 见完整值域 | 事件 |  |
| EVENT_TIME | 发生时间 | DATETIME |  |  |  |  | 事件 |  |
| EVENT_OPERATOR | 操作人 | VARCHAR | 32 |  |  |  | 事件 |  |
| EVENT_OBJECT_TYPE | 对象类型 | VARCHAR | 32 |  |  |  | 事件 |  |
| EVENT_OBJECT_ID | 对象编号 | VARCHAR | 64 |  |  |  | 事件 |  |
| EVENT_PAYLOAD | 事件载荷 | TEXT |  |  |  | 敏感内容不入日志 | 事件 |  |
| EVENT_TRACE_ID | 链路编号 | VARCHAR | 64 |  |  |  | 事件 |  |
| EVENT_REMARK | 事件备注 | VARCHAR | 500 |  |  |  | 事件 |  |
| CONFIG_ID | 配置编号 | VARCHAR | 32 |  |  |  | 配置 |  |
| CONFIG_KEY | 配置键 | VARCHAR | 128 |  |  | 唯一性另定 | 配置 |  |
| CONFIG_VALUE | 配置值 | VARCHAR | 2000 |  |  | 敏感值脱敏 | 配置 |  |
| CONFIG_TYPE | 配置类型 | VARCHAR | 32 |  |  | 见完整值域 | 配置 |  |
| CONFIG_STATUS | 配置状态 | VARCHAR | 16 |  | ACTIVE | 见完整值域 | 配置 |  |
| CONFIG_SCOPE | 配置范围 | VARCHAR | 32 |  |  |  | 配置 |  |
| CONFIG_VERSION | 配置版本 | INT | 10 |  | 0 | 乐观锁候选 | 配置 |  |
| CONFIG_EFFECTIVE_TIME | 生效时间 | DATETIME |  |  |  |  | 配置 |  |
| CONFIG_EXPIRE_TIME | 失效时间 | DATETIME |  |  |  |  | 配置 |  |
| CONFIG_OPERATOR | 配置人 | VARCHAR | 32 |  |  |  | 配置 |  |
| CONFIG_REMARK | 配置备注 | VARCHAR | 500 |  |  |  | 配置 |  |
| CONFIG_SECRET | 保密标识 | CHAR | 1 |  | 0 | 见完整值域 | 配置 |  |
| AUDIT_ID | 审计编号 | VARCHAR | 32 |  |  |  | 审计 |  |
| AUDIT_ACTION | 审计动作 | VARCHAR | 32 |  |  |  | 审计 |  |
| AUDIT_STATUS | 审计状态 | VARCHAR | 16 |  | SUCCESS | 见完整值域 | 审计 |  |
| AUDIT_OPERATOR | 操作人 | VARCHAR | 32 |  |  |  | 审计 |  |
| AUDIT_TIME | 操作时间 | DATETIME |  |  |  |  | 审计 |  |
| AUDIT_OBJECT_TYPE | 对象类型 | VARCHAR | 32 |  |  |  | 审计 |  |
| AUDIT_OBJECT_ID | 对象编号 | VARCHAR | 64 |  |  |  | 审计 |  |
| AUDIT_BEFORE | 变更前内容 | TEXT |  |  |  | 敏感内容脱敏 | 审计 |  |
| AUDIT_AFTER | 变更后内容 | TEXT |  |  |  | 敏感内容脱敏 | 审计 |  |
| AUDIT_IP | 操作地址 | VARCHAR | 64 |  |  | 脱敏展示另定 | 审计 |  |
| AUDIT_TRACE_ID | 链路编号 | VARCHAR | 64 |  |  |  | 审计 |  |
| AUDIT_REMARK | 审计备注 | VARCHAR | 500 |  |  |  | 审计 |  |
| ARCHIVE_ID | 归档编号 | VARCHAR | 32 |  |  |  | 归档 |  |
| ARCHIVE_TYPE | 归档类型 | VARCHAR | 32 |  |  | 见完整值域 | 归档 |  |
| ARCHIVE_STATUS | 归档状态 | VARCHAR | 16 |  | PENDING | 见完整值域 | 归档 |  |
| ARCHIVE_SOURCE | 归档来源 | VARCHAR | 32 |  |  |  | 归档 |  |
| ARCHIVE_TIME | 归档时间 | DATETIME |  |  |  |  | 归档 |  |
| ARCHIVE_OPERATOR | 归档人 | VARCHAR | 32 |  |  |  | 归档 |  |
| ARCHIVE_RETENTION | 保留期限 | INT | 10 |  | 0 | 单位由业务契约确定 | 归档 |  |
| ARCHIVE_LOCATION | 归档位置 | VARCHAR | 500 |  |  | 外部存储路径 | 归档 |  |
| ARCHIVE_HASH | 归档摘要 | VARCHAR | 128 |  |  | 算法另定 | 归档 |  |
| ARCHIVE_VERSION | 归档版本 | VARCHAR | 32 |  |  |  | 归档 |  |
| ARCHIVE_REMARK | 归档备注 | VARCHAR | 500 |  |  |  | 归档 |  |
| LEGACY_STAGE | 历史处理阶段 | VARCHAR | 16 |  |  | 已删除，仅作历史追溯 | 归档 | 删除 |
