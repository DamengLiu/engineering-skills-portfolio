"""Query maintained Markdown catalogs; no database, network, or persistent cache."""
import argparse
import hashlib
import json
import re
from pathlib import Path

CATALOGS = {
    "field": ("standard-fields.md", 9),
    "domain": ("dictionary-domains.md", 7),
    "primitive": ("data-primitives.md", 4),
}


def read_catalog(path, width):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    rows, header, guidance = [], None, []
    for number, line in enumerate(lines, 1):
        if not line.startswith("|"):
            if header is None and line.strip():
                guidance.append([number, line])
            continue
        cells = [c.strip().replace(r"\|", "|")
                 for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if len(cells) != width:
            raise ValueError(f"{path}:{number}: expected {width} columns")
        if header is None:
            header = cells
        elif not all(re.fullmatch(r":?-+:?", c) for c in cells):
            rows.append((number, cells))
    if not header or not rows:
        raise ValueError(f"{path}: missing catalog")
    return {"path": str(path.resolve()), "columns": header,
            "guidance": guidance, "rows": rows}


def matches(term, cells):
    # Codes are exact tokens: ACT must not accidentally select ACT_TYPE.
    if re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_]*", term):
        return any(term.upper() in re.findall(r"[A-Z][A-Z0-9_]*", c.upper())
                   for c in cells)
    return any(term.casefold() in c.casefold() for c in cells)


def query(refs, terms, kind="field"):
    selected = ["field", "domain"] if kind == "field" else [kind]
    docs = {k: read_catalog(refs / CATALOGS[k][0], CATALOGS[k][1])
            for k in selected}
    # Domain-only queries still inspect field records to resolve a known code/name.
    lookup = docs.copy()
    if kind == "domain":
        lookup["field"] = read_catalog(refs / CATALOGS["field"][0], 9)
    keys, direct = set(), set()
    for doc in lookup.values():
        for _, cells in doc["rows"]:
            if any(matches(t, cells) for t in terms):
                keys.add(cells[0])
                direct.add(cells[0])
    # Follow small explicit code references in governance prose, never equate
    # fields or infer aliases from shared values. Bulk coverage lists are not edges.
    notes = lookup.get("domain", {}).get("guidance", [])
    edges = []
    for _, line in notes:
        codes = set(re.findall(r"`([A-Z][A-Z0-9_]*)`", line))
        if 1 <= len(codes) <= 3:
            edges.append(codes)
            if any(matches(t, [line]) for t in terms):
                keys.update(codes)
    while True:
        expanded = keys | set().union(*(e for e in edges if e & keys), set())
        if expanded == keys:
            break
        keys = expanded
    result = {"query": terms, "kind": kind, "catalogs": [],
              "related_codes": sorted(keys - direct),
              "note": "关联记录不代表字段等价；按场景和治理说明判断。未找到的字段属性不得推断。"}
    for k, doc in docs.items():
        rows = [[n, cells] for n, cells in doc["rows"] if cells[0] in keys]
        result["catalogs"].append({
            "kind": k, "source": doc["path"], "columns": doc["columns"],
            "guidance": doc["guidance"], "rows": rows, "count": len(rows)})
    result["found"] = any(c["count"] for c in result["catalogs"])
    result["unmatched_terms"] = [
        t for t in terms if not any(
            matches(t, cells) for doc in lookup.values() for _, cells in doc["rows"]
        ) and not any(matches(t, [line]) for _, line in notes)]
    # Include source bytes AND implementation: any change invalidates reuse,
    # even if the query happens to select the same rows.
    digest = hashlib.sha256()
    digest.update(Path(__file__).read_bytes())
    digest.update(json.dumps([str(refs.resolve()), terms, kind],
                             ensure_ascii=False).encode("utf-8"))
    for k in sorted(lookup):
        digest.update((refs / CATALOGS[k][0]).read_bytes())
    result["fingerprint"] = digest.hexdigest()
    return result


def evidence(paths):
    """Read-only fingerprints for task-local source evidence, not conclusions."""
    return {str(p.resolve()): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("terms", nargs="*", help="字段代码、中文名称；可一次多个")
    parser.add_argument("--kind", choices=CATALOGS, default="field",
                        help="field 同查字段及完整值域；domain 只输出值域；primitive 查元语")
    parser.add_argument("--refs", type=Path,
                        default=Path(__file__).resolve().parents[1] / "references")
    parser.add_argument("--known", help="仅限当前上下文仍保留完整结果时传入上次 fingerprint")
    parser.add_argument("--evidence", type=Path, nargs="+",
                        help="输出指定源码文件的内容指纹；不读取为模型上下文")
    args = parser.parse_args()
    try:
        if args.evidence:
            if args.terms or args.known:
                parser.error("--evidence 不与查询或 --known 混用")
            result = {"evidence": evidence(args.evidence)}
        else:
            terms = sorted(set(t.strip() for t in args.terms if t.strip()))
            if not terms:
                parser.error("至少提供一个非空查询词")
            result = query(args.refs, terms, args.kind)
            if args.known == result["fingerprint"]:
                result = {"status": "unchanged", "fingerprint": args.known,
                          "query": terms, "note": "仅复用当前上下文仍保留的原结果；否则去掉 --known 重查。"}
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    except (OSError, ValueError) as exc:
        parser.exit(2, f"查询失败：{exc}\n")


if __name__ == "__main__":
    main()
