# Step 2 -- Version Impact Analysis

## Supportability Matrix

Data loaded from two version streams per the Version Streams table in Security Configuration.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Version Impact Table

CVE-2026-31812 affects quinn-proto versions before 0.11.14. The fix threshold is **0.11.14**.

Dependency versions extracted from Cargo.lock at each pinned commit tag (from the mock lock file data):

| Version | Stream | Pinned Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.8` | -- | **YES** | retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### Key observations

- **2.1.x stream**: All versions (2.1.0, 2.1.1) are affected, shipping quinn-proto 0.11.9.
- **2.2.x stream**: Versions 2.2.0 through 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version 0.11.14.
- **Version 2.2.2** is a retag of 2.2.1 (same backend pinned commit `v0.4.8`) -- the affected status is carried forward from 2.2.1 without re-checking the lock file.
- All version impact assessments use the pinned commit tags from the supportability matrix, not branch HEAD.

## Dependency Chain Context (Cargo)

```
Dependency chain for quinn-proto:
  backend (workspace) -> reqwest [features: http3] -> h3 -> quinn -> quinn-proto
  Profile: production (reqwest is a runtime dependency)
```
