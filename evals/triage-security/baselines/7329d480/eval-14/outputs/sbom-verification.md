# Step 2.3.5 -- SBOM Verification: TC-8005

## Dependency Chain for openssl-libs (RPM)

### Classification Method

cosign is available at `/usr/bin/cosign`. Both rpms.lock.yaml and SBOM verification were performed for affected versions.

### Per-Version Results

#### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3) -- AFFECTED

| Signal | Source | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | `git show v0.4.5:rpms.lock.yaml` | openssl-libs **present** -- explicit install |
| Final image SBOM | `cosign download sbom <image>@<digest>` | openssl-libs **present** |
| Base image SBOM | `cosign download sbom <base-image>` | openssl-libs **present** |
| SBOM comparison | final SBOM vs base SBOM | present in **both** -- base image |

**Disagreement**: rpms.lock.yaml says **explicit install** but SBOM comparison says **base image**.

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

---

#### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4) -- AFFECTED

| Signal | Source | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | `git show v0.4.8:rpms.lock.yaml` | openssl-libs **present** -- explicit install |
| Final image SBOM | `cosign download sbom <image>@<digest>` | openssl-libs **present** |
| Base image SBOM | `cosign download sbom <base-image>` | openssl-libs **present** |
| SBOM comparison | final SBOM vs base SBOM | present in **both** -- base image |

**Disagreement**: rpms.lock.yaml says **explicit install** but SBOM comparison says **base image**.

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

---

#### Version 2.2.2 (tag v0.4.9, retag of 2.2.1) -- AFFECTED

| Signal | Source | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | `git show v0.4.9:rpms.lock.yaml` (retag of v0.4.8) | openssl-libs **present** -- explicit install |
| Final image SBOM | `cosign download sbom <image>@<digest>` | openssl-libs **present** |
| Base image SBOM | `cosign download sbom <base-image>` | openssl-libs **present** |
| SBOM comparison | final SBOM vs base SBOM | present in **both** -- base image |

**Disagreement**: rpms.lock.yaml says **explicit install** but SBOM comparison says **base image**.

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

Note: Version 2.2.2 is a retag of 2.2.1 (backend tag v0.4.8 reused as v0.4.9). Results carried forward from 2.2.1.

---

#### Versions 2.2.3 and 2.2.4 -- NOT AFFECTED

These versions ship openssl-libs 3.0.7-28.el9_4 (the fix version). SBOM verification was not performed because these versions are not within the affected range.

---

### Side-by-Side Summary

| Version | openssl-libs | Affected? | rpms.lock.yaml | SBOM Comparison | Agreement? |
|---------|--------------|-----------|----------------|-----------------|------------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | present (explicit install) | in both final + base (base image) | NO -- DISAGREE |
| 2.2.1 | 3.0.7-27.el9_4 | YES | present (explicit install) | in both final + base (base image) | NO -- DISAGREE |
| 2.2.2 | 3.0.7-27.el9_4 | YES | present (explicit install) | in both final + base (base image) | NO -- DISAGREE |
| 2.2.3 | 3.0.7-28.el9_4 | NO | n/a (not affected) | n/a | n/a |
| 2.2.4 | 3.0.7-28.el9_4 | NO | n/a (not affected) | n/a | n/a |

### Analysis

For all three affected versions (2.2.0, 2.2.1, 2.2.2), the two classification signals **disagree**:

- **rpms.lock.yaml** lists openssl-libs, classifying it as an **explicit install**. This implies remediation should update the package spec in rpms.in.yaml / rpms.lock.yaml.
- **SBOM comparison** shows openssl-libs present in **both** the final image SBOM and the base image SBOM, classifying it as a **base image** package. This implies remediation should update the base image tag/digest to a version that includes patched openssl-libs.

The disagreement suggests that openssl-libs may be both inherited from the base image AND explicitly pinned in rpms.lock.yaml (a redundant explicit install that duplicates a base image package). Manual investigation is required to determine:

1. Whether rpms.lock.yaml is intentionally pinning openssl-libs (overriding the base image version)
2. Whether removing the rpms.lock.yaml entry would cause the base image version to be used instead
3. Which remediation path is correct: updating rpms.lock.yaml, updating the base image, or both
