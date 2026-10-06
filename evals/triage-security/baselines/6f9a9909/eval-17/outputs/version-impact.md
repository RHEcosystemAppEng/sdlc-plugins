# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | **YES** | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | **YES** | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | **YES** | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | **YES** | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | **YES** | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | Fixed: ships >= 0.11.14 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | Fixed: ships >= 0.11.14 |

## Summary

- **Affected versions**: 2.1.0, 2.1.1 (stream 2.1.x); 2.2.0, 2.2.1, 2.2.2 (stream 2.2.x)
- **Not affected versions**: 2.2.3, 2.2.4 (stream 2.2.x) -- already ship quinn-proto 0.11.14 (the fixed version)
- **Fix threshold**: quinn-proto >= 0.11.14

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: source dependency (Cargo)
  Ecosystem: Cargo
  Lock file: Cargo.lock

  quinn-proto is a QUIC transport protocol implementation.
  The vulnerability (DoS via excessive stream counts) affects
  versions before 0.11.14.

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.lock
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD (from matrix) | Fixed? |
|--------|-----------|-----------------|-------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at latest tag v0.3.12) | **NO** -- upstream backport needed |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at latest tag v0.4.12) | **YES** -- fix already present |

### Remediation Path

- **Stream 2.2.x**: The fix is already present in later builds (v0.4.11+). Affected versions 2.2.0, 2.2.1, and 2.2.2 shipped with vulnerable quinn-proto. Since the upstream branch `release/0.4.z` already has the fix (v0.4.11 onward ships 0.11.14), the downstream propagation task only needs to ensure the Konflux release repo references a tag that includes the fix.
- **Stream 2.1.x**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9. An upstream backport PR is needed to bump quinn-proto to >= 0.11.14 on the `release/0.3.z` branch, followed by a downstream Konflux release repo update.

## Cross-Stream Impact

The issue TC-8001 is **scoped to stream 2.2.x** (suffix `[rhtpa-2.2]`), but the version impact analysis shows that **stream 2.1.x is also affected** (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This triggers **Case A** (cross-stream impact) in Step 8.

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which does not correspond to any configured version stream (no 2.0.x stream exists). Since the issue is scoped to stream 2.2.x, the corrected Affects Versions should include only the affected 2.2.x versions:

```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Note: RHTPA 2.2.3 and RHTPA 2.2.4 are NOT included because they ship the fixed version (0.11.14).
