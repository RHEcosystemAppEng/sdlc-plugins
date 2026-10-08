# Step 2 -- Version Impact Analysis: CVE-2026-31812 (quinn-proto < 0.11.14)

## Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

## Summary

- **2.1.x stream**: all versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is vulnerable. Upstream branch `release/0.3.z` has NOT been fixed yet.
- **2.2.x stream**: versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable versions of quinn-proto (0.11.9 and 0.11.12). Versions 2.2.3 and 2.2.4 ship the fixed version 0.11.14. Upstream branch `release/0.4.z` already ships the fix.
- This issue is scoped to stream 2.2.x per the `[rhtpa-2.2]` suffix. Stream 2.1.x is also affected (Case A -- cross-stream impact).
