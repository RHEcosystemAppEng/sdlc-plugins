# Version Impact Analysis — CVE-2026-28940

## Vulnerability Summary

- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | Tag | serde_json | Affected? | Notes |
|---------|--------|-----|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 1.0.137 | NO | ships patched version (>= 1.0.135) |
| 2.1.1 | 2.1.x | v0.3.12 | 1.0.137 | NO | ships patched version (>= 1.0.135) |
| 2.2.0 | 2.2.x | v0.4.5 | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.1 | 2.2.x | v0.4.8 | 1.0.138 | NO | ships patched version (>= 1.0.135) |
| 2.2.2 | 2.2.x | v0.4.9 | 1.0.138 | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 1.0.139 | NO | ships patched version (>= 1.0.135) |
| 2.2.4 | 2.2.x | v0.4.12 | 1.0.139 | NO | ships patched version (>= 1.0.135) |

**Result: NO supported version is affected.** All supported versions ship serde_json >= 1.0.135, which is at or above the fix threshold.

## Analysis Details

The vulnerability (CVE-2026-28940) affects serde_json versions before 1.0.135. The fix was introduced in version 1.0.135.

- The **earliest** serde_json version found across all supported product versions is **1.0.137** (in stream 2.1.x, tags v0.3.8 and v0.3.12).
- The **latest** serde_json version found is **1.0.139** (in stream 2.2.x, tags v0.4.11 and v0.4.12).
- All versions (1.0.137, 1.0.138, 1.0.139) are **above** the fix threshold of 1.0.135.

The vulnerable version of serde_json was never shipped in any supported product release. The dependency was already at a patched version before the earliest supported product version (2.1.0) was built.

## Upstream Fix Status

Not applicable — no supported versions are affected, so no upstream fix check is needed.
