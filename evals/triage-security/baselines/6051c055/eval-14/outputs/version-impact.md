# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for rhtpa-release.0.4.z (2.2.x stream)
Last-Updated: 2026-06-28T10:00:00Z (9 days ago -- within 14-day freshness threshold)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
Fix threshold: 3.0.7-28.el9_4

| Version | Tag | openssl-libs version | Source |
|---------|-----|----------------------|--------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | rpms.lock.yaml |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | rpms.lock.yaml |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | rpms.lock.yaml |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | rpms.lock.yaml |

## 2.3.5 -- Dependency Chain Context

### Versions 2.2.0 through 2.2.2 (affected)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM comparison result: present in both final and base image SBOMs --> base image origin

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    rpms.lock.yaml says: explicit install (package IS listed in lock file)
    SBOM comparison says: base image origin (package appears in both final and base image SBOMs)
    Investigate manually -- the package may be both explicitly installed AND present
    in the base image, or the lock file entry may be redundant.

  Primary signal: rpms.lock.yaml (explicit install) -- lock file remains authoritative
  Origin (per rpms.lock.yaml): explicit install

  Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml to
  openssl-libs >= 3.0.7-28.el9_4
```

### Versions 2.2.3 and 2.2.4 (not affected)

These versions already ship openssl-libs 3.0.7-28.el9_4 (the fixed version). No dependency chain trace needed.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix.

**SBOM verification note**: cosign is available and SBOM comparison was performed for affected versions. The SBOM classification (base image origin) disagrees with the rpms.lock.yaml classification (explicit install) for versions 2.2.0--2.2.2. The rpms.lock.yaml remains the primary signal; the discrepancy is flagged for manual investigation. See dependency chain output above for details.
