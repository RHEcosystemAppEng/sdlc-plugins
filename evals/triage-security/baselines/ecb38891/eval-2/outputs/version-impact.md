# Step 2 -- Version Impact Analysis for TC-8002

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md Last-Updated timestamp is `2026-06-28T10:00:00Z`. Today is 2026-07-31. The matrix is approximately 33 days old, which exceeds the 14-day default threshold. In a live triage, a staleness warning would be presented. For this analysis, proceeding with the available matrix data.

## Supportability Matrix

Loaded from local security-matrix.md covering two streams:
- **2.1.x** (rhtpa-release.0.3.z): 2 versions (2.1.0, 2.1.1)
- **2.2.x** (rhtpa-release.0.4.z): 5 versions (2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4)

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | Tag | serde_json | Affected? | Notes |
|---------|--------|-----|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 1.0.137 | NO | >= 1.0.135 |
| 2.1.1 | 2.1.x | `v0.3.12` | 1.0.137 | NO | >= 1.0.135 |
| 2.2.0 | 2.2.x | `v0.4.5` | 1.0.138 | NO | >= 1.0.135 |
| 2.2.1 | 2.2.x | `v0.4.8` | 1.0.138 | NO | >= 1.0.135 |
| 2.2.2 | 2.2.x | `v0.4.9` | 1.0.138 | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 1.0.139 | NO | >= 1.0.135 |
| 2.2.4 | 2.2.x | `v0.4.12` | 1.0.139 | NO | >= 1.0.135 |

**Result**: ALL supported versions ship serde_json >= 1.0.135, which is outside the affected range (< 1.0.135). No supported version is affected by CVE-2026-28940.

## Version Evidence Summary

- **2.1.x stream**: Both versions (2.1.0, 2.1.1) ship serde_json 1.0.137, well above the fix threshold of 1.0.135.
- **2.2.x stream**: All five versions (2.2.0 through 2.2.4) ship serde_json 1.0.138 or 1.0.139, all above the fix threshold of 1.0.135.
- **Retag handling**: Version 2.2.2 is a retag of 2.2.1 (identical backend source commit v0.4.8). The serde_json version (1.0.138) is carried forward from 2.2.1.

No dependency chain context is needed since no versions are affected.
