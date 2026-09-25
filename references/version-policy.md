# Version and component replacement policy

The toolkit uses Semantic Versioning. PATCH fixes installer/docs without changing contracts; MINOR adds providers, capabilities, or profiles compatibly; MAJOR changes manifest schemas or removes providers.

Components are addressed by capability, not by repository name:

```text
profile -> capability -> provider -> adapter -> install/check command
```

Provider lifecycle: `active -> candidate -> active` or `active -> deprecated -> removed`. A candidate must pass compatibility checks and fixture benchmarks before becoming the default. Keep the previous provider as a fallback for at least one major release when practical.

Every replacement must record its reason, contract/interface version, install method, compatibility result, migration steps, rollback path, and upstream source in the changelog and catalog.
