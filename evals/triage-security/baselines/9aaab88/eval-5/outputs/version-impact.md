# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs, affected before 3.0.7-28.el9_4)

### Stream: 2.2.x (rhtpa-release.0.4.z) -- Issue-scoped stream

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | fixed version |

### Stream: 2.1.x (rhtpa-release.0.3.z) -- Cross-stream analysis

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |

## Dependency Chain Context (RPM, explicit install)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml confirms: openssl-libs present in lock file
  Origin: explicit install (package is listed in rpms.lock.yaml)

  Remediation: update openssl-libs package spec in rpms.lock.yaml
  (or rpms.in.yaml) to >= 3.0.7-28.el9_4 and regenerate lock file.
```

The package `openssl-libs` is present in `rpms.lock.yaml` for all checked versions, making it an **explicit install** (not inherited from base image). Remediation requires updating the package spec in the RPM lock file configuration.

## Upstream Fix Status

RPM ecosystem has no upstream branch configured (Upstream Branch column is `--` in Ecosystem Mappings). The fix is delivered via the RHSA errata (RHSA-2026:4021) and available as openssl-libs-3.0.7-28.el9_4 from the RPM repositories.

## Summary

- **2.2.x stream (scoped)**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are fixed
- **2.1.x stream (cross-stream)**: versions 2.1.0, 2.1.1 are affected -- this is outside the current issue's scope and would be tracked by a companion CVE issue or proactive remediation
