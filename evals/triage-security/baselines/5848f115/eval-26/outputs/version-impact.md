# Step 2 -- Version Impact Analysis: TC-8050

CVE-2026-99001 (criterion < 0.5.2, fix: 0.5.2)

## Version Impact Table -- Stream 2.2.x (issue scope)

| Version | Build Tag | criterion | Affected? | Notes |
|---------|-----------|-----------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.2.1 | v0.4.8 | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.2.4 | v0.4.12 | 0.5.1 | YES | 0.5.1 < 0.5.2 |

**All 2.2.x versions are affected.** Every version ships criterion 0.5.1, which is below the fix threshold of 0.5.2.

## Cross-Stream Impact -- Stream 2.1.x (outside issue scope)

| Version | Build Tag | criterion | Affected? | Notes |
|---------|-----------|-----------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.1.1 | v0.3.12 | 0.5.1 | YES | 0.5.1 < 0.5.2 |

**Stream 2.1.x is also affected.** This triggers Case A (cross-stream impact) in Step 8.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

**Dependency scope assessment:** criterion is declared in `[dev-dependencies]` in `backend/Cargo.toml`. It is used for benchmarks only and is NOT shipped in production builds or container images. Per the dependency scope decision tree:

- Dev-only dependencies still require remediation (supply chain risk -- compromised dev deps can inject malicious code during builds)
- Remediation tasks receive the `dev-dependency` label
- Priority is overridden to **Normal** regardless of CVE severity
- Task descriptions include: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

Remediation approach: bump criterion to >= 0.5.2 in `backend/Cargo.toml` `[dev-dependencies]` section (direct dependency -- straightforward version bump).

## Step 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Action |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Upstream backport needed: bump criterion to >= 0.5.2 |
| 2.1.x | Cargo | release/0.3.z | Cross-stream -- tracked separately (Case A) |

Note: Upstream fix status at branch HEAD was not checked (eval mode -- no git access). The remediation tasks assume the upstream fix has not yet been applied.
