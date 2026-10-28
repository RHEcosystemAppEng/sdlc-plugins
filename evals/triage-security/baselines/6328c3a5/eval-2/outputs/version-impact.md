# Version Impact Analysis -- TC-8002 (CVE-2026-28940)

## Vulnerability Summary

- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Stream | Version | Build Tag | serde_json version | Affected? | Notes |
|--------|---------|-----------|-------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 1.0.137 | NO | Ships fixed version (1.0.137 >= 1.0.135) |
| 2.1.x | 2.1.1 | v0.3.12 | 1.0.137 | NO | Ships fixed version (1.0.137 >= 1.0.135) |
| 2.2.x | 2.2.0 | v0.4.5 | 1.0.138 | NO | Ships fixed version (1.0.138 >= 1.0.135) |
| 2.2.x | 2.2.1 | v0.4.8 | 1.0.138 | NO | Ships fixed version (1.0.138 >= 1.0.135) |
| 2.2.x | 2.2.2 | v0.4.9 | 1.0.138 | NO | Retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 1.0.139 | NO | Ships fixed version (1.0.139 >= 1.0.135) |
| 2.2.x | 2.2.4 | v0.4.12 | 1.0.139 | NO | Ships fixed version (1.0.139 >= 1.0.135) |

## Analysis

**Every supported version across all streams ships serde_json >= 1.0.137**, which is above the fix threshold of 1.0.135. The vulnerability (CVE-2026-28940) was fixed in serde_json 1.0.135, and the earliest version of serde_json found in any shipped product version is 1.0.137 (in the 2.1.x stream).

**No supported version is affected by this vulnerability.**

The fix for CVE-2026-28940 (recursion limit defaulting to 128 levels) was already included in the serde_json versions shipped by every product release.

## Dependency Chain Context

Not applicable -- since no versions are affected, no remediation chain analysis is required.

## Upstream Fix Status

Not applicable -- all versions already ship the fixed dependency. There is no remediation needed upstream or downstream.
