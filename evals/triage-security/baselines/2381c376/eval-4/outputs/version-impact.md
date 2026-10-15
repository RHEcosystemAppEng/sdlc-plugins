# Step 2 -- Version Impact Analysis: TC-8004

## CVE-2026-33501 (h2 < 0.4.8)

### Version Impact Table

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 (fix threshold) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 (fix threshold) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | 2.2.x | v0.4.9 | 0.4.8 | NO | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | 0.4.9 > 0.4.8 (above fix threshold) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | 0.4.9 > 0.4.8 (above fix threshold) |

### Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Impact |
|--------|-------------------|---------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | **ALL versions affected** |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **NO versions affected** |

### Mixed Impact Analysis

This CVE demonstrates **mixed impact across streams**:
- The **2.1.x stream** ships h2 0.4.5, which is below the fix threshold of 0.4.8. All released versions in this stream (2.1.0 and 2.1.1) are affected.
- The **2.2.x stream** ships h2 >= 0.4.8 in all released versions (starting from 2.2.0). No versions in this stream are affected.

### Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (h2 is an HTTP/2 runtime dependency)
```

### Upstream Fix Status

The h2 crate fix is available as version 0.4.8. The 2.2.x stream already ships this fix. For the 2.1.x stream (upstream branch `release/0.3.z`), the latest pinned build (v0.3.12) still ships h2 0.4.5, indicating the upstream branch has not yet been updated to include h2 >= 0.4.8.

Since h2 0.4.8 is a published crate release, remediation for the 2.1.x stream is a dependency bump (`cargo update -p h2`) rather than an upstream backport requiring source code changes.

| Stream | Ecosystem | Upstream Branch | Pinned h2 | Fixed? |
|--------|-----------|-----------------|-----------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 | **NO** -- bump needed |
| 2.2.x | Cargo | release/0.4.z | 0.4.8+ | YES -- already ships fix |
