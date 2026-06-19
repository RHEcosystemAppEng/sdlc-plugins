# Step 2 -- Version Impact Analysis: TC-8004

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 |
| 2.2.2 | 2.2.x | v0.4.9 | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1 both ship h2 0.4.5)
- **2.2.x stream**: NO versions affected (all ship h2 >= 0.4.8)

The impact is **mixed across streams** -- only the 2.1.x stream ships a vulnerable version of h2, while the 2.2.x stream has already picked up the fix (h2 0.4.8+) starting from its first release (2.2.0).

## Dependency Chain Context

Dependency chain for h2 (Cargo):
- backend (workspace) ships h2 as a transitive dependency via the HTTP stack
- Lock file: `Cargo.lock`
- Profile: production (h2 is a runtime dependency used for HTTP/2 server communication)

The 2.1.x stream pins backend at tags v0.3.8 and v0.3.12, both of which include h2 0.4.5.
The 2.2.x stream pins backend at tags v0.4.5+, all of which include h2 >= 0.4.8.

The fix was incorporated into the backend repository between the 0.3.z and 0.4.z release branches.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Needs backport -- h2 must be bumped to >= 0.4.8 on this branch |
| 2.2.x | Cargo | release/0.4.z | Already fixed -- h2 0.4.8+ already present |

Remediation is required only for the **2.1.x stream** (upstream branch `release/0.3.z`).
