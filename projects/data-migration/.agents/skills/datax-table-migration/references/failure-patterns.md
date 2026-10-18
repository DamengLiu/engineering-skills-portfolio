# 6 错误模式集

只在当前工作出现相应信号时选读。每条模式用于定位应核对的关系，具体字段、环境和结论仍以当前表的 mapping、作业与执行证据为准；不要把旧表结论直接套用。

| 信号 | 通用失效条件 | 当前表需具体化的证据 |
|---|---|---|
| 字段数看似相同，迁后仍缺值或错列 | 来源映射、查询别名、Writer 和目标结构未逐字段闭环；多来源被合并计数 | 每个来源的完整目标字段集、列顺序、固定值与不迁移依据 |
| 字段闭环通过，但码值、固定值或条件结果错误 | mapping 的业务规则只核对了查询别名和 Writer，未同时核对后处理白名单、异常分支和核验 SQL | 当前 mapping 的输入—条件—输出规则，以及 SQL、Transformer/Groovy、值域校验和核验 SQL 的对应结果 |
| Shell 收到日期，查询却未按该日期取数 | 参数在 Shell、Python 模板、DataX 渲染或校验口径的一环丢失 | 实际调用参数、渲染后的 SQL、源与目标的同口径范围 |
| 本地修改正确，运行结果却像旧版本 | 实际执行路径、作业文件或配置与检查对象不同 | 部署目录、被调用脚本、配置加载路径和版本标识 |
| 作业输出成功，但有脏数据或校验空缺 | 退出码、错误记录、必需核验与成功判定未闭环 | DataX 错误数、必需字段与键检查、未取得的指标 |
| 清理或写入在失败后留下部分结果 | 清理范围、执行顺序和失败后的重跑边界不清 | 已写入范围、来源顺序、清理位置及恢复方案 |

只把重复出现且可用明确条件判断的模式加入自动检查。其余模式保留为排查提示，避免前检随案例数量膨胀。


## 6.1 英文译文 | English translation

This reference belongs to the DataX migration project. Follow the Chinese workflow above for scope, mapping, execution, and verification. Confirm project-specific field semantics and obtain explicit authorization before database access or migration execution.
