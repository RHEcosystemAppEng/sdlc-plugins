# Step 2 -- Version Impact Analysis for CVE-2026-40215

## Version Impact Table (scoped stream: 2.2.x)

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

## Cross-Stream Impact (2.1.x -- outside issue scope)

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | |

## Dependency Chain Context (RPM)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install (openssl-libs listed in rpms.lock.yaml)
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the openssl-libs package spec in rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

## Analysis Summary

- **2.2.x stream**: Versions 2.2.0, 2.2.1, and 2.2.2 shipped vulnerable openssl-libs
  (versions 3.0.7-25.el9_3 and 3.0.7-27.el9_4, both below the fix threshold of
  3.0.7-28.el9_4). The fix was picked up starting in version **2.2.3** (build tag
  v0.4.11), which ships openssl-libs 3.0.7-28.el9_4. The latest release (2.2.4)
  also ships the fixed version. No new remediation task is needed for the 2.2.x
  stream -- the fix is already present in current releases.

- **2.1.x stream (cross-stream)**: Both 2.1.0 and 2.1.1 ship openssl-libs 3.0.7-24.el9,
  which is vulnerable. The 2.1.x stream has NOT picked up the fix. This is tracked
  outside the scope of TC-8005 (which is scoped to 2.2.x).
