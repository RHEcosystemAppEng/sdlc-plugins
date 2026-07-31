# Step 2 - Version Impact Analysis for CVE-2026-40215

## Version Impact Table (2.2.x stream)

Scoped to the 2.2.x stream per issue suffix [rhtpa-2.2].

Data source: rpms.lock.yaml at each pinned commit (tag) from the supportability matrix.

| Version | Tag | openssl-libs (from rpms.lock.yaml) | Affected? | Notes |
|---------|-----|-------------------------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before fix 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before fix 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fix version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fix version |

Fix threshold: 3.0.7-28.el9_4 (from Jira description).

Versions 2.2.0, 2.2.1, and 2.2.2 ship openssl-libs versions earlier than the fix
threshold and are affected. Versions 2.2.3 and 2.2.4 ship the fixed version
(3.0.7-28.el9_4) and are not affected.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT --> explicit install
  SBOM verification: skipped -- external tools (cosign) are not available in eval mode; using rpms.lock.yaml classification only
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.
```

The openssl-libs package is present in rpms.lock.yaml, which is the primary classification signal for RPM packages. Its presence in the lock file indicates it is an explicitly installed package (not inherited from the base image). SBOM verification via cosign was skipped because external tools are not available in this evaluation context -- the rpms.lock.yaml classification is used alone.

## Cross-Stream Impact

The 2.1.x stream is also present in the security matrix. Checking openssl-libs versions
for the 2.1.x stream (for Case A cross-stream impact reporting):

| Version | Tag | openssl-libs (from rpms.lock.yaml) | Affected? |
|---------|-----|-------------------------------------|-----------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES |

The 2.1.x stream is also affected. This is noted for Case A cross-stream impact but
remediation tasks are only created for the 2.2.x stream (the issue's scoped stream).
