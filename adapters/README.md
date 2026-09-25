# Adapter layer

The adapter boundary keeps workflow/profile logic independent from a specific upstream repository.

Each future provider should document its capability, interface version, install/version-pinning command, local and CI checks, machine-readable output, license, upstream source, fixture result, migration, and rollback notes.

Do not add a second active provider for the same capability without a compatibility decision. Add a provider to `components/registry.json`, validate it against `components/compatibility.json`, then promote it from `candidate` to `active` in a separate release.
