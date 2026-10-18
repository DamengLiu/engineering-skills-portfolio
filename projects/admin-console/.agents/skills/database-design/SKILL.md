---
name: database-design
description: 用于 管理后台项目 中需要规范化设计的数据模型、标准字段、字典值域、关键索引约束或复杂 MyBatis 映射的设计审查与受控实施；普通 SQL 和已有字段映射的局部调整只查适用规范。
---

# 数据库设计 Skill

## 适用范围

仅在数据模型设计需要遵循统一规范，或 Mapper / MyBatis 映射改动需要专项设计审查时使用本 Skill，例如：

- 新建表，或对既有表进行影响数据模型语义、兼容性或完整性的结构设计。
- 新增、删除或调整索引、唯一约束等关键约束。
- 涉及复杂结果映射、动态 SQL、分页策略或批量处理方案的 Mapper / Mapper XML 调整。
- 需要确定字段命名、类型、长度、默认值、审计规则或数据元语依据的设计评审。
- 需要新增或修改状态、类别、标志、模式等有限值字段，或核对数据库字段与字典值域的一致性。

不改变字段定义、值域或约束的常规业务赋值、普通 SQL、Entity/PO 和 Mapper/XML 局部调整，只检查数据库规范适用的 SQL、ORM、索引章节及受影响映射，无需进入本 Skill 的完整设计流程。纯业务代码同样无需使用；管理后台 前端或接口只涉及字典展示和返回时，由 `mgt-modification` Skill 路由到本 Skill 的字典值域资料。

## 按需查询参考资料

完整 Markdown 目录是维护来源，不另建人工维护的摘要；只读任务相关内容，不默认全文加载字段、元语或字典目录。

| 任务 | 必查资料 |
|---|---|
| 新建表 | [database-design-rules.md](references/database-design-rules.md) 全文及本次字段记录 |
| 字段定义或语义调整 | 数据库规范的命名、字段及相关章节；[standard-fields.md](references/standard-fields.md) 使用规则、来源说明及匹配记录 |
| 新名称无标准字段可复用 | 再查询 [data-primitives.md](references/data-primitives.md) 使用规则及相关元语 |
| 有限值编码设计或核对 | [dictionary-domains.md](references/dictionary-domains.md) 使用规则、治理规则及字段在对应场景的完整值域 |
| 索引、SQL、ORM 设计或调整 | 数据库规范适用章节；仅涉及字段属性或值域时查询对应目录 |

查询顺序：
1. 先读目标目录的使用规则；同一任务已读且未变化时不重复读取。
2. 用字段代码精确检索，未知代码时按中文业务名称检索；一次可组合查询多个字段。
3. 读取全部匹配记录及备注、主题域、修订记录；同码多义、场景别名、废弃编码和治理说明一起核对。值域不得只取首条或截断。
4. 无匹配时检查名称变体、别名及相关元语；仍缺失或语义冲突时说明缺口，不补造定义。
5. 结果保留来源文件和行号。目录互相链接仅用于导航，不代表递归全读。

项目同类表和映射可作为兼容性参考，不机械复制与规范冲突的历史写法。


## 固定查询工具与证据复用

优先使用 [reference_query.py](scripts/reference_query.py)，直接读取原目录，无第三方依赖或持久缓存。`field`（默认）同查字段和完整值域，`domain` 只输出值域，`primitive` 查询命名元语；支持多个字段代码或中文词。关联记录不代表同义字段，不自动替代业务判断。

```powershell
# 本机已验证的 Python；其他环境使用其可用的 Python 3。
python -B -X utf8 .agents/skills/database-design/scripts/reference_query.py REQUEST_STATUS REVIEW_RESULT
# 上述命令可追加：--kind domain / --kind primitive / --known 上次fingerprint
```

返回表头、完整行、来源路径与行号、使用和治理说明。`unmatched_terms` 或 `found=false` 表示需继续查证，不证明该业务概念不存在。原目录格式异常时退出码为 2，不使用部分结果。该工具不返回 MySQL 物理规范，仍按上方路由读取适用章节。

同一任务且完整结果仍在当前上下文时，可将上次 `fingerprint` 传入 `--known`；仅查询条件、资料和工具内容均未变化时返回 `unchanged`。新任务、上下文压缩后原结果不可见或业务场景改变时重新查询，不传旧指纹。工具只复用资料，不能据此认定数据库、接口或运行环境未变。

