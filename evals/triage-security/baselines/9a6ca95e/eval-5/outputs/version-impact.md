# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs versions before 3.0.7-28.el9_4):

### 2.2.x stream (in-scope)

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 0.4.8 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 0.4.9 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 0.4.12 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

### 2.1.x stream (cross-stream, out of scope for this issue)

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | 0.3.12 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

### Summary

- **In-scope (2.2.x):** versions 2.2.0, 2.2.1, and 2.2.2 are affected; versions 2.2.3 and 2.2.4 are NOT affected (ship the fixed version 3.0.7-28.el9_4).
- **Cross-stream (2.1.x):** all versions (2.1.0, 2.1.1) are affected (ship 3.0.7-24.el9, well below the fix threshold). This is relevant for Step 8 Case B cross-stream impact.

## Dependency Chain (Step 2.3.5)

Dependency chain for openssl-libs (RPM):

```
rpms.lock.yaml: openssl-libs PRESENT -> explicit install
SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.lock.yaml (or rpms.in.yaml).
```

The package `openssl-libs` is present in `rpms.lock.yaml` at each pinned tag, confirming it is an **explicitly installed** RPM package (not inherited from the base image). Since `cosign` is not available in this environment, SBOM comparison to cross-check the rpms.lock.yaml classification was skipped. The rpms.lock.yaml classification alone is used.

### Introduction point

openssl-libs is present across all checked versions in both the 2.1.x and 2.2.x streams. It was not introduced at a specific version boundary -- it has been an explicit dependency throughout all tracked releases.

## Upstream Fix Status (Step 2.5)

The RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings table (the column is empty: `--`). RPM system packages are not sourced from an upstream git branch -- they come from the distribution vendor's package repositories. Therefore, the upstream fix check is not applicable for this ecosystem.

The fix is available as RHSA-2026:4021 (Red Hat Security Advisory), which provides the patched openssl-libs 3.0.7-28.el9_4 package.
