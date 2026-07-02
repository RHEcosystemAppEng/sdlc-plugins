# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- ships quinn-proto 0.11.9
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 affected -- fixed in 2.2.3 (ships quinn-proto 0.11.14)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| 2.2.x | Cargo | release/0.4.z | >= 0.11.14 | FIXED (v0.4.11+ ships 0.11.14) |
| 2.1.x | Cargo | release/0.3.z | >= 0.11.14 | NOT FIXED (latest v0.3.12 ships 0.11.9) |

## Cross-Stream Impact

This issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`).

Cross-stream impact detected: the **2.1.x** stream is also affected. Both versions in the 2.1.x stream (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the vulnerable range (< 0.11.14). The 2.1.x stream does not yet have a fix on its upstream branch (release/0.3.z).
