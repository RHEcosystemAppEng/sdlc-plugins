# Version Impact Analysis — TC-8002

## CVE-2026-28940: serde_json < 1.0.135

### Version Impact Table

All versions across both supported streams (2.1.x and 2.2.x) were analyzed using serde_json versions extracted from `Cargo.lock` at each pinned source commit.

| Stream | Version | Build Tag | serde_json version | Affected? | Notes |
|--------|---------|-----------|-------------------|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 1.0.137 | **NO** | >= 1.0.135 fix threshold |
| 2.1.x | 2.1.1 | `v0.3.12` | 1.0.137 | **NO** | >= 1.0.135 fix threshold |
| 2.2.x | 2.2.0 | `v0.4.5` | 1.0.138 | **NO** | >= 1.0.135 fix threshold |
| 2.2.x | 2.2.1 | `v0.4.8` | 1.0.138 | **NO** | >= 1.0.135 fix threshold |
| 2.2.x | 2.2.2 | `v0.4.9` | 1.0.138 | **NO** | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | `v0.4.11` | 1.0.139 | **NO** | >= 1.0.135 fix threshold |
| 2.2.x | 2.2.4 | `v0.4.12` | 1.0.139 | **NO** | >= 1.0.135 fix threshold |

### Key Finding

**No supported versions ship a vulnerable version of serde_json.**

The fix threshold is version 1.0.135. The lowest serde_json version found across all shipped product versions is **1.0.137** (in the 2.1.x stream), which is already above the fix threshold. All other versions ship 1.0.138 or 1.0.139.

Every shipped version already includes a patched serde_json — the vulnerability (stack overflow on deeply nested input) does not affect any supported release.

### Scoped vs Full Analysis

- The issue is **scoped to stream 2.2.x** (per the `[rhtpa-2.2]` suffix in the summary).
- Within the scoped stream (2.2.x): **0 of 5 versions affected** — all ship serde_json >= 1.0.138.
- Cross-stream check (2.1.x): also **not affected** — ships serde_json 1.0.137, which is above the fix threshold.

### Upstream Fix Status

Not explicitly checked (no external tool calls in eval mode), but the lock file evidence shows all pinned commits already include serde_json versions well above the fix threshold, confirming the fix was picked up before any currently supported version was built.
