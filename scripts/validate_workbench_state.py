#!/usr/bin/env python3
"""Deterministically validate the public EP817 workbench machine state.

This validator uses only the Python standard library.  It deliberately checks
content-addressed links between the public certificates and their source files,
as well as referential integrity in the NDJSON corpus.  It is not a substitute
for the mathematical proof, Lean elaboration, or the finite certificate run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tomllib
from pathlib import Path
from typing import Any, Iterable


if not __debug__:
    raise SystemExit(
        "FAIL CLOSED: Python assertions are disabled; rerun without -O."
    )


SCHEMA = "ep817-workbench-state-receipt-v1"
STRUCTURED_SUFFIXES = frozenset({".json", ".ndjson", ".toml"})
EXCLUDED_DIRECTORY_NAMES = frozenset(
    {".git", ".lake", "output", "receipts", "reviews", "tmp", "__pycache__"}
)
DECLARED_FILE_KEYS = ("reader", "tex", "lean_entrypoint", "certificate")
CERTIFICATE_FILES = (
    "certificates/certificate_fast.json",
    "certificates/certificate_extended.json",
)
LEAN_RECEIPT_FILE = "certificates/lean_core_receipt.json"
CLAIMS_FILE = "corpus/claims.ndjson"
DEPENDENCIES_FILE = "corpus/dependencies.ndjson"
CROSSWALKS_FILE = "corpus/crosswalks.ndjson"
SOURCE_INDEX_FILE = "sources/source-index.json"


class ValidationFailure(RuntimeError):
    """A deterministic validation failure suitable for a public receipt."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative_name(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValidationFailure) as exc:
        raise ValidationFailure(f"invalid JSON {path.name}: {exc}") from exc


