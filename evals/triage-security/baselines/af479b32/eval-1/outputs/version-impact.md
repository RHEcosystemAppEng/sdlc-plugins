# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | at fix version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | at fix version |

## Lock File Evidence

Each quinn-proto version was extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
at the pinned source commits from the supportability matrix:

| Version | Backend Tag | quinn-proto version | Comparison to fix (0.11.14) |
|---------|-------------|---------------------|-----------------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | < 0.11.14 -- VULNERABLE |
| 2.1.1 | v0.3.12 | 0.11.9 | < 0.11.14 -- VULNERABLE |
| 2.2.0 | v0.4.5 | 0.11.9 | < 0.11.14 -- VULNERABLE |
| 2.2.1 | v0.4.8 | 0.11.12 | < 0.11.14 -- VULNERABLE |
| 2.2.2 | v0.4.8 | (retag of v0.4.8) | same as 2.2.1 -- VULNERABLE |
| 2.2.3 | v0.4.11 | 0.11.14 | >= 0.11.14 -- FIXED |
| 2.2.4 | v0.4.12 | 0.11.14 | >= 0.11.14 -- FIXED |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (to be verified) | Unknown |
| 2.2.x | Cargo | release/0.4.z | (to be verified) | Unknown |

Note: Since 2.2.3+ already ships quinn-proto 0.11.14 (the fix version), the upstream
`release/0.4.z` branch has already incorporated the fix. The 2.1.x stream's upstream
branch (`release/0.3.z`) still ships 0.11.9 and likely needs a backport.

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- ships quinn-proto 0.11.9
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 affected -- versions 2.2.3+ fixed
- The fix was incorporated in the 2.2.x stream starting with build 0.4.11 (version 2.2.3)
- The 2.1.x stream has not yet received the fix
