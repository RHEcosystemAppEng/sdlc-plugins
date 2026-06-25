# Step 2 -- Version Impact Analysis: TC-8004

## CVE-2026-33501 (h2 < 0.4.8)

### Version Impact Table

Version Impact for CVE-2026-33501 (h2 versions before 0.4.8):

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | pinned at v0.3.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | pinned at v0.3.12 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | ships fix version (pinned at v0.4.5) |
| 2.2.1 | 2.2.x | 0.4.8 | NO | ships fix version (pinned at v0.4.8) |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.9 | NO | ships version above fix (pinned at v0.4.11) |
| 2.2.4 | 2.2.x | 0.4.9 | NO | ships version above fix (pinned at v0.4.12) |

**Summary**: Mixed impact across streams.
- **2.1.x stream**: ALL versions affected (2.1.0 and 2.1.1 ship h2 0.4.5 which is below the fix threshold of 0.4.8)
- **2.2.x stream**: NO versions affected (all 2.2.x versions ship h2 >= 0.4.8, the fix version)

### Dependency Chain Context (Step 2.3.5)

Dependency chain for h2 (Cargo):
```
backend (workspace) -> hyper -> h2
Profile: production (hyper is a runtime dependency)
```

The h2 crate is a transitive dependency pulled in via hyper (HTTP library). It is present in production profile -- this is a shipped dependency, not dev-only.

- Present in 2.1.x at version 0.4.5 (below fix threshold)
- Present in 2.2.x at version 0.4.8+ (at or above fix threshold)

The 2.2.x stream already ships the patched version starting from the earliest release (2.2.0).

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 version at HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (simulated) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (simulated) | YES |

The 2.1.x upstream branch (release/0.3.z) has NOT been updated with the fix -- remediation requires an upstream PR to bump h2 to >= 0.4.8 on the release/0.3.z branch, followed by a downstream Konflux release repo update.
