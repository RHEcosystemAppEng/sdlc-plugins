# Step 2 -- Version Impact Analysis: CVE-2026-48901

## Enriched Fix Threshold

Library: **h2**
Affected range: **< 0.4.8** (from Step 1.5 cross-validated MITRE + OSV.dev data)
Fix version: **0.4.8**

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Backend Tag | h2 version | Affected? | Notes |
|--------|---------|-------------|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected Versions | Not Affected Versions |
|--------|-------------------|-----------------------|
| 2.1.x | 2.1.0, 2.1.1 | (none) |
| 2.2.x | (none) | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 |

## Issue Stream Scope Analysis

This issue (TC-8030) is scoped to stream **2.2.x** per the summary suffix `[rhtpa-2.2]`.

Within the scoped stream (2.2.x): **No versions are affected.** All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold.

Outside the scoped stream (2.1.x): **All versions are affected.** Both 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the fix threshold. This cross-stream impact is noted for awareness but is outside the scope of TC-8030. The 2.1.x stream would need its own CVE tracking issue from PSIRT.

## Dependency Chain Context

h2 is a Cargo (Rust) dependency in the backend repository.

Dependency chain for h2:
- Ecosystem: Cargo (crates.io)
- Lock file: Cargo.lock
- h2 is a transitive dependency commonly pulled in through HTTP libraries (e.g., hyper, reqwest)

For versions where h2 = 0.4.5 (2.1.x stream):
- h2 0.4.5 is below the fix threshold (0.4.8)
- The HTTP/2 CONTINUATION flood vulnerability is present

For versions where h2 >= 0.4.8 (2.2.x stream):
- h2 0.4.8+ includes the fix for the CONTINUATION frame limit
- The vulnerability is not present

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | All released versions already ship h2 >= 0.4.8 -- no remediation needed |
| 2.1.x | Cargo | release/0.3.z | Ships h2 0.4.5 -- needs upstream fix to bump h2 to >= 0.4.8 |

Upstream fix PR: https://github.com/hyperium/h2/pull/800
