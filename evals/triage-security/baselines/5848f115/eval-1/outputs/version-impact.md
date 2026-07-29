# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed at 0.11.14 |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- quinn-proto 0.11.9 shipped in both
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3+ fixed (quinn-proto bumped to 0.11.14 in build 0.4.11)
- **Fix threshold**: quinn-proto >= 0.11.14
- **Fix introduced**: build 0.4.11 (version 2.2.3, released 2026-03-23) in the 2.2.x stream
- **2.1.x stream**: no fix available in any released version

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Check Command | Notes |
|--------|-----------|-----------------|---------------|-------|
| 2.1.x | Cargo | release/0.3.z | `git show release/0.3.z:Cargo.lock` | Needs upstream fix verification |
| 2.2.x | Cargo | release/0.4.z | `git show release/0.4.z:Cargo.lock` | Fixed at v0.4.11+ (quinn-proto 0.11.14) |
