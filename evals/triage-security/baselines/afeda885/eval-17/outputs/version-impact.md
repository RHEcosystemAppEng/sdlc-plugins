# Step 2 — Version Impact Analysis

## Supportability Matrix

Data aggregated from both version streams (2.1.x and 2.2.x).

### Stream 1: 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

### Stream 2: 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 (retag of 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 |

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Dependency Version Extraction

Extracted quinn-proto versions from `Cargo.lock` at each pinned backend tag:

| Tag | quinn-proto version |
|-----|---------------------|
| v0.3.8 | 0.11.9 |
| v0.3.12 | 0.11.9 |
| v0.4.5 | 0.11.9 |
| v0.4.8 | 0.11.12 |
| v0.4.9 | _(retag of v0.4.8)_ |
| v0.4.11 | 0.11.14 |
| v0.4.12 | 0.11.14 |

## Version Impact Table

Fix threshold: quinn-proto >= 0.11.14 (versions before 0.11.14 are vulnerable)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | **YES** | < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | **YES** | < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | **YES** | < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | **YES** | < 0.11.14 |
| 2.2.2 | 2.2.x | — | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed) |

## Stream Impact Summary

| Stream | Affected Versions | Fixed Versions |
|--------|-------------------|----------------|
| 2.1.x | 2.1.0, 2.1.1 | (none) |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 |

## Affects Versions Correction (Step 3)

The issue TC-8001 is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).

- **Current Affects Versions (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed Affects Versions (from lock file analysis, scoped to 2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned version "RHTPA 2.0.0" is incorrect — there is no 2.0.x stream in the Security Configuration. The correct affected versions within the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2 (which is a retag of 2.2.1). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which is the fixed version.

## Cross-Stream Impact

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9), but this issue is scoped to 2.2.x only. Cross-stream impact will be addressed in Step 7 Case B (proactive remediation or cross-stream notice).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Expected Version at HEAD | Fixed? |
|--------|-----------|-----------------|--------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | (needs verification) | Unknown |
| 2.2.x | Cargo | release/0.4.z | (needs verification) | Unknown |

Note: The upstream fix PR is available at [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048). Since versions 2.2.3+ already ship the fixed version 0.11.14, the upstream branch for the 2.2.x stream (release/0.4.z) likely already has the fix.
