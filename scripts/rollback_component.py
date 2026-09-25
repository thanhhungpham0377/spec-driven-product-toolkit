"""Restore a generated manifest backup."""
from __future__ import annotations
import argparse, shutil
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--backup", required=True, type=Path)
    args = ap.parse_args()
    manifest, backup = args.manifest.resolve(), args.backup.resolve()
    if not backup.is_file():
        raise SystemExit(f"backup not found: {backup}")
    shutil.copy2(backup, manifest)
    print(f"restored {manifest} from {backup}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
