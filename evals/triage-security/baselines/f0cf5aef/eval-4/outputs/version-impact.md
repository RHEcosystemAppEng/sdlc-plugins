# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | 0.4.9 | v0.4.8 | 0.4.8 | NO | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.4.9 | NO | 0.4.9 > 0.4.8 |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.4.9 | NO | 0.4.9 > 0.4.8 |

### Summary

| Stream | Affected Versions | Not Affected Versions | Impact |
|--------|-------------------|-----------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | **ALL versions affected** |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **No versions affected** |

**Mixed impact**: The 2.1.x stream ships h2 0.4.5 (vulnerable) in all released versions. The 2.2.x stream ships h2 >= 0.4.8 (the fixed version) in all released versions, including the earliest version (2.2.0). The vulnerability was already resolved in the 2.2.x stream before the first 2.2.x release shipped.

### Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> [hyper/reqwest] -> h2
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime dependency used for HTTP/2 transport)

  Stream 2.1.x: h2 0.4.5 at all versions (v0.3.8, v0.3.12)
  Stream 2.2.x: h2 0.4.8+ at all versions (v0.4.5 onward)
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 version shipped | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 | **NO** -- needs backport |
| 2.2.x | Cargo | release/0.4.z | 0.4.8+ | YES -- already ships fixed version |

The 2.1.x upstream branch (release/0.3.z) still ships h2 0.4.5 based on the latest pinned tag (v0.3.12). Remediation requires an upstream backport to bump h2 to >= 0.4.8 on that branch, followed by downstream propagation in the Konflux release repo.
