# Step 2.3.5 -- SBOM Verification Results

## Dependency Chain for openssl-libs (RPM)

Cosign is available at `/usr/bin/cosign`. SBOM verification was performed by comparing
final image SBOMs against base image SBOMs using `cosign download sbom`.

### Version 2.2.0 (tag v0.4.5)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs present | explicit install |
| SBOM (final image) | openssl-libs-3.0.7-25.el9_3 present | -- |
| SBOM (base image) | openssl-libs-3.0.7-25.el9_3 present | base image origin |
| **Verdict** | **DISAGREE** | -- |

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
> explicit install but SBOM comparison says base image origin (present in both
> final and base image SBOMs). Investigate manually.

rpms.lock.yaml remains the primary signal. Classification: **explicit install** (per rpms.lock.yaml).

### Version 2.2.1 (tag v0.4.8)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs present | explicit install |
| SBOM (final image) | openssl-libs-3.0.7-27.el9_4 present | -- |
| SBOM (base image) | openssl-libs-3.0.7-27.el9_4 present | base image origin |
| **Verdict** | **DISAGREE** | -- |

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
> explicit install but SBOM comparison says base image origin (present in both
> final and base image SBOMs). Investigate manually.

rpms.lock.yaml remains the primary signal. Classification: **explicit install** (per rpms.lock.yaml).

### Version 2.2.2 (tag v0.4.9 -- retag of v0.4.8)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs present (same as 2.2.1) | explicit install |
| SBOM (final image) | openssl-libs-3.0.7-27.el9_4 present | -- |
| SBOM (base image) | openssl-libs-3.0.7-27.el9_4 present | base image origin |
| **Verdict** | **DISAGREE** | -- |

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
> explicit install but SBOM comparison says base image origin (present in both
> final and base image SBOMs). Investigate manually.

rpms.lock.yaml remains the primary signal. Classification: **explicit install** (per rpms.lock.yaml).

## Discrepancy Analysis

For all three affected versions (2.2.0, 2.2.1, 2.2.2), the rpms.lock.yaml and
SBOM signals disagree:

- **rpms.lock.yaml** lists openssl-libs as an explicit install, meaning it is
  deliberately specified in `rpms.in.yaml` and locked in `rpms.lock.yaml`.
- **SBOM comparison** shows openssl-libs present in both the final image SBOM
  and the base image SBOM, which would normally indicate base image origin.

This discrepancy likely means the package is both inherited from the base image
AND explicitly installed (possibly to pin a specific version). The rpms.lock.yaml
classification is the **primary** signal because it reflects the build intent
declared in the Konflux release repo. The SBOM comparison supplements but does
not override the lock file classification.

**Remediation path** (based on rpms.lock.yaml classification as explicit install):
Update the package spec in `rpms.in.yaml` / `rpms.lock.yaml` to >= 3.0.7-28.el9_4.

Note: versions 2.2.3 and 2.2.4 already ship openssl-libs 3.0.7-28.el9_4 (the
fixed version) and are NOT affected. SBOM verification was not performed for
non-affected versions as it is only needed for remediation context on affected versions.
