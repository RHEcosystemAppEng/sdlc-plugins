# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Evidence

Lock file versions extracted from `git show <tag>:Cargo.lock` for the backend repository:

| Tag | quinn-proto version | Source |
|-----|---------------------|--------|
| v0.3.8 (2.1.0) | 0.11.9 | Cargo.lock |
| v0.3.12 (2.1.1) | 0.11.9 | Cargo.lock |
| v0.4.5 (2.2.0) | 0.11.9 | Cargo.lock |
| v0.4.8 (2.2.1) | 0.11.12 | Cargo.lock |
| v0.4.9 (2.2.2) | -- | retag of v0.4.8 |
| v0.4.11 (2.2.3) | 0.11.14 | Cargo.lock |
| v0.4.12 (2.2.4) | 0.11.14 | Cargo.lock |

Fix threshold: quinn-proto >= 0.11.14 (from Jira description, confirmed by CVE record).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Fixed at v0.4.11+ (quinn-proto 0.11.14) |
| 2.1.x | Cargo | release/0.3.z | NOT fixed (latest v0.3.12 ships 0.11.9) |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- ships quinn-proto 0.11.9
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3, 2.2.4 NOT affected (ship fixed quinn-proto 0.11.14)
- The fix was introduced in the 2.2.x stream starting with build 0.4.11 (version 2.2.3)
- The 2.1.x stream has no upstream fix on release/0.3.z
