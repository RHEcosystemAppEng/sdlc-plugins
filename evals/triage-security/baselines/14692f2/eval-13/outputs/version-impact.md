# Step 2 -- Version Impact Analysis for TC-8001

## CVE-2026-31812: quinn-proto < 0.11.14

### Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | Tag v0.3.8 |
| 2.1.1 | 2.1.x | 0.11.9 | YES | Tag v0.3.12 |
| 2.2.0 | 2.2.x | 0.11.9 | YES | Tag v0.4.5 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | Tag v0.4.8 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Tag v0.4.11 -- at fix threshold |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Tag v0.4.12 -- at fix threshold |

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> reqwest [features: http3] -> h3 -> quinn -> quinn-proto
  Profile: production (reqwest is a runtime dependency)

Present in all versions: 2.1.0 through 2.2.4
quinn-proto is a transitive dependency brought in via the http3 feature of reqwest.
```

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (would check via `git show release/0.3.z:Cargo.lock`) | TBD |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (based on v0.4.11+ already fixed) | YES |

### Summary

- **2.2.x stream** (issue scope): Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix (0.11.14).
- **2.1.x stream** (cross-stream): All versions (2.1.0, 2.1.1) are affected -- both ship quinn-proto 0.11.9.
- The upstream fix is already present on the release/0.4.z branch (2.2.x stream), so remediation for 2.2.x is a downstream propagation to pick up an older fixed commit.
- The 2.1.x stream needs investigation on release/0.3.z to determine if an upstream backport is needed.

### Affects Versions Correction (Step 3)

PSIRT set Affects Versions to `RHTPA 2.0.0`, which is incorrect. There is no 2.0.x
stream in the Version Streams configuration. Based on lock file evidence:

- **Correct Affects Versions for 2.2.x scope**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- Versions 2.2.3 and 2.2.4 are NOT affected (ship 0.11.14, the fix version)
- RHTPA 2.0.0 should be removed (no such stream exists)
