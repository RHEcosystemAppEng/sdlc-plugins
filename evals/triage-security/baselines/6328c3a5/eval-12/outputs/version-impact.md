# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: h2 < **0.4.8** is affected (MITRE and OSV.dev agree).

## Version Impact Table for CVE-2026-48901 (h2 < 0.4.8)

### Stream 2.2.x (issue scope: rhtpa-2.2)

| Version | Build Tag | h2 Version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fix version) |
| 2.2.2 | v0.4.9 | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Stream 2.1.x (cross-stream analysis)

| Version | Build Tag | h2 Version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

## Summary

### Stream 2.2.x (in scope)
- **Affected versions**: 2.2.0 only
- **Not affected versions**: 2.2.1, 2.2.2, 2.2.3, 2.2.4
- The fix was introduced at build tag v0.4.8 (product version 2.2.1), which ships h2 0.4.8 -- the exact fix version.

### Stream 2.1.x (cross-stream)
- **Affected versions**: 2.1.0, 2.1.1 (all versions in stream)
- Both versions ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct or transitive dependency (from Cargo.lock)
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock
  Source pinning: artifacts.lock.yaml (download URL contains tag)
```

## Cross-Stream Impact

This issue is scoped to stream 2.2.x (`[rhtpa-2.2]`). Cross-stream analysis shows that stream 2.1.x is also affected (all versions ship h2 0.4.5 < 0.4.8). This triggers Case A (cross-stream impact) in Step 8.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at latest build tag | Fixed? |
|--------|-----------|-----------------|------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (at v0.4.12) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | NO |

- Stream 2.2.x: The latest versions (2.2.1+) already ship h2 >= 0.4.8. The fix is present on the upstream branch.
- Stream 2.1.x: All versions ship h2 0.4.5. The fix is NOT present on the release/0.3.z upstream branch.
