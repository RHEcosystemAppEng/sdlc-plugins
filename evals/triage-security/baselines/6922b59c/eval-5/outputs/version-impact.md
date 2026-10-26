# Step 2 -- Version Impact Analysis: CVE-2026-40215

## Version Impact Table

CVE-2026-40215 (openssl-libs, affected versions before 3.0.7-28.el9_4):

| Version | Stream | Build Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|--------|-----------|-------------------------------|-----------|-------|
| 2.2.0 | 2.2.x | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 2.2.x | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fix version |
| 2.2.4 | 2.2.x | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fix version |

### Cross-stream reference (2.1.x stream, not in issue scope)

| Version | Stream | Build Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|--------|-----------|-------------------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | 2.1.x | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

### Summary

- **2.2.x stream (in scope):** versions 2.2.0, 2.2.1, and 2.2.2 are affected; versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs (3.0.7-28.el9_4)
- **2.1.x stream (out of scope):** both 2.1.0 and 2.1.1 are affected; cross-stream impact applies (Case A)

## Dependency Chain (Step 2.3.5)

### openssl-libs (RPM)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT -> explicit install
  SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

- **Package origin:** explicit install (openssl-libs is listed in rpms.lock.yaml at every pinned tag in the 2.2.x stream)
- **SBOM verification status:** Skipped. cosign is not available in this environment, so SBOM comparison between the final container image and base image could not be performed. The rpms.lock.yaml classification (explicit install) is used as the sole determination of package origin.
- **Introduction point:** present in all versions across both streams; not newly introduced

### RPM version progression (2.2.x stream)

| Build Tag | openssl-libs version | Delta |
|-----------|---------------------|-------|
| v0.4.5 | 3.0.7-25.el9_3 | initial |
| v0.4.8 | 3.0.7-27.el9_4 | bumped from el9_3 to el9_4 |
| v0.4.9 | (retag of v0.4.8) | -- |
| v0.4.11 | 3.0.7-28.el9_4 | bumped to fix version |
| v0.4.12 | 3.0.7-28.el9_4 | unchanged |

## Upstream Fix Status

RPM ecosystem has no upstream branch configured (marked as "--" in Ecosystem Mappings).
The fix was picked up through the RPM package update pipeline. The fixed version
(3.0.7-28.el9_4) is available via RHSA-2026:4021 and was incorporated starting
with build tag v0.4.11 (product version 2.2.3).
