"""Check structural alignment in the fictional migration example."""

import argparse
import csv
import json
from pathlib import Path


def validate_mapping(mapping_path: Path, manifest_path: Path) -> list[str]:
    with mapping_path.open(newline="", encoding="utf-8") as mapping_file:
        reader = csv.DictReader(mapping_file)
        if reader.fieldnames != ["source", "target", "transform"]:
            return ["mapping must have source,target,transform columns"]
        rows = list(reader)

    if not rows or any(not all(row.values()) for row in rows):
        return ["mapping must contain complete rows"]

    with manifest_path.open(encoding="utf-8") as manifest_file:
        manifest = json.load(manifest_file)

    errors = []
    for side, field in (("reader", "source"), ("writer", "target")):
        expected = [row[field] for row in rows]
        actual = manifest.get(f"{side}_columns")
        if not isinstance(actual, list) or any(not isinstance(value, str) for value in actual):
            errors.append(f"{side}_columns must be a list of strings")
            continue
        if len(set(expected)) != len(expected):
            errors.append(f"mapping has duplicate {field} columns")
        if actual != expected:
            errors.append(f"{side} column order differs from mapping")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mapping", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()

    try:
        errors = validate_mapping(args.mapping, args.manifest)
    except (OSError, UnicodeError, csv.Error, json.JSONDecodeError) as exc:
        parser.exit(2, f"Cannot read example files: {exc}\n")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print("PASS: reader and writer columns match the mapping order")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
