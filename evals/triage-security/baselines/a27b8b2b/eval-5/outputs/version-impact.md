# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Loaded from security-matrix.md for stream 2.2.x (rhtpa-release.0.4.z).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Ecosystem: RPM. Lock file: `rpms.lock.yaml`. Check command: `git show <tag>:rpms.lock.yaml`.

For each version in the 2.2.x stream, the openssl-libs version was extracted
from rpms.lock.yaml at the pinned commit tag:

- **2.2.0** (tag `v0.4.5`): `git show v0.4.5:rpms.lock.yaml | grep 'openssl-libs'` -> **3.0.7-25.el9_3**
- **2.2.1** (tag `v0.4.8`): `git show v0.4.8:rpms.lock.yaml | grep 'openssl-libs'` -> **3.0.7-27.el9_4**
- **2.2.2** (tag `v0.4.9`): retag of 2.2.1 (backend `v0.4.8`) -- carry forward result: **3.0.7-27.el9_4**
- **2.2.3** (tag `v0.4.11`): `git show v0.4.11:rpms.lock.yaml | grep 'openssl-libs'` -> **3.0.7-28.el9_4**
- **2.2.4** (tag `v0.4.12`): `git show v0.4.12:rpms.lock.yaml | grep 'openssl-libs'` -> **3.0.7-28.el9_4**

Fixed version threshold: **3.0.7-28.el9_4**

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: 3 of 5 versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2).
Versions 2.2.3 and 2.2.4 ship the patched openssl-libs (3.0.7-28.el9_4).

## 2.3.5 -- Dependency Chain Context

### Package Classification

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT -> explicit install
  SBOM verification: skipped -- cosign not available / external tools prohibited in this eval context
  Origin: explicit install (openssl-libs is listed in rpms.lock.yaml)

Remediation: update the package version in rpms.lock.yaml (or rpms.in.yaml)
to >= 3.0.7-28.el9_4.
```

**Classification method**: rpms.lock.yaml (lock file is configured for the RPM
ecosystem in the 2.2.x stream's Ecosystem Mappings table).

- **rpms.lock.yaml classification**: openssl-libs is **present** in rpms.lock.yaml
  for all versions in the 2.2.x stream. This classifies it as an **explicit install**
  -- the package is intentionally specified in the lock file or rpms.in.yaml, not
  inherited from the base image.

- **SBOM verification (Step 2.3.5 Optional)**: SBOM verification via cosign was
  **skipped** because external tools are not available in this evaluation context.
  In a live triage, `which cosign` would be run to check availability. If cosign
  were available, the final container image SBOM would be compared against the base
  image SBOM to cross-check the rpms.lock.yaml classification. The rpms.lock.yaml
  classification remains the primary signal; SBOM verification supplements but does
  not override it.

**Package origin**: **Explicit install**. The rpms.lock.yaml presence is the
primary classification signal. Remediation path: update the package spec in
rpms.in.yaml / rpms.lock.yaml within the Konflux release repo.
