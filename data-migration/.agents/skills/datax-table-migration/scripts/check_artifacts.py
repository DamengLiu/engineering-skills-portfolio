#!/usr/bin/env python3
"""检查单表迁移完整交付或局部修改，不连接数据库或执行 DataX。"""

from __future__ import annotations

import argparse
import ast
import contextlib
import io
from datetime import date
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch


SELECT_STAR_PATTERN = re.compile(r"\bselect\s+\*", re.IGNORECASE)
QUOTED_ALIAS_PATTERN = re.compile(
    r'\bAS\s+"([A-Za-z_][A-Za-z0-9_]*)"', re.IGNORECASE)
REQUIRED_FUNCTIONS = (
    ("precheckMigration", "precheck_migration"),
    ("runMigration", "run_migration"),
    ("validateMigration", "validate_migration"),
)
REQUIRED_MAPPING_ITEMS = (
    "需求确认完成",
    "确认人",
    "确认日期",
    "源业务键",
    "目标业务键",
    "目标物理主键",
    "目标必填字段",
    "目标清理",
)
MAPPING_HEADERS = ("源字段", "源字段含义", "目标字段", "目标字段含义", "说明")
FIELD_NAME_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
RENDER_PARAMS = {"V_STARTDATE": date(2026, 9, 1), "V_ENDDATE": date(2026, 9, 7)}


class Report:
    """保存检查明细，分别报告已执行结果、覆盖程度和整体状态。"""

    def __init__(self) -> None:
        self.items: list[tuple[str, str]] = []
        self.missing_required_checks: list[str] = []

    def pass_(self, message: str) -> None:
        self.items.append(("PASS", message))

    def warn(self, message: str) -> None:
        self.items.append(("WARN", message))

    def fail(self, message: str) -> None:
        self.items.append(("FAIL", message))

    def skip(self, message: str, required: bool = False) -> None:
        """记录未执行项；仅必需检查缺失影响完成判定。"""
        self.items.append(("Skipped", message))
        if required:
            self.missing_required_checks.append(message)

    @property
    def failed(self) -> bool:
        return any(level == "FAIL" for level, _ in self.items)

    @property
    def incomplete(self) -> bool:
        return bool(self.missing_required_checks)

    def print(self) -> None:
        for level, message in self.items:
            print(f"[{level}] {message}")
        print()
        print("已执行检查：" + ("Failure" if self.failed else "Success"))
        print("必需检查覆盖：" + ("未完成" if self.incomplete else "已完成"))
        status = "Failure" if self.failed or self.incomplete else "Success"
        print("静态检查结果：" + status)


def read_text(path: Path, report: Report) -> str | None:
    """读取 UTF-8 文本，同时检查 BOM 和换行格式。"""
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        report.fail(f"{path.name} 含 UTF-8 BOM")
    if b"\r\n" in data or b"\r" in data:
        report.fail(f"{path.name} 不是 LF 换行")
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        report.fail(f"{path.name} 不是有效 UTF-8：{exc}")
        return None
    report.pass_(f"{path.name} 可按 UTF-8 读取")
    return text


def find_one(directory: Path, pattern: str, label: str, report: Report) -> Path | None:
    """查找唯一匹配文件；缺失或重复时记录失败。"""
    matches = sorted(directory.glob(pattern))
    if len(matches) != 1:
        names = "、".join(path.name for path in matches) or "无"
        report.fail(f"{label} 应有且仅有一个，实际为：{names}")
        return None
    report.pass_(f"找到{label}：{matches[0].name}")
    return matches[0]


def literal_assignments(tree: ast.AST) -> dict[str, object]:
    """提取模块顶层可安全求值的常量赋值。"""
    values: dict[str, object] = {}
    for node in getattr(tree, "body", []):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        try:
            values[target.id] = ast.literal_eval(node.value)
        except (ValueError, TypeError):
            continue
    return values


def query_shape(tree: ast.AST, report: Report, filename: str) -> tuple[str, str] | None:
    """不执行作业代码，提取字面量或 f-string 的 SQL 形状。"""
    for node in getattr(tree, "body", []):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or target.id not in ("SOURCE_QUERY", "querySql"):
            continue
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return target.id, node.value.value
        if not isinstance(node.value, ast.JoinedStr):
            return None
        parts = []
        for part in node.value.values:
            if isinstance(part, ast.Constant) and isinstance(part.value, str):
                parts.append(part.value)
            elif isinstance(part, ast.FormattedValue):
                if isinstance(part.value, ast.Name) and part.value.id.startswith("V_"):
                    report.fail(
                        f"{filename} 将 {part.value.id} 当作 Python f-string 变量；"
                        "DataX 日期占位符应保留到参数渲染阶段"
                    )
                parts.append("__DYNAMIC_SQL_EXPRESSION__")
        report.warn(f"{filename} 含动态 SQL 表达式；仅检查静态 SQL 形状和参数")
        return target.id, "".join(parts)
    return None


