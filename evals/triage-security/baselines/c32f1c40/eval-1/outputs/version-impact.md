# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

All versions from the supportability matrix across all configured streams are
included below. Dependency versions are extracted from pinned commit tags in
the supportability matrix (not branch HEAD), per Important Rule 13.

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1, backend tag v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### Summary

- **Affected**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected**: 2.2.3, 2.2.4
- **Retag**: 2.2.2 is a retag of 2.2.1 (identical backend source commit `v0.4.8`);
  the lock file check was skipped and the affected status was carried forward from
  2.2.1.

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (quinn-proto is listed in Cargo.lock at the workspace level)
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

### Upstream Fix Status

The upstream fix PR is available at https://github.com/quinn-rs/quinn/pull/2048.

For each affected stream, the upstream branch from Ecosystem Mappings would be
checked at HEAD to determine whether the fix is already available:

| Stream | Ecosystem | Upstream Branch | Upstream Fix Status |
|--------|-----------|-----------------|---------------------|
| 2.1.x | Cargo | `release/0.3.z` | Would need to be checked via `git show release/0.3.z:Cargo.lock` |
| 2.2.x | Cargo | `release/0.4.z` | Would need to be checked via `git show release/0.4.z:Cargo.lock` |

> **Note**: No `git show` commands were executed. The upstream fix status
> would be determined by inspecting the lock file at each upstream branch HEAD.
> Versions 2.2.3+ already ship quinn-proto 0.11.14, suggesting the fix is
> available on the `release/0.4.z` branch. The `release/0.3.z` branch status
> is unknown and would need to be verified.
