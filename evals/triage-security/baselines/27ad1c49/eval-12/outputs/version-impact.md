# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using the cross-validated fix threshold from Step 1.5: **h2 < 0.4.8 is affected** (fixed in 0.4.8).

## Version Impact Table for CVE-2026-48901 (h2 < 0.4.8)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Tag | h2 version | Affected? | Notes |
|---------|-----|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scoped stream

| Version | Tag | h2 version | Affected? | Notes |
|---------|-----|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Combined Version Impact Summary

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.1 | 2.2.x | 0.4.8 | NO | at fix threshold |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | above fix threshold |
| 2.2.4 | 2.2.x | 0.4.9 | NO | above fix threshold |

## Scoped Stream Analysis

The issue TC-8030 is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).

**Within the scoped stream (2.2.x)**: All 5 versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8 and are **NOT affected**. The earliest 2.2.x release (2.2.0, tag v0.4.5) already ships h2 0.4.8, which is at the fix threshold.

**Outside the scoped stream (2.1.x)**: Both versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold. Stream 2.1.x **IS affected**.

## Dependency Chain Context

h2 is a Cargo (Rust) dependency in the backend repository. Based on the ecosystem classification:
- Ecosystem: Cargo (source dependency)
- Lock file: Cargo.lock
- The h2 crate provides HTTP/2 protocol support

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Upstream fix status unknown from available data |
| 2.2.x | Cargo | release/0.4.z | Already ships fixed version (h2 >= 0.4.8) |

## Key Finding

The enriched fix threshold from Step 1.5 (0.4.8) was essential for this analysis. The Jira description provided no usable version constraint ("versions prior to the fix" / "see advisory"). Without external CVE data enrichment, the version impact analysis could not have been performed -- the MITRE and OSV.dev data provided the precise boundary needed to determine that 2.2.x ships the fix while 2.1.x does not.
