# Version Impact Analysis -- TC-8004

## CVE-2026-33501: h2 (versions before 0.4.8)

Fix threshold: h2 >= 0.4.8

## Version Impact Table

| Version | Stream | Build Tag | h2 Version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (ships fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (ships fixed version) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Status |
|--------|-------------------|---------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | (none) | ALL versions affected |
| 2.2.x | (none) | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | NO versions affected |

## Mixed Impact Analysis

This is a **mixed impact** scenario: the 2.1.x stream ships h2 0.4.5 (vulnerable) while the 2.2.x stream ships h2 >= 0.4.8 (patched). The vulnerability was fixed in the upstream h2 crate at version 0.4.8, and the 2.2.x stream picked up this fix starting from its first release (2.2.0).

The 2.1.x stream uses backend tags v0.3.8 and v0.3.12, which both pin h2 at 0.4.5 -- well below the fix threshold of 0.4.8. Both 2.1.x versions are affected.

The 2.2.x stream uses backend tags v0.4.5 and later, which all pin h2 at 0.4.8 or higher. No 2.2.x versions are affected.

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo (lock file: Cargo.lock)

  2.1.x stream: h2 0.4.5 at both v0.3.8 and v0.3.12 (VULNERABLE)
  2.2.x stream: h2 0.4.8+ at v0.4.5 and later (FIXED)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at Branch HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|-------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | NO -- upstream branch still ships vulnerable version |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (at v0.4.12) | YES -- already ships fixed version |

The 2.1.x upstream branch (release/0.3.z) has NOT been updated with the h2 fix. An upstream backport is required to bump h2 to >= 0.4.8 on the release/0.3.z branch before a downstream propagation can pick it up.
