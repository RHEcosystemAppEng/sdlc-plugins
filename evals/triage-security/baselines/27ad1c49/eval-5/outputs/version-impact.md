# Step 2 -- Version Impact Analysis: CVE-2026-40215

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | Stream | openssl-libs | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 3.0.7-24.el9 | YES | |
| 2.1.1 | 2.1.x | 3.0.7-24.el9 | YES | |
| 2.2.0 | 2.2.x | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 2.2.x | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1: 3.0.7-27.el9_4) |
| 2.2.3 | 2.2.x | 3.0.7-28.el9_4 | NO | at fix version |
| 2.2.4 | 2.2.x | 3.0.7-28.el9_4 | NO | at fix version |

Data source: rpms.lock.yaml at each pinned commit (tags from supportability matrix).
Fix threshold: 3.0.7-28.el9_4 (from Jira description).

## Dependency Chain (Step 2.3.5)

### openssl-libs (RPM) -- 2.2.x stream

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs entries found at tags v0.4.5, v0.4.8, v0.4.11, v0.4.12)
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)
  SBOM verification: skipped -- cosign not available in eval environment; using rpms.lock.yaml classification only
```

The package is classified as an **explicit install** because it is present in rpms.lock.yaml. This means remediation involves updating the package spec in rpms.in.yaml / rpms.lock.yaml.

SBOM verification status: cosign is not available in this environment, so SBOM cross-validation between the final container image and the base image could not be performed. The rpms.lock.yaml classification is used alone. In a production triage, running `which cosign` would determine availability, and if present, `cosign download sbom <image-reference>@<image-digest>` would compare final and base image SBOMs to confirm the lock file classification.

### openssl-libs (RPM) -- 2.1.x stream

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs entries found at tags v0.3.8, v0.3.12)
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)
  SBOM verification: skipped -- cosign not available in eval environment; using rpms.lock.yaml classification only
```

Same classification as 2.2.x stream -- the package is an explicit install in rpms.lock.yaml across both streams.

## Cross-Stream Impact Summary

The issue is scoped to stream 2.2.x, but the version impact table shows that stream 2.1.x is also affected:

- **2.1.x stream**: Both versions (2.1.0, 2.1.1) ship openssl-libs 3.0.7-24.el9, which is within the affected range.
- **2.2.x stream**: Versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3 and 2.2.4 already ship the fix (3.0.7-28.el9_4).

This cross-stream impact would trigger Step 8 Case A (cross-stream impact comment and preemptive remediation for 2.1.x if no sibling CVE Jira exists).

## Upstream Fix Status

RPM ecosystem has no upstream branch configured (Upstream Branch column is `--` in Ecosystem Mappings). The fix availability is determined by the RPM repository / base image vendor errata, not by a source branch check. The fixed version (3.0.7-28.el9_4) is already present in versions 2.2.3+ as confirmed by rpms.lock.yaml.