def check_render_params(
    query: str, filename: str, report: Report, required: bool,
) -> None:
    """以样例日期复现 DataX 的字符串参数替换，不访问外部环境。"""
    if not re.search(r"\{+V_(?:STARTDATE|ENDDATE)\b", query):
        report.skip(f"{filename} 未发现日期占位符；日期参数渲染不适用")
        return
    try:
        rendered = query.format(**RENDER_PARAMS)
    except KeyError as exc:
        report.skip(
            f"{filename} 使用未提供样例值的参数 {exc}；需核对运行参数",
            required=required,
        )
        return
    except (ValueError, IndexError, AttributeError, TypeError) as exc:
        report.fail(f"{filename} SQL 参数渲染失败：{exc}")
        return
    if re.search(r"\{V_(?:STARTDATE|ENDDATE)(?::[^}]*)?\}", rendered):
        report.fail(f"{filename} 日期占位符在渲染后仍未替换")
    else:
        report.pass_(f"{filename} SQL 日期参数离线渲染通过；不验证 SQL 语义")


def describe_column_mismatch(aliases: list[str], columns: list[str]) -> str:
    """返回首个字段错位位置，避免在检查结果中输出完整字段列表。"""
    for position, (alias, column) in enumerate(zip(aliases, columns), start=1):
        if alias != column:
            return (
                f"第 {position} 列不一致：查询={alias}，Writer={column}；"
                f"查询列数={len(aliases)}，Writer 列数={len(columns)}"
            )
    position = min(len(aliases), len(columns)) + 1
    query_column = aliases[position - 1] if len(aliases) >= position else "无"
    writer_column = columns[position - 1] if len(columns) >= position else "无"
    return (
        f"第 {position} 列不一致：查询={query_column}，Writer={writer_column}；"
        f"查询列数={len(aliases)}，Writer 列数={len(columns)}"
    )


def check_mapping(path: Path, report: Report) -> str | None:
    """检查需求基线文件包含必要确认信息且没有待确认状态。"""
    text = read_text(path, report)
    if text is None:
        return None
    for item in REQUIRED_MAPPING_ITEMS:
        if item not in text:
            report.fail(f"{path.name} 缺少“{item}”")
    if "待确认" in text or "需求确认待定" in text:
        report.fail(f"{path.name} 仍包含待确认项")
    else:
        report.pass_(f"{path.name} 未发现待确认项")
    return text


def mapping_columns(text: str, sources: list[str]) -> dict[str, list[str]]:
    """从五列表格取各来源目标字段；多来源以来源标题划分。"""
    result, _ = mapping_target_rules(text, sources)
    return result


def mapping_target_rules(
    text: str, sources: list[str],
) -> tuple[dict[str, list[str]], dict[str, set[str]]]:
    """提取逐来源目标字段及以 ``FIELD*`` 标记的加密字段。"""
    result: dict[str, list[str]] = {source: [] for source in sources}
    encrypted: dict[str, set[str]] = {source: set() for source in sources}
    current_source = sources[0] if len(sources) == 1 else None
    in_mapping_table = False
    for line in text.splitlines():
        if line.startswith("#"):
            matches = [source for source in sources if source.upper() in line.upper()]
            if matches:
                current_source = max(matches, key=len)
            in_mapping_table = False
            continue
        if not line.startswith("|"):
            in_mapping_table = False
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if tuple(cells) == MAPPING_HEADERS:
            in_mapping_table = True
            continue
        if not in_mapping_table or len(cells) != 5 or current_source is None:
            continue
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
            continue
        target = cells[2].strip("` ")
        if target in ("无", "不迁移", "—", "-"):
            continue
        # ``DBTR_*`` 一类历史通配写法不是单字段的加密标记；只有
        # ``FIELD*`` 才表示该单一目标字段需要加密。
        if target.endswith("*") and not target.endswith("_*"):
            target = target[:-1].rstrip()
            encrypted[current_source].add(target)
        if "写入前加密" in cells[4]:
            encrypted[current_source].add(target)
        result[current_source].append(target)
    return result, encrypted


def encryption_columns(
    values: dict[str, object], path: Path, report: Report,
) -> set[str] | None:
    """读取作业的显式加密字段常量，不执行作业代码。"""
    declared = values.get("ENCRYPT_COLUMNS")
    if declared is None:
        return None
    if not isinstance(declared, (list, tuple, set)) or not all(
        isinstance(column, str) for column in declared
    ):
        report.fail(f"{path.name} 的 ENCRYPT_COLUMNS 必须是字符串集合")
        return None
    return set(declared)


