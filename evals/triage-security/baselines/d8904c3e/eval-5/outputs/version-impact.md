# Step 2 -- Version Impact Analysis: CVE-2026-40215

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### Stream 2.2.x (scoped stream)

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | fixed version |

### Stream 2.1.x (cross-stream analysis)

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | |

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

SBOM verification was not performed because `cosign` is not available in the
current environment. The rpms.lock.yaml classification (explicit install) is
used as the sole determination of package origin.

## Cross-Stream Impact Summary

- **2.2.x** (scoped): versions 2.2.0, 2.2.1, 2.2.2 are affected; 2.2.3 and 2.2.4 are fixed
- **2.1.x** (cross-stream): versions 2.1.0, 2.1.1 are affected -- requires Case A cross-stream impact notice
