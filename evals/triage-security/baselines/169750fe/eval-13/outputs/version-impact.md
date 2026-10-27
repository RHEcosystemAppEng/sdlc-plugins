# Step 2 -- Version Impact Analysis: TC-8001

## Vulnerability Summary

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: < 0.11.14
- **Fixed version**: 0.11.14
- **Ecosystem**: Cargo

## Version Impact Table

### Stream 2.1.x (rhtpa-release.0.3.z) -- outside issue scope

| Product Version | Build | Backend Tag | quinn-proto Version | Affected? | Evidence |
|-----------------|-------|-------------|---------------------|-----------|----------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

- Upstream branch: `release/0.3.z`
- Latest pinned tag: `v0.3.12` ships quinn-proto 0.11.9
- **Upstream fix status**: Fix NOT available on `release/0.3.z` (latest tag still ships 0.11.9)

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Product Version | Build | Backend Tag | quinn-proto Version | Affected? | Evidence |
|-----------------|-------|-------------|---------------------|-----------|----------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | `v0.4.9` | 0.11.12 | **YES** | Retag of v0.4.8 -- same as 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |

- Upstream branch: `release/0.4.z`
- Latest pinned tag: `v0.4.12` ships quinn-proto 0.11.14
- **Upstream fix status**: Fix IS available on `release/0.4.z` (v0.4.11+ ships 0.11.14)

## Step 2.5 -- Upstream Fix Status Summary

| Stream | Upstream Branch | Latest Tag | quinn-proto at HEAD | Fix Available? |
|--------|-----------------|------------|---------------------|----------------|
| 2.1.x | `release/0.3.z` | `v0.3.12` | 0.11.9 | **NO** |
| 2.2.x | `release/0.4.z` | `v0.4.12` | 0.11.14 | **YES** |

## Impact Summary

- **Stream 2.2.x** (in scope): 3 versions affected (2.2.0, 2.2.1, 2.2.2), 2 versions fixed (2.2.3, 2.2.4). Upstream fix already available -- use dependency bump variant.
- **Stream 2.1.x** (out of scope): All 2 versions affected (2.1.0, 2.1.1). Upstream fix NOT available -- use upstream backport variant. Triggers Case A (cross-stream impact).

## Affects Versions Correction (Step 3)

The issue is scoped to stream 2.2.x. Only 2.2.x versions are in scope for Affects Versions.

- **Current**: `[RHTPA 2.0.0]` (wrong -- RHTPA 2.0.0 does not correspond to any version in the 2.2.x supportability matrix)
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` (the three affected 2.2.x versions)
- RHTPA 2.2.3 and RHTPA 2.2.4 are NOT affected and excluded from Affects Versions.

## Retag Handling

- Version 2.2.2 (build 0.4.9, tag `v0.4.9`) is a retag of 2.2.1 (build 0.4.8, tag `v0.4.8`) per the supportability matrix note "backend retag of 2.2.1". Lock file check skipped; result carried forward from 2.2.1 (quinn-proto 0.11.12, AFFECTED).
