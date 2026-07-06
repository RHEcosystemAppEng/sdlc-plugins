# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= fix threshold |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= fix threshold |

Fix threshold: 0.11.14 (from Jira description; versions < 0.11.14 are vulnerable).

## Stream Impact Summary

| Stream | Affected Versions | Not Affected Versions |
|--------|-------------------|-----------------------|
| 2.1.x | 2.1.0, 2.1.1 | -- |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (check required) | Unknown |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (per v0.4.11+) | YES |

The latest builds in the 2.2.x stream (v0.4.11, v0.4.12) already ship quinn-proto 0.11.14, which is the fix version. The upstream fix is present on the release/0.4.z branch for the 2.2.x stream.

The 2.1.x stream (release/0.3.z) still ships quinn-proto 0.11.9 as of the latest build (v0.3.12). Upstream fix status on release/0.3.z needs verification.
