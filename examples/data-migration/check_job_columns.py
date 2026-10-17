"""检查虚构迁移示例的列顺序 / Check fictional migration column order."""

import argparse
import csv
import json
from pathlib import Path


def validate_mapping(mapping_path: Path, manifest_path: Path) -> list[str]:
    with mapping_path.open(newline="", encoding="utf-8") as mapping_file:
        reader = csv.DictReader(mapping_file)
        if reader.fieldnames != ["source", "target", "transform"]:
            return ["映射表需要 source,target,transform 三列 / mapping must have these columns"]
        rows = list(reader)

    if not rows or any(not all(row.values()) for row in rows):
        return ["映射表须包含完整记录 / mapping must contain complete rows"]

    with manifest_path.open(encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)

    errors = []
    for side, field in (("reader", "source"), ("writer", "target")):
        expected = [row[field] for row in rows]
        actual = manifest.get(f"{side}_columns")
        if not isinstance(actual, list) or any(not isinstance(value, str) for value in actual):
            errors.append(f"{side}_columns 须为字符串列表 / must be a list of strings")
            continue
        if len(set(expected)) != len(expected):
            errors.append(f"映射表存在重复 {field} 列 / mapping has duplicate {field} columns")
        if actual != expected:
            errors.append(f"{side} 列顺序与映射不一致 / {side} column order differs from mapping")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mapping", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    try:
        errors = validate_mapping(args.mapping, args.manifest)
    except (OSError, UnicodeError, csv.Error, json.JSONDecodeError) as exc:
        parser.exit(2, f"无法读取示例文件 / Cannot read example files: {exc}\n")

    if errors:
        for error in errors:
            print(f"失败 / FAIL: {error}")
        return 1

    print("通过 / PASS: Reader 和 Writer 列顺序与映射一致 / columns match mapping order")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
