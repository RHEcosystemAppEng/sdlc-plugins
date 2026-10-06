# Version Impact Analysis -- CVE-2026-28940

## Fix Threshold

- Vulnerable library: serde_json
- Affected range: versions before 1.0.135
- Fixed version: >= 1.0.135

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json Version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | NO | Ships fixed version (1.0.137 >= 1.0.135) |
| 2.1.1 | v0.3.12 | 1.0.137 | NO | Ships fixed version (1.0.137 >= 1.0.135) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue Scoped Stream

| Version | Build Tag | serde_json Version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | NO | Ships fixed version (1.0.138 >= 1.0.135) |
| 2.2.1 | v0.4.8 | 1.0.138 | NO | Ships fixed version (1.0.138 >= 1.0.135) |
| 2.2.2 | v0.4.9 | 1.0.138 | NO | Retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 1.0.139 | NO | Ships fixed version (1.0.139 >= 1.0.135) |
| 2.2.4 | v0.4.12 | 1.0.139 | NO | Ships fixed version (1.0.139 >= 1.0.135) |

## Summary

**No supported versions are affected.** Every version across both streams ships serde_json >= 1.0.137, which is well above the fix threshold of 1.0.135. The vulnerability was already remediated before any currently supported version was released.

- Earliest serde_json version in any stream: **1.0.137** (streams 2.1.x)
- Latest serde_json version in any stream: **1.0.139** (stream 2.2.x, versions 2.2.3-2.2.4)
- Fix threshold: **1.0.135**
- All shipped versions exceed the fix threshold by at least 2 minor versions
