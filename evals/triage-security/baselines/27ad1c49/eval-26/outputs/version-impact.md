# Step 2 -- Version Impact Analysis: CVE-2026-99001

## Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | Stream | criterion | Affected? | Notes |
|---------|--------|-----------|-----------|-------|
| 2.1.0 | 2.1.x | 0.5.1 | YES | outside issue scope |
| 2.1.1 | 2.1.x | 0.5.1 | YES | outside issue scope |
| 2.2.0 | 2.2.x | 0.5.1 | YES | |
| 2.2.1 | 2.2.x | 0.5.1 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same backend commit v0.4.8) |
| 2.2.3 | 2.2.x | 0.5.1 | YES | |
| 2.2.4 | 2.2.x | 0.5.1 | YES | |

All versions across both streams ship criterion 0.5.1, which is within the
affected range (< 0.5.2). Every version is affected.

### Source evidence

| Version | Backend Tag | criterion version | Fix threshold (0.5.2) |
|---------|-------------|-------------------|-----------------------|
| 2.1.0 | v0.3.8 | 0.5.1 | BELOW |
| 2.1.1 | v0.3.12 | 0.5.1 | BELOW |
| 2.2.0 | v0.4.5 | 0.5.1 | BELOW |
| 2.2.1 | v0.4.8 | 0.5.1 | BELOW |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | BELOW |
| 2.2.3 | v0.4.11 | 0.5.1 | BELOW |
| 2.2.4 | v0.4.12 | 0.5.1 | BELOW |

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

  First appeared: 2.1.0 (initial project setup)
  Present in all versions
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```

### Dependency scope assessment

criterion is declared in `[dev-dependencies]` and is used for benchmarks only.
It is NOT shipped in production builds. Per the dependency scope decision tree:

- **Label**: `dev-dependency` to be added to remediation tasks
- **Priority override**: Normal (regardless of CVE severity of Medium/5.3)
- **Rationale**: Dev-only dependencies are not shipped in production. They still
  represent a supply chain risk (compromised dev deps can inject malicious code
  during builds), so remediation tasks are still created, but at reduced priority.

## Cross-stream impact

The issue is scoped to stream 2.2.x (suffix `[rhtpa-2.2]`). The version impact
analysis reveals that the 2.1.x stream is also affected:

| Stream | Affected versions | Status |
|--------|-------------------|--------|
| 2.2.x | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | In scope -- remediation tasks created |
| 2.1.x | 2.1.0, 2.1.1 | Outside scope -- cross-stream impact (Case A) |
