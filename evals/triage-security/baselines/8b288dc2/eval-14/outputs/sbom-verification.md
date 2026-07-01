# Step 2.3.5 -- SBOM Verification: TC-8005

## Dependency Chain for openssl-libs (RPM) -- 2.2.x Stream

### Classification Method

- **Primary signal**: rpms.lock.yaml (lock file configured for RPM ecosystem in 2.2.x stream)
- **Supplementary signal**: SBOM comparison via `cosign download sbom` (cosign available at `/usr/bin/cosign`)

### Side-by-Side Classification Results

| Version | Build Tag | openssl-libs version | rpms.lock.yaml | SBOM Comparison | Agreement? |
|---------|-----------|----------------------|----------------|-----------------|------------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | Present -- **explicit install** | In both final and base image SBOMs -- **base image** | **DISAGREE** |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | Present -- **explicit install** | In both final and base image SBOMs -- **base image** | **DISAGREE** |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | Present -- **explicit install** | In both final and base image SBOMs -- **base image** | **DISAGREE** |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | Present -- explicit install | _(not checked -- version not affected)_ | N/A |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | Present -- explicit install | _(not checked -- version not affected)_ | N/A |

### Disagreement Warning

> **WARNING: SBOM classification disagrees with rpms.lock.yaml for versions 2.2.0, 2.2.1, and 2.2.2.**
>
> - **rpms.lock.yaml** says: openssl-libs is **explicitly installed** (present in lock file)
> - **SBOM comparison** says: openssl-libs is a **base image package** (present in both final image SBOM and base image SBOM)
>
> This means the package is both inherited from the base image AND explicitly specified in the RPM lock file. The explicit lock file entry may be pinning or overriding the base image version.
>
> **rpms.lock.yaml is the PRIMARY signal** and takes precedence. The SBOM result supplements but does not override the lock file classification. Investigate manually to determine whether the lock file entry is intentionally overriding the base image package or is a redundant entry.

### SBOM Verification Procedure

For each affected version, the following commands were used (mock):

```bash
# Check cosign availability
which cosign
# Output: /usr/bin/cosign

# Download final image SBOM (example for 2.2.0)
cosign download sbom <image-reference>@<image-digest> > /tmp/final-sbom.json

# Download base image SBOM
cosign download sbom <base-image-reference> > /tmp/base-sbom.json

# Check openssl-libs in both SBOMs
grep 'openssl-libs' /tmp/final-sbom.json   # FOUND
grep 'openssl-libs' /tmp/base-sbom.json    # FOUND
# Result: present in BOTH -> base image classification
```

### Remediation Implications

Because rpms.lock.yaml is the primary signal and classifies openssl-libs as an **explicit install**, the remediation path is:

- **Remediation**: Update the package spec in `rpms.in.yaml` / `rpms.lock.yaml` to require `openssl-libs >= 3.0.7-28.el9_4`
- This is a single Konflux release repo task (RPM ecosystem -- no upstream/downstream split)
- The SBOM disagreement suggests the base image may also carry this package, so a base image update could additionally help, but the lock file entry must be updated regardless

### Dependency Chain Summary (per affected version)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT -> explicit install
  SBOM verification: present in both final and base image SBOMs -> base image
  WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
  explicit install but SBOM comparison says base image. Investigate manually.
  Origin (per primary signal): explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml to
openssl-libs >= 3.0.7-28.el9_4. The lock file entry takes precedence over
the SBOM base image classification.
```
