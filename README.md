# 工程实践作品集 | Engineering Skills Portfolio

这份作品集展示我如何把 Agent 参与的工程任务做成可定位、可交接、可验证的工作流。它包含两个脱敏项目：DataX 数据迁移与管理后台功能交付。公开版保留原项目的规则分工、关键判断和离线检查方式；名称、字段与示例数据已泛化或虚构。

## 内容与适合阅读的对象

适合关注数据正确性、后端与前端协作、平台工程或 Agent 工程化的技术面试官和同行阅读。这里重点说明**为什么这样设计、规则怎样落到任务、现有证据能证明什么**。想先了解全貌，可读本页；想检查可执行细节，可进入项目的 `AGENTS.md`、代表 Skill 和示例。

| 项目 | 工程内容 | 本页展开的代表 Skill | 其他 Skill 的职责 |
| --- | --- | --- | --- |
| [DataX 数据迁移](projects/data-migration/README.md) | 单表新建、已有作业修改、批量编排 | [单表新建](projects/data-migration/.agents/skills/datax-table-migration/SKILL.md)：从需求澄清到迁后校验的五阶段 | [单表修改](projects/data-migration/.agents/skills/datax-table-modify/SKILL.md)追踪已有作业的直接影响；[批量迁移](projects/data-migration/.agents/skills/datax-batch-migration/SKILL.md)管理任务清单、顺序和批次结论，不重定义单表映射 |
| [管理后台功能交付](projects/admin-console/README.md) | 完整交付、局部修改、数据库设计 | [局部修改](projects/admin-console/.agents/skills/mgt-modification/SKILL.md)：沿实际入口定位、控制影响并分级验收 | [完整功能交付](projects/admin-console/.agents/skills/mgt-feature-delivery/SKILL.md)维护需求与开发批次；[数据库设计](projects/admin-console/.agents/skills/database-design/SKILL.md)管理结构、字段语义和完整值域 |

两个项目均提供项目级 `AGENTS.md`、场景 Skill、按需读取的 reference，以及可审阅的样例或离线工具。以下只深入讲解每个项目的一个 Skill，以具体决策说明整体设计。

## 整体设计：规则分层，任务闭环

```text
项目 AGENTS.md：共同的架构、权限、质量和完成标准
       ↓
场景 Skill：任务入口、阶段步骤、专项判断和交付条件
       ↓
按需读取的 reference、模板与离线检查脚本
```

[`DataX AGENTS.md`](projects/data-migration/AGENTS.md)把数据库授权、Python/Shell 质量和“迁移完成”的口径放在项目层；[`管理后台 AGENTS.md`](projects/admin-console/AGENTS.md)约束分层、公共组件复用、接口兼容、权限和验证。两者都不替场景 Skill 决定具体步骤。场景 Skill 选择当前任务的入口与停止条件；reference 承载阶段细则；脚本处理适合确定性计算的检查。当前表的 mapping、当前需求和真实运行入口仍来自任务证据，不能被通用规则代替。

这样分工解决两类常见问题：一是同一权限或完成标准在多个 Skill 中复制后逐渐分叉；二是把所有资料一次塞给 Agent，使当前阶段的关键条件被无关内容淹没。分层并不降低标准：只读分析、文件修改、数据库查询和真实执行仍各按其权限边界判断。

这里还使用一个**解释工作方式**的双层循环模型。外层用 PDCA 管理任务目标、阶段推进与收尾：确定范围和验收口径，执行当前阶段，检查证据，再决定继续、修正或停止。内层是每个子任务的操控循环：先用已确认输入和门禁做前馈控制，再用差异、工具结果或业务核验做反馈控制。PDCA 是对这些规则的归纳表达，不是原始 Skill 自称采用的正式章节或新增流程。

| 工作步骤 | 设计决策 | 可见的约束与例子 |
| --- | --- | --- |
| 选择入口 | 按交付对象选择主 Skill，避免一个流程接管所有任务 | 批量 Skill 不接管单表字段映射；普通 SQL 局部调整不自动进入完整数据库设计 |
| 建立依据 | 为本次任务确定当前有效的事实来源 | 单表以当前 mapping 和可靠结构为准；后台先确认运行路由与接口，再查相关字段、字典目录 |
| 控制风险 | 项目约束给出共同边界，Skill 按实际影响升级 | 数据库操作须有环境、对象、范围、动作的授权；后台按 L0/L1/L2 判断契约和状态风险 |
| 执行与交接 | 每一步留下可检查的产物，作为下一步输入 | 单表的 mapping、Python、Shell、核验 SQL；后台的入口证据、必要修改和验证记录 |
| 验证与收尾 | 结论不能超过证据覆盖范围 | 列顺序通过不证明转换值正确；页面截图不证明后端权限或持久化回显 |

