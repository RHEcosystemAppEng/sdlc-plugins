# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

### All Streams (full landscape)

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | (0.11.12) | YES | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

### Stream-Scoped Summary (2.2.x only, per issue scope)

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | `v0.4.9` | (0.11.12) | YES | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | ships fixed version |

### Retag Identification

- **2.2.2** (build 0.4.9, tag `v0.4.9`) is a retag of **2.2.1** (build 0.4.8, tag `v0.4.8`). The backend column shows the same pinned commit `v0.4.8`. Lock file check was skipped for 2.2.2; the quinn-proto version (0.11.12) is carried forward from 2.2.1.

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn or reqwest [features: http3] -> quinn-proto
  Ecosystem: Cargo (Cargo.lock)
  Profile: production (runtime dependency)

  Present in all versions from 2.1.0 onward.
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fixed? | Notes |
|--------|-----------|-----------------|--------|-------|
| 2.2.x | Cargo | release/0.4.z | YES | 2.2.3+ already ships 0.11.14 (the fixed version) |

The upstream branch `release/0.4.z` already contains the fix -- versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14. Remediation for affected versions (2.2.0, 2.2.1, 2.2.2) requires a Konflux release repo update to reference a source tag that includes quinn-proto >= 0.11.14.

### Cross-Stream Impact

The 2.1.x stream (versions 2.1.0 and 2.1.1) is also affected (quinn-proto 0.11.9 < 0.11.14). However, this issue is scoped to the 2.2.x stream per the `[rhtpa-2.2]` suffix. Cross-stream impact for 2.1.x would be tracked by a separate PSIRT-created companion issue.
