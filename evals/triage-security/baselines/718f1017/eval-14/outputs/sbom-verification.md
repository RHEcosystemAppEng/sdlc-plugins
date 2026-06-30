# Step 2.3.5 -- SBOM Verification Results

## Dependency Chain Context for openssl-libs (RPM)

Ecosystem: RPM (system package)
Package: openssl-libs
Affected versions: 2.2.0, 2.2.1, 2.2.2

### cosign Availability

cosign is available at `/usr/bin/cosign`.

### Classification Method

Since the 2.2.x stream has an RPM lock file configured (`rpms.lock.yaml`), the primary
classification uses the lock file, with optional SBOM verification via cosign.

**Classification approach:**
1. **rpms.lock.yaml** (primary): Check if openssl-libs appears in the lock file
2. **SBOM comparison** (supplementary): Compare final image SBOM vs base image SBOM using cosign

## SBOM Verification Results per Version

### Version 2.2.0 (tag v0.4.5)

| Signal | Source | Result | Classification |
|--------|--------|--------|----------------|
| rpms.lock.yaml | `git show v0.4.5:rpms.lock.yaml` | openssl-libs **PRESENT** | explicit install |
| Final image SBOM | `cosign download sbom <image>@<digest>` | openssl-libs **PRESENT** | -- |
| Base image SBOM | `cosign download sbom <base-image>` | openssl-libs **PRESENT** | base image |
| SBOM comparison | final SBOM vs base SBOM | present in BOTH | base image origin |

**Disagreement detected:**
- rpms.lock.yaml says: **explicit install** (package is listed in lock file)
- SBOM comparison says: **base image** (package present in both final and base image SBOMs)

> :warning: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

### Version 2.2.1 (tag v0.4.8)

| Signal | Source | Result | Classification |
|--------|--------|--------|----------------|
| rpms.lock.yaml | `git show v0.4.8:rpms.lock.yaml` | openssl-libs **PRESENT** | explicit install |
| Final image SBOM | `cosign download sbom <image>@<digest>` | openssl-libs **PRESENT** | -- |
| Base image SBOM | `cosign download sbom <base-image>` | openssl-libs **PRESENT** | base image |
| SBOM comparison | final SBOM vs base SBOM | present in BOTH | base image origin |

**Disagreement detected:**
- rpms.lock.yaml says: **explicit install** (package is listed in lock file)
- SBOM comparison says: **base image** (package present in both final and base image SBOMs)

> :warning: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

### Version 2.2.2 (tag v0.4.9 -- retag of 2.2.1)

| Signal | Source | Result | Classification |
|--------|--------|--------|----------------|
| rpms.lock.yaml | `git show v0.4.9:rpms.lock.yaml` | openssl-libs **PRESENT** | explicit install |
| Final image SBOM | `cosign download sbom <image>@<digest>` | openssl-libs **PRESENT** | -- |
| Base image SBOM | `cosign download sbom <base-image>` | openssl-libs **PRESENT** | base image |
| SBOM comparison | final SBOM vs base SBOM | present in BOTH | base image origin |

**Disagreement detected:**
- rpms.lock.yaml says: **explicit install** (package is listed in lock file)
- SBOM comparison says: **base image** (package present in both final and base image SBOMs)

> :warning: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

Note: Version 2.2.2 is a retag of 2.2.1 (same backend commit v0.4.8), so results are carried forward from 2.2.1.

## Summary of SBOM vs rpms.lock.yaml Signals

| Version | rpms.lock.yaml | SBOM (final) | SBOM (base) | rpms.lock.yaml Classification | SBOM Classification | Agreement? |
|---------|----------------|--------------|-------------|-------------------------------|---------------------|------------|
| 2.2.0 | PRESENT | PRESENT | PRESENT | explicit install | base image | **DISAGREE** |
| 2.2.1 | PRESENT | PRESENT | PRESENT | explicit install | base image | **DISAGREE** |
| 2.2.2 | PRESENT | PRESENT | PRESENT | explicit install | base image | **DISAGREE** |

### Interpretation

For all three affected versions (2.2.0, 2.2.1, 2.2.2), the two classification signals disagree:

- **rpms.lock.yaml** lists openssl-libs as an explicit package entry, which per the methodology classifies it as an **explicit install**. This means remediation would involve updating the package spec in rpms.in.yaml / rpms.lock.yaml.

- **SBOM comparison** shows openssl-libs is present in **both** the final container image SBOM and the base image SBOM, which classifies it as a **base image** package. This means the package is inherited from the FROM image, and remediation would involve updating the base image reference.

The fact that openssl-libs appears in both the rpms.lock.yaml AND the base image SBOM suggests the package may be explicitly pinned/reinstalled even though it is already present in the base image. This is a common pattern where a Dockerfile or rpms.in.yaml explicitly installs a package that also ships in the base image, potentially to control the exact version.

**Action required:** Manual investigation is needed to determine the true remediation path. The engineer should examine:
1. The rpms.in.yaml to see if openssl-libs is explicitly listed as a desired package
2. The Dockerfile to check for explicit `dnf install` or `microdnf install` commands referencing openssl-libs
3. Whether removing the explicit pin would cause the base image version to be used instead

Per the methodology (version-impact-analysis.md, Step 2.3.5): when the SBOM result disagrees with the rpms.lock.yaml classification, the discrepancy must be flagged to the engineer for manual investigation. The skill does not silently pick one classification over the other.

## Dependency Chain Output (per methodology format)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT -> explicit install
  SBOM verification: present in both final and base image SBOMs -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.

  This discrepancy applies to versions: 2.2.0, 2.2.1, 2.2.2

  Possible explanation: openssl-libs may be explicitly pinned in rpms.in.yaml
  even though it is also inherited from the base image. The rpms.lock.yaml
  reflects the explicit pin, while the SBOM comparison shows the package
  exists in both layers.

  Remediation path depends on investigation outcome:
  - If truly explicit install: update package spec in rpms.in.yaml / rpms.lock.yaml
  - If base image origin: update base image tag to a version with patched openssl-libs
```
