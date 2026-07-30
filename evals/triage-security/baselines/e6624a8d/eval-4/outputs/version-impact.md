# Step 2 -- Version Impact Analysis: TC-8004

## CVE-2026-33501 (h2 < 0.4.8)

### Version Impact Table

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 fix threshold |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 fix threshold |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | ships fix version (= 0.4.8) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | ships fix version (= 0.4.8) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | ships version above fix threshold |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | ships version above fix threshold |

### Summary

**Mixed impact across streams:**
- **2.1.x stream**: ALL versions affected -- both 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the fix threshold of 0.4.8
- **2.2.x stream**: NO versions affected -- all 2.2.x versions ship h2 >= 0.4.8 (the fix version or above)

### Dependency Chain (Step 2.3.5)

```
backend (workspace) -> hyper -> h2
Profile: production (hyper is a runtime HTTP dependency)
```

The h2 crate is a transitive dependency pulled in via hyper (HTTP library). It is present in production profile -- this is a shipped runtime dependency, not dev-only.

- Present in 2.1.x at version 0.4.5 (below fix threshold)
- Present in 2.2.x at version 0.4.8+ (at or above fix threshold)

The 2.2.x stream already ships the patched version starting from the earliest release (2.2.0).

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 version at HEAD | Fixed at HEAD? |
|--------|-----------|-----------------|---------------------|----------------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (simulated) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (simulated) | YES |

The 2.1.x upstream branch (release/0.3.z) has NOT been updated with the fix. Remediation requires an upstream PR to bump h2 to >= 0.4.8 on the release/0.3.z branch, followed by a downstream Konflux release repo update.
