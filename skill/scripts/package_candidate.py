#!/usr/bin/env python3
"""Validate a generated Skill and pack a verified ASCII-only ZIP."""
import sys
import zipfile
from pathlib import Path
from validate_candidate import validate


def package(root, output):
    root = Path(root).resolve()
    output = Path(output).resolve()
    errors = validate(root)
    if errors:
        raise ValueError("Candidate not ready: " + "; ".join(errors))
    files = sorted(p for p in root.rglob("*") if p.is_file())
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    try:
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file in files:
                arcname = f"{root.name}/{file.relative_to(root).as_posix()}"
                if not arcname.isascii():
                    raise ValueError(f"Non-ASCII ZIP path: {arcname}")
                zf.write(file, arcname)
        with zipfile.ZipFile(output) as zf:
            names = zf.namelist()
            expected = [f"{root.name}/{p.relative_to(root).as_posix()}" for p in files]
            if names != expected or zf.testzip() is not None:
                raise ValueError("ZIP readback failed")
        return output
    except Exception:
        output.unlink(missing_ok=True)
        raise


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: package_candidate.py <skill-directory> <output.zip>")
        sys.exit(2)
    try:
        print(package(sys.argv[1], sys.argv[2]))
    except (OSError, ValueError) as e:
        print("FAIL:", e)
        sys.exit(1)
