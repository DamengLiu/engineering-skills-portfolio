# 需求材料布局

默认根目录：项目内的 `docs/feature-records/<feature-key>/`。`<feature-key>` 采用稳定、简短、可读的功能标识，例如 `approval-flow`。

## 最小材料

任何需要沉淀的功能至少维护：

```text
index.md
```

它可以包含需求、PRD、设计、批次和测试章节。小功能不要为了目录完整性拆出多个空文件。

## 内容扩大后的拆分

当单份材料不便维护，按已经进入的阶段创建，不要求一次创建全部文件：

```text
index.md                              当前状态、链接、变更记录、需求追踪
01-requirement/
  requirement.md                       需求澄清、范围、待确认项
  prd.md                               主流程、核心功能、后续能力和验收口径
02-prototype/
  prototype.md                         页面、交互、状态和原型链接/截图说明
03-design/
  api/
    api-design.md                      API 契约和兼容性决定；可按接口继续拆分
  data-model/
    data-model.md                      数据模型、字段、状态和存储设计
    sql/
      forward.sql                      设计中的变更 SQL
      rollback.sql                     与 forward.sql 对应的回滚 SQL
04-development/
  implementation.md                    分批开发记录与开发自检
05-functional-test/
  functional-test.md                   全部功能完成后的功能性测试
```

按已经进入的阶段创建目录和文件，不预建空目录。不涉及页面、数据模型、SQL 或原型时，省略相应目录。需要多个 API 或多个子功能时，可以在相应文件内继续分章节，或在同一阶段目录中按接口/子功能拆分。

## 记录边界

- `index.md` 是唯一续接入口，至少保留当前阶段、下一步、待确认项、材料链接和变更记录。
- 需求或 PRD 记录“当前有效结论”；变更记录保留为什么改、影响什么，不保留已失效结论作为当前规则。
- API、数据模型文档只记录已经确认或明确标记待确认的内容，不根据常见模式补造字段、错误码或状态。
- `03-design/api/` 保存 API 设计材料；`03-design/data-model/` 保存数据模型和设计 SQL。SQL 涉及表、字段、索引、约束或复杂映射时，按 `database-design` Skill 执行设计与核对。
- `04-development/implementation.md` 记录批次目标、实际影响范围、开发自检和遗留项；不把它写成最终功能测试报告。
- `05-functional-test/functional-test.md` 在全部功能开发完成后建立，记录测试范围、用例、结果、缺陷和未测边界。

## 模板

- 新建或续接入口使用 [index 模板](../assets/index.template.md)。
- 需要独立记录需求澄清时使用 [需求模板](../assets/requirement.template.md)。
