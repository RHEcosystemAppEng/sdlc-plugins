# Step 2 -- Version Impact Analysis

## CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### Scoped stream: 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|-----|-------------------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 0.4.9 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8: 3.0.7-27.el9_4) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | equals fixed version |

### Cross-stream impact: 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|-----|-------------------------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | 0.3.12 | `v0.3.12` | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

### Dependency Chain Context

Dependency chain for openssl-libs (RPM):
- rpms.lock.yaml: openssl-libs IS present in the lock file
- Origin: **explicit install** (package is specified in rpms.lock.yaml, not inherited from base image)
- Remediation: update the package spec in rpms.lock.yaml (or rpms.in.yaml) to >= 3.0.7-28.el9_4

### Summary

- **Scoped stream (2.2.x):** versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs (3.0.7-28.el9_4).
- **Cross-stream (2.1.x):** both 2.1.0 and 2.1.1 are affected. These are tracked by a companion issue (different stream scope) or may require separate PSIRT triage.
