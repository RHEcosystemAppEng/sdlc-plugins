# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | meets fix threshold |
| 2.2.4 | 3.0.7-28.el9_4 | NO | meets fix threshold |

## Cross-stream Impact (informational)

The 2.1.x stream is also affected but is outside this issue's scope:

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | |
| 2.1.1 | 3.0.7-24.el9 | YES | |

## Dependency Chain Context (Step 2.3.5)

Dependency chain for openssl-libs (RPM):

- **Ecosystem**: RPM (system package)
- **Lock file**: rpms.lock.yaml
- **Presence in lock file**: openssl-libs IS present in rpms.lock.yaml
- **Classification**: **explicit install** — the package is specified in the RPM lock file (rpms.lock.yaml), not inherited from the base image
- **Remediation path**: Update the package spec in rpms.lock.yaml (or rpms.in.yaml) to >= 3.0.7-28.el9_4
