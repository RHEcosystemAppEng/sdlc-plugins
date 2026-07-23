# Version Impact Analysis -- CVE-2026-28940

## Vulnerability Summary

- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135
- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Stream | Version | Build Tag | serde_json version | Affected? | Notes |
|--------|---------|-----------|-------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 1.0.137 | NO | ships fixed version |
| 2.1.x | 2.1.1 | v0.3.12 | 1.0.137 | NO | ships fixed version |
| 2.2.x | 2.2.0 | v0.4.5 | 1.0.138 | NO | ships fixed version |
| 2.2.x | 2.2.1 | v0.4.8 | 1.0.138 | NO | ships fixed version |
| 2.2.x | 2.2.2 | v0.4.9 | 1.0.138 | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 1.0.139 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 1.0.139 | NO | ships fixed version |

## Analysis

**All supported versions across both streams ship serde_json >= 1.0.135.**

The earliest serde_json version found is **1.0.137** (in the 2.1.x stream), which is already above the fix threshold of 1.0.135. The 2.2.x stream ships versions 1.0.138 and 1.0.139 -- all well above the fix threshold.

**No supported version is affected by CVE-2026-28940.**

## Scoped Stream Detail (2.2.x)

Since TC-8002 is scoped to the 2.2.x stream via its `[rhtpa-2.2]` suffix, the primary assessment covers versions 2.2.0 through 2.2.4. All five versions ship serde_json >= 1.0.138, which exceeds the fix threshold of 1.0.135.

## Cross-Stream Check (2.1.x)

The 2.1.x stream also ships serde_json 1.0.137 across all its versions. No cross-stream impact exists -- no versions in any stream are affected.

## Upstream Fix Status

Not applicable -- the vulnerability is already fixed in all shipped versions. No upstream backport or downstream propagation is needed.
