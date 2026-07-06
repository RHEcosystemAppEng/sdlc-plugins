# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### Scoped stream: 2.2.x

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs.
Versions 2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4).

### Cross-stream analysis: 2.1.x

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | |

**Cross-stream impact**: All versions in the 2.1.x stream are also affected.
The 2.1.x stream ships openssl-libs 3.0.7-24.el9, which is within the
vulnerable range (< 3.0.7-28.el9_4). This triggers Case B (cross-stream
impact notice). A companion CVE Jira with stream suffix `[rhtpa-2.1]` should
be checked; if none exists, preemptive remediation tasks should be created
for the 2.1.x stream.

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available and external tools prohibited
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The package `openssl-libs` is present in `rpms.lock.yaml` at each pinned tag
in the 2.2.x stream, confirming it is an explicitly installed package (not
inherited from the base image).

**SBOM verification status**: SBOM comparison was not performed because
`cosign` is not available in this environment and external tool invocation is
prohibited. The rpms.lock.yaml classification (explicit install) is used as
the sole source of truth for package origin.
