# Step 2 -- Version Impact Analysis: CVE-2026-99001

## Version Impact for CVE-2026-99001 (criterion < 0.5.2)

### Stream 2.2.x (issue scope)

| Version | Build | backend tag | criterion version | Affected? | Notes |
|---------|-------|-------------|-------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.5.1 | YES | |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.5.1 | YES | |
| 2.2.2 | 0.4.9 | `v0.4.8` | 0.5.1 | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.5.1 | YES | |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.5.1 | YES | |

All versions in the 2.2.x stream ship criterion 0.5.1, which is within the affected range (< 0.5.2).

### Stream 2.1.x (cross-stream -- outside issue scope)

| Version | Build | backend tag | criterion version | Affected? | Notes |
|---------|-------|-------------|-------------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.5.1 | YES | |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.5.1 | YES | |

All versions in the 2.1.x stream also ship criterion 0.5.1 (affected).

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

### Dependency Scope Assessment

criterion is declared in `[dev-dependencies]` in `backend/Cargo.toml`. Dev-dependencies in Cargo are used for tests and benchmarks only and are NOT compiled into the production binary or shipped in the container image. This means:

- The vulnerable code (path traversal in benchmark output) is **not reachable in production**
- The risk is limited to **supply chain** concerns (compromised dev dependency during builds)
- Per the dependency scope decision tree: remediation tasks receive the `dev-dependency` label and priority is overridden to **Normal** regardless of CVE severity

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | `release/0.4.z` | criterion 0.5.1 at all tags -- not yet fixed upstream on this branch |
| 2.1.x | Cargo | `release/0.3.z` | criterion 0.5.1 at all tags -- not yet fixed upstream on this branch |

Upstream fix is not yet present on either release branch. Remediation requires an upstream PR to bump criterion to >= 0.5.2, followed by downstream propagation.

## Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x, but the 2.1.x stream is also affected. Per Case A of the remediation workflow, cross-stream impact must be reported and preemptive remediation tasks created for streams without their own CVE Jira.