def check_encryption_closure(
    text: str, jobs: list[tuple[Path, dict[str, object]]], report: Report,
    required: bool = True, all_sources: list[str] | None = None,
) -> None:
    """核对 mapping 加密标记、Writer 列和 dx_encrypt 配置。"""
    sources = [
        str(values.get("SOURCE_TABLE") or path.stem.split("_to_")[0])
        for path, values in jobs
    ]
    mapped, mapped_encrypted = mapping_target_rules(text, all_sources or sources)
    explicit = re.findall(r"(?m)^\s*[-*]?\s*目标加密字段[：:]\s*(.+)$", text)
    global_columns = None
    if explicit:
        global_columns = set(FIELD_NAME_PATTERN.findall(" ".join(explicit)))
        if not global_columns and any(value.strip() != "无" for value in explicit):
            report.skip("目标加密字段清单无法静态解析", required=True)
            return
    for (path, values), source in zip(jobs, sources):
        expected = mapped_encrypted[source]
        declared = encryption_columns(values, path, report)
        if global_columns is not None:
            expected = global_columns.intersection(mapped[source])
            if mapped_encrypted[source] - global_columns:
                report.fail(f"{path.name} 的逐来源加密说明与目标加密清单冲突")
        elif not expected and declared:
            report.skip(f"{path.name} 缺少可识别的 mapping 加密依据，需人工核对", required=True)
            continue
        has_transformer = values.get("ENCRYPT_BINDING")
        writer_columns = values.get("TARGET_COLUMNS", values.get("WRITER_COLUMNS"))
        if expected and (
            not isinstance(writer_columns, list)
            or not all(isinstance(column, str) for column in writer_columns)
        ):
            report.skip(
                f"{path.name} Writer 字段不可静态读取，未核对加密字段",
                required=True,
            )
            continue
        if expected and not expected.issubset(set(writer_columns)):
            report.fail(
                f"{path.name} 的加密字段不在 Writer 中："
                f"{sorted(expected - set(writer_columns))[:5]}"
            )
        if expected and declared is None:
            report.fail(f"{path.name} 缺少 ENCRYPT_COLUMNS，无法覆盖 mapping 加密字段")
            continue
        if (expected or declared) and has_transformer is not True:
            report.skip(f"{path.name} 未确认 transformer 中 dx_encrypt 的 columnNames 引用 ENCRYPT_COLUMNS，需人工核对", required=True)
            continue
        if declared is None:
            continue
        if declared != expected:
            report.fail(
                f"{path.name} 的 ENCRYPT_COLUMNS 与 mapping 加密字段不一致："
                f"缺少 {sorted(expected - declared)[:5]}，"
                f"多出 {sorted(declared - expected)[:5]}"
            )
        elif expected and expected.issubset(set(writer_columns)):
            report.pass_(f"{path.name} 加密字段与静态 transformer 参数一致（{len(expected)} 列）；运行时使用和处理顺序需复核")


def encryption_binding(tree: ast.AST) -> bool:
    """只识别 transformer 列表中的配置；不执行模块或假定动态组装结果。"""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if not isinstance(key, ast.Constant) or key.value != "transformer":
                continue
            if not isinstance(value, (ast.List, ast.Tuple)):
                continue
            configs = []
            for item in value.elts:
                if not isinstance(item, ast.Dict):
                    continue
                fields = {k.value: v for k, v in zip(item.keys, item.values)
                          if isinstance(k, ast.Constant)}
                name = fields.get("name")
                if isinstance(name, ast.Constant) and name.value == "dx_encrypt":
                    configs.append(fields)
            if len(configs) != 1:
                continue
            parameter = configs[0].get("parameter")
            if isinstance(parameter, ast.Dict):
                for k, v in zip(parameter.keys, parameter.values):
                    if (isinstance(k, ast.Constant) and k.value == "columnNames"
                            and isinstance(v, ast.Name) and v.id == "ENCRYPT_COLUMNS"):
                        return True
    return False


def check_mapping_closure(
    text: str, jobs: list[tuple[Path, dict[str, object]]], report: Report,
    required: bool = True, all_sources: list[str] | None = None,
) -> None:
    """逐来源比较 mapping 与 Writer 的目标字段集合。"""
    sources = [
        str(values.get("SOURCE_TABLE") or path.stem.split("_to_")[0])
        for path, values in jobs
    ]
    mapped = mapping_columns(text, all_sources or sources)
    for (path, values), source in zip(jobs, sources):
        columns = values.get("TARGET_COLUMNS", values.get("WRITER_COLUMNS"))
        if not isinstance(columns, list) or not all(
            isinstance(column, str) for column in columns
        ):
            report.skip(
                f"{path.name} Writer 字段不可静态读取，未核对 mapping 闭环",
                required=required,
            )
            continue
        targets = mapped[source]
        if not targets:
            report.skip(
                f"{path.name} 未找到来源 {source} 的五列映射，未核对闭环",
                required=required,
            )
            continue
        ambiguous = sorted({target for target in targets if not FIELD_NAME_PATTERN.fullmatch(target)})
        if ambiguous:
            report.skip(
                f"{path.name} 的 mapping 目标字段未逐项列明：{ambiguous[:3]}；需人工展开",
                required=required,
            )
            continue
        duplicates = sorted({target for target in targets if targets.count(target) > 1})
        if duplicates:
            report.fail(f"{path.name} 的 mapping 重复列出目标字段：{duplicates}")
        missing = sorted(set(columns) - set(targets))
        extra = sorted(set(targets) - set(columns))
        if missing or extra:
            report.fail(
                f"{path.name} 的 mapping 与 Writer 不闭环："
                f"mapping 缺少 {missing[:5]}，Writer 缺少 {extra[:5]}"
            )
        elif not duplicates:
            report.pass_(f"{path.name} 的 mapping 与 Writer 逐来源字段闭环（{len(columns)} 列）")


