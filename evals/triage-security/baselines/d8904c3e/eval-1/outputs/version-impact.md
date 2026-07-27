# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | at fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | at fixed version |

## Evidence

Lock file versions extracted via `git show <tag>:Cargo.lock` for each pinned backend commit:

| Tag | quinn-proto version | Source |
|-----|---------------------|--------|
| v0.3.8 | 0.11.9 | Cargo.lock at backend v0.3.8 |
| v0.3.12 | 0.11.9 | Cargo.lock at backend v0.3.12 |
| v0.4.5 | 0.11.9 | Cargo.lock at backend v0.4.5 |
| v0.4.8 | 0.11.12 | Cargo.lock at backend v0.4.8 |
| v0.4.9 | _(retag of v0.4.8)_ | skipped -- same source as v0.4.8 |
| v0.4.11 | 0.11.14 | Cargo.lock at backend v0.4.11 |
| v0.4.12 | 0.11.14 | Cargo.lock at backend v0.4.12 |

## Fix Threshold

- Fix threshold: **0.11.14** (from Jira description; cross-validated with external CVE data)
- Versions < 0.11.14 are affected
- Versions >= 0.11.14 are NOT affected

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- ships quinn-proto 0.11.9
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 affected -- fixed starting at 2.2.3 (ships quinn-proto 0.11.14)
