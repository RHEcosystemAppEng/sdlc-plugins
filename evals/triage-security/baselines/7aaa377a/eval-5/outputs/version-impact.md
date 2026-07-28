# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4)

Scoped to the **2.2.x** stream per issue suffix `[rhtpa-2.2]`.

Data source: `rpms.lock.yaml` at each pinned commit tag from the supportability matrix.

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | NO | fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | NO | fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship the vulnerable openssl-libs
package. Versions 2.2.3 and 2.2.4 ship the patched version (3.0.7-28.el9_4).

## Step 2.3.5 -- Dependency Chain Context

### Package classification (RPM)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT --> explicit install
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

  SBOM verification: skipped -- cosign is not available and external tool
  invocation is prohibited in this eval context. Using rpms.lock.yaml
  classification only.

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to openssl-libs >= 3.0.7-28.el9_4.
```

The primary classification signal is the **rpms.lock.yaml** lock file. The
package `openssl-libs` is present in rpms.lock.yaml for all versions in the
2.2.x stream, which classifies it as an **explicit install** -- the package
is intentionally included in the container image via the RPM lock file, not
inherited from the base image.

### SBOM Verification (Step 2.3.5)

SBOM verification via cosign was **not performed**. The `cosign` CLI tool is
not available in this environment, and the eval prohibits invocation of
external tools. Per the version-impact-analysis.md procedure:

> "If cosign is not available or any SBOM download fails, skip with a warning
> and use the rpms.lock.yaml classification alone."

The rpms.lock.yaml classification (explicit install) is used as the sole
classification signal. The SBOM verification step is optional and supplementary
-- it does not override the lock file classification.