def check_python(
    path: Path, report: Report, require_contract: bool = True,
) -> dict[str, object]:
    """检查 Python 语法、核心常量及查询列与 Writer 列的一致性。"""
    text = read_text(path, report)
    if text is None:
        return {}
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        report.fail(f"{path.name} Python 语法错误：第 {exc.lineno} 行 {exc.msg}")
        return {}
    report.pass_(f"{path.name} Python 语法正确")

    if "_to_" in path.stem:
        report.pass_(f"{path.name} 使用来源表到目标表命名")
    elif re.fullmatch(r"[A-Z][A-Za-z0-9]*", path.stem):
        report.warn(f"{path.name} 使用兼容的历史 UpperCamelCase 文件名")
    else:
        report.warn(f"{path.name} 未使用 UpperCamelCase；继续执行兼容检查")

    values = literal_assignments(tree)
    values["ENCRYPT_BINDING"] = encryption_binding(tree)
    shaped_query = query_shape(tree, report, path.name)
    if shaped_query is not None and shaped_query[0] not in values:
        values[shaped_query[0]] = shaped_query[1]
    required = ("SOURCE_TABLE", "TARGET_TABLE", "PRE_SQL")
    for name in required:
        if name not in values:
            if require_contract:
                report.fail(f"{path.name} 缺少可静态读取的 {name}")
            else:
                report.warn(f"{path.name} 无法静态读取 {name}，需人工复核对应规则")

    query_name = "SOURCE_QUERY" if "SOURCE_QUERY" in values else "querySql"
    columns_name = "TARGET_COLUMNS" if "TARGET_COLUMNS" in values else "WRITER_COLUMNS"
    query = values.get(query_name)
    columns = values.get(columns_name)
    for name in (query_name, columns_name):
        if name not in values:
            if require_contract:
                report.fail(f"{path.name} 缺少可静态读取的 {name}")
            else:
                report.warn(f"{path.name} 无法静态读取 {name}，需人工复核对应规则")
    if query_name != "SOURCE_QUERY" or columns_name != "TARGET_COLUMNS":
        report.warn(
            f"{path.name} 使用兼容字段名 {query_name} / {columns_name}；"
            "已按相同规则检查字段顺序"
        )

    if query_name in values and not isinstance(query, str):
        report.fail(f"{path.name} 的 {query_name} 必须是字符串")
    if columns_name in values and (
        not isinstance(columns, list)
        or not columns
        or not all(isinstance(item, str) for item in columns)
    ):
        report.fail(f"{path.name} 的 {columns_name} 必须是非空字符串列表")
    if isinstance(query, str):
        check_render_params(query, path.name, report, required=require_contract)
        if SELECT_STAR_PATTERN.search(query):
            report.fail(f"{path.name} 的 SOURCE_QUERY 使用了 SELECT *")
        aliases = QUOTED_ALIAS_PATTERN.findall(query)
        if not aliases:
            report.fail(f"{path.name} 的 SOURCE_QUERY 未找到双引号目标别名")
        elif isinstance(columns, list) and all(isinstance(item, str) for item in columns):
            if aliases == columns:
                report.pass_(f"{path.name} 查询别名与 Writer 列静态匹配；不验证 SQL 语义")
            else:
                report.fail(
                    f"{path.name} 的 {query_name} 与 {columns_name} 不一致："
                    f"{describe_column_mismatch(aliases, columns)}"
                )
    if isinstance(columns, list) and all(isinstance(item, str) for item in columns):
        duplicates = sorted(
            {item for item in columns if columns.count(item) > 1})
        if duplicates:
            report.fail(f"{columns_name} 存在重复字段：{duplicates}")
        else:
            report.pass_(f"{columns_name} 不存在重复字段")

    pre_sql = values.get("PRE_SQL")
    if isinstance(pre_sql, list) and pre_sql:
        report.warn("PRE_SQL 已启用；须另行确认迁移范围、清理规则和执行授权")
    elif isinstance(pre_sql, list):
        report.pass_("PRE_SQL 默认未启用")
    return values


