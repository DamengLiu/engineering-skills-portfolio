# 3 验证与交付

依据实际修改和直接影响选择检查，产出有明确覆盖范围的结论。

## 3.1 核对修改结果

按 [AGENTS.md](../../../../AGENTS.md) 完成修改文件的最低静态检查。人工核对字段含义、SQL 语义、前检和核验口径。涉及固定值、码值、分支、默认值、去重或时间生成时，执行 [语义映射复核](../../datax-table-migration/references/semantic-mapping-review.md)；不一致时同步修订生成表达式、后处理或值域校验及核验 SQL，不只修其中一处。

加密字段核对 mapping 真实字段清单、各来源 ENCRYPT_COLUMNS、Writer、dx_encrypt 参数与顺序。无法静态确认的部分另行核对；未确认加解密校验方法时，不以密文与源值相等作为通过条件。

## 3.2 局部检查

从项目根目录运行；文件名以目标表目录为基准：

```text
py .agents/skills/datax-table-migration/scripts/check_artifacts.py <目标表目录> --files <修改文件名> [其他修改文件名]
```

检查器核对可静态读取的字段对应、加密配置、Shell 语法及 SQL 日期参数。修改 mapping 时核对关联来源作业；动态 SQL、字段含义、实际结构及核验 SQL 语义须另行检查。历史交付物缺失单独报告，不要求局部修复补建整套文件。

必要检查完成且通过、受影响业务规则已核对后，才能报告本次修改完成；工具通过只说明其覆盖范围。

## 3.3 运行验证与交付

数据库前检、DataX 执行和迁后查询须取得对应环境、对象、范围和动作授权。按需读取 [迁移前检](../../datax-table-migration/references/precheck.md) 与 [迁移校验](../../datax-table-migration/references/verification.md)，复用未修改文件的有效检查结果。

交付问题依据、实际修改文件、mapping 与运行影响、已完成检查及结果、未执行检查和剩余风险。关键业务规则未确认时只交付分析或方案；局部检查不能替代完整交付或真实迁移验收。


## 3.4 英文译文 | English translation

This reference belongs to the DataX migration project. Follow the Chinese workflow above for scope, mapping, execution, and verification. Confirm project-specific field semantics and obtain explicit authorization before database access or migration execution.
