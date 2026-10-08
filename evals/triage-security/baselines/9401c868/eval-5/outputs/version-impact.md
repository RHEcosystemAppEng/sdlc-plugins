# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scoped to **2.2.x** stream per issue suffix `[rhtpa-2.2]`.

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

### Cross-stream impact (for Case A evaluation)

The 2.1.x stream is also affected (outside this issue's scope):

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -- explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update openssl-libs package spec in rpms.lock.yaml
(or rpms.in.yaml) to >= 3.0.7-28.el9_4.
```

The openssl-libs package is present in `rpms.lock.yaml` across all checked tags in the
2.2.x stream, confirming it is an explicitly installed package (not inherited from the
base image).

**SBOM verification status**: cosign is not available in this environment.
SBOM comparison between final and base image SBOMs was skipped.
Classification is based on rpms.lock.yaml presence only.
