# 管理后台功能交付项目 | Admin Console Delivery Project

这个项目展示如何把“一个后台需求”从口头描述变成可续接、可定位、可验证的工程交付。它聚焦 Spring/MyBatis 风格的管理后台，但方法本身适用于需要页面、接口、权限、状态与数据模型协同的业务系统。

## 适合阅读的对象与关注点

适合关注后端、前端协作及业务系统风险控制的技术读者。以下问题可用于选择需要深入的材料。

| 关注点 | 仓库中的回答 |
| --- | --- |
| 如何避免需求迭代后依据旧结论实现？ | [功能交付 Skill](.agents/skills/mgt-feature-delivery/SKILL.md)将当前有效需求、范围、待确认项、开发批次和最终测试材料串联到 `index.md`。 |
| 如何判断改动风险，而不是凭代码行数猜测？ | [局部修改 Skill](.agents/skills/mgt-modification/SKILL.md)用 L0/L1/L2 区分唯一文件的低风险调整、常规页面/接口修改，以及公共契约、状态、权限、双人复核、外部调用和数据库设计。 |
| 如何避免字段、码值和字典展示靠猜？ | [数据库设计 Skill](.agents/skills/database-design/SKILL.md)按需查询标准字段、完整值域和元语；工具带来源行号、关联提示和内容指纹。 |
| 如何验证“改好了”覆盖了真正的调用链？ | 前端、后端、数据库、权限/双人复核分别有验证要求；实际采用哪些检查由风险等级和影响范围决定。 |

## 复用入口

先阅读本项目的 [AGENTS.md](AGENTS.md)，再按下面的“三条工作流”选择主 Skill。局部修改应准备真实页面 URL 或接口请求、对应代码与当前现象；完整功能交付还需当前有效需求与验收目标；数据库设计需要获批的结构、字段与字典资料。Skill 会据实际影响选择前端、后端或数据库细则，不能用公开的虚构目录替代目标项目的事实来源。

希望先检查可复验部分，可查看[虚构审批案例](examples/README.md)如何列出状态、权限和重复操作的验收条件，或按[仓库首页的离线命令](../../README.md#可复用的沉淀与证据边界)运行目录查询工具测试。这里没有可运行的管理后台应用；局部修改的预期交付是已定位的最小改动及按风险分级的验证结论，真实页面、接口和持久化结果须在接入项目中核验。

## 三条工作流

1. [完整功能交付](.agents/skills/mgt-feature-delivery/SKILL.md)：记录需求、原型、设计、开发批次与最终功能性测试。它区分本期核心功能、后续能力和待确认项，便于中断后继续，也避免把规划误写成已完成。
2. [局部修改](.agents/skills/mgt-modification/SKILL.md)：从运行路由或接口入口开始定位，围绕实际调用链做最小修改。对于 L2 改动，明确受影响契约、兼容性、回滚方式和组合验收。
3. [数据库设计](.agents/skills/database-design/SKILL.md)：处理字段语义、有限值、索引、SQL 和复杂 Mapper 映射；普通局部 SQL 不被无端升级成完整设计流程。

## 值得展开讨论的设计

### 1. 需求材料是工程输入，而不是会议纪要

每项功能都有稳定目录和 `index.md`。材料记录事实、决策、范围和验证结论，不粘贴长日志或大段源码。需求发生实质变化时更新当前有效版本并记录影响，让下一轮开发或修改能够追溯“为什么这样做”。

### 2. 风险分级来自契约与运行入口

L0 只适用于目标文件唯一、无动态路由歧义、无接口或数据语义变化的情况。一旦涉及页面入口、公共 DTO、权限、状态机、幂等、双人复核、外部调用或数据库，就按实际影响升级。这样可以避免把“只改几行”误判成低风险。

### 3. 目录查询工具让资料证据可复用也可失效

字段与字典资料不被复制成零散摘要。查询工具只读取相关目录并返回完整匹配行、来源位置和关联提示；查询条件、工具代码或资料内容改变时 fingerprint 会变化，提示使用者重新核验。公开仓库使用虚构目录来演示机制，真实项目必须替换为获批的资料来源。

## 可验证证据

- [目录查询工具](.agents/skills/database-design/scripts/reference_query.py)及其测试覆盖完整值域、关联码、废弃码、未知项、Markdown 表格格式和指纹失效。
- [虚构审批案例](examples/README.md)展示需求记录、数据模型审查与前后端修改三条工作流如何交接，并列出正常、越权、重复、并发和失败场景所需的验收证据。
- [项目约定](AGENTS.md)约束 Controller/Service/Mapper 分层、公共能力复用、异常处理和局部验证，避免 Skill 脱离既有工程上下文。

## English overview

This project demonstrates three cooperating workflows for an admin console: feature delivery, focused changes, and database design. The key ideas are to preserve the active requirements as engineering input, classify risk by contracts and runtime entry points instead of diff size, and use source-traceable catalog lookups whose evidence expires when the source changes. Readers need their own application code and approved field catalogs to adapt the Skills. Public catalogs and cases are fictional fixtures; the workflow and verification logic are preserved.
