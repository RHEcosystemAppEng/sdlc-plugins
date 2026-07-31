# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

All versions from the supportability matrix across all streams are included (Important Rule 4). Dependency versions are extracted at pinned commit tags from the supportability matrix, not branch HEAD (Important Rule 13).

| Version | Stream | Pinned Tag | quinn-proto version | Affected? | Notes |
|---------|--------|------------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (backend tag `v0.4.8` is identical); carries forward affected status from 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | = 0.11.14 (fixed version) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | = 0.11.14 (fixed version) |

### Evidence Sources

All quinn-proto versions above were extracted via simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` at the pinned commit tags from the supportability matrix. No branch HEAD was used for released versions.

### Summary

- **Affected versions (2.1.x stream)**: 2.1.0, 2.1.1
- **Affected versions (2.2.x stream)**: 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1)
- **Not affected (2.2.x stream)**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14, the fixed version)

### Cross-stream Impact (Case A)

This issue is scoped to stream 2.2.x (per the `[rhtpa-2.2]` suffix). However, the version impact analysis reveals that the **2.1.x** stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This cross-stream impact would be reported via a comment on TC-8001 and proactive remediation tasks or companion issue tracking per Case A procedures.
