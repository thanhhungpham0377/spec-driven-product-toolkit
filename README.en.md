# Spec-Driven Product Toolkit

[Phiên bản tiếng Việt](README.md)

An installable skill and tooling kit for developing products with AI coding agents through a structured process:

```text
Specification → Design → Planning → Implementation → Testing → Audit → Review → Release
```

The toolkit is designed for controlled vibe coding: the agent can move quickly, but important changes still have acceptance criteria, verification commands, and audit evidence.

> This is an independent composition and integration layer, not an official distribution of any upstream project. The projects that inspired or contributed ideas and tool roles are documented in the [source catalog](references/catalog.md).

## What is included?

| Component | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Codex skill entry point |
| [`references/profiles.md`](references/profiles.md) | Profile selection criteria and workflow stages |
| [`references/catalog.md`](references/catalog.md) | Component responsibilities, upstream repositories, and provenance |
| [`scripts/install_profile.py`](scripts/install_profile.py) | Profile selection, preflight checks, and installation manifest generation |
| [`components/registry.json`](components/registry.json) | Capability-to-provider registry and upstream provenance |
| [`profiles/`](profiles/) | Versioned profile definitions |
| [`scripts/check_compatibility.py`](scripts/check_compatibility.py) | Conflict and local availability checks |
| [`scripts/upgrade_component.py`](scripts/upgrade_component.py) | Safe candidate-provider switch with backup |
| [`scripts/rollback_component.py`](scripts/rollback_component.py) | Manifest-only rollback |
| [`agents/openai.yaml`](agents/openai.yaml) | Codex display name and default prompt |

## Three profiles

| Profile | Best for | Method | Main stages |
|---|---|---|---|
| `prototype` | Small prototypes, MVPs, low-risk projects | Matt Pocock workflow with fast feedback | Grill → plan → implement → smoke test → review |
| `balanced` | Real applications and small/medium teams | Matt Pocock plus executable quality gates | Discover → design → plan → implement → test → audit → PR review |
| `production` | Deployed products, sensitive data, multiple contributors | Balanced plus Spec Kit and protected security/release gates | Spec → design → plan → implement → full audit → protected PR → release/retro |

### Which profile should I choose?

- Choose `prototype` when you are validating an idea quickly and handling no sensitive data.
- Choose `balanced` for a real product with UI, APIs, and/or a database where you want code, UI, dependency, secret, and baseline security checks.
- Choose `production` when the project has authentication, payments, PII, important migrations, production CI/CD, multiple contributors, or audit requirements.

## Tools by profile

### Prototype

- Matt Pocock Skills: clarify requirements, plan, implement, and review.
- Playwright: optional UI smoke tests for web applications.
- The project's native formatter, linter, type checker, and test runner.

### Balanced

- Everything in Prototype.
- `pre-commit`: local quality hooks.
- `Semgrep`: SAST and code-pattern auditing.
- `Gitleaks`: secret detection.
- `OSV-Scanner`: dependency vulnerability checks.
- `SQLFluff`: SQL linting when SQL is present.
- `Reviewdog`: publish audit findings in pull requests.
- `axe-core` and `Lighthouse`: accessibility, performance, SEO, and best-practice checks.

### Production

- Everything in Balanced.
- `Spec Kit`: durable specifications for large features.
- `Trivy`: container, filesystem, and IaC scanning.
- `CodeQL`: deeper semantic security analysis.
- `Zizmor`: GitHub Actions workflow auditing.
- `Atlas` or the repository's existing migration authority: schema diff and migration planning.
- Visual regression and mandatory CI artifacts.

## Installation

### Let the installer ask you to choose a profile

```powershell
python scripts/install_profile.py --target D:\path\to\your-project
```

### List profiles before installing

```powershell
python scripts/install_profile.py --target D:\path\to\your-project --list-profiles
```

### Check tools without changing the project

```powershell
python scripts/install_profile.py --target D:\path\to\your-project --profile balanced --check-only
```

### Install a selected profile

```powershell
python scripts/install_profile.py --target D:\path\to\your-project --profile balanced
```

The installer creates `.spec-product/` in the target project with:

- `manifest.json`: selected profile and components.
- `README.md`: scope, method, and stages.
- `source-catalog.md`: upstream sources for the selected components.

Missing tools are never silently ignored. The installer reports an incomplete verification state so tools can be installed before the workflow is considered verified.

## Conflict and duplication rules

- Matt Pocock is the primary workflow orchestrator.
- Spec Kit is added only for large feature specifications in the `production` profile.
- Playwright is the default browser runner.
- axe-core is the accessibility engine; Lighthouse is the performance/SEO auditor.
- Semgrep, Gitleaks, OSV-Scanner, Trivy, and CodeQL have different responsibilities and are not substitutes for one another.
- Atlas must not become a second schema authority when the project already uses Prisma, Drizzle, or another migration system.

## Attribution and provenance

This toolkit is an original composition layer maintained by the repository author. It is inspired by and selectively integrates ideas and responsibilities from several open-source projects. It is not an endorsement or official fork. The full list of upstream repositories, component roles, and traceability links is available in [references/catalog.md](references/catalog.md).

When reusing or redistributing this toolkit, review the license and contribution terms of each upstream project.

## Future-proofing and upgrades

Components are addressed by capability rather than repository name:

```text
profile → capability → provider → adapter → install/check command
```

Use [`references/version-policy.md`](references/version-policy.md) for the replacement lifecycle and [`references/migration-guide.md`](references/migration-guide.md) for upgrade/rollback commands. Changes are tracked in [`VERSION`](VERSION) and [`CHANGELOG.md`](CHANGELOG.md).

## License

This repository provides integration configuration and documentation. Each upstream tool remains subject to its own license.
