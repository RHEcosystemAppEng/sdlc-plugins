# Step 2 -- Version Impact Analysis for CVE-2026-40215

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

All versions across both configured streams are analyzed. The issue is scoped to 2.2.x per the `[rhtpa-2.2]` suffix, but cross-stream impact on 2.1.x is also assessed.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scoped stream

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fix version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fix version |

## Dependency Chain Context (RPM)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The openssl-libs package is present in `rpms.lock.yaml` at each pinned tag, indicating it is an explicitly installed package (not inherited from the base image). Remediation is to update the package spec in the lock file.

## Upstream Fix Status

RPM ecosystem has no upstream source repository configured (Repository column is `--`). The fix is managed via the system package vendor (Red Hat errata). The Red Hat Security Advisory RHSA-2026:4021 provides the patched package version 3.0.7-28.el9_4.

## Cross-Stream Impact Summary

- **2.1.x**: ALL versions affected (2.1.0, 2.1.1) -- this is outside the current issue's scope
- **2.2.x**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are NOT affected (already at fix version)

The 2.1.x stream is also affected but is tracked separately. A cross-stream impact comment would be posted (Case B), and if no sibling CVE Jira exists for the 2.1.x stream, a preemptive remediation task would be created.
