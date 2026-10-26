# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | YES | < 0.11.14 |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | YES | < 0.11.14 |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | >= fixed version |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | >= fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: source dependency (Cargo)
  Lock file: Cargo.lock
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.lock via cargo update
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag at HEAD | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|--------------------|--------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

### Remediation path implications

- **2.2.x stream**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (fixed). Remediation is a **dependency bump** (`cargo update -p quinn-proto`) plus downstream propagation to update the backend source reference in `rhtpa-release.0.4.z`.
- **2.1.x stream**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 (vulnerable). Remediation requires an **upstream backport** (bump quinn-proto on `release/0.3.z`) plus downstream propagation.

## Affects Versions Correction (Step 3)

The issue is scoped to 2.2.x. Only 2.2.x versions should be in Affects Versions.

- **Current Affects Versions**: RHTPA 2.0.0 (INCORRECT -- no 2.0.x stream exists)
- **Proposed Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14). The 2.1.x versions are affected but belong to a different stream scope and would be tracked via a sibling CVE issue or preemptive remediation tasks.

## Cross-Stream Impact Summary

The issue is scoped to **2.2.x** via suffix `[rhtpa-2.2]`. Stream **2.1.x** is also affected (all versions ship quinn-proto 0.11.9). Since no sibling CVE Jira exists for the 2.1.x stream, **Case A** applies: preemptive remediation tasks will be created for the 2.1.x stream.
