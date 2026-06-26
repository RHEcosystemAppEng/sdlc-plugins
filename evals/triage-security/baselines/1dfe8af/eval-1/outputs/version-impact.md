# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Pinned Tag | quinn-proto | Affected? | Notes |
|---------|------------|-------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | `v0.4.8` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Method

- **Lock file**: `Cargo.lock` (per Ecosystem Mappings)
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- **Fix threshold**: 0.11.14 (from Jira description; cross-validated with external CVE databases)
- **Retag handling**: Version 2.2.2 uses pinned tag `v0.4.8` (same as 2.2.1 per supportability matrix note "backend retag of 2.2.1"), so the lock file check was skipped and the result carried forward from 2.2.1.

## Cross-Stream Summary

- **Stream 2.1.x**: ALL versions affected (2.1.0, 2.1.1 both ship quinn-proto 0.11.9)
- **Stream 2.2.x**: Versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3, 2.2.4 ship the fixed version (0.11.14)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.14 | Needs verification (check branch HEAD) |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | Fixed in released versions 2.2.3+ (v0.4.11 ships 0.11.14) |
