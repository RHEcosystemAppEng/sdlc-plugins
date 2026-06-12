# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Supportability Matrix

Data loaded from two Konflux release repos following forward pointers:

- **Stream 2.1.x**: `rhtpa-release.0.3.z`
- **Stream 2.2.x**: `rhtpa-release.0.4.z` (latest stream, no forward pointer)

## Version Impact Table

CVE-2026-28940 affects serde_json versions **before 1.0.135**. The fixed version is **1.0.135**.

| Stream | Version | Build Tag | serde_json version | Affected? | Notes |
|--------|---------|-----------|-------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 1.0.137 | **NO** | >= 1.0.135 (fixed) |
| 2.1.x | 2.1.1 | v0.3.12 | 1.0.137 | **NO** | >= 1.0.135 (fixed) |
| 2.2.x | 2.2.0 | v0.4.5 | 1.0.138 | **NO** | >= 1.0.135 (fixed) |
| 2.2.x | 2.2.1 | v0.4.8 | 1.0.138 | **NO** | >= 1.0.135 (fixed) |
| 2.2.x | 2.2.2 | v0.4.9 | 1.0.138 | **NO** | retag of 2.2.1; same as 2.2.1 |
| 2.2.x | 2.2.3 | v0.4.11 | 1.0.139 | **NO** | >= 1.0.135 (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 1.0.139 | **NO** | >= 1.0.135 (fixed) |

## Issue-Scoped Impact (2.2.x stream only)

Since TC-8002 is scoped to the 2.2.x stream via the `[rhtpa-2.2]` suffix, the in-scope versions are:

| Version | serde_json version | Affected? | Notes |
|---------|-------------------|-----------|-------|
| 2.2.0 | 1.0.138 | **NO** | >= 1.0.135 (fixed) |
| 2.2.1 | 1.0.138 | **NO** | >= 1.0.135 (fixed) |
| 2.2.2 | 1.0.138 | **NO** | retag of 2.2.1; same as 2.2.1 |
| 2.2.3 | 1.0.139 | **NO** | >= 1.0.135 (fixed) |
| 2.2.4 | 1.0.139 | **NO** | >= 1.0.135 (fixed) |

**Result: NO supported versions in the 2.2.x stream are affected.**

All versions in the 2.2.x stream ship serde_json 1.0.138 or 1.0.139, both of which are above the fixed version threshold of 1.0.135. The vulnerability (affecting versions before 1.0.135) does not apply to any shipped version.

## Cross-Stream Analysis

The 2.1.x stream (out of scope for this issue) is also **not affected** -- both 2.1.0 and 2.1.1 ship serde_json 1.0.137, which is above the fix threshold.

**No stream ships a vulnerable version of serde_json.**

## Dependency Chain Context

Not applicable -- no versions are affected, so dependency chain tracing for remediation context is not needed.

## Upstream Fix Status

Not applicable -- the vulnerability is already fixed in all shipped versions. No upstream remediation is needed.