## 案例一：DataX 单表新建的五阶段

单表迁移最难发现的错误是作业正常结束，却写入了错列、错误码值或错误范围。[原流程保留的五阶段](projects/data-migration/.agents/skills/datax-table-migration/SKILL.md)把这一风险拆成五次有门禁的交接。每个阶段按“输入 → 判断与产物 → 检查 → 下一阶段条件”形成小闭环。

| 阶段 | 输入与关键判断 | 阶段产物、检查与门禁 |
| --- | --- | --- |
| 1. 需求澄清 | 读取可靠源/目标结构、当前已确认规则和参考作业；逐来源做五列映射；区分源业务键、目标业务键与物理主键；确认来源优先级、覆盖范围、重跑与清理、加密和不迁移字段 | 及时保存当前表的 `<target_table>_mapping.md`。目标字段、键、范围或转换仍待确认时标为“需求确认待定”，只交付映射，不生成可运行脚本 |
| 2. 脚本生成 | 已确认 mapping 是业务基线；每个来源独立生成作业，明确读取、转换、写入和日期传递 | 交付 mapping、DataX Python、Shell、核验 SQL 四类文件。[离线检查器](projects/data-migration/.agents/skills/datax-table-migration/scripts/check_artifacts.py)核对 mapping、查询列、Writer 和日期参数；固定值、码值及条件分支还要单独做[语义映射复核](projects/data-migration/.agents/skills/datax-table-migration/references/semantic-mapping-review.md)。全部必要检查通过才称“脚本生成完成” |
| 3. 迁移前检 | 对照运行环境和待迁数据，核查字段约束、长度精度、必填、日期、值域与键冲突 | 输出结构化前检结果；未执行的查询不能记作 0 或通过。必需条件未满足时停止，不启动 DataX |
| 4. 迁移执行 | 核对环境、对象、范围、动作的明确授权，以及已通过的前检 | 作业正常结束且 DataX 错误记录为 0，才得出“迁移执行成功”；这还不是“数据迁移完成” |
| 5. 迁后校验 | 使用同一 mapping 规定的范围、键和业务规则核对结果 | 核对数量关系、重复键、必填、固定值及关键业务字段；多来源过滤或覆盖时不能机械比较两边总数。执行与必要校验均通过，才报告“数据迁移完成” |

五阶段的关键不是增加表单，而是防止上一阶段的不确定性被下一阶段当成事实。[虚构订单案例](projects/data-migration/examples/README.md)故意把 Writer 一列改错：离线测试会拒绝这个结构错误。案例同时保留金额、状态和时间转换的语义问题，提醒读者结构检查无法证明转换值正确。[错误模式集](projects/data-migration/.agents/skills/datax-table-migration/references/failure-patterns.md)还记录日期参数在 Shell 与作业间丢失、作业成功但脏数据未核验等失效条件；这些模式是排查线索，最终结论仍须回到当前表证据。

## 案例二：管理后台局部修改的决策过程

后台的“小改动”可能落在同名动态页面、公共接口、权限或状态转换上。这里按[局部修改 Skill](projects/admin-console/.agents/skills/mgt-modification/SKILL.md)的**决策顺序**组织阅读，不把它改称原文并不存在的固定五阶段。

| 决策环节 | 必须确认的细节 | 交接与停止条件 |
| --- | --- | --- |
| 1. 判断请求与风险 | 区分排查、方案、直接实施和回滚；按真实影响判 L0/L1/L2。L0 只适用于目标文件唯一、无动态路由歧义、无接口或数据语义变化 | 只读请求交付发现；方案请求先交付方案。入口或影响不明确时继续定位，不把小 diff 自动判为低风险 |
| 2. 证明实际入口 | 前端用浏览器 URL、route、列表/详情组件与 API 建立“页面身份证”；后端从实际 URL、Method、参数追到 Controller → DTO/VO → Service → Mapper | 候选页面不唯一时暂停写入；运行请求与源码或服务版本不一致时先查环境，不在相似文件上补丁 |
| 3. 按影响读取资料 | 页面、后端、验证和历史案例各按需读取；字段与字典查询保留完整匹配值域和来源；结构或语义变化才进入完整数据库设计 | 形成受影响的调用链、字段含义和验证范围；普通 SQL 局部调整只查适用规范 |
| 4. 受控实施 | 复用项目既有组件与分层，只改必要文件。L2 进一步明确接口契约、兼容、权限、状态、双人复核、回滚和持久化影响 | 最终差异与授权目标一致；出现意外差异时停止相关写入并核查 |
| 5. 分级验收 | L1 验证目标页面或最小接口；L2 组合覆盖前后端、权限、状态、重复操作和再次查询后的回显 | 报告“已完成且已验证”“已实现未运行验证”“仅方案或 SQL”或“阻塞未完成”，不把局部通过扩写为整链路通过 |

