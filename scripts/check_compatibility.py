"""Check registry/profile conflicts and local tool availability."""
from __future__ import annotations
import argparse, json, shutil
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", choices=["prototype", "balanced", "production"], required=True)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = ap.parse_args()
    root = args.root.resolve()
    registry = json.loads((root / "components" / "registry.json").read_text(encoding="utf-8"))["components"]
    profile = json.loads((root / "profiles" / f"{args.profile}.json").read_text(encoding="utf-8"))
    chosen = [x for x in registry.values() if x["capability"] in profile["capabilities"]]
    caps = [x["capability"] for x in chosen]
    duplicate_caps = sorted({c for c in caps if caps.count(c) > 1})
    inactive = [x["provider"] for x in chosen if x["status"] != "active"]
    missing = [x["provider"] for x in chosen if x["command"] and not shutil.which(x["command"])]
    result = {"profile": args.profile, "duplicate_capabilities": duplicate_caps, "inactive": inactive, "missing_commands": missing, "compatible": not (duplicate_caps or inactive)}
    print(json.dumps(result, indent=2))
    return 0 if result["compatible"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
