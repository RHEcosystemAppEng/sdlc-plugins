# Step 2 -- Version Impact Analysis for CVE-2026-40215

## Version Impact Table

CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4), scoped to 2.2.x stream:

| Version | Stream | Tag | openssl-libs | Affected? | Notes |
|---------|--------|-----|--------------|-----------|-------|
| 2.2.0 | 2.2.x | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 3.0.7-28.el9_4 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 3.0.7-28.el9_4 | NO | |

All versions from the 2.2.x stream supportability matrix are included (2.2.0 through 2.2.4). Version impact is determined by comparing the openssl-libs version at each pinned commit tag against the fix threshold of 3.0.7-28.el9_4. Data is extracted from rpms.lock.yaml using `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`.

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    - For versions 2.2.0 through 2.2.2 (affected):
      Final image SBOM: openssl-libs PRESENT
      Base image SBOM: openssl-libs PRESENT
      SBOM classification: base image (present in both final and base image SBOMs)
    - rpms.lock.yaml classification: explicit install (openssl-libs listed in rpms.lock.yaml)

    WARNING: SBOM classification disagrees with rpms.lock.yaml
    rpms.lock.yaml says: explicit install (openssl-libs is listed in rpms.lock.yaml)
    SBOM comparison says: base image (present in both final and base image SBOMs)

    Discrepancy flagged for manual investigation. The rpms.lock.yaml classification
    remains the primary signal -- the SBOM result supplements but does not override it.
    The package may be both explicitly installed AND present in the base image, which
    would explain the disagreement. Investigate manually to confirm the remediation path.

  Origin (primary): explicit install (per rpms.lock.yaml -- primary classification signal)
```

**SBOM verification procedure** (described, not executed per eval constraints):

1. Check cosign availability: `which cosign` -> `/usr/bin/cosign` (available)
2. Download final image SBOM: `cosign download sbom <image-reference>@<image-digest> > /tmp/final-sbom.json`
3. Extract base image reference from Dockerfile's FROM line
4. Download base image SBOM: `cosign download sbom <base-image-reference> > /tmp/base-sbom.json`
5. Compare openssl-libs presence in both SBOMs:
   - Result for versions 2.2.0-2.2.2: present in BOTH final and base image SBOMs -> SBOM says base image
   - rpms.lock.yaml says: explicit install (openssl-libs is in the lock file)
   - **Disagreement detected** -- flagged to engineer with warning

The rpms.lock.yaml classification (explicit install) is the primary signal. The SBOM result (base image) supplements but does not override it. The discrepancy is presented to the engineer for manual investigation.
