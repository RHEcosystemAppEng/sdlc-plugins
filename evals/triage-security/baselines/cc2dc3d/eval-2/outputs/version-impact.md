# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Supportability Matrix

Data loaded from two Konflux release repos per Security Configuration:

- **Stream 2.1.x**: `rhtpa-release.0.3.z` (local path: `/home/dev/repos/rhtpa-release.0.3.z`)
- **Stream 2.2.x**: `rhtpa-release.0.4.z` (local path: `/home/dev/repos/rhtpa-release.0.4.z`)

Forward pointer from 2.1.x repo points to 2.2.x repo. The 2.2.x repo has no forward pointer (latest stream).

## Version Impact Table

CVE-2026-28940 affects serde_json versions **before 1.0.135**. The fixed version is **1.0.135**.

| Stream | Version | Build Tag | serde_json version | Affected? | Notes |
|--------|---------|-----------|-------------------|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 1.0.137 | **NO** | Ships patched version (>= 1.0.135) |
| 2.1.x | 2.1.1 | `v0.3.12` | 1.0.137 | **NO** | Ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.0 | `v0.4.5` | 1.0.138 | **NO** | Ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.1 | `v0.4.8` | 1.0.138 | **NO** | Ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.2 | `v0.4.9` | 1.0.138 | **NO** | Retag of 2.2.1 -- same as 2.2.1 |
| 2.2.x | 2.2.3 | `v0.4.11` | 1.0.139 | **NO** | Ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.4 | `v0.4.12` | 1.0.139 | **NO** | Ships patched version (>= 1.0.135) |

## Key Finding

**No supported version ships a vulnerable version of serde_json.** Every version across both streams (2.1.x and 2.2.x) ships serde_json >= 1.0.137, which is well above the fix threshold of 1.0.135. The vulnerability (affecting versions before 1.0.135) does not apply to any shipped product version.

## Dependency Chain Context

Since no versions are affected, detailed dependency chain tracing (Step 2.3.5) is not required. For reference, serde_json is a Cargo (Rust) dependency in the backend repository and is resolved via `Cargo.lock`.

## Upstream Fix Status

Not applicable -- the vulnerability is already fixed in all shipped versions. All lock files already contain serde_json >= 1.0.137, which includes the fix (introduced in 1.0.135).
