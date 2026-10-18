# 管理后台项目 | Admin Console Project

本项目按原有职责拆分为完整功能交付、局部修改和数据库设计。公开版保留需求材料、分批开发、页面与接口定位、双人复核、幂等、字段目录查询和分级验收的流程；专有组件名与真实业务目录已替换为角色描述及虚构样例。

## 阅读顺序

1. [项目约定](AGENTS.md)：分层、公共组件、权限、日志和验证规则。
2. [完整功能交付](.agents/skills/mgt-feature-delivery/SKILL.md)：需求、原型、设计、开发批次与最终功能性测试。
3. [局部修改](.agents/skills/mgt-modification/SKILL.md)：L0/L1/L2 风险分级、前后端路由与验收。
4. [数据库设计](.agents/skills/database-design/SKILL.md)：规范、字段、字典和元语目录的按需查询。
5. [虚构审批案例](examples/README.md)：展示三个 Skill 的协作边界。

## 公开样例的边界

字段、字典和元语文件保持原查询工具所需的 9/7/4 列结构，并使用虚构数据验证完整值域、关联码、废弃码及指纹失效。它们仅演示机制；真实项目必须接入获批目录。数据库规范保留设计决策和强制/推荐层级，但具体项目阈值、命名和组件以目标工程为准。

## English translation

The project keeps separate skills for full feature delivery, focused modifications, and database design. It preserves layered implementation rules, dual review, idempotency, source-backed catalog lookup, and risk-based verification. Proprietary catalog entries and component names have been replaced with fictional fixtures or functional roles; production use requires approved project definitions.
