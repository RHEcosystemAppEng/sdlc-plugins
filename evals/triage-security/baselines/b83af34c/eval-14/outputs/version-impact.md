# Step 2 -- Version Impact Analysis for TC-8005

## CVE-2026-40215: openssl-libs (versions before 3.0.7-28.el9_4)

Stream scope: **2.2.x** (per issue suffix `[rhtpa-2.2]`)

## 2.1 -- Supportability Matrix

Loaded from security-matrix-mock.md. Stream 2.2.x covers versions 2.2.0 through 2.2.4.

## 2.3 -- Dependency Version Extraction

Ecosystem: RPM. Lock file: rpms.lock.yaml. Fixed version threshold: 3.0.7-28.el9_4.

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

## 2.3.5 -- Dependency Chain Context

For each affected version, the dependency chain traces how openssl-libs entered the
container image build. The classification uses rpms.lock.yaml as the primary signal,
with optional SBOM verification via cosign providing a supplementary cross-check.

### Version 2.2.0 (v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) --> explicit install
  SBOM verification (cosign download sbom):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

  Primary classification (rpms.lock.yaml): explicit install
  Origin: explicit install (rpms.lock.yaml is the primary signal; SBOM result
  supplements but does not override)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml.
```

### Version 2.2.1 (v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) --> explicit install
  SBOM verification (cosign download sbom):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

  Primary classification (rpms.lock.yaml): explicit install
  Origin: explicit install (rpms.lock.yaml is the primary signal; SBOM result
  supplements but does not override)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml.
```

### Version 2.2.2 (v0.4.9) -- retag of 2.2.1

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (same as 2.2.1 / v0.4.8: 3.0.7-27.el9_4) --> explicit install
  SBOM verification (cosign download sbom):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

  Primary classification (rpms.lock.yaml): explicit install
  Origin: explicit install (rpms.lock.yaml is the primary signal; SBOM result
  supplements but does not override)

Note: retag of 2.2.1 -- same dependency chain applies.
```

## Cross-Stream Impact (informational)

The 2.1.x stream (outside issue scope) also ships vulnerable openssl-libs versions:
- 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9 -- AFFECTED
- 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9 -- AFFECTED

These versions are tracked by companion issues or may require separate PSIRT triage.

## Summary

Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs (below the 3.0.7-28.el9_4
fix threshold). Versions 2.2.3 and 2.2.4 ship the fixed version and are not affected.

For all affected versions, rpms.lock.yaml classifies openssl-libs as an explicit install.
SBOM verification via `cosign download sbom` shows the package present in both the final
container image SBOM and the base image SBOM, which would classify it as a base image
package. This disagrees with the rpms.lock.yaml classification. Per the skill protocol,
rpms.lock.yaml remains the primary signal -- the SBOM result supplements but does not
override the lock file classification. The discrepancy is flagged for manual investigation.
