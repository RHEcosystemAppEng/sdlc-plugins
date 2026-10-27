# Step 2 -- Version Impact Analysis

## Scoped Stream: 2.2.x

Lock file: `rpms.lock.yaml`
Vulnerable package: openssl-libs
Affected range: versions before 3.0.7-28.el9_4
Fixed version: 3.0.7-28.el9_4

### Version Impact Table

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fixed version |

### Cross-Stream Impact (informational, for Case A)

The 2.1.x stream is also affected (for cross-stream impact notice):

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |

## Dependency Chain

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign is not available (external tools prohibited in this eval)
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The package openssl-libs is present in `rpms.lock.yaml` across all tags in the 2.2.x stream, confirming it is an **explicit install** (not inherited from the base image). This means remediation is a direct update of the package version in the RPM lock file or package spec.

### SBOM Verification Status

SBOM verification was **skipped** because cosign is not available and external tool invocation is prohibited in this context. The rpms.lock.yaml classification (explicit install) is used as the sole evidence for package origin. In a production triage, cosign SBOM comparison would cross-validate this classification by comparing final and base image SBOMs.
