# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed version |

## Summary

- **Issue stream scope**: 2.2.x (from summary suffix [rhtpa-2.2])
- **Affected in-scope versions (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected in-scope versions (2.2.x)**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14)
- **Cross-stream impact (2.1.x)**: 2.1.0, 2.1.1 are also affected (quinn-proto 0.11.9)
