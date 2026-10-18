# 3 单表调用

承接已通过前检的执行计划，按确认的参数调用单表 Shell。产出逐执行单元的原始结果和日志，交给批量校验核对；这里不计算整批结论。

## 3.1 按计划推进任务

第一版串行执行。批量层调用完整的单表 Shell，不导入单表 Python，也不绕过它自身的前检、写入和校验顺序。复用脚本生成阶段的静态检查结果，不格式化单表 Python，也不重复检查未修改的单表 Shell。

## 3.2 隔离失败，继续独立任务

单表或分片失败时停止当前执行单元，保存真实退出码与原始日志，默认继续其他独立表。若同一目标表的后续分片依赖失败分片，则停止该表后续分片；确认互不依赖后才可继续。既有入口实行遇错停止时，如实记录未执行任务，不为套用新策略而顺带改造。后续命令不得覆盖已有失败状态。

## 3.3 留存每个范围的执行记录

新生成的记录至少包含 `batch_id`、`task_name`、可选 `group` 和 `shard_id`、起止日期或范围、`status`、`exit_code`、`started_at`、`ended_at`、`elapsed_seconds`、`log_path` 和 `error_summary`。可靠取得时再附加记录数与 DataX 指标。既有格式不强制改造，但要能辨认已成功、失败和未执行的表与范围。

执行单元状态只用 `Success`、`Failure`；未执行、跳过和待优化项单列明细，不预先标为成功。所有计划单元都有结果或明确的未执行原因后，执行阶段才可收束。保存范围与日志，为后续补传提供依据；不自动重传。

按月、按天切片、受控并发与自动补传属于后续能力。同一目标表默认不并行写入。


## 3.4 英文译文 | English translation

This reference belongs to the DataX migration project. Follow the Chinese workflow above for scope, mapping, execution, and verification. Confirm project-specific field semantics and obtain explicit authorization before database access or migration execution.
