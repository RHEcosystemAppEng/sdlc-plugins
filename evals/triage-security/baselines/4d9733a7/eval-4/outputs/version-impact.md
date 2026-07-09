# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

The version impact table includes ALL versions from the security-matrix.md supportability matrix across ALL streams (Important Rule 4). Since the issue is unscoped, all streams are checked. Each version uses the pinned commit tag from the supportability matrix (Important Rule 13).

| Version | Stream | Pinned Tag | h2 | Affected? | Notes |
|---------|--------|------------|-----|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | `v0.4.8` | 0.4.8 | NO | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | >= 0.4.8 (fixed) |

## Mixed Impact Summary

The version impact is **mixed across streams**:

- **2.1.x stream**: ALL versions (2.1.0, 2.1.1) are **YES** (affected) -- they ship h2 0.4.5, which is < 0.4.8
- **2.2.x stream**: ALL versions (2.2.0 through 2.2.4) are **NO** (not affected) -- they ship h2 >= 0.4.8 (the fixed version or later)

The 2.2.x stream already ships the patched version of h2. Remediation is only needed for the 2.1.x stream.

### Retag Handling (Important Rule 5)

Version 2.2.2 is a retag of 2.2.1 (identical backend source commit `v0.4.8`). The lock file check was skipped for 2.2.2 and the affected status was carried forward from 2.2.1: h2 0.4.8, which is >= 0.4.8, so 2.2.2 is also **NO** (not affected).

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (based on lock file evidence)
  Profile: production (h2 is a runtime HTTP/2 dependency)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml
```
