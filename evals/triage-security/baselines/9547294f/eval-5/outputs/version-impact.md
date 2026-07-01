# Step 2 — Version Impact Analysis for CVE-2026-40215

## Version Impact Table

Issue is scoped to **2.2.x** stream (suffix `[rhtpa-2.2]`). All versions from the 2.2.x supportability matrix are included.

Lock file used: **rpms.lock.yaml** (RPM ecosystem)

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|-------------------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship the vulnerable openssl-libs package. Versions 2.2.3 and 2.2.4 ship the patched version (3.0.7-28.el9_4) and are NOT affected.

## Dependency Chain Context (Step 2.3.5)

### Package Origin Classification

**Method**: rpms.lock.yaml inspection (RPM lock file is configured for the 2.2.x stream)

Dependency chain for openssl-libs (RPM):
- **rpms.lock.yaml**: present — openssl-libs is listed in rpms.lock.yaml for affected versions (v0.4.5, v0.4.8)
- **Classification**: **explicit install** — openssl-libs appears in rpms.lock.yaml, indicating it is an explicitly installed package in the container image (not solely inherited from the base image)
- **SBOM verification**: skipped — cosign is not available in the current environment (external tools are prohibited for this eval). Using rpms.lock.yaml classification only.

> Note: SBOM verification was skipped because external tools (including cosign) are not permitted in this evaluation context. In a live triage, if cosign were available, the skill would download the final container image SBOM and base image SBOM via `cosign download sbom` and compare openssl-libs presence in both to cross-check the rpms.lock.yaml classification. The rpms.lock.yaml classification remains the primary signal regardless of SBOM results.

**Origin**: explicit install (openssl-libs specified via rpms.lock.yaml / rpms.in.yaml)
**Remediation path**: Update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4, then regenerate the lock file.
