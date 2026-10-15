# Step 2 — Version Impact Analysis

## Supportability Matrix (2.2.x stream)

Loaded from security-matrix.md for stream rhtpa-release.0.4.z (2.2.x).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Dependency Version Extraction (rpms.lock.yaml)

Ecosystem: **RPM**
Lock file: **rpms.lock.yaml**
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

| Version | Tag | openssl-libs version (from rpms.lock.yaml) |
|---------|-----|---------------------------------------------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 |
| 2.2.2 | `v0.4.9` | _(retag of v0.4.8 — same as 2.2.1)_ |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 |

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | — | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | **NO** | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | **NO** | = fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship the vulnerable openssl-libs version. Versions 2.2.3 and 2.2.4 ship the patched version (3.0.7-28.el9_4).

## Step 2.3.5 — Dependency Chain Context

### Package Classification

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT — explicit install
  SBOM verification: skipped — cosign is not available (external tools are prohibited in this eval environment)
  Origin: explicit install (openssl-libs is specified in rpms.lock.yaml)
```

**rpms.lock.yaml classification**: openssl-libs is **present** in rpms.lock.yaml for all 2.2.x versions. This presence is the **primary classification signal** — the lock file is the source of truth for determining package origin.

- **Classification**: explicit install (package is listed in rpms.lock.yaml)
- **Remediation path**: update the package spec in rpms.lock.yaml (or the corresponding rpms.in.yaml)

### SBOM Verification Status

SBOM verification was **skipped** because cosign is not available in this eval environment (external tools are prohibited). The rpms.lock.yaml classification alone is used:

> SBOM verification skipped -- cosign not available. Using rpms.lock.yaml classification only.

The rpms.lock.yaml classification (explicit install) is the primary and authoritative signal. SBOM comparison via cosign would serve as a supplementary cross-check but does not override the lock file classification.
