# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

The version impact table includes ALL versions from the security-matrix.md supportability matrix across both streams (Important Rule 4). Each version uses the pinned commit tag from the supportability matrix, not branch HEAD (Important Rule 13).

| Version | Stream | Pinned Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.8` | 0.11.12 | YES | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | |

### Retag Handling (Important Rule 5)

Version 2.2.2 is a retag of 2.2.1 (identical backend source commit `v0.4.8`). The lock file check was skipped for 2.2.2 and the affected status was carried forward from 2.2.1: quinn-proto 0.11.12, which is < 0.11.14, so 2.2.2 is also **YES** (affected).

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

### Cross-Stream Observation

The 2.1.x stream (versions 2.1.0, 2.1.1) is also affected. Since this issue is scoped to [rhtpa-2.2], this observation will be reported as a cross-stream impact notice in Step 8 (Case B).
