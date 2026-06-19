# Step 2 - Version Impact Analysis: TC-8005

## CVE-2026-40215 (openssl-libs, affected versions before 3.0.7-28.el9_4)

### Version Impact Table (2.2.x stream)

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

### Dependency Chain Context (RPM, system package)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml confirms: openssl-libs present in lock file
  Origin: explicit install (present in rpms.lock.yaml)

  Remediation: update openssl-libs package spec in rpms.lock.yaml
  (or rpms.in.yaml) to >= 3.0.7-28.el9_4.
```

### Cross-Stream Impact (informational)

The 2.1.x stream is also affected (for reference, outside this issue's scope):

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

This is informational only - the 2.1.x stream is tracked by a separate PSIRT issue (if one exists).

### Summary

- **Affected versions in 2.2.x stream**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions in 2.2.x stream**: 2.2.3, 2.2.4
- The fix was picked up starting with build v0.4.11 (version 2.2.3), which includes openssl-libs 3.0.7-28.el9_4.
