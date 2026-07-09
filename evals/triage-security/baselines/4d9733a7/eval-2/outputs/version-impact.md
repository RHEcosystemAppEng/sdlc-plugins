# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-28940 (serde_json < 1.0.135)

The version impact table includes ALL versions from the security-matrix.md supportability matrix across both streams (Important Rule 4). Each version uses the pinned commit tag from the supportability matrix (Important Rule 13).

| Version | Stream | Pinned Tag | serde_json | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 1.0.137 | NO | >= 1.0.135 |
| 2.1.1 | 2.1.x | `v0.3.12` | 1.0.137 | NO | >= 1.0.135 |
| 2.2.0 | 2.2.x | `v0.4.5` | 1.0.138 | NO | >= 1.0.135 |
| 2.2.1 | 2.2.x | `v0.4.8` | 1.0.138 | NO | >= 1.0.135 |
| 2.2.2 | 2.2.x | `v0.4.8` | 1.0.138 | NO | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 1.0.139 | NO | >= 1.0.135 |
| 2.2.4 | 2.2.x | `v0.4.12` | 1.0.139 | NO | >= 1.0.135 |

**Result**: ALL supported versions ship serde_json >= 1.0.135, which is outside the affected range (< 1.0.135). **No supported versions are affected.**

### Evidence Summary

Every version across both streams ships a serde_json version that is at or above the fix threshold:
- 2.1.x stream: all versions ship 1.0.137
- 2.2.x stream: versions ship 1.0.138 or 1.0.139
- The lowest shipped version (1.0.137) is well above the fix threshold (1.0.135)
