# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | YES | before 3.0.7-28.el9_4 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | YES | before 3.0.7-28.el9_4 |
| 2.2.2 | 0.4.9 | `v0.4.9` | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | equals fixed version |

## Cross-stream Impact (informational)

The 2.1.x stream (outside this issue's scope) is also affected:

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|--------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |
| 2.1.1 | `v0.3.12` | 3.0.7-24.el9 | YES | before 3.0.7-28.el9_4 |

Cross-stream impact is informational only -- tracked by companion PSIRT issues.

## Dependency Chain (Step 2.3.5)

Dependency chain for openssl-libs (RPM):

- rpms.lock.yaml: **present** -- explicit install
- Origin: **explicit install** (openssl-libs is specified in rpms.lock.yaml)
- Remediation path: update the package version spec in rpms.lock.yaml (or rpms.in.yaml) to >= 3.0.7-28.el9_4

## Upstream Fix Status

RPM ecosystem has no upstream branch configured (the Upstream Branch column is empty
for RPM in the Ecosystem Mappings table). The fix is available as RHSA-2026:4021 from
Red Hat's errata pipeline. No upstream branch check is needed -- the remediation is
to update the RPM lock file to reference the patched package version.
