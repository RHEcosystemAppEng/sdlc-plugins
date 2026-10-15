# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: security-matrix.md for rhtpa-release.0.4.z

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Lock file data for criterion (from `git show <tag>:Cargo.lock`):

| Tag | criterion version | Fix threshold (0.5.2) | Affected? |
|-----|-------------------|-----------------------|-----------|
| `v0.4.5` | 0.5.1 | < 0.5.2 | YES |
| `v0.4.8` | 0.5.1 | < 0.5.2 | YES |
| `v0.4.9` | _(retag of v0.4.8)_ | _(same as v0.4.8)_ | YES |
| `v0.4.11` | 0.5.1 | < 0.5.2 | YES |
| `v0.4.12` | 0.5.1 | < 0.5.2 | YES |

## 2.3.5 -- Dependency Chain Context

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

**Dependency scope assessment:** criterion is declared in `[dev-dependencies]` and
is used exclusively for benchmarks. It is NOT included in production builds or
shipped container images. This is a supply chain risk only -- a compromised dev
dependency could inject malicious code during the build/test process, but the
vulnerable code path (path traversal in benchmark output) cannot be triggered in
production.

Per the dependency scope decision tree: dev-only dependencies still require
remediation tasks, but with the `dev-dependency` label and priority overridden
to **Normal** regardless of CVE severity.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | dev-dependency only |
| 2.2.1 | 0.5.1 | YES | dev-dependency only |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.5.1 | YES | dev-dependency only |
| 2.2.4 | 0.5.1 | YES | dev-dependency only |

**All versions in the 2.2.x stream are affected.** However, criterion is a
dev-only dependency (`[dev-dependencies]`) and is NOT present in production
builds. The vulnerability (path traversal in benchmark output) cannot be
exploited in production.

## Cross-stream note (for Case A analysis)

The 2.1.x stream also ships criterion 0.5.1 at all versions (v0.3.8: 0.5.1,
v0.3.12: 0.5.1). The 2.1.x stream is also affected but is outside this issue's
scope (issue is scoped to 2.2.x via `[rhtpa-2.2]` suffix).

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at latest tag | Fixed? |
|--------|-----------|-----------------|----------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.5.1 (at v0.4.12) | NO |

The upstream branch (`release/0.4.z`) has not yet been updated to criterion
0.5.2. Remediation requires an upstream dependency bump followed by downstream
propagation.
