# Migration guide

## Upgrade a generated installation

```powershell
python scripts/upgrade_component.py --manifest D:\path\to\project\.spec-product\manifest.json --component accessibility-audit --provider axe-core --dry-run
python scripts/upgrade_component.py --manifest D:\path\to\project\.spec-product\manifest.json --component accessibility-audit --provider axe-core
```

The command creates a timestamped backup before changing the manifest. It refuses providers that are not in the registry or that conflict with another active provider for the same capability.

## Roll back

```powershell
python scripts/rollback_component.py --manifest D:\path\to\project\.spec-product\manifest.json --backup D:\path\to\project\.spec-product\backups\manifest-<timestamp>.json
```

Rollback restores the manifest only; it does not delete packages or alter source code.
