# Version Impact Analysis — CVE-2026-28940

## CVE Details

- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135
- **Fix threshold used**: 1.0.135 (from Jira description; external enrichment via MITRE CVE API and OSV.dev would be performed in live triage to cross-validate)

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Stream | Version | Build Tag | serde_json version | Affected? | Notes |
|--------|---------|-----------|-------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 1.0.137 | **NO** | >= 1.0.135 (fixed) |
| 2.1.x | 2.1.1 | v0.3.12 | 1.0.137 | **NO** | >= 1.0.135 (fixed) |
| 2.2.x | 2.2.0 | v0.4.5 | 1.0.138 | **NO** | >= 1.0.135 (fixed) |
| 2.2.x | 2.2.1 | v0.4.8 | 1.0.138 | **NO** | >= 1.0.135 (fixed) |
| 2.2.x | 2.2.2 | v0.4.9 | 1.0.138 | **NO** | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 1.0.139 | **NO** | >= 1.0.135 (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 1.0.139 | **NO** | >= 1.0.135 (fixed) |

## Summary

**No supported versions are affected.** All versions across both streams (2.1.x and 2.2.x) ship serde_json >= 1.0.137, which is well above the fix threshold of 1.0.135. The vulnerability (stack overflow on deeply nested JSON input, fixed by introducing a configurable recursion limit) was addressed before any currently supported product version was built.

### Scoped stream (2.2.x) detail

The issue is scoped to stream 2.2.x (from the `[rhtpa-2.2]` suffix). Within this stream:

- Earliest serde_json version shipped: **1.0.138** (versions 2.2.0, 2.2.1, 2.2.2)
- Latest serde_json version shipped: **1.0.139** (versions 2.2.3, 2.2.4)
- All versions are >= 1.0.135 (the fix threshold)

### Cross-stream (2.1.x) detail

The 2.1.x stream also ships serde_json 1.0.137 across all its versions, which is above the fix threshold. No cross-stream impact exists.

## Dependency Chain Context

Since no versions are affected (all ship a patched version of serde_json), dependency chain tracing (Step 2.3.5) is not required. The package serde_json is present in all builds but at versions that include the fix.

## Upstream Fix Status

Not applicable -- no versions are affected. All shipped versions already contain a patched serde_json. Upstream fix check (Step 2.5) is unnecessary.
