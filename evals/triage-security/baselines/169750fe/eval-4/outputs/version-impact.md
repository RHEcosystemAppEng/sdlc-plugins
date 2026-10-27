# Step 2 -- Version Impact Analysis: TC-8004

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | >= 0.4.8 (fixed) |

## Stream-Level Summary

| Stream | Versions Affected | Versions Not Affected | Stream Status |
|--------|-------------------|-----------------------|---------------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | **AFFECTED** -- all versions ship h2 0.4.5 |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NOT AFFECTED** -- all versions ship h2 >= 0.4.8 |

## Mixed Impact Analysis

This is a **mixed impact** scenario: the vulnerability affects versions across streams differently.

- **2.1.x stream**: ALL versions (2.1.0, 2.1.1) ship h2 0.4.5, which is within the affected range (< 0.4.8). Both versions are **affected**.
- **2.2.x stream**: ALL versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold. No versions in this stream are affected.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime dependency)

  2.1.x stream: h2 0.4.5 (vulnerable)
  2.2.x stream: h2 >= 0.4.8 (fixed)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 version at branch | Fixed? |
|--------|-----------|-----------------|----------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | _(to be verified)_ | _(to be verified)_ |
| 2.2.x | Cargo | `release/0.4.z` | >= 0.4.8 | YES |

The 2.2.x stream already ships the fixed version. Remediation is needed only for the 2.1.x stream.
