# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### Scoped stream: 2.2.x

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | 0.4.9 | `v0.4.9` | 3.0.7-27.el9_4 | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | fixed version |

### Cross-stream analysis: 2.1.x

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |
| 2.1.1 | 0.3.12 | `v0.3.12` | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |

### Summary

- **2.2.x stream** (scoped): versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs (3.0.7-28.el9_4).
- **2.1.x stream** (cross-stream): all versions (2.1.0, 2.1.1) are affected. This stream has no version shipping the fix.

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs pinned in lock file) --> explicit install
  SBOM verification: skipped -- cosign not available / external tools prohibited
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

  Affected versions in 2.2.x stream:
    2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3
    2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4
    2.2.2 (v0.4.9): openssl-libs 3.0.7-27.el9_4 (retag of 2.2.1)

  Fixed in 2.2.x stream starting with:
    2.2.3 (v0.4.11): openssl-libs 3.0.7-28.el9_4

  Remediation: update openssl-libs to >= 3.0.7-28.el9_4 in rpms.lock.yaml
  (regenerate from rpms.in.yaml or equivalent package spec).
```

## Upstream Fix Status

Not applicable for RPM ecosystem -- openssl-libs is a system package with no upstream branch configured in the Ecosystem Mappings table. The fix is tracked via RHSA-2026:4021.
