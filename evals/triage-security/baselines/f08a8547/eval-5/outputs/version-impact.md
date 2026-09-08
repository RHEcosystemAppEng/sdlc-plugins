# Step 2 -- Version Impact Analysis

## CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4)

### Version Impact Table

#### Stream 2.2.x (issue scope)

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fixed version |

#### Stream 2.1.x (cross-stream analysis)

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |

### Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4).
- **2.1.x stream**: all versions (2.1.0, 2.1.1) are affected. This stream ships an older openssl-libs (3.0.7-24.el9).
- Cross-stream impact: the 2.1.x stream is also affected but is outside this issue's scope (TC-8005 is scoped to 2.2.x via `[rhtpa-2.2]`). This triggers Case A (cross-stream impact notification).

### Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available in this environment
  Origin: explicit install (openssl-libs is specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The openssl-libs package is present in `rpms.lock.yaml` at each pinned tag, confirming it is an **explicitly installed** RPM package (not inherited from the base image). SBOM verification via `cosign` was not performed because `cosign` is not available in this environment. The rpms.lock.yaml classification alone is used to determine the package origin.

### Upstream Fix Status

The RPM ecosystem has no configured Upstream Branch in the Ecosystem Mappings table (the column is `--`). Upstream fix status is not applicable for system RPM packages -- the fix is delivered via the base distribution's errata pipeline (RHSA-2026:4021).
