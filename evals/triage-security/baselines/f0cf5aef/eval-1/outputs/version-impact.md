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

- **Stream 2.1.x**: ALL versions affected (2.1.0, 2.1.1) -- both ship quinn-proto 0.11.9
- **Stream 2.2.x**: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3 and 2.2.4 ship the fixed version 0.11.14

The fix threshold is quinn-proto >= 0.11.14. Versions shipping 0.11.9 or 0.11.12 are within the affected range (< 0.11.14). Version 2.2.2 is a retag of 2.2.1 and inherits the same quinn-proto version (0.11.12).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

- **Stream 2.2.x (release/0.4.z)**: Fixed upstream -- the branch HEAD ships quinn-proto 0.11.14 (based on v0.4.11+ data). Downstream propagation only needed.
- **Stream 2.1.x (release/0.3.z)**: NOT fixed upstream -- the branch HEAD still ships quinn-proto 0.11.9. An upstream backport PR is needed first.
