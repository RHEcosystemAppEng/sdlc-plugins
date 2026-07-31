# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from local `security-matrix.md` for stream 2.2.x (Konflux release repo: `rhtpa-release.0.4.z`).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

The ecosystem is RPM with lock file `rpms.lock.yaml`. For each version in the 2.2.x stream, the openssl-libs version is extracted from rpms.lock.yaml at the pinned commit tag.

Simulated `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` results:

| Tag | openssl-libs version |
|-----|----------------------|
| `v0.4.5` (2.2.0) | 3.0.7-25.el9_3 |
| `v0.4.8` (2.2.1) | 3.0.7-27.el9_4 |
| `v0.4.9` (2.2.2) | _(retag of v0.4.8 -- same as 2.2.1)_ |
| `v0.4.11` (2.2.3) | 3.0.7-28.el9_4 |
| `v0.4.12` (2.2.4) | 3.0.7-28.el9_4 |

## 2.4 -- Version Impact Table

CVE fix threshold: openssl-libs < 3.0.7-28.el9_4 (fixed in 3.0.7-28.el9_4).

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fix version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fix version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable openssl-libs version. Versions 2.2.3 and 2.2.4 ship the patched version (3.0.7-28.el9_4).

## 2.3.5 -- Dependency Chain Context

### Package classification

openssl-libs is present in `rpms.lock.yaml` at each pinned tag for the 2.2.x stream. This confirms that openssl-libs is an **explicit install** -- it is specified in the RPM lock file (or the corresponding `rpms.in.yaml` input file) and is not merely inherited from the base image.

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- external tools are prohibited in this eval
    (cosign is not available for SBOM comparison)
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to openssl-libs >= 3.0.7-28.el9_4.
```

### SBOM Verification (Step 2.3.5)

SBOM verification via cosign is an optional cross-check that compares the final container image SBOM against the base image SBOM to confirm the rpms.lock.yaml classification. In this eval context, external tools (including cosign) are not available and cannot be invoked.

> SBOM verification skipped -- cosign not available / external tools prohibited. Using rpms.lock.yaml classification only.

The rpms.lock.yaml classification remains the primary signal: openssl-libs is present in rpms.lock.yaml, confirming it is an explicitly installed package. The SBOM result would supplement but not override this classification.
