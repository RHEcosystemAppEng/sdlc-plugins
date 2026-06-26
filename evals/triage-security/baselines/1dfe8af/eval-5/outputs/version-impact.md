# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

| Version | Build | openssl-libs | Affected? | Notes |
|---------|-------|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  Origin: explicit install (openssl-libs pinned in rpms.lock.yaml)

Remediation: update openssl-libs package spec in rpms.lock.yaml
(or rpms.in.yaml) to >= 3.0.7-28.el9_4 and regenerate the lock file.
```

## Cross-Stream Impact

The 2.1.x stream also ships vulnerable openssl-libs versions:

| Version | openssl-libs | Affected? |
|---------|--------------|-----------|
| 2.1.0 | 3.0.7-24.el9 | YES |
| 2.1.1 | 3.0.7-24.el9 | YES |

This issue is scoped to 2.2.x. The 2.1.x stream impact would be reported
via a cross-stream comment (Step 7 Case B) but remediation tasks are only
created for the 2.2.x stream within this issue's scope.
