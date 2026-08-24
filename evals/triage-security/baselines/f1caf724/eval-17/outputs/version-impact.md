# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

### Stream 2.2.x (scoped stream -- rhtpa-release.0.4.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | Fixed (>= 0.11.14) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | Fixed (>= 0.11.14) |

### Stream 2.1.x (cross-stream -- rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |

## Summary

- **Stream 2.2.x** (scoped): versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.
- **Stream 2.1.x** (cross-stream): all versions (2.1.0, 2.1.1) are affected. Both ship quinn-proto 0.11.9 which is within the vulnerable range (< 0.11.14).

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo ecosystem)
  Lock file: Cargo.lock
  Profile: production (quinn-proto is a runtime QUIC transport dependency)
```

quinn-proto is a direct dependency of the backend workspace, making remediation straightforward: bump quinn-proto to >= 0.11.14 in Cargo.toml.

## Affects Versions Correction (Step 3)

The issue is scoped to stream 2.2.x. The PSIRT-assigned Affects Versions are incorrect:

- **Current**: RHTPA 2.0.0 (no 2.0.x stream exists in the configuration)
- **Proposed** (scoped to 2.2.x only): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Versions 2.2.3 and 2.2.4 are NOT affected and must not be included. The 2.1.x versions belong to a companion/sibling issue scope and are excluded from this scoped issue's Affects Versions.

## Cross-Stream Impact (Case A)

This is a **scoped** issue (suffix `[rhtpa-2.2]`). The version impact analysis reveals that stream **2.1.x** is also affected (all versions ship quinn-proto 0.11.9 < 0.11.14).

Per Case A of the skill, a cross-stream impact comment would be posted and preemptive remediation tasks created for stream 2.1.x (unless a sibling CVE Jira already exists for that stream).
