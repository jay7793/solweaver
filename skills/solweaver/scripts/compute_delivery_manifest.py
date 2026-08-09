#!/usr/bin/env python3
"""Create a reproducible content manifest for installed delivery artifacts."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path, PurePosixPath


MANIFEST_VERSION = "solweaver-delivery-v1"


def assignment(value: str) -> tuple[str, Path]:
    label, separator, raw_path = value.partition("=")
    if not separator or not label or not raw_path:
        raise argparse.ArgumentTypeError("expected LABEL=PATH")
    normalized = PurePosixPath(label)
    if (
        normalized.is_absolute()
        or normalized.as_posix() == "."
        or ".." in normalized.parts
        or "\\" in label
        or label.endswith("/")
    ):
        raise argparse.ArgumentTypeError("LABEL must be a relative canonical path")
    return normalized.as_posix(), Path(raw_path).expanduser().resolve()


def add_record(records: dict[str, str], label: str, path: Path) -> None:
    if path.is_symlink():
        raise ValueError(f"symlink requires an explicit materialized artifact: {path}")
    if not path.is_file():
        raise ValueError(f"artifact is not a regular file: {path}")
    if label in records:
        raise ValueError(f"duplicate manifest label: {label}")
    records[label] = hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        action="append",
        default=[],
        type=assignment,
        metavar="LABEL=PATH",
        help="Recursively include regular files below PATH under LABEL.",
    )
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        type=assignment,
        metavar="LABEL=PATH",
        help="Include one regular file using the exact canonical LABEL.",
    )
    args = parser.parse_args()
    if not args.root and not args.file:
        parser.error("at least one --root or --file is required")

    records: dict[str, str] = {}
    for root_label, root in args.root:
        if root.is_symlink() or not root.is_dir():
            parser.error(f"root is not a materialized directory: {root}")
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                parser.error(f"root contains a symlink: {path}")
            if path.is_file():
                relative = path.relative_to(root).as_posix()
                try:
                    add_record(records, f"{root_label}/{relative}", path)
                except ValueError as exc:
                    parser.error(str(exc))

    for label, path in args.file:
        try:
            add_record(records, label, path)
        except ValueError as exc:
            parser.error(str(exc))

    serialized = "".join(f"{records[label]}  {label}\n" for label in sorted(records))
    digest = hashlib.sha256(
        f"{MANIFEST_VERSION}\n{serialized}".encode("utf-8")
    ).hexdigest()

    print(f"MANIFEST_VERSION {MANIFEST_VERSION}")
    print(serialized, end="")
    print(f"DELIVERY_ARTIFACT_MANIFEST sha256:{digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
