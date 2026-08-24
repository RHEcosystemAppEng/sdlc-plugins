# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### 2.2.x Stream (issue scope)

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 0.4.8 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 0.4.9 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | v0.4.11 | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | 0.4.12 | v0.4.12 | 3.0.7-28.el9_4 | NO | at fixed version |

**Data source**: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` for each
pinned tag in the 2.2.x supportability matrix.

### 2.1.x Stream (cross-stream impact -- Case A)

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | 0.3.12 | v0.3.12 | 3.0.7-24.el9 | YES | |

The 2.1.x stream is also affected. Since this issue is scoped to the 2.2.x
stream, the 2.1.x impact is reported as cross-stream context (Case A). The
2.1.x stream is tracked by a companion issue or may require separate PSIRT triage.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

**Package origin classification**: openssl-libs is present in `rpms.lock.yaml`
for the 2.2.x stream, classifying it as an **explicit install**. The package
is directly specified in the lock file, not inherited from a base image.

**SBOM verification status**: SBOM cross-validation was not performed because
`cosign` is not available in this environment. The rpms.lock.yaml classification
(explicit install) is used as the sole determination of package origin. When
cosign becomes available, SBOM comparison between the final container image and
the base image can confirm whether openssl-libs is added by the lock file or
inherited from the FROM image.

## Summary

- **Affected versions (2.2.x scope)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected (2.2.x scope)**: 2.2.3, 2.2.4 (ship fixed version 3.0.7-28.el9_4)
- **Cross-stream impact**: 2.1.x stream (2.1.0, 2.1.1) is also affected
- **Fix already present**: the fix was incorporated starting with build 0.4.11 (version 2.2.3)
