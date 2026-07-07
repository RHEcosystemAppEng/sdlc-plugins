# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

### Scoped stream: 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Cross-stream: 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |

## Summary

- **2.2.x stream** (issue scope): versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.
- **2.1.x stream** (cross-stream): all versions (2.1.0, 2.1.1) are affected, shipping quinn-proto 0.11.9 which is within the vulnerable range (< 0.11.14).

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at Tag | Fixed? |
|--------|-----------|-----------------|----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11+) | YES |

- **2.2.x**: The upstream branch `release/0.4.z` already carries the fix at v0.4.11 and later. Remediation is a downstream propagation: update the source reference in the Konflux release repo to pick up an already-fixed tag.
- **2.1.x**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9. Remediation requires an upstream backport PR to bump quinn-proto on this branch, followed by downstream propagation.

## Affects Versions Correction

The Jira issue currently has Affects Versions set to **RHTPA 2.0.0**, which does not match any configured version stream. Based on version impact analysis, the correct Affects Versions are:

- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

(Scoped to the 2.2.x stream per the issue's `[rhtpa-2.2]` suffix. Cross-stream impact on 2.1.x is handled via Case B.)