[案例 C08](projects/admin-console/.agents/skills/mgt-modification/references/case-patterns.md)记录了根据菜单或目录猜组件，结果改到同名页面的失效模式；因此“页面身份证”成为写入前的约束。[案例 C03](projects/admin-console/.agents/skills/mgt-modification/references/case-patterns.md)说明双人复核场景应先查已有框架能力，并区分登录操作人与复核人；验收须检查权限、状态和最终数据。公开案例是脱敏的问题模式与验收方法，不冒充本仓库中可运行的后台应用或生产验收结果。

## 从两个案例提炼的最佳实践

| 方法 | 防止什么问题 | 本仓库如何说明或验证 |
| --- | --- | --- |
| 双层规则与双层循环 | 共性规则分叉、任务推进失控、局部检查越级代表整体完成 | 两份 `AGENTS.md` 统一架构与完成口径，代表 Skill 决定阶段；每阶段用输入、产物、检查和门禁闭环。外层追踪任务是否达到最终验收，内层根据检查结果修正当前子任务 |
| 渐进式信息披露 | 无关资料占满上下文、旧案例覆盖当前事实 | 先选场景与阶段，再只读相关 reference；用表名、字段、URL 或 API 精确检索，零命中或歧义时扩展。字典的完整匹配值域不能为节省上下文而截断 |
| 阶段产物作为下一阶段的输入契约 | 未确认规则被静默假设、执行结果无法复核 | 单表 mapping 固定字段与范围，四类交付物围绕它闭环；前检、执行和迁后校验分别产生不同状态。后台把入口证据、影响范围和验证结论逐步交接 |
| 确定性检查与语义判断分工 | 工具“绿灯”掩盖业务值错误 | 离线脚本能抓出 Writer 错列；码值、固定值、范围关系仍需语义复核和真实数据核验。页面静态检查也不能替代权限、状态与持久化验证 |
| 按实际风险做最小干预 | 因错误入口或过度改动扩大回归面 | 动态路由候选不唯一先停止写入；L0/L1/L2 决定所需定位与验收；普通 SQL 调整不自动升级为完整数据库设计，局部修改不触发全仓格式化 |

**渐进式读取的效果如何证明？** 仓库中的 Skill 已明确路由规则，但目前没有“全量加载”与“按需加载”的同任务对照数据，因此不宣称节省了多少 token 或提升了多少正确率。后续可用相同任务和模型分别执行两种读取策略，记录加载 token、无关资料数、关键约束遗漏数、无依据推断数和阶段门禁判断；只有在质量不下降且上下文负担下降时，才报告改进。这个评估方案也把“上下文更好”转成可检验的命题。

## 可复用的沉淀与证据边界

这两个项目沉淀了四种可迁移做法：把共同约束与场景步骤分开维护；用当前任务的事实文件或真实入口代替模型猜测；让阶段产物带着检查结论交给下一阶段；按风险和证据范围报告完成状态。迁移项目重在数据语义和运行门禁，后台项目重在入口证明、公共能力复用与联动验收。

仓库提供可运行的**离线证据**。以下命令使用虚构样例或临时数据，不连接数据库、不执行 DataX，也不启动管理后台：

```bash
python -X utf8 projects/data-migration/examples/check_job_columns.py projects/data-migration/examples/mapping.csv projects/data-migration/examples/job-manifest.json
python -X utf8 -m unittest discover -s projects/data-migration/examples -p "test_*.py"
python -X utf8 -m unittest discover -s projects/admin-console/.agents/skills/database-design/scripts -p "test_*.py"
```

迁移项目还包含[单表交付物检查器](projects/data-migration/.agents/skills/datax-table-migration/scripts/check_artifacts.py)与[批量交付物检查器](projects/data-migration/.agents/skills/datax-batch-migration/scripts/check_batch_artifacts.py)的自检入口；后台项目包含[字段与字典目录查询工具](projects/admin-console/.agents/skills/database-design/scripts/reference_query.py)。它们证明相应的离线规则可执行，不能证明真实系统的运行效果。原工程和原 Skill 未因公开作品集而修改；公开示例不含客户或生产数据。

## English overview

This portfolio presents two sanitized engineering projects through one representative Skill each: a five-stage DataX single-table migration and a risk-based admin-console modification workflow. Project-level `AGENTS.md` files set shared constraints; scenario Skills define decisions and handoffs; references and offline tools provide details when needed. The included tests support only their stated offline checks. Live migration, application behavior, and quantitative productivity gains are not claimed.
