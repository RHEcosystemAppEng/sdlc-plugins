# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-28940 (serde_json < 1.0.135)

All supported versions are checked per Important Rule 4. The issue is scoped to stream 2.2.x via the `[rhtpa-2.2]` suffix, but all streams are analyzed for completeness and cross-stream impact assessment (Step 8 Case A).

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Tag | serde_json version | Affected? | Notes |
|---------|-----|--------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 1.0.137 | NO | 1.0.137 >= 1.0.135 (outside affected range) |
| 2.1.1 | `v0.3.12` | 1.0.137 | NO | 1.0.137 >= 1.0.135 (outside affected range) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue Scope

| Version | Tag | serde_json version | Affected? | Notes |
|---------|-----|--------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 1.0.138 | NO | 1.0.138 >= 1.0.135 (outside affected range) |
| 2.2.1 | `v0.4.8` | 1.0.138 | NO | 1.0.138 >= 1.0.135 (outside affected range) |
| 2.2.2 | `v0.4.9` | 1.0.138 | NO | retag of 2.2.1 -- same as 2.2.1 (carries forward NOT affected) |
| 2.2.3 | `v0.4.11` | 1.0.139 | NO | 1.0.139 >= 1.0.135 (outside affected range) |
| 2.2.4 | `v0.4.12` | 1.0.139 | NO | 1.0.139 >= 1.0.135 (outside affected range) |

### Summary

**All supported versions across all streams ship serde_json >= 1.0.135, which is outside the CVE's affected range (< 1.0.135).** No supported version is affected by CVE-2026-28940.

- Stream 2.1.x: 0 of 2 versions affected
- Stream 2.2.x: 0 of 5 versions affected
- **Total: 0 of 7 versions affected**
