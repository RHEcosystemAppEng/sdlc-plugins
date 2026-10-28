# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as v0.4.8: quinn-proto 0.11.12) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | **NO** | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | **NO** | ships fixed version |

## Evidence

All quinn-proto versions were extracted from `Cargo.lock` at the pinned source commits listed in the supportability matrix. Version 2.2.2 is a retag of 2.2.1 (build v0.4.9 retags v0.4.8), so the lock file check was skipped and the result carried forward from 2.2.1.

Fix threshold: quinn-proto >= 0.11.14 (from Jira description and CVE record).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|------------|---------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | `v0.3.12` | 0.11.9 | **NO** |
| 2.2.x | Cargo | `release/0.4.z` | `v0.4.12` | 0.11.14 | **YES** |

### Upstream fix analysis

- **2.2.x stream (release/0.4.z):** The upstream branch already ships quinn-proto 0.11.14. The fix was incorporated starting with build v0.4.11 (version 2.2.3, released 2026-03-23). Versions 2.2.3 and 2.2.4 already include the fix. Remediation approach: dependency bump variant (the fix is already available on the branch).

- **2.1.x stream (release/0.3.z):** The upstream branch still ships quinn-proto 0.11.9, which is within the affected range. Neither version 2.1.0 nor 2.1.1 includes the fix. Remediation approach: upstream backport required (the fix is not yet available on this branch).

## Summary

- **2.1.x stream:** ALL versions affected (2.1.0, 2.1.1). Upstream fix NOT available.
- **2.2.x stream:** Versions 2.2.0, 2.2.1, 2.2.2 affected. Versions 2.2.3, 2.2.4 NOT affected (fix already shipped). Upstream fix available on release/0.4.z.
