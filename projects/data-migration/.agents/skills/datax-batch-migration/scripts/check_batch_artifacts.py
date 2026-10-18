#!/usr/bin/env python3
"""离线检查 DataX 批量迁移入口、任务清单和单表 Shell。"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Task:
    order: int
    group: str
    shell_name: str
    enabled: str
    description: str


@dataclass(frozen=True)
class TaskDocument:
    tasks: list[Task]
    column_count: int
    comments: list[str]


class CheckError(ValueError):
    """表示批量交付物不满足离线检查要求。"""


def read_text_file(path: Path) -> str:
    """读取 UTF-8 无 BOM、LF 换行的文本文件。"""
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise CheckError(f"{path}: 文件包含 UTF-8 BOM")
    if b"\r\n" in data or b"\r" in data:
        raise CheckError(f"{path}: 文件不是 LF 换行")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CheckError(f"{path}: 文件不是有效 UTF-8") from exc


def select_one(root: Path, pattern: str, label: str) -> Path:
    """在批次根目录选择唯一的指定文件。"""
    matches = sorted(path for path in root.glob(pattern) if path.is_file())
    if len(matches) != 1:
        raise CheckError(f"{label}应有且仅有 1 个，实际为 {len(matches)} 个")
    return matches[0]


def select_task_file(root: Path) -> Path:
    """选择唯一的标准或带批次前缀的任务清单。"""
    matches = {path for path in root.glob("*_tasks.conf") if path.is_file()}
    standard = root / "tasks.conf"
    if standard.is_file():
        matches.add(standard)
    if len(matches) != 1:
        raise CheckError(f"任务清单应有且仅有 1 个，实际为 {len(matches)} 个")
    return next(iter(matches))


def is_separator(parts: list[str]) -> bool:
    """判断当前行是否为任务清单分隔线。"""
    return bool(parts) and all(part and set(part) <= {"-", ":"} for part in parts)


def parse_task_document(path: Path) -> TaskDocument:
    """解析任务清单、普通注释和列结构。"""
    tasks: list[Task] = []
    comments: list[str] = []
    column_count: int | None = None
    for line_number, raw_line in enumerate(read_text_file(path).splitlines(), 1):
        stripped = raw_line.strip()
        if not stripped:
            continue
        content = stripped[1:].strip() if stripped.startswith("#") else stripped
        comment_parts = [part.strip() for part in content.split("|")]
        if comment_parts[0] in {"顺序", "序号", "order", "seq"} or is_separator(comment_parts):
            continue
        if stripped.startswith("#"):
            comments.append(content)
            continue
        parts = [part.strip() for part in raw_line.split("|")]
        if len(parts) == 4:
            order_text, shell_name, enabled_text, description = parts
            group = ""
        elif len(parts) == 5:
            order_text, group, shell_name, enabled_text, description = parts
        else:
            raise CheckError(f"{path}:{line_number}: 任务清单必须为 4 列或 5 列")
        if column_count is None:
            column_count = len(parts)
        elif column_count != len(parts):
            raise CheckError(f"{path}:{line_number}: 任务清单列数不一致")
        try:
            order = int(order_text)
        except ValueError as exc:
            raise CheckError(f"{path}:{line_number}: 顺序必须是整数") from exc
        if not shell_name:
            raise CheckError(f"{path}:{line_number}: Shell脚本名称不能为空")
        enabled = enabled_text.upper()
        if enabled not in {"Y", "N"}:
            raise CheckError(f"{path}:{line_number}: 启用状态只能是 Y 或 N")
        tasks.append(Task(order, group, shell_name, enabled, description))
    if not tasks:
        raise CheckError(f"{path}: 没有可用任务")
    return TaskDocument(tasks, column_count or 4, comments)


def display_width(value: str) -> int:
    """计算项目常用编辑器中的近似显示宽度。"""
    width = 0
    for char in value:
        if unicodedata.combining(char):
            continue
        width += 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
    return width


def pad(value: str, width: int, align_right: bool = False) -> str:
    """按显示宽度补齐单元格。"""
    spaces = " " * max(0, width - display_width(value))
    return f"{spaces}{value}" if align_right else f"{value}{spaces}"


def task_values(task: Task, column_count: int) -> list[str]:
    """按当前清单结构返回任务字段。"""
    if column_count == 4:
        return [str(task.order), task.shell_name, task.enabled, task.description]
    return [str(task.order), task.group, task.shell_name, task.enabled, task.description]


def task_headers(column_count: int) -> list[str]:
    """返回当前清单结构的标准表头。"""
    if column_count == 4:
        return ["顺序", "Shell脚本名称", "启用", "说明"]
    return ["顺序", "分组", "Shell脚本名称", "启用", "说明"]


def render_task_document(document: TaskDocument) -> str:
    """按统一列模型生成任务清单文本。"""
    headers = task_headers(document.column_count)
    rows = [task_values(task, document.column_count) for task in document.tasks]
    widths = [max(display_width(header), *(display_width(row[index]) for row in rows)) for index, header in enumerate(headers)]

    def render_row(values: list[str], numeric: bool = False) -> str:
        cells = [
            pad(value, widths[index], numeric and index == 0)
            for index, value in enumerate(values)
        ]
        return " | ".join(cells).rstrip()

    lines = [f"# {render_row(headers)}"]
    lines.append(f"# {' | '.join('-' * width for width in widths)}")
    lines.extend(f"# {comment}" for comment in document.comments)
    lines.extend(render_row(row, numeric=True) for row in rows)
    return "\n".join(lines) + "\n"


def ensure_task_format(path: Path, document: TaskDocument) -> None:
    """确认任务清单已按统一列模型排版。"""
    if read_text_file(path) != render_task_document(document):
        raise CheckError(
            f"{path}: 任务清单未按统一列模型对齐；运行 --format 自动整理"
        )


def format_task_document(path: Path) -> None:
    """将任务清单重排为统一列模型。"""
    document = parse_task_document(path)
    path.write_text(render_task_document(document), encoding="utf-8", newline="\n")


def ensure_unique(tasks: list[Task]) -> None:
    """检查任务顺序和 Shell 名称是否唯一。"""
    orders: set[int] = set()
    shell_names: set[str] = set()
    for task in tasks:
        if task.order in orders:
            raise CheckError(f"任务顺序重复: {task.order}")
        if task.shell_name in shell_names:
            raise CheckError(f"Shell脚本名称重复: {task.shell_name}")
        orders.add(task.order)
        shell_names.add(task.shell_name)


def resolve_enabled_shells(root: Path, tasks: list[Task]) -> list[Path]:
    """确认每个启用 Shell 在批次目录内唯一存在。"""
    resolved: list[Path] = []
    for task in tasks:
        if task.enabled != "Y":
            continue
        matches = sorted(path for path in root.rglob(task.shell_name) if path.is_file())
        if len(matches) != 1:
            raise CheckError(
                f"{task.shell_name}: 启用 Shell 应唯一存在，实际为 {len(matches)} 个"
            )
        resolved.append(matches[0])
    return resolved


def check_shell_syntax(paths: list[Path]) -> list[str]:
    """检查本次生成的 Shell；不可用的解释器只记录警告。"""
    warnings: list[str] = []
    for shell in ("sh", "bash"):
        executable = shutil.which(shell)
        if not executable:
            warnings.append(f"未找到 {shell}，未执行 {shell} -n")
            continue
        probe = subprocess.run(
            [executable, "-n"],
            input="",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if probe.returncode != 0:
            warnings.append(f"{shell} 当前不可用，未执行 {shell} -n")
            continue
        for path in paths:
            result = subprocess.run(
                [executable, "-n", str(path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            if result.returncode != 0:
                detail = result.stderr.strip() or result.stdout.strip() or "未知语法错误"
                raise CheckError(f"{path}: {shell} -n 失败: {detail}")
    return warnings


def check_batch(root: Path) -> tuple[int, list[str]]:
    """执行第一版批量交付物离线检查。"""
    if not root.is_dir():
        raise CheckError(f"批次目录不存在: {root}")
    task_file = select_task_file(root)
    import_script = select_one(root, "*_import.sh", "批量导入 Shell")
    check_script = select_one(root, "*_check.sh", "批量检查 Shell")
    document = parse_task_document(task_file)
    ensure_unique(document.tasks)
    resolve_enabled_shells(root, document.tasks)
    checked_paths = [task_file, import_script, check_script]
    for path in checked_paths:
        read_text_file(path)
    ensure_task_format(task_file, document)
    warnings = check_shell_syntax([import_script, check_script])
    return len(document.tasks), warnings


def self_test() -> None:
    """用中英文混排样本验证格式化、解析和重复顺序检查。"""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        (root / "demo_import.sh").write_text(
            "#!/bin/sh\nexit 0\n", encoding="utf-8", newline="\n"
        )
        (root / "demo_check.sh").write_text(
            "#!/bin/sh\nexit 0\n", encoding="utf-8", newline="\n"
        )
        table_dir = root / "T_DEMO"
        table_dir.mkdir()
        (table_dir / "run_T_DEMO.sh").write_text(
            "#!/bin/sh\nexit 0\n", encoding="utf-8", newline="\n"
        )
        task_file = root / "tasks.conf"
        task_file.write_text(
            "# 顺序|分组|Shell脚本名称|启用|说明\n"
            "# 中英文混排格式化样本\n"
            "10|history|run_T_DEMO.sh|Y|演练任务\n"
            "100|history|run_T_DEMO_H.sh|N|生产任务\n",
            encoding="utf-8",
            newline="\n",
        )
        format_task_document(task_file)
        document = parse_task_document(task_file)
        if document.column_count != 5 or len(document.tasks) != 2:
            raise AssertionError("五列任务清单未正确格式化")
        count, _ = check_batch(root)
        if count != 2:
            raise AssertionError("格式化后的批次未通过检查")
        task_file.write_text(
            "10|run_T_DEMO.sh|Y|demo\n"
            "10|run_T_DEMO_H.sh|N|duplicate\n",
            encoding="utf-8",
            newline="\n",
        )
        try:
            ensure_unique(parse_task_document(task_file).tasks)
        except CheckError as exc:
            if "顺序重复" not in str(exc):
                raise AssertionError("重复顺序未得到预期错误") from exc
        else:
            raise AssertionError("重复顺序未被识别")
        task_file.write_text(
            "10|run_T_DEMO.sh|Y|演练任务\n"
            "100|run_T_DEMO_H.sh|N|生产任务\n",
            encoding="utf-8",
            newline="\n",
        )
        format_task_document(task_file)
        document = parse_task_document(task_file)
        if document.column_count != 4 or len(document.tasks) != 2:
            raise AssertionError("四列任务清单未正确格式化")


def main() -> int:
    """解析参数并输出检查结论。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_dir", nargs="?", type=Path, help="批次作业根目录")
    parser.add_argument("--format", action="store_true", help="按统一列模型重排任务清单")
    parser.add_argument("--self-test", action="store_true", help="运行内置自检")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            print("状态：Success")
            print("自检通过")
            return 0
        if args.batch_dir is None:
            parser.error("必须提供批次目录，或使用 --self-test")
        if args.format:
            task_file = select_task_file(args.batch_dir.resolve())
            format_task_document(task_file)
            print(f"FORMATTED: {task_file}")
        task_count, warnings = check_batch(args.batch_dir.resolve())
        print("状态：Success")
        print(f"批量交付物检查通过，任务数 {task_count}")
        for warning in warnings:
            print(f"WARN: {warning}")
        return 0
    except CheckError as exc:
        print("状态：Failure", file=sys.stderr)
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
