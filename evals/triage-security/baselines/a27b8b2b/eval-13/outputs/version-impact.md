# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Tag (pinned commit) | quinn-proto | Affected? | Notes |
|---------|---------------------|-------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | |

All versions were checked using pinned commit tags from the supportability matrix, not branch HEAD (Important Rule 13). Version 2.2.2 is a retag of 2.2.1 (identical backend source commit `v0.4.8`), so the lock file check was skipped and the result was carried forward (Important Rule 5).

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Cross-Stream Impact

The issue is scoped to stream 2.2.x (suffix `[rhtpa-2.2]`), but version impact analysis reveals that stream **2.1.x** is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This triggers Case A (cross-stream impact) in Step 8.
