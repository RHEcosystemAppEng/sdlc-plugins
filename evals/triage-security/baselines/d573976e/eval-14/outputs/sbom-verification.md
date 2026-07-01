# Step 2.3.5 -- SBOM Verification Results

## Cosign Availability

cosign is available at `/usr/bin/cosign`.

## RPM Dependency Chain Analysis for openssl-libs

### Version 2.2.0 (tag v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs-3.0.7-25.el9_3) -> explicit install
  SBOM verification: present in both final and base image SBOMs -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
  Origin: DISPUTED -- rpms.lock.yaml says explicit install, SBOM says base image
```

**SBOM verification details:**

1. Final image SBOM downloaded via:
   ```
   cosign download sbom <image-reference>@<image-digest-for-2.2.0>
   ```
   Result: openssl-libs-3.0.7-25.el9_3.x86_64 **found** in final image SBOM.

2. Base image reference extracted from Dockerfile `FROM` line at `v0.4.5`.

3. Base image SBOM downloaded via:
   ```
   cosign download sbom <base-image-reference>
   ```
   Result: openssl-libs-3.0.7-25.el9_3.x86_64 **found** in base image SBOM.

4. Comparison: present in **both** final and base image SBOMs -> **base image** classification.

5. rpms.lock.yaml classification: openssl-libs IS present in rpms.lock.yaml -> **explicit install** classification.

6. **Disagreement detected**:
   > SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

The rpms.lock.yaml classification (explicit install) remains the **primary signal**. The SBOM result supplements but does not override it. The discrepancy is flagged to the engineer for manual investigation.

---

### Version 2.2.1 (tag v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs-3.0.7-27.el9_4) -> explicit install
  SBOM verification: present in both final and base image SBOMs -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
  Origin: DISPUTED -- rpms.lock.yaml says explicit install, SBOM says base image
```

**SBOM verification details:**

1. Final image SBOM downloaded via:
   ```
   cosign download sbom <image-reference>@<image-digest-for-2.2.1>
   ```
   Result: openssl-libs-3.0.7-27.el9_4.x86_64 **found** in final image SBOM.

2. Base image SBOM downloaded via:
   ```
   cosign download sbom <base-image-reference>
   ```
   Result: openssl-libs-3.0.7-27.el9_4.x86_64 **found** in base image SBOM.

3. Comparison: present in **both** final and base image SBOMs -> **base image** classification.

4. rpms.lock.yaml classification: openssl-libs IS present in rpms.lock.yaml -> **explicit install** classification.

5. **Disagreement detected**:
   > SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

---

### Version 2.2.2 (tag v0.4.9 -- retag of 2.2.1)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: same as 2.2.1 (retag of v0.4.8)
  SBOM verification: same as 2.2.1 (retag -- identical container image)
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
  Origin: DISPUTED -- same as 2.2.1
```

Version 2.2.2 is a retag of 2.2.1 (identical source commits at `v0.4.8`). The lock file data and SBOM content are identical. The same disagreement applies.

---

### Versions 2.2.3 (tag v0.4.11) and 2.2.4 (tag v0.4.12) -- NOT AFFECTED

These versions ship openssl-libs 3.0.7-28.el9_4, which is the fixed version. They are not affected by CVE-2026-40215. SBOM verification is not performed for unaffected versions since the dependency chain context is only needed for remediation planning of affected versions.

---

## Summary: SBOM Verification vs rpms.lock.yaml

| Version | rpms.lock.yaml | SBOM Comparison | Agreement? | Action |
|---------|---------------|-----------------|------------|--------|
| 2.2.0 | Explicit install (present in lock file) | Base image (in both final & base SBOMs) | **DISAGREE** | Flagged for manual investigation |
| 2.2.1 | Explicit install (present in lock file) | Base image (in both final & base SBOMs) | **DISAGREE** | Flagged for manual investigation |
| 2.2.2 | Same as 2.2.1 (retag) | Same as 2.2.1 (retag) | **DISAGREE** | Flagged for manual investigation |
| 2.2.3 | N/A (not affected) | N/A (not affected) | -- | -- |
| 2.2.4 | N/A (not affected) | N/A (not affected) | -- | -- |

**Key finding**: For all affected versions (2.2.0 through 2.2.2), the rpms.lock.yaml classifies openssl-libs as an explicit install (the package is listed in the lock file), while the SBOM comparison classifies it as a base image package (present in both the final and base image SBOMs). This disagreement is flagged to the engineer for manual investigation per Step 2.3.5 sub-step 5.

The rpms.lock.yaml classification remains the **primary signal** per the skill protocol. The SBOM result supplements but does not override it. The engineer should investigate whether the package is genuinely explicitly installed and also happens to be present in the base image (which would explain the dual presence), or whether the lock file entry is stale/incorrect.

Possible explanations for the disagreement:
- The package may be both inherited from the base image AND explicitly pinned in rpms.lock.yaml for version control purposes
- The rpms.lock.yaml may include base image packages for reproducibility tracking
- The lock file generation process may capture all installed packages regardless of origin

Manual investigation by the engineer is required to determine the correct remediation path.
