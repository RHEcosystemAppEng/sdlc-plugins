# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### Scoped stream: 2.2.x

| Version | Build | Tag | openssl-libs version | Affected? | Notes |
|---------|-------|-----|----------------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 0.4.8 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 0.4.9 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 0.4.12 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

### Cross-stream reference: 2.1.x (not in scope, for Case A assessment)

| Version | Build | Tag | openssl-libs version | Affected? | Notes |
|---------|-------|-----|----------------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | 0.3.12 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

### Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs 3.0.7-28.el9_4.
- **2.1.x stream**: all versions (2.1.0, 2.1.1) are affected. This is cross-stream impact to be reported in Case A.
- The fix was introduced in the 2.2.x stream starting with build 0.4.11 (version 2.2.3, released 2026-03-23).

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs entry found) --> explicit install
  SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update openssl-libs version in rpms.lock.yaml (and rpms.in.yaml if applicable)
to >= 3.0.7-28.el9_4.
```

The openssl-libs package is present in rpms.lock.yaml at each pinned tag, confirming it is an explicitly installed package (not inherited from a base image). SBOM cross-validation via cosign was not performed because cosign is not available in this environment. The rpms.lock.yaml classification is used as the sole source of truth for package origin.

## Upstream Fix Status

No upstream branch is configured for the RPM ecosystem in the Ecosystem Mappings table (Upstream Branch column is empty). Upstream fix status is determined from the Red Hat Security Advisory RHSA-2026:4021, which provides the fixed package version 3.0.7-28.el9_4. This fix is already present in the 2.2.x stream starting with version 2.2.3.
