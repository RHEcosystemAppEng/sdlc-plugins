# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4)

Scope: **2.2.x stream** (from issue stream suffix [rhtpa-2.2])

Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 0.4.8 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 0.4.9 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.4.11 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 0.4.12 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable openssl-libs. Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4) and are NOT affected.

## Cross-Stream Impact (informational)

The 2.1.x stream (outside the scope of this issue) is also affected:

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|--------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

Cross-stream impact: openssl-libs vulnerability also affects stream 2.1.x. These streams are tracked by companion issues or may require separate PSIRT triage.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to openssl-libs >= 3.0.7-28.el9_4.
```

Package origin classification:
- **Method**: rpms.lock.yaml inspection (RPM lock file is configured for this stream)
- **Result**: openssl-libs IS present in rpms.lock.yaml, indicating it is an **explicit install** (not inherited from a base image)
- **SBOM verification**: Skipped -- cosign is not available in this environment. The rpms.lock.yaml classification is used alone.
- **Remediation path**: Update the package version specification in `rpms.in.yaml` and regenerate `rpms.lock.yaml`

## Upstream Fix Status

RPM ecosystem has no upstream branch configured (Upstream Branch column is empty in Ecosystem Mappings). The fix is delivered via Red Hat errata RHSA-2026:4021, which provides openssl-libs 3.0.7-28.el9_4. No upstream source repo check is applicable for system packages.
