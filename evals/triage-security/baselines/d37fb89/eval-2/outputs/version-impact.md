# Version Impact Analysis -- TC-8002 (CVE-2026-28940)

## CVE Details

- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Stream | Version | Build Tag | serde_json version | Affected? | Notes |
|--------|---------|-----------|-------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 1.0.137 | NO | Ships patched version (>= 1.0.135) |
| 2.1.x | 2.1.1 | v0.3.12 | 1.0.137 | NO | Ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.0 | v0.4.5 | 1.0.138 | NO | Ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.1 | v0.4.8 | 1.0.138 | NO | Ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.2 | v0.4.9 | 1.0.138 | NO | Retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 1.0.139 | NO | Ships patched version (>= 1.0.135) |
| 2.2.x | 2.2.4 | v0.4.12 | 1.0.139 | NO | Ships patched version (>= 1.0.135) |

## Analysis

**No supported version is affected.** Every version across both streams (2.1.x and 2.2.x) ships serde_json >= 1.0.135, which is at or above the fixed version. The vulnerability (affecting versions before 1.0.135) does not apply to any shipped product version.

- **2.1.x stream**: All versions ship serde_json 1.0.137
- **2.2.x stream**: All versions ship serde_json 1.0.138 or 1.0.139

The lowest serde_json version across all shipped versions is **1.0.137** (in 2.1.0 and 2.1.1), which is still above the fix threshold of 1.0.135.

## Upstream Fix Status

Not applicable -- no versions are affected, so no upstream fix check is needed. For completeness, serde_json on all upstream branches already exceeds the fix threshold.
