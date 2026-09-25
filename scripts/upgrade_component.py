"""Switch a capability provider in a generated manifest with a backup."""
from __future__ import annotations
import argparse, json, shutil
from datetime import datetime, timezone
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--component", required=True, help="Capability name")
    ap.add_argument("--provider", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    manifest = args.manifest.resolve()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    registry_path = Path(__file__).resolve().parents[1] / "components" / "registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))["components"]
    components = data.get("components", [])
    target = next((x for x in components if x.get("capability") == args.component), None)
    if target is None:
        raise SystemExit(f"capability not found: {args.component}")
    if args.provider not in registry:
        raise SystemExit(f"provider is not registered: {args.provider}")
    if registry[args.provider]["capability"] != args.component:
        raise SystemExit(f"provider {args.provider} does not implement {args.component}")
    if target.get("provider") == args.provider:
        print("already selected")
        return 0
    replacement = dict(registry[args.provider])
    replacement["name"] = args.provider
    replacement["status"] = "candidate"
    if args.dry_run:
        print(json.dumps({"from": target.get("provider"), "to": replacement}, indent=2))
        return 0
    backup_dir = manifest.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    shutil.copy2(manifest, backup_dir / f"manifest-{stamp}.json")
    data["components"] = [replacement if x is target else x for x in components]
    data["replacement_pending_validation"] = True
    manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"candidate provider written; validate before promoting: {args.provider}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
