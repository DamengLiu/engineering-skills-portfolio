# 数据库设计规范

适用于采用 MySQL 与 MyBatis 的示例项目。`【强制】`和`【推荐】`保留原有分级含义，但以下命名、阈值和部署策略都是公开示例；接入真实项目时以其已批准规范为准。

## 1. 通用与命名

- 【强制】默认使用 InnoDB、utf8mb4；建表无需显式声明存储引擎和字符集。
- 【强制】生产环境禁止存储过程、触发器、视图和外键（开源软件除外）。大文件存对象存储或网络共享，数据库只存路径等索引信息。
- 【强制】名称仅用小写字母、数字和下划线，以字母开头，单词以单下划线分隔；禁止两个下划线中间仅数字（多级分表除外）；长度遵守目标数据库及项目规范；不得使用 MySQL 保留字。
- 【强制】数据库和表采用可读前缀，例如 `app_demo`、`request_item`；分库分表序号遵循目标项目约定。
- 【强制】唯一索引命名 `uk_字段名`，普通索引命名 `idx_字段名`；主键使用 MySQL 默认 Primary Key。
- 【强制】字段、表、索引命名先查询数据元语；已有元语能表达时必须复用。

## 2. 表与字段

- 【强制】每张表必须有自增物理主键：`id bigint(20) not null auto_increment`。
- 【强制】每张表包含 `create_time`、`update_time`；前台操作表还包含 `is_deleted`、`version`、`create_by`、`create_time`、`update_by`、`update_time`。
- 【强制】前台操作表审计字段按以下定义：

```sql
is_deleted tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '逻辑删除标志：1-是，0-否',
version int(10) unsigned NOT NULL DEFAULT '0' COMMENT '版本号',
create_by varchar(64) NOT NULL DEFAULT '' COMMENT '创建人',
create_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间戳',
update_by varchar(64) NOT NULL DEFAULT '' COMMENT '更新人',
update_time datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间戳'
```

- 【强制】字段必须有 `COMMENT`；状态字段必须在注释中列明全部状态值。
- 【强制】不使用数据库枚举类型；使用 `tinyint`。布尔字段命名为 `is_xxx`，类型为 `unsigned tinyint`，1 表示是、0 表示否。
- 【强制】小数使用 `decimal`，禁止 `float`、`double`；索引字段必须 `NOT NULL`。
- 【推荐】字段优先 `tinyint`、`int`、`bigint`、`varchar`、`char`，避免 `text`、`blob` 或超过 500 的大 `varchar`；日期/时间分别使用 `date`、`time`、`datetime`，时间戳用 `timestamp`。
- 【推荐】字段优先 `NOT NULL` 并提供默认值；时间字段使用 `NOT NULL DEFAULT CURRENT_TIMESTAMP`；字符优先 `varchar`，固定长度用 `char`。
- 【推荐】金额单位、精度和类型由业务契约明确；整数最小单位可使用 `bigint`，金额运算使用项目统一组件。
- 【推荐】单表字段数和分库分表阈值由目标项目按数据量、增长率和查询负载确定，不凭固定数字拆分。

## 3. 索引

- 【强制】联机库索引数量和组合索引字段数应受控；超出项目阈值时进行数据库与架构评审。
- 【强制】索引首字段必须出现在相关 SQL 的 `WHERE` 条件；组合索引首字段选择区分度高的字段。
- 【强制】不在更新频繁、区分度低字段上建索引；业务唯一字段（包括组合字段）必须建唯一索引。
- 【强制】页面搜索禁止左模糊或全模糊；需要时使用搜索引擎。
- 【推荐】SQL 性能至少达到 `range`，优先 `ref`，可达时使用 `const`。

## 4. SQL

- 【强制】使用 `count(*)` 统计行数；`SUM` 处理空值时使用 `IFNULL(SUM(column), 0)`。
- 【强制】禁止 `WHERE 1=1`、隐式类型转换、以 `%` 开头的模糊查询、对索引字段做数学/函数运算。
- 【强制】程序代码中禁止 DDL、DCL；`INSERT` 必须显式指定字段；查询必须显式列字段，禁止 `SELECT *`。
- 【强制】使用 `ISNULL()` 判断空值；分页查询 `count` 为 0 时直接返回；线上联机业务库禁止 `JOIN` 查询。
- 【推荐】SQL 关键字大写，表名和字段名小写；避免 `NOT IN`、`NOT LIKE`、`!=` 等负向查询。

## 5. ORM 与访问

- 【强制】统一使用 MyBatis；每表定义 `resultMap`，不得使用 `resultClass`、`HashMap` 或 `Hashtable` 直接承接查询结果。
- 【强制】POJO 布尔属性不加 `is`，数据库 `is_xxx` 字段在 `resultMap` 映射。
- 【强制】Mapper XML 使用 `#{}` 参数绑定，禁止 `${}`；更新记录必须同步更新 `update_time`。
- 【强制】禁止跨机房访问数据库，应用通过配置 DNS 域名连接；读写连接主库，大数据优先抽取本地备库。
- 【强制】数据库连接超时遵循目标项目及数据库配置。
- 【推荐】连接池大小按目标项目的并发、容量和数据库限制确定，并在流量高峰前预热。

## 6. 安全与历史数据

- 【强制】数据库账号不得明文公开于代码、配置、Wiki 等；不同线上业务不得共用账号，生产账号和权限须经 DBA 同意。
- 【强制】生产应用默认仅授予 `SELECT`、`INSERT`、`UPDATE`；`DELETE`、DDL 等需 DBA 审核。
- 【推荐】分库分表的历史数据清理方案提前与 DBA 沟通；历史数据清理以已确认的保留期限、归档结果和数据库评审为前提。

## 英文译文 | English translation

This reference describes project-specific decisions and checks for the workflow above. The public examples use fictional names; confirm the actual component, field, and policy in the target project before applying them.
