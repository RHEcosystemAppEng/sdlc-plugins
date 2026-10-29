# Step 2 -- Version Impact Analysis: CVE-2026-48901 (h2)

## Enriched Fix Threshold

- **Library**: h2
- **Affected range**: < 0.4.8 (from Step 1.5 cross-validated MITRE + OSV.dev)
- **Fixed version**: 0.4.8
- **Comparison rule**: h2 < 0.4.8 = AFFECTED; h2 >= 0.4.8 = NOT AFFECTED

## Version Impact Table

All supported versions across all streams are analyzed per the triage-security skill requirement to "check ALL supported versions."

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | h2 Version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Scoped Stream

| Version | Build Tag | h2 Version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | v0.4.9 | -- | **NO** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 |

### Combined Impact Summary

| Stream | Versions Affected | Versions Not Affected | Stream Status |
|--------|-------------------|-----------------------|---------------|
| 2.1.x | 2.1.0, 2.1.1 (all) | (none) | **ALL AFFECTED** |
| 2.2.x (scoped) | (none) | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 (all) | **NOT AFFECTED** |

## Scoped Stream Analysis (2.2.x)

The issue TC-8030 is scoped to stream 2.2.x via the `[rhtpa-2.2]` suffix.

**Result**: No versions in the 2.2.x stream are affected. All 2.2.x versions ship h2 >= 0.4.8 (the fix threshold). The earliest 2.2.x version (2.2.0, build v0.4.5) already ships h2 0.4.8, which is exactly the fixed version.

## Cross-Stream Impact

Stream 2.1.x **is affected**: both versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8. This cross-stream impact is relevant for Case A (proactive remediation) in Step 8.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime HTTP/2 dependency)

  Stream 2.1.x: h2 0.4.5 (AFFECTED -- below fix threshold 0.4.8)
  Stream 2.2.x: h2 0.4.8+ (NOT AFFECTED -- at or above fix threshold)
```

## Upstream Fix Status

The h2 crate fix (version 0.4.8) is already published on crates.io. The upstream fix PR is [hyperium/h2#800](https://github.com/hyperium/h2/pull/800).

| Stream | Ecosystem | Upstream Branch | h2 at Latest Released Tag | Fix Available? |
|--------|-----------|-----------------|---------------------------|----------------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | YES (h2 0.4.8 published on crates.io) |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (at v0.4.12) | YES (already shipping fixed version) |

Since the fix (h2 0.4.8) is already published upstream, the remediation for 2.1.x is a **dependency bump** (`cargo update -p h2`) rather than an upstream backport, followed by downstream propagation.

## Affects Versions Correction (Step 3 Proposal)

**Scoped to stream 2.2.x** (per issue suffix `[rhtpa-2.2]`):

- **Current**: RHTPA 2.2.0
- **Proposed**: (empty -- no 2.2.x versions are affected)
- **Rationale**: Lock file analysis confirms all 2.2.x versions ship h2 >= 0.4.8, which is at or above the cross-validated fix threshold.

PROPOSAL: Remove RHTPA 2.2.0 from Affects Versions. Post correction comment documenting the lock file evidence.
