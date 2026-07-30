# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

Data source: `rpms.lock.yaml` at each pinned tag in the 2.2.x supportability matrix.

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

### Summary

- **Affected**: 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1)
- **Not affected**: 2.2.3, 2.2.4
- Versions 2.2.0 through 2.2.2 ship openssl-libs versions older than the fix threshold (3.0.7-28.el9_4).
- Versions 2.2.3 and 2.2.4 ship the patched version 3.0.7-28.el9_4.

## Dependency Chain Context (Step 2.3.5)

### cosign availability

```
which cosign
/usr/bin/cosign
```

cosign is available. SBOM verification will be performed to cross-check the rpms.lock.yaml classification.

### Dependency chain for openssl-libs (RPM)

#### Version 2.2.0 (v0.4.5) -- AFFECTED

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification (cosign download sbom):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
  WARNING: SBOM classification disagrees with rpms.lock.yaml
    rpms.lock.yaml says: explicit install (package listed in lock file)
    SBOM comparison says: base image (present in both final and base image SBOMs)
    Investigate manually.
  Origin (primary signal -- rpms.lock.yaml): explicit install
```

#### Version 2.2.1 (v0.4.8) -- AFFECTED

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign download sbom):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
  WARNING: SBOM classification disagrees with rpms.lock.yaml
    rpms.lock.yaml says: explicit install (package listed in lock file)
    SBOM comparison says: base image (present in both final and base image SBOMs)
    Investigate manually.
  Origin (primary signal -- rpms.lock.yaml): explicit install
```

#### Version 2.2.2 (v0.4.9) -- AFFECTED (retag of 2.2.1)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install (same as 2.2.1, retag)
  SBOM verification (cosign download sbom):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
  WARNING: SBOM classification disagrees with rpms.lock.yaml
    rpms.lock.yaml says: explicit install (package listed in lock file)
    SBOM comparison says: base image (present in both final and base image SBOMs)
    Investigate manually.
  Origin (primary signal -- rpms.lock.yaml): explicit install
```

#### Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) -- NOT AFFECTED

These versions ship the fixed openssl-libs version (3.0.7-28.el9_4). No remediation needed. Dependency chain tracing is not required for unaffected versions.

### SBOM Discrepancy Summary

For all three affected versions (2.2.0, 2.2.1, 2.2.2), the SBOM classification **disagrees** with the rpms.lock.yaml classification:

| Version | rpms.lock.yaml | SBOM Comparison | Agreement? |
|---------|----------------|-----------------|------------|
| 2.2.0 | explicit install (present in lock file) | base image (in both final and base SBOMs) | NO |
| 2.2.1 | explicit install (present in lock file) | base image (in both final and base SBOMs) | NO |
| 2.2.2 | explicit install (present in lock file) | base image (in both final and base SBOMs) | NO |

The rpms.lock.yaml classification remains the **primary signal** -- the SBOM result supplements but does not override it. However, this discrepancy suggests that openssl-libs may be both inherited from the base image AND explicitly pinned in rpms.lock.yaml (a common pattern where the lock file re-declares a package already in the base image to control its version). Manual investigation is recommended to determine the correct remediation path:

- If the package is primarily a base image dependency that was re-pinned for version control, remediation may involve updating the base image tag rather than (or in addition to) the rpms.lock.yaml entry.
- If the package is a genuinely explicit install that also happens to be in the base image, remediation involves updating the version spec in rpms.in.yaml and regenerating rpms.lock.yaml.

## Cross-Stream Impact

The 2.1.x stream also ships vulnerable openssl-libs versions:

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

However, this issue is scoped to 2.2.x. Cross-stream impact for 2.1.x would be handled via Case A (cross-stream impact comment and preemptive remediation tasks) or through the 2.1.x stream's own CVE Jira.
