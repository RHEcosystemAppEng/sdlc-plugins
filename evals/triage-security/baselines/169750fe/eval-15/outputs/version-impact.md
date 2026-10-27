# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **Affected versions (2.2.x stream -- issue scope)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (2.2.x stream)**: 2.2.3, 2.2.4
- **Affected versions (2.1.x stream -- outside issue scope)**: 2.1.0, 2.1.1
- **Fix threshold**: quinn-proto >= 0.11.14

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are not affected.
Versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto versions below 0.11.14 and are affected.

The 2.1.x stream (2.1.0, 2.1.1) is also affected but is outside this issue's scope
(scoped to 2.2.x per the `[rhtpa-2.2]` suffix). Cross-stream impact will be reported
in Step 8 (Case A).
