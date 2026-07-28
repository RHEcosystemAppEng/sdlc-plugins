# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-28940 (serde_json < 1.0.135)

Per Important Rule 4, all supported versions across all streams are checked,
not just the scoped stream.

### 2.2.x Stream (scoped -- issue suffix [rhtpa-2.2])

| Version | Tag | serde_json | Affected? | Notes |
|---------|-----|------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 1.0.138 | NO | 1.0.138 >= 1.0.135 |
| 2.2.1 | `v0.4.8` | 1.0.138 | NO | 1.0.138 >= 1.0.135 |
| 2.2.2 | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 1.0.139 | NO | 1.0.139 >= 1.0.135 |
| 2.2.4 | `v0.4.12` | 1.0.139 | NO | 1.0.139 >= 1.0.135 |

### 2.1.x Stream (cross-stream check)

| Version | Tag | serde_json | Affected? | Notes |
|---------|-----|------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 1.0.137 | NO | 1.0.137 >= 1.0.135 |
| 2.1.1 | `v0.3.12` | 1.0.137 | NO | 1.0.137 >= 1.0.135 |

### Summary

**No supported versions are affected.** Every version across all streams ships
serde_json >= 1.0.135, which is at or above the fix threshold. The vulnerable
range (< 1.0.135) is not present in any supported product version.

- 2.2.x stream: all 5 versions ship 1.0.138 or 1.0.139 (all >= 1.0.135)
- 2.1.x stream: all 2 versions ship 1.0.137 (>= 1.0.135)
