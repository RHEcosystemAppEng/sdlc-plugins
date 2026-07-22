# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs versions before 3.0.7-28.el9_4):

### 2.2.x stream (scoped)

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|--------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | at fixed version |

### 2.1.x stream (cross-stream reference)

| Version | Build Tag | openssl-libs | Affected? | Notes |
|---------|-----------|--------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | |

**Summary**: Within the scoped 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs 3.0.7-28.el9_4. The 2.1.x stream is also affected across all versions (cross-stream impact -- see Case B in Step 8).

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.lock.yaml to >= 3.0.7-28.el9_4.
```

openssl-libs is present in `rpms.lock.yaml` for all checked tags in the 2.2.x stream, classifying it as an **explicit install** (not inherited from the base image). The SBOM cross-verification via cosign was not performed because cosign is not available in this environment. The rpms.lock.yaml classification stands as the sole source for package origin determination.

## Upstream Fix Status

RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings table (column is `--`). Upstream fix check is not applicable for system packages -- the fix is delivered through the RPM package update pipeline (RHSA-2026:4021 advisory confirms the fix is available at 3.0.7-28.el9_4).
