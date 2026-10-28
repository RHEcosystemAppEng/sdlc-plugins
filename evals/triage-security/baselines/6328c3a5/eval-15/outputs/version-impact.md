# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **Affected versions (2.2.x stream, in scope):** 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (2.2.x stream):** 2.2.3, 2.2.4 (ship quinn-proto 0.11.14, the fix version)
- **Affected versions (2.1.x stream, out of scope):** 2.1.0, 2.1.1
- **Cross-stream impact:** Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.11+) | YES |

The upstream fix is available on the 2.2.x stream's branch (release/0.4.z ships quinn-proto 0.11.14 from v0.4.11 onward). For 2.2.x, the remediation is a dependency bump + downstream propagation. For 2.1.x, the upstream branch (release/0.3.z) does NOT yet ship the fix -- remediation would require an upstream backport.
