# Step 2 -- Version Impact Analysis

## CVE-2026-40215: openssl-libs (versions before 3.0.7-28.el9_4)

### Version Impact Table (2.2.x stream -- scoped by issue suffix)

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | vulnerable (< 3.0.7-28.el9_4) |
| 2.2.1 | 3.0.7-27.el9_4 | YES | vulnerable (< 3.0.7-28.el9_4) |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fixed version |

### Cross-stream Impact (informational -- outside issue scope)

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | vulnerable (< 3.0.7-28.el9_4) |
| 2.1.1 | 3.0.7-24.el9 | YES | vulnerable (< 3.0.7-28.el9_4) |

The 2.1.x stream is also affected but is outside this issue's scope (tracked by separate PSIRT issue if applicable).

### Dependency Chain Context (RPM -- rpms.lock.yaml)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml confirms: openssl-libs present in lock file
  Origin: explicit install (package listed in rpms.lock.yaml)

  Remediation: update the package spec in rpms.lock.yaml (or rpms.in.yaml)
  to reference openssl-libs >= 3.0.7-28.el9_4.
```

### Upstream Fix Status

Not applicable for RPM ecosystem. The RPM `rpms.lock.yaml` does not have an Upstream Branch configured in the Ecosystem Mappings. The fix is already available in the RHEL repositories (RHSA-2026:4021 provides openssl-libs-3.0.7-28.el9_4). Remediation is a Konflux release repo change: update the RPM lock file to pick up the patched version.

### Data Sources

All openssl-libs versions were extracted from `rpms.lock.yaml` at the pinned tags in the 2.2.x stream supportability matrix:

| Tag | Command (simulated) | openssl-libs version |
|-----|---------------------|----------------------|
| v0.4.5 | `git show v0.4.5:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-25.el9_3 |
| v0.4.8 | `git show v0.4.8:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-27.el9_4 |
| v0.4.9 | (retag of v0.4.8 -- skipped) | -- |
| v0.4.11 | `git show v0.4.11:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-28.el9_4 |
| v0.4.12 | `git show v0.4.12:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-28.el9_4 |
