# Version Impact Analysis -- TC-8004

## CVE-2026-33501: h2 (affected range: < 0.4.8, fixed in: 0.4.8)

### Version Impact Table

| Version | Stream | Build Tag | h2 Version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | `v0.4.9` | _(retag)_ | NO | same as 2.2.1 (retag of v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Stream Impact Summary

| Stream | Versions Checked | Affected Versions | Impact |
|--------|-----------------|-------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | 2.1.0, 2.1.1 | **ALL AFFECTED** -- all versions ship h2 0.4.5 |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | _(none)_ | **NOT AFFECTED** -- all versions ship h2 >= 0.4.8 |

### Mixed Impact Across Streams

This is a **mixed impact** scenario:
- The **2.1.x stream** is fully affected. All released versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.
- The **2.2.x stream** is not affected. Even the earliest version (2.2.0) ships h2 0.4.8, which is at the fix threshold. Later versions ship 0.4.8 or 0.4.9.

### Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo
  Lock file: Cargo.lock

  2.1.x stream (v0.3.8, v0.3.12): h2 0.4.5 -- VULNERABLE
  2.2.x stream (v0.4.5+): h2 0.4.8+ -- FIXED
```

The h2 crate is a transitive dependency pulled in via the hyper HTTP library, which is a core runtime dependency of the backend service. This is a production dependency (not dev/test-only).

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Shipped h2 Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | 0.4.5 | **NO** -- needs backport |
| 2.2.x | Cargo | `release/0.4.z` | 0.4.8+ | YES -- already ships fixed version |

Remediation is needed only for the 2.1.x stream. The upstream branch `release/0.3.z` needs a dependency bump of h2 to >= 0.4.8.
