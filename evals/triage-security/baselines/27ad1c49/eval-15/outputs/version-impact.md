# Step 2 - Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed at 0.11.14 |

## Summary

- **Affected versions (2.2.x stream, in scope)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (2.2.x stream)**: 2.2.3, 2.2.4
- **Affected versions (2.1.x stream, cross-stream)**: 2.1.0, 2.1.1
- **Fix threshold**: quinn-proto >= 0.11.14

## Dependency Chain Context

Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present directly in Cargo.lock)
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock

## Cross-Stream Impact

The issue is scoped to stream 2.2.x via the `[rhtpa-2.2]` suffix, but the version impact analysis reveals that stream **2.1.x** is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, which is within the vulnerable range). This cross-stream impact triggers Case A handling in Step 8.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

- **2.2.x stream**: the upstream branch `release/0.4.z` already ships the fix (0.11.14). Remediation is a dependency bump (`cargo update`) + downstream propagation.
- **2.1.x stream**: the upstream branch `release/0.3.z` does NOT ship the fix (0.11.9). Remediation requires an upstream backport + downstream propagation.
