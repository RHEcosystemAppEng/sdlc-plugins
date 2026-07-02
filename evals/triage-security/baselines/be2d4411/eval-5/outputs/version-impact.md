# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|--------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | at fixed version |

Affected versions: 2.2.0, 2.2.1, 2.2.2
Not affected: 2.2.3, 2.2.4

## Cross-Stream Impact (informational)

The 2.1.x stream is also affected (both versions ship openssl-libs < 3.0.7-28.el9_4):

| Version | Tag | openssl-libs | Affected? |
|---------|-----|--------------|-----------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES |

This is Case B -- cross-stream impact would be reported via comment on TC-8005.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign is not available and external tools are
    prohibited in this evaluation context. Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to openssl-libs >= 3.0.7-28.el9_4.
```

The package `openssl-libs` is present in `rpms.lock.yaml` as an explicit install
(not inherited from the base image). This means remediation targets the lock file
directly in the Konflux release repo, not a base image update.

SBOM verification was not performed because cosign is not available in this
environment and external tool invocation is prohibited. The rpms.lock.yaml
classification alone is used to determine the package origin.
