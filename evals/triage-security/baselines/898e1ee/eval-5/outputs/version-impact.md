# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Stream scope: **2.2.x** (from issue suffix `[rhtpa-2.2]`)

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 0.4.9 | `v0.4.9` | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | equals fixed version |

**Data source**: `rpms.lock.yaml` at each pinned tag in the Konflux release repo `rhtpa-release.0.4.z`.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present → explicit install
  Origin: explicit install (openssl-libs is specified in rpms.lock.yaml)

Remediation: update the package version spec in rpms.lock.yaml (or rpms.in.yaml)
to >= 3.0.7-28.el9_4, then regenerate the lock file.
```

## Cross-Stream Impact

The 2.1.x stream also ships vulnerable versions of openssl-libs:

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|--------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | `v0.3.12` | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

The 2.1.x stream is outside this issue's scope (`[rhtpa-2.2]`). Cross-stream impact would be reported via comment on TC-8005 (Step 7, Case B).