def run_shell_syntax(
    shell: str, path: Path, report: Report, required: bool = True,
) -> None:
    """本机存在对应 Shell 时执行语法检查，否则明确标记未执行。"""
    executable = shutil.which(shell)
    if executable is None:
        report.skip(f"本机没有 {shell}，未执行 {shell} -n", required=required)
        return
    result = subprocess.run(
        [executable, "-n", str(path)],
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        report.pass_(f"{path.name} 通过 {shell} -n")
    else:
        raw_detail = result.stderr or result.stdout
        if b"\x00" in raw_detail:
            detail = raw_detail.decode("utf-16-le", errors="replace").strip()
        else:
            detail = raw_detail.decode("utf-8", errors="replace").strip()
        unavailable_markers = (
            "CreateInstance", "E_ACCESSDENIED", "WSL", "Service/")
        if any(marker.lower() in detail.lower() for marker in unavailable_markers):
            report.skip(
                f"{shell} 当前不可用，未完成 {shell} -n：{detail}",
                required=required,
            )
        else:
            report.fail(f"{path.name} 未通过 {shell} -n：{detail}")


def check_shell(path: Path, python_paths: list[Path], report: Report) -> None:
    """检查入口对各来源作业的显式文件引用及三个核心阶段。"""
    text = read_text(path, report)
    if text is None:
        return
    if not text.startswith("#!/bin/bash"):
        report.fail(f"{path.name} 未使用 #!/bin/bash")
    if path.name == f"{path.parent.name}_migrate.sh":
        report.pass_(f"{path.name} 使用单表 Shell 命名")
    elif path.name.startswith("run_datasync_jobs_dataTransfer_"):
        report.warn(f"{path.name} 使用兼容的历史 Shell 命名")
    else:
        report.warn(f"{path.name} 使用其他入口名称；继续执行兼容检查")
    try:
        active_text = "\n".join(shlex.split(text, comments=True))
    except ValueError as exc:
        report.fail(f"{path.name} 无法静态解析作业引用：{exc}")
        active_text = ""
    references = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*\.py\b", active_text))
    for python_path in python_paths:
        if python_path.name not in references:
            report.fail(f"{path.name} 未显式引用 {python_path.name}，需核对调用方式")
        else:
            report.pass_(f"{path.name} 引用了 {python_path.name}")
    for reference in sorted(references):
        if reference == "datax.py":
            continue  # DataX 外部入口不属于目标目录的来源作业。
        if not (path.parent / reference).is_file():
            report.fail(f"{path.name} 引用的 Python 文件不存在于目标目录：{reference}")
    if not re.search(r"(?m)^\s*export\s+DATAX_HOME(?:\s|$)", text):
        report.fail(f"{path.name} 未导出 DATAX_HOME")
    for current_name, legacy_name in REQUIRED_FUNCTIONS:
        if re.search(rf"(?m)^\s*{re.escape(current_name)}\s*\(\)", text):
            continue
        if re.search(rf"(?m)^\s*{re.escape(legacy_name)}\s*\(\)", text):
            report.warn(f"{path.name} 使用兼容的历史方法 {legacy_name}()")
            continue
        report.fail(f"{path.name} 缺少 {current_name}() 或兼容方法 {legacy_name}()")
    run_shell_syntax("bash", path, report)
    run_shell_syntax("sh", path, report)


def check_sql(path: Path, values: dict[str, object], report: Report) -> None:
    """检查人工核验 SQL 非空，并覆盖已声明的源表和目标表。"""
    text = read_text(path, report)
    if text is None:
        return
    if not text.strip():
        report.fail(f"{path.name} 内容为空")
        return
    for name in ("SOURCE_TABLE", "TARGET_TABLE"):
        table = values.get(name)
        if isinstance(table, str) and table.lower() not in text.lower():
            report.fail(f"{path.name} 未引用 {name}={table}")
    report.pass_(f"{path.name} 已完成基本引用检查")


def check_directory(directory: Path) -> Report:
    """检查统一 mapping、各来源作业、Shell 和总核验 SQL。"""
    report = Report()
    if not directory.is_dir():
        report.fail(f"目录不存在：{directory}")
        return report

    python_paths = sorted(
        path for path in directory.glob("*.py") if path.name != "__init__.py"
    )
    if not python_paths:
        report.fail("未找到来源 Python 作业")
    shell_path = find_one(directory, "*.sh", "Shell 入口", report)
    mapping_path = find_one(directory, "*_mapping.md", "mapping 文件", report)
    sql_path = find_one(directory, "*_check.sql", "核验 SQL", report)
    if not python_paths or None in (shell_path, mapping_path, sql_path):
        return report

    assert shell_path is not None
    assert mapping_path is not None
    assert sql_path is not None
    mapping_text = check_mapping(mapping_path, report)
    target_tables = set()
    jobs = []
    for python_path in python_paths:
        values = check_python(python_path, report)
        jobs.append((python_path, values))
        target_table = values.get("TARGET_TABLE")
        if isinstance(target_table, str):
            target_tables.add(target_table)
        check_sql(sql_path, values, report)
    if mapping_text is not None:
        check_mapping_closure(mapping_text, jobs, report)
        check_encryption_closure(mapping_text, jobs, report)
    if len(target_tables) > 1:
        report.fail(f"来源作业的目标表不一致：{sorted(target_tables)}")
    elif len(target_tables) == 1:
        target_table = next(iter(target_tables))
        expected_mapping = f"{target_table}_mapping.md"
        expected_sql = f"{target_table}_check.sql"
        if mapping_path.name == expected_mapping:
            report.pass_(f"{mapping_path.name} 使用目标表 mapping 命名")
        else:
            report.warn(
                f"{mapping_path.name} 使用兼容的历史 mapping 命名；"
                f"新建或明确整改时使用 {expected_mapping}"
            )
        if sql_path.name == expected_sql:
            report.pass_(f"{sql_path.name} 使用目标表核验 SQL 命名")
        else:
            report.warn(
                f"{sql_path.name} 使用兼容的历史核验 SQL 命名；"
                f"新建或明确整改时使用 {expected_sql}"
            )
    check_shell(shell_path, python_paths, report)
    return report


def check_files(directory: Path, filenames: list[str]) -> Report:
    """只检查指定修改文件，不要求补齐整套历史交付物。"""
    report = Report()
    root = directory.resolve()
    if not root.is_dir():
        report.fail(f"目录不存在：{root}")
        return report
    paths = sorted({(root / filename).resolve() for filename in filenames})
    changed_jobs: list[tuple[Path, dict[str, object]]] = []
    mapping_changed = any(path.name.endswith("_mapping.md") for path in paths)
    for path in paths:
        if not path.is_relative_to(root):
            report.fail(f"修改文件超出目标目录：{path}")
            continue
        if not path.is_file():
            report.fail(f"修改文件不存在：{path}")
            continue
        if path.suffix == ".py":
            changed_jobs.append((path, check_python(path, report, require_contract=False)))
        elif path.suffix == ".sh":
            if read_text(path, report) is not None:
                run_shell_syntax("bash", path, report)
                run_shell_syntax("sh", path, report)
        elif path.suffix in (".md", ".sql"):
            read_text(path, report)
        else:
            report.fail(f"不支持的修改文件类型：{path.name}")
    if changed_jobs or mapping_changed:
        mappings = sorted(root.glob("*_mapping.md"))
        if len(mappings) == 1:
            try:
                mapping_text = mappings[0].read_text(encoding="utf-8-sig")
            except UnicodeDecodeError as exc:
                report.fail(f"{mappings[0].name} 不是有效 UTF-8：{exc}")
                mapping_text = None
            jobs = changed_jobs
            if mapping_changed:
                jobs = []
                for path in sorted(root.glob("*.py")):
                    if path.name == "__init__.py":
                        continue
                    try:
                        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
                        values = literal_assignments(tree)
                        values["ENCRYPT_BINDING"] = encryption_binding(tree)
                    except (UnicodeDecodeError, SyntaxError) as exc:
                        report.warn(f"{path.name} 无法读取关联字段：{exc}")
                        continue
                    jobs.append((path, values))
            if mapping_text is not None and jobs:
                all_sources = [
                    path.stem.split("_to_")[0]
                    for path in root.glob("*.py") if path.name != "__init__.py"
                ]
                all_sources.extend(
                    str(values.get("SOURCE_TABLE") or path.stem.split("_to_")[0])
                    for path, values in jobs
                )
                check_mapping_closure(
                    mapping_text, jobs, report, required=False,
                    all_sources=sorted(set(all_sources)),
                )
                check_encryption_closure(
                    mapping_text, jobs, report, required=False,
                    all_sources=sorted(set(all_sources)),
                )
        else:
            report.warn("局部修复未找到唯一 mapping，未核对逐来源字段闭环")
    report.warn("局部修复模式：直接关联业务规则需人工复核；不代表完整交付验收")
    return report


def self_test() -> int:
    """用临时交付物验证边界；模拟 Shell 检查，不运行真实迁移。"""
    optional_report = Report()
    optional_report.warn("代码风格待优化")
    with patch.object(shutil, "which", return_value=None):
        run_shell_syntax(
            "optional-shell", Path("optional.sh"), optional_report, required=False,
        )
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        optional_report.print()
    if (
        optional_report.failed
        or optional_report.incomplete
        or "静态检查结果：Success" not in output.getvalue()
    ):
        print("自检失败：可选检查未执行不应影响整体状态")
        return 1

    def write_fixture(path: Path, content: str) -> None:
        path.write_text(content, encoding="utf-8", newline="\n")

    def job_text(
        source: str, column: str = "ID", encrypt_columns: list[str] | None = None,
    ) -> str:
        text = (
            f"SOURCE_TABLE = '{source}'\nTARGET_TABLE = 'T_TARGET'\n"
            f"SOURCE_QUERY = 'SELECT ID AS \"ID\" FROM {source}'\n"
            f"TARGET_COLUMNS = ['{column}']\nPRE_SQL = []\n"
        )
        if encrypt_columns is not None:
            text += (
                f"ENCRYPT_COLUMNS = {encrypt_columns!r}\n"
                "JOB = {'transformer': [{'name': 'dx_encrypt', "
                "'parameter': {'columnNames': ENCRYPT_COLUMNS}}]}\n"
            )
        return text

    def mapping_text(*sources: str) -> str:
        header = (
            "需求确认完成\n确认人：测试\n确认日期：2026-09-29\n"
            "源业务键：ID\n目标业务键：ID\n目标物理主键：ID\n"
            "目标必填字段：ID\n目标清理：不清理\n"
        )
        sections = "".join(
            f"\n## {source} 字段映射\n"
            "| 源字段 | 源字段含义 | 目标字段 | 目标字段含义 | 说明 |\n"
            "|---|---|---|---|---|\n"
            "| ID | 主键 | ID | 主键 | 直接迁移 |\n"
            for source in sources
        )
        return header + sections

    def complete_report(directory: Path) -> Report:
        # 模拟可用解释器及成功退出，单独测试不可用和失败分支。
        with patch.object(shutil, "which", return_value="test-shell"), patch.object(
            subprocess, "run",
            return_value=subprocess.CompletedProcess([], 0, b"", b""),
        ):
            return check_directory(directory)

    with tempfile.TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir) / "T_TARGET"
        directory.mkdir()
        mapping = directory / "T_TARGET_mapping.md"
        write_fixture(mapping, mapping_text("SRC"))
        python_path = directory / "SRC_to_T_TARGET.py"
        write_fixture(python_path, job_text("SRC"))
        shell_path = directory / "T_TARGET_migrate.sh"
        shell_text = (
            "#!/bin/bash\nexport DATAX_HOME\nJOB_SCRIPT='SRC_to_T_TARGET.py'\n"
            "precheckMigration() { :; }\nrunMigration() { :; }\n"
            "validateMigration() { :; }\n"
        )
        write_fixture(shell_path, shell_text)
        write_fixture(
            directory / "T_TARGET_check.sql",
            "SELECT COUNT(*) FROM SRC;\nSELECT COUNT(*) FROM SRC_TWO;\n"
            "SELECT COUNT(*) FROM T_TARGET;\n",
        )
        report = complete_report(directory)
        if report.failed or report.incomplete:
            report.print()
            return 1

        encrypted_mapping = mapping_text("SRC").replace(
            "| ID | 主键 | ID | 主键 | 直接迁移 |",
            "| ID | 主键 | ID* | 主键 | 直接迁移 |",
        )
        write_fixture(mapping, encrypted_mapping)
        write_fixture(python_path, job_text("SRC", encrypt_columns=["ID"]))
        encrypted_report = complete_report(directory)
        if encrypted_report.failed or encrypted_report.incomplete:
            print("自检失败：加密字段闭环被误报")
            return 1
        write_fixture(mapping, mapping_text("SRC") + "\n目标加密字段：`ID`\n")
        for filenames in ([python_path.name], [mapping.name]):
            report = check_files(directory, filenames)
            if report.failed or report.incomplete:
                report.print()
                return 1
        for invalid_job in (
            job_text("SRC") + "ENCRYPT_COLUMNS = ['ID']\nNOTE = 'dx_encrypt'\n",
            job_text("SRC", encrypt_columns=["ID"]).replace(
                "'columnNames': ENCRYPT_COLUMNS", "'columnNames': ['OTHER']",
            ),
        ):
            write_fixture(python_path, invalid_job)
            report = complete_report(directory)
            if not (report.failed or report.incomplete):
                print("自检失败：未绑定的加密配置被误判通过")
                return 1
        write_fixture(python_path, job_text("SRC", encrypt_columns=["ID"]))
        write_fixture(mapping, mapping_text("SRC").replace(
            "| 直接迁移 |", "| 写入前加密 |",
        ))
        report = complete_report(directory)
        if report.failed or report.incomplete:
            report.print()
            return 1
        write_fixture(mapping, encrypted_mapping)
        write_fixture(python_path, job_text("SRC", encrypt_columns=[]))
        if not complete_report(directory).failed:
            print("自检失败：加密字段与 mapping 不一致未被识别")
            return 1
        write_fixture(mapping, mapping_text("SRC"))
        write_fixture(python_path, job_text("SRC"))
        legacy_shell = directory / "run_datasync_jobs_dataTransfer_T_TARGET.sh"
        shell_path.rename(legacy_shell)
        legacy_report = complete_report(directory)
        if legacy_report.failed or not any(
            "兼容的历史 Shell 命名" in message
            for _, message in legacy_report.items
        ):
            print("自检失败：历史 Shell 命名未保持兼容")
            return 1
        legacy_shell.rename(shell_path)

        mapping.rename(directory / "source_to_target_mapping.md")
        mapping = directory / "source_to_target_mapping.md"
        write_fixture(mapping, mapping_text("SRC", "SRC_TWO"))
        write_fixture(directory / "__init__.py", "")
        second_path = directory / "SRC_TWO_to_T_TARGET.py"
        write_fixture(second_path, job_text("SRC_TWO"))
        dual_shell_text = (
            shell_text + "JOB_TWO='SRC_TWO_to_T_TARGET.py'\n"
            "# 旧作业 OldJob.py 不参与本次执行\n"
        )
        write_fixture(shell_path, dual_shell_text)
        report = complete_report(directory)
        if report.failed or report.incomplete:
            report.print()
            return 1
        local_report = check_files(directory, [python_path.name])
        if local_report.failed or not any(
            "mapping 与 Writer 逐来源字段闭环" in message
            for _, message in local_report.items
        ):
            print("自检失败：局部修改未按来源核对 mapping")
            return 1

        write_fixture(mapping, mapping_text("SRC"))
        if not complete_report(directory).incomplete:
            print("自检失败：第二来源缺少映射未被识别")
            return 1
        write_fixture(mapping, mapping_text("SRC", "SRC_TWO"))
        write_fixture(mapping, mapping_text("SRC", "SRC_TWO").replace(
            "| ID | 主键 | ID | 主键 | 直接迁移 |\n",
            "| ID | 主键 | OTHER_ID | 主键 | 直接迁移 |\n", 1,
        ))
        if not complete_report(directory).failed:
            print("自检失败：来源映射与 Writer 不一致未被识别")
            return 1
        write_fixture(mapping, mapping_text("SRC", "SRC_TWO"))

        write_fixture(second_path, job_text("SRC_TWO", "OTHER_ID"))
        mismatch_report = complete_report(directory)
        mismatch_messages = [message for _, message in mismatch_report.items]
        if not mismatch_report.failed or not any(
            "第 1 列不一致：查询=ID，Writer=OTHER_ID" in message
            for message in mismatch_messages
        ):
            print("自检失败：第二来源字段错位未被识别")
            return 1
        write_fixture(second_path, job_text("SRC_TWO"))
        write_fixture(shell_path, shell_text)
        if not complete_report(directory).failed:
            print("自检失败：第二来源缺失引用未被识别")
            return 1
        write_fixture(shell_path, dual_shell_text + "JOB_MISSING='MissingJob.py'\n")
        if not complete_report(directory).failed:
            print("自检失败：入口引用不存在的作业未被识别")
            return 1
        write_fixture(shell_path, dual_shell_text)

        with patch.object(shutil, "which", return_value=None):
            report = check_directory(directory)
        if report.failed or not report.incomplete:
            print("自检失败：Shell 未执行的覆盖状态错误")
            return 1
        output = io.StringIO()
        with patch.object(shutil, "which", return_value=None), patch.object(
            sys, "argv", [__file__, str(directory)],
        ), contextlib.redirect_stdout(output):
            exit_code = main()
        if exit_code != 1 or "静态检查结果：Failure" not in output.getvalue():
            print("自检失败：检查未完成时退出码或整体状态错误")
            return 1
        with patch.object(shutil, "which", return_value="test-shell"), patch.object(
            subprocess, "run",
            return_value=subprocess.CompletedProcess([], 2, b"", b"syntax error"),
        ):
            if not check_directory(directory).failed:
                print("自检失败：Shell 语法错误未被识别")
                return 1

        local_dir = Path(temp_dir) / "local_fix"
        local_dir.mkdir()
        write_fixture(local_dir / python_path.name, job_text("SRC"))
        if check_files(local_dir, [python_path.name]).failed:
            print("自检失败：局部修复不应要求历史交付物")
            return 1
        escaped_query = (
            "SOURCE_TABLE = 'SRC'\nTARGET_TABLE = 'T_TARGET'\n"
            "SOURCE_QUERY = f\"SELECT ID AS \\\"ID\\\" FROM SRC "
            "WHERE DT BETWEEN '{{V_STARTDATE}}' AND '{{V_ENDDATE}}'\"\n"
            "TARGET_COLUMNS = ['ID']\nPRE_SQL = []\n"
        )
        write_fixture(local_dir / python_path.name, escaped_query)
        if check_files(local_dir, [python_path.name]).failed:
            print("自检失败：正确转义的 f-string 日期参数被误报")
            return 1
        write_fixture(local_dir / python_path.name, escaped_query.replace(
            "{{V_STARTDATE}}", "{V_STARTDATE}",
        ))
        if not check_files(local_dir, [python_path.name]).failed:
            print("自检失败：f-string 日期参数提前求值未被识别")
            return 1
        write_fixture(local_dir / python_path.name, job_text("SRC"))
        with patch.object(
            sys, "argv", [__file__, str(local_dir), "--files", python_path.name],
        ), contextlib.redirect_stdout(io.StringIO()):
            if main() != 0:
                return 1
        if not check_directory(local_dir).failed:
            print("自检失败：完整交付未发现缺失文件")
            return 1
        if not check_files(local_dir, ["../T_TARGET/SRC_to_T_TARGET.py"]).failed:
            print("自检失败：局部文件范围越界未被识别")
            return 1
    print("check_artifacts.py 自检通过（模拟 Shell，无数据库或 DataX 操作）")
    return 0


def main() -> int:
    """解析命令行并执行目录检查或自检。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, help="目标表交付目录")
    parser.add_argument("--self-test", action="store_true", help="运行内置自检")
    parser.add_argument("--files", nargs="+", help="只检查目标目录内指定修改文件")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.directory is None:
        parser.error("请提供目标表交付目录，或使用 --self-test")
    directory = args.directory.resolve()
    if args.files:
        report = check_files(directory, args.files)
        print("检查范围：局部修复")
    else:
        report = check_directory(directory)
        print("检查范围：完整交付")
    report.print()
    return 1 if report.failed or report.incomplete else 0


if __name__ == "__main__":
    sys.exit(main())
