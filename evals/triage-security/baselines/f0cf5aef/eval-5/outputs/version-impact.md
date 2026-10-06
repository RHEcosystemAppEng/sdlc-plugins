# Step 2 -- Version Impact Analysis: CVE-2026-40215

## Version Impact Table

CVE-2026-40215: openssl-libs (affected versions before 3.0.7-28.el9_4)

Issue is scoped to the **2.2.x** stream. Cross-stream analysis of 2.1.x is included for Case A assessment.

### 2.2.x stream (in scope)

| Version | Build Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----------|---------------------------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fix version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fix version |

### 2.1.x stream (cross-stream -- out of scope)

| Version | Build Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----------|---------------------------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |

## Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, and 2.2.2 are affected. The fix was picked up in version 2.2.3 (build v0.4.11, released 2026-03-23) and remains in 2.2.4.
- **2.1.x stream**: all versions (2.1.0, 2.1.1) are affected. This stream has NOT picked up the fix. Cross-stream impact applies (Case A).

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -- explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package version in rpms.lock.yaml (and rpms.in.yaml
if applicable) to >= 3.0.7-28.el9_4.
```

openssl-libs is present in `rpms.lock.yaml` at each pinned tag, confirming it is an **explicitly installed** package (not inherited from a base image). SBOM cross-validation via `cosign` was not performed because `cosign` is not available in this environment. The rpms.lock.yaml classification is used as the sole source of truth for package origin.

## Upstream Fix Status

RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings table (the Upstream Branch column shows `--` for RPM). Upstream fix check is not applicable for system packages -- the fix comes from the RPM vendor (Red Hat), tracked via RHSA-2026:4021.