必要时用同一工具的 `--evidence 文件路径 [更多路径]` 获取源码内容指纹，记录“结论、适用场景、来源路径/行号、指纹”。再次依赖该结论前检查相关文件及新增调用方影响；发生变化则重读相关内容。运行数据、权限和配置环境等动态证据另行核验，禁止只凭源码指纹复用。

工具不可用时退回 `rg` 按原查询顺序检索，不为此安装数据库或中止正常排查。维护工具后运行 `scripts/test_reference_query.py` 检查完整性和指纹失效行为。

## 规范优先级与冲突处理

1. `database-design-rules.md` 定义 MySQL 物理设计、SQL 和 ORM 规范；保留强制要求与推荐项的区别，不将推荐项升级为硬性门槛。
2. `standard-fields.md` 是字段语义、标准代码和来源追溯依据；其中源系统类型、默认值与 MySQL 强制规范冲突时，以 `database-design-rules.md` 为准，并在方案中列明差异。
3. `data-primitives.md` 用于新名称的元语组合，不替代标准字段定义。
4. `dictionary-domains.md` 是有限值编码的唯一事实源；不得根据历史代码自行扩展、改写或合并值域。
5. 规范之间、规范与现有实现之间存在语义冲突或场景不明时，必须列为待确认项，不得静默选择。

## 工作流程

### 1. 明确影响范围

先确认业务含义、数据生命周期、读写场景、查询条件、排序分页方式、唯一性、并发与历史数据影响。信息不足时标记待确认，不自行假定字段语义、数据量、唯一性或保留期限。

### 2. 设计前检查

- 查找项目内同类表、字段、索引与 Mapper XML。
- 新字段先查标准字段目录；没有匹配项时再按数据元语表组合命名，不自行创造英文缩写。
- 状态、类别、标志、模式等有限值字段必须核对字典值域、适用场景和编码长度。
- 检查 MySQL 保留字、名称长度、字段类型、NOT NULL/默认值、注释和审计字段要求。
- 检查索引对应的实际 SQL：首字段是否进入 `WHERE`、组合索引首字段区分度、唯一性和更新成本。

### 3. 输出设计与变更方案

在实施前说明：

- 表、字段、索引的名称、类型、长度、默认值、`COMMENT` 与标准字段或数据元语依据。
- 有限值字段的值域、适用场景，以及数据库、Mapper、接口和前端之间的编码映射。
- 主键、审计字段、逻辑删除和乐观锁字段是否适用。
- 关键 SQL、查询字段、条件、分页与预期索引。
- 受影响的 Entity/PO、DTO/VO、Mapper、Mapper XML、Service 和接口。
- 兼容性、历史数据、回滚方式和待确认项。

未经明确授权不得执行 DDL、DCL、生产数据修改或删除操作；仅提供可审阅的 SQL 和回滚 SQL。

### 4. 实施要求

- 仅实施已确认范围，保持项目已有 MyBatis 使用方式。
- SQL 显式列出查询/写入字段，使用 `#{}` 参数绑定和 `resultMap`。
- 数据库字段采用 `is_xxx` 时，POJO 布尔属性不带 `is`，并在 `resultMap` 中映射。
- 结构变更同步更新相关 Entity/PO、Mapper、Mapper XML、DTO/VO、Service、接口和测试。

### 5. 验证

至少核对：

- SQL、字段、Entity/PO、Mapper XML 和 DTO/VO 一致。
- 有限值字段与字典值域一致，未知编码、废弃编码和跨场景别名均已处理。
- 索引与实际 `WHERE`、排序、唯一性需求一致。
- `EXPLAIN`（可执行时）核对实际计划；按规范推荐达到 `range`，优先 `ref` 或 `const`，结合查询场景说明结果，不作为一律阻塞的门槛。
- 变更 SQL 与精确回滚 SQL 已提供；不能执行的检查如实说明。

## 输出要求

按以下顺序简要汇报：设计依据、变更范围、SQL/回滚、受影响代码、验证结果和待确认风险。不要把完整公司规范重复写入需求方案。

## 英文译文 | English translation

Use this skill for the scope stated above. Keep the established workflow, authorization boundary, source evidence, and verification gates. Catalog entries and examples in this public project are illustrative; the target project's approved definitions take precedence.
