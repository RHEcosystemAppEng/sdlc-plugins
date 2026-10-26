# Version Impact Analysis -- TC-8004

## CVE-2026-33501 (h2 < 0.4.8)

### Version Impact Table

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | v0.4.9 | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 (fixed) |

### Stream Impact Summary

| Stream | Versions Affected | Versions Not Affected | Overall |
|--------|-------------------|-----------------------|---------|
| 2.1.x | 2.1.0, 2.1.1 (all versions) | _(none)_ | **AFFECTED** |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 (all versions) | **NOT AFFECTED** |

### Mixed Impact Analysis

This is a **mixed impact** scenario: the 2.1.x stream ships a vulnerable version of h2 (0.4.5), while the 2.2.x stream ships the fixed version (0.4.8 or later) in all its releases. The vulnerability was resolved in the 2.2.x stream from its first release (2.2.0).

### Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Check command: git show <tag>:Cargo.lock

  2.1.x stream: h2 0.4.5 (vulnerable) in all versions
  2.2.x stream: h2 0.4.8+ (fixed) in all versions
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Fix required -- current builds ship h2 0.4.5, needs bump to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already fixed -- all builds ship h2 >= 0.4.8 |

The upstream fix (hyperium/h2#812) is available. For the 2.1.x stream, the h2 dependency must be bumped to >= 0.4.8 on the release/0.3.z branch.
