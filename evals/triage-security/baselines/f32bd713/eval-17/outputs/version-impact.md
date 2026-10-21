# Step 2 -- Version Impact Analysis: TC-8001

## CVE Details

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14 (< 0.11.14)
- **Fixed version**: 0.11.14

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Source Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

### Impact Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- quinn-proto 0.11.9 < 0.11.14
- **2.2.x stream**: 3 of 5 versions affected (2.2.0, 2.2.1, 2.2.2) -- fixed in 2.2.3+

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Profile: production (quinn-proto is a runtime dependency)
  Ecosystem: Cargo (lock file: Cargo.lock)
  
Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | 0.11.9 | **NO** |
| 2.2.x | Cargo | `release/0.4.z` | 0.11.14 | **YES** |

### Upstream Fix Analysis

- **2.2.x stream (release/0.4.z)**: The upstream branch already ships quinn-proto 0.11.14 (the fixed version). Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already include the fix. Remediation for older 2.2.x versions is a **dependency bump** (the fix is available upstream).

- **2.1.x stream (release/0.3.z)**: The upstream branch still ships quinn-proto 0.11.9, which is within the affected range. Remediation for 2.1.x requires an **upstream backport** -- the fix must be applied to the release/0.3.z branch first, then propagated downstream.

## Cross-Stream Impact (Scoped Issue)

This issue is scoped to **2.2.x** (from summary suffix `[rhtpa-2.2]`). However, the version impact analysis reveals that the **2.1.x** stream is also affected. Case A (cross-stream impact) applies -- see remediation output for details.

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions field currently contains **RHTPA 2.0.0**, which does not correspond to any supported version in the configured streams. Based on version impact analysis, the correct Affects Versions for the scoped 2.2.x stream should be:

- **RHTPA 2.2.0**
- **RHTPA 2.2.1**
- **RHTPA 2.2.2**

Versions RHTPA 2.2.3 and RHTPA 2.2.4 should NOT be in Affects Versions (they ship the fixed version 0.11.14).
