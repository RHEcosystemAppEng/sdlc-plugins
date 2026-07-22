# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-99001 (criterion versions before 0.5.2):

| Version | Build Tag | criterion | Affected? | Notes |
|---------|-----------|-----------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.5.1 | YES | |
| 2.2.1 | v0.4.8 | 0.5.1 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.5.1 | YES | |
| 2.2.4 | v0.4.12 | 0.5.1 | YES | |

All versions in the 2.2.x stream ship criterion 0.5.1, which is below the fix threshold of 0.5.2.

## Cross-Stream Check (informational)

Since this issue is scoped to the 2.2.x stream, only the 2.2.x versions are analyzed for remediation. For cross-stream awareness, the 2.1.x stream also ships criterion 0.5.1 at all versions (v0.3.8 and v0.3.12), but remediation for that stream is tracked by its own CVE Jira if one exists.

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

**Dependency scope assessment**: criterion is declared in `[dev-dependencies]` in
`backend/Cargo.toml`. It is used for benchmarks only and is NOT shipped in
production builds. Per the dependency scope decision tree, this is a dev-only
dependency. Remediation tasks will carry the `dev-dependency` label and priority
will be set to Normal regardless of CVE severity (supply chain risk only).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Unknown -- criterion at branch HEAD not checked (simulated environment) |

Note: In a real triage, the upstream branch HEAD would be inspected via
`git show release/0.4.z:Cargo.lock` to determine if the fix is already present.
