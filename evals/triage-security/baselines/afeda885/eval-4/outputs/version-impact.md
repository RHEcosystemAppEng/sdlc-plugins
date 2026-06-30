# Version Impact Analysis — TC-8004

## CVE-2026-33501: h2 < 0.4.8 (Memory exhaustion via CONTINUATION frames)

Fix threshold: **h2 >= 0.4.8** (cross-validated against advisory GHSA-2026-kv8p-r3n7)

### Version Impact Table

| Version | Stream | Build Tag | h2 Version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Impact |
|--------|-------------------|---------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | _(none)_ | **ALL versions affected** |
| 2.2.x | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **No versions affected** |

The vulnerability has **mixed impact across streams**: the 2.1.x stream ships
h2 0.4.5 (vulnerable), while the 2.2.x stream ships h2 >= 0.4.8 (patched).

### Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo (Cargo.lock)
  Lock file: Cargo.lock

  2.1.x stream (v0.3.8, v0.3.12): h2 0.4.5 — VULNERABLE
  2.2.x stream (v0.4.5+):         h2 0.4.8+ — PATCHED
```

The h2 crate is a transitive dependency pulled in through the HTTP stack (hyper).
The 2.2.x stream already ships the patched version (0.4.8+), indicating the
upstream source repository's release/0.4.z branch was updated before 2.2.0 shipped.
The 2.1.x stream remains on h2 0.4.5 across all released versions.

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at Branch HEAD | Fixed Upstream? |
|--------|-----------|-----------------|-------------------|-----------------|
| 2.1.x | Cargo | release/0.3.z | _(requires git show check)_ | Unknown — needs verification |
| 2.2.x | Cargo | release/0.4.z | 0.4.8+ (based on shipped versions) | YES |

The 2.2.x upstream branch already ships a patched h2 version. For the 2.1.x
stream, the upstream branch release/0.3.z should be checked to determine if a
fix has been backported. Based on the shipped versions (h2 0.4.5 in both 2.1.0
and 2.1.1), the upstream branch likely still ships the vulnerable version.