def load_ndjson(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ValidationFailure(f"cannot read NDJSON {path.name}: {exc}") from exc
    for line_number, line in enumerate(lines, start=1):
        require(line.strip() != "", f"blank NDJSON line in {path.name}:{line_number}")
        try:
            value = json.loads(line, object_pairs_hook=reject_duplicate_json_keys)
        except (json.JSONDecodeError, ValidationFailure) as exc:
            raise ValidationFailure(
                f"invalid NDJSON {path.name}:{line_number}: {exc}"
            ) from exc
        require(
            isinstance(value, dict),
            f"NDJSON record is not an object in {path.name}:{line_number}",
        )
        records.append(value)
    require(records, f"NDJSON file has no records: {path.name}")
    return records


def load_toml(path: Path) -> dict[str, Any]:
    try:
        value = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise ValidationFailure(f"invalid TOML {path.name}: {exc}") from exc
    require(isinstance(value, dict), f"TOML root is not a table: {path.name}")
    return value


def public_structured_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in STRUCTURED_SUFFIXES:
            continue
        relative_parts = path.relative_to(root).parts
        if any(part in EXCLUDED_DIRECTORY_NAMES for part in relative_parts[:-1]):
            continue
        files.append(path)
    return sorted(files, key=lambda item: relative_name(root, item))


def parse_structured_files(root: Path) -> tuple[dict[Path, Any], dict[str, int]]:
    parsed: dict[Path, Any] = {}
    counts = {"json": 0, "ndjson": 0, "toml": 0}
    for path in public_structured_files(root):
        suffix = path.suffix.lower()
        if suffix == ".json":
            parsed[path] = load_json(path)
            counts["json"] += 1
        elif suffix == ".ndjson":
            parsed[path] = load_ndjson(path)
            counts["ndjson"] += 1
        elif suffix == ".toml":
            parsed[path] = load_toml(path)
            counts["toml"] += 1
    require(sum(counts.values()) > 0, "no public structured state files found")
    return parsed, counts


def parsed_value(parsed: dict[Path, Any], path: Path) -> Any:
    require(path in parsed, f"required structured file was not parsed: {path.name}")
    return parsed[path]


def resolve_declared_file(root: Path, raw: Any, key: str) -> Path:
    require(isinstance(raw, str) and raw != "", f"{key} is not a nonempty path")
    candidate = Path(raw)
    require(not candidate.is_absolute(), f"{key} must be relative: {raw!r}")
    resolved_root = root.resolve(strict=True)
    resolved = (root / candidate).resolve(strict=False)
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValidationFailure(f"{key} escapes the workbench root: {raw!r}") from exc
    require(resolved.is_file(), f"{key} does not name a file: {raw!r}")
    require(resolved.stat().st_size > 0, f"{key} names an empty file: {raw!r}")
    return resolved


def nonempty_string(record: dict[str, Any], key: str, context: str) -> str:
    value = record.get(key)
    require(
        isinstance(value, str) and value != "",
        f"{context}.{key} is not a nonempty string",
    )
    return value


def unique_values(values: Iterable[str], context: str) -> set[str]:
    result: set[str] = set()
    for value in values:
        require(value not in result, f"duplicate {context}: {value}")
        result.add(value)
    return result


def validate(root: Path) -> dict[str, Any]:
    parsed, structured_counts = parse_structured_files(root)
    workbench_path = root / "workbench.json"
    workbench = parsed_value(parsed, workbench_path)
    require(isinstance(workbench, dict), "workbench.json root is not an object")

    declared_paths: dict[str, str] = {}
    resolved_declared: dict[str, Path] = {}
    for key in DECLARED_FILE_KEYS:
        resolved = resolve_declared_file(root, workbench.get(key), key)
        resolved_declared[key] = resolved
        declared_paths[key] = relative_name(root, resolved)

    claims = parsed_value(parsed, root / CLAIMS_FILE)
    dependencies = parsed_value(parsed, root / DEPENDENCIES_FILE)
    crosswalks = parsed_value(parsed, root / CROSSWALKS_FILE)
    source_index = parsed_value(parsed, root / SOURCE_INDEX_FILE)
    require(isinstance(source_index, dict), "source-index.json root is not an object")
    sources = source_index.get("sources")
    require(isinstance(sources, list), "source-index.json.sources is not an array")

    claim_ids = unique_values(
        (nonempty_string(record, "id", "claim") for record in claims), "claim id"
    )
    source_ids = unique_values(
        (
            nonempty_string(record, "id", "source")
            for record in sources
            if isinstance(record, dict)
        ),
        "source id",
    )
    require(len(source_ids) == len(sources), "a source-index entry is not an object")

    primary_claim = nonempty_string(workbench, "primary_claim_id", "workbench")
    require(primary_claim in claim_ids, f"unknown primary claim id: {primary_claim}")

    for index, edge in enumerate(dependencies, start=1):
        source_claim = nonempty_string(edge, "from", f"dependency[{index}]")
        target_claim = nonempty_string(edge, "to", f"dependency[{index}]")
        require(
            source_claim in claim_ids,
            f"dependency[{index}] has unknown from claim: {source_claim}",
        )
        require(
            target_claim in claim_ids,
            f"dependency[{index}] has unknown to claim: {target_claim}",
        )

    for index, edge in enumerate(crosswalks, start=1):
        claim = nonempty_string(edge, "claim", f"crosswalk[{index}]")
        source = nonempty_string(edge, "source", f"crosswalk[{index}]")
        require(claim in claim_ids, f"crosswalk[{index}] has unknown claim: {claim}")
        require(
            source in source_ids,
            f"crosswalk[{index}] has unknown source: {source}",
        )

    content_address_errors: list[str] = []
    certificate_validator = resolved_declared["certificate"]
    validator_digest = sha256(certificate_validator)
    for relative in CERTIFICATE_FILES:
        certificate = parsed_value(parsed, root / relative)
        require(isinstance(certificate, dict), f"{relative} root is not an object")
        recorded = certificate.get("validator_sha256")
        if recorded != validator_digest:
            content_address_errors.append(
                f"{relative} validator_sha256 mismatch: recorded={recorded!r}, "
                f"actual={validator_digest}"
            )

    lean_receipt = parsed_value(parsed, root / LEAN_RECEIPT_FILE)
    require(isinstance(lean_receipt, dict), "Lean receipt root is not an object")
    lean_source = resolved_declared["lean_entrypoint"]
    recorded_lean_path = lean_receipt.get("checked_source")
    require(
        recorded_lean_path == relative_name(root, lean_source),
        "Lean receipt checked_source does not match workbench lean_entrypoint",
    )
    actual_lean_digest = sha256(lean_source)
    recorded_lean_digest = lean_receipt.get("checked_source_sha256")
    if recorded_lean_digest != actual_lean_digest:
        content_address_errors.append(
            f"Lean source hash mismatch: recorded={recorded_lean_digest!r}, "
            f"actual={actual_lean_digest}"
        )

    pdf_path = resolved_declared["reader"]
    require(pdf_path.suffix.lower() == ".pdf", "reader path is not a PDF")
    pdf_size = pdf_path.stat().st_size
    require(pdf_size > 0, "reader PDF is empty")
    require(not content_address_errors, "; ".join(content_address_errors))

    return {
        "schema": SCHEMA,
        "status": "PASS",
        "checks": {
            "structured_files": structured_counts,
            "declared_files": declared_paths,
            "claim_ids_unique": len(claim_ids),
            "dependency_edges_resolved": len(dependencies),
            "crosswalks_resolved": len(crosswalks),
            "source_ids_unique": len(source_ids),
            "finite_validator_sha256": validator_digest,
            "lean_source_sha256": actual_lean_digest,
            "pdf": {
                "path": relative_name(root, pdf_path),
                "size_bytes": pdf_size,
                "sha256": sha256(pdf_path),
            },
        },
        "state_validator_sha256": sha256(Path(__file__)),
    }


def failure_report(root: Path, message: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "FAIL",
        "error": message,
        "state_validator_sha256": sha256(Path(__file__)),
        "workbench": root.name,
    }


def render(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="workbench root (defaults to the parent of scripts/)",
    )
    parser.add_argument("--output", type=Path, help="optional deterministic JSON receipt")
    args = parser.parse_args()
    root = args.root.resolve(strict=True)

    try:
        report = validate(root)
        exit_code = 0
    except (OSError, ValidationFailure) as exc:
        report = failure_report(root, str(exc))
        exit_code = 1

    rendered = render(report)
    if args.output is not None:
        output = args.output
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    sys.stdout.write(rendered)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
