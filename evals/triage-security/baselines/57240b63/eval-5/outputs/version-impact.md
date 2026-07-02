# Step 2 -- Version Impact Analysis: CVE-2026-40215

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs versions before 3.0.7-28.el9_4):

### 2.2.x stream (issue scope)

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|--------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

### 2.1.x stream (cross-stream reference)

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|--------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | |

Cross-stream impact: openssl-libs versions before 3.0.7-28.el9_4 also affects stream 2.1.x. The 2.1.x stream is tracked separately and may require its own PSIRT triage or companion CVE Jira.

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs found in rpms.lock.yaml at all build tags) -> explicit install
  SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to openssl-libs >= 3.0.7-28.el9_4, then regenerate the lock file.
```

The openssl-libs package is present in `rpms.lock.yaml` at every build tag in the 2.2.x stream, confirming it is an explicitly installed package (not inherited from the base image). The fix is to update the package specification to require >= 3.0.7-28.el9_4 and regenerate `rpms.lock.yaml`.

Note: SBOM verification via cosign was not performed because cosign is not available in this environment. The rpms.lock.yaml classification (explicit install) is used as the sole source of truth for package origin.

## Upstream Fix Status

RPM ecosystem does not have an Upstream Branch configured in the Ecosystem Mappings table (the Upstream Branch column is empty for the RPM row). Upstream fix check is not applicable -- the fix is delivered via the Red Hat advisory (RHSA-2026:4021) and picked up by updating the package spec in the Konflux release repo.
