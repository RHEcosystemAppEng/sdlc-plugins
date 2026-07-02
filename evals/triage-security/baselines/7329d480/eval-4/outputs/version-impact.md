# Version Impact Analysis -- TC-8004

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Backend Tag | h2 version | Affected? | Notes |
|---------|--------|-------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.2 | 2.2.x | v0.4.8 | 0.4.8 | NO | retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Impact Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- ships h2 0.4.5
- **2.2.x stream**: NO versions affected -- ships h2 >= 0.4.8 (the fixed version)

This is a **mixed impact** scenario: the vulnerability affects the 2.1.x stream but NOT the 2.2.x stream. The 2.2.x stream already ships the patched version of h2 starting from its earliest release (2.2.0).

## Dependency Chain

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo (source dependency in Cargo.lock)
  Lock file: Cargo.lock

  2.1.x stream (v0.3.8, v0.3.12): h2 0.4.5 -- VULNERABLE
  2.2.x stream (v0.4.5+): h2 0.4.8+ -- FIXED
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at branch HEAD (inferred) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (latest tag v0.3.12 ships 0.4.5) | NO -- needs upstream backport |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (latest tag v0.4.12 ships 0.4.9) | YES |

The 2.1.x upstream branch (release/0.3.z) still ships the vulnerable h2 0.4.5. An upstream backport is required to bump h2 to >= 0.4.8 on this branch before a downstream propagation can pick up the fix.
