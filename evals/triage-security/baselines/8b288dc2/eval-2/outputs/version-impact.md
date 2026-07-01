# Version Impact Analysis -- TC-8002

## CVE-2026-28940 (serde_json < 1.0.135)

Fix threshold: **1.0.135** (from Jira description; to be cross-validated via MITRE CVE API and OSV.dev in a live triage)

### Version Impact Table

| Version | Stream | Tag | serde_json version | Affected? | Notes |
|---------|--------|-----|--------------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 1.0.137 | NO | Ships patched version (1.0.137 >= 1.0.135) |
| 2.1.1 | 2.1.x | `v0.3.12` | 1.0.137 | NO | Ships patched version (1.0.137 >= 1.0.135) |
| 2.2.0 | 2.2.x | `v0.4.5` | 1.0.138 | NO | Ships patched version (1.0.138 >= 1.0.135) |
| 2.2.1 | 2.2.x | `v0.4.8` | 1.0.138 | NO | Ships patched version (1.0.138 >= 1.0.135) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | Retag of 2.2.1; same as 2.2.1 (1.0.138) |
| 2.2.3 | 2.2.x | `v0.4.11` | 1.0.139 | NO | Ships patched version (1.0.139 >= 1.0.135) |
| 2.2.4 | 2.2.x | `v0.4.12` | 1.0.139 | NO | Ships patched version (1.0.139 >= 1.0.135) |

### Summary

**No supported versions are affected.** All versions across both the 2.1.x and 2.2.x streams ship serde_json at version 1.0.137 or higher, which is at or above the fix threshold of 1.0.135. The vulnerable version range (before 1.0.135) is not present in any supported release.

### Scoped Stream Detail (2.2.x)

Since TC-8002 is scoped to the 2.2.x stream, the in-scope versions are 2.2.0 through 2.2.4. All five versions ship serde_json >= 1.0.138, well above the fix threshold.

### Cross-Stream Detail (2.1.x)

The 2.1.x stream also ships serde_json 1.0.137, which is above the fix threshold. No cross-stream impact exists.
