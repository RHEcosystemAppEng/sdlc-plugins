# Version Impact Analysis -- CVE-2026-28940 (serde_json < 1.0.135)

## Version Impact Table

| Version | Stream | Build Tag | serde_json version | Affected? | Notes |
|---------|--------|-----------|--------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 1.0.137 | NO | >= 1.0.135 (fixed) |
| 2.1.1 | 2.1.x | v0.3.12 | 1.0.137 | NO | >= 1.0.135 (fixed) |
| 2.2.0 | 2.2.x | v0.4.5 | 1.0.138 | NO | >= 1.0.135 (fixed) |
| 2.2.1 | 2.2.x | v0.4.8 | 1.0.138 | NO | >= 1.0.135 (fixed) |
| 2.2.2 | 2.2.x | v0.4.9 | 1.0.138 | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 1.0.139 | NO | >= 1.0.135 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 1.0.139 | NO | >= 1.0.135 (fixed) |

## Summary

**No supported versions are affected.** Every version across both the 2.1.x and 2.2.x streams ships serde_json >= 1.0.135, which is at or above the fix threshold.

- The **earliest** serde_json version found across all supported releases is **1.0.137** (in the 2.1.x stream).
- The **fixed version** for CVE-2026-28940 is **1.0.135**.
- Since 1.0.137 > 1.0.135, even the oldest supported release already ships a patched version of serde_json.

The vulnerable version range (serde_json < 1.0.135) was never shipped in any supported product version. The vulnerability does not apply to any currently supported release.
