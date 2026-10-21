# Step 2 -- Version Impact Analysis: TC-8005

CVE-2026-40215 | openssl-libs | versions before 3.0.7-28.el9_4

## 2.1 -- Supportability Matrix (Loaded)

Loaded security matrix for two streams from `security-matrix-mock.md`:

- **2.1.x** (rhtpa-release.0.3.z): 2 versions (2.1.0, 2.1.1)
- **2.2.x** (rhtpa-release.0.4.z): 5 versions (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4)

Matrix Last-Updated: 2026-06-28T10:00:00Z (within 14-day freshness threshold as of triage date).

## 2.2 -- Stream Scope

Issue is scoped to **2.2.x** stream via the `[rhtpa-2.2]` summary suffix. Version impact analysis focuses on the 2.2.x stream. The 2.1.x stream is analyzed for cross-stream impact reporting (Case A).

## 2.3 -- Dependency Version Extraction

Ecosystem: **RPM** (system package)
Lock file: `rpms.lock.yaml`
Fix threshold: **3.0.7-28.el9_4** (from Jira description)

### 2.2.x stream (scoped)

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.8 | 3.0.7-27.el9_4 | **YES** | retag of 2.2.1 (same backend commit v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fixed version |

### 2.1.x stream (cross-stream impact check)

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | **YES** | < 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | **YES** | < 3.0.7-28.el9_4 |

**Cross-stream finding**: The 2.1.x stream is also affected. All 2.1.x versions ship openssl-libs 3.0.7-24.el9, which is within the vulnerable range. This will be reported as cross-stream impact in Case A (Step 8).

## 2.3.5 -- Dependency Chain Context (RPM)

### Version 2.2.0 (v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs present
    Base image SBOM: openssl-libs present
    Classification: present in BOTH final and base image SBOMs -> base image
  rpms.lock.yaml vs SBOM: DISAGREE
    rpms.lock.yaml says: explicit install (package listed in lock file)
    SBOM comparison says: base image (present in both final and base SBOMs)

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

  Origin: DISPUTED -- rpms.lock.yaml lists the package (explicit install) but
  SBOM comparison shows it in both final and base images (base image origin).
```

### Version 2.2.1 (v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs present
    Base image SBOM: openssl-libs present
    Classification: present in BOTH final and base image SBOMs -> base image
  rpms.lock.yaml vs SBOM: DISAGREE
    rpms.lock.yaml says: explicit install (package listed in lock file)
    SBOM comparison says: base image (present in both final and base SBOMs)

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

  Origin: DISPUTED -- rpms.lock.yaml lists the package (explicit install) but
  SBOM comparison shows it in both final and base images (base image origin).
```

### Version 2.2.2 (v0.4.8 -- retag of 2.2.1)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  (same backend commit v0.4.8 as 2.2.1 -- retag, carried forward)
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs present
    Base image SBOM: openssl-libs present
    Classification: present in BOTH final and base image SBOMs -> base image
  rpms.lock.yaml vs SBOM: DISAGREE
    rpms.lock.yaml says: explicit install (package listed in lock file)
    SBOM comparison says: base image (present in both final and base SBOMs)

  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

  Origin: DISPUTED -- rpms.lock.yaml lists the package (explicit install) but
  SBOM comparison shows it in both final and base images (base image origin).
```

### Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12)

Not affected -- openssl-libs 3.0.7-28.el9_4 equals the fixed version. No dependency chain analysis required.

## SBOM Verification Summary

For all three affected 2.2.x versions (2.2.0, 2.2.1, 2.2.2), the SBOM classification **disagrees** with the rpms.lock.yaml classification:

| Version | rpms.lock.yaml | SBOM comparison | Agreement? |
|---------|---------------|-----------------|------------|
| 2.2.0 | explicit install (listed) | base image (in both SBOMs) | **DISAGREE** |
| 2.2.1 | explicit install (listed) | base image (in both SBOMs) | **DISAGREE** |
| 2.2.2 | explicit install (listed) | base image (in both SBOMs) | **DISAGREE** |

This discrepancy suggests that openssl-libs is explicitly pinned in rpms.lock.yaml (perhaps to control the exact version), but the same package also exists in the base image. The package may be an explicit overlay of a base image package. Manual investigation is recommended to determine the correct remediation path:

- If the rpms.lock.yaml pin is intentional (version override), remediation is: update the package spec in rpms.lock.yaml / rpms.in.yaml.
- If the rpms.lock.yaml entry is a leftover and the base image is the true source, remediation is: update the base image to a version that includes the patched openssl-libs.

## 2.4 -- Version Impact Table (Consolidated)

```
Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

Scoped stream: 2.2.x

| Version | openssl-libs     | Affected? | Notes                                    |
|---------|------------------|-----------|------------------------------------------|
| 2.2.0   | 3.0.7-25.el9_3   | YES       |                                          |
| 2.2.1   | 3.0.7-27.el9_4   | YES       |                                          |
| 2.2.2   | 3.0.7-27.el9_4   | YES       | retag of 2.2.1                           |
| 2.2.3   | 3.0.7-28.el9_4   | NO        | equals fixed version                     |
| 2.2.4   | 3.0.7-28.el9_4   | NO        | equals fixed version                     |

Cross-stream impact (2.1.x -- outside issue scope):

| Version | openssl-libs     | Affected? | Notes                                    |
|---------|------------------|-----------|------------------------------------------|
| 2.1.0   | 3.0.7-24.el9     | YES       |                                          |
| 2.1.1   | 3.0.7-24.el9     | YES       |                                          |
```

**Result**: 3 of 5 versions in the scoped 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2). Versions 2.2.3 and 2.2.4 ship the fixed openssl-libs 3.0.7-28.el9_4 and are not affected. The 2.1.x stream is also fully affected (cross-stream impact).

## 2.5 -- Upstream Fix Check

Ecosystem: RPM. No Upstream Branch is configured for RPM in the Ecosystem Mappings table (the Upstream Branch column is `--` for the RPM row). Upstream fix check is not applicable for system packages -- the fix comes from the RPM repository / base image vendor's errata pipeline, not from an upstream source branch.

The fixed version (3.0.7-28.el9_4) is already available as evidenced by versions 2.2.3 and 2.2.4 shipping it. Remediation for affected versions (2.2.0-2.2.2) requires updating the rpms.lock.yaml or base image reference to pick up the patched package.
